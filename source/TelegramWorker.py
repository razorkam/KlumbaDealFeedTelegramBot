from .UserStore import UserStore
from .User import User
from . import creds
from . import TextSnippets
from .TelegramCommandsHandler import *
import requests
import logging
import time


class TgWorker:
    USERS = UserStore()
    MESSAGE_UPDATE_TYPE = 'message'
    # last update offset / incoming msg limit / long polling timeout / allowed messages types
    GET_UPDATES_PARAMS = {'offset': 0, 'limit': 100, 'timeout': 45, 'allowed_updates': [MESSAGE_UPDATE_TYPE]}
    REQUESTS_TIMEOUT = 1.5 * GET_UPDATES_PARAMS['timeout']
    REQUESTS_MAX_ATTEMPTS = 5
    GLOBAL_LOOP_ERROR_TIMEOUT = 60  # seconds
    SESSION = requests.session()
    PROXIES = [creds.HTTPS_PROXY_FINLAND, creds.HTTPS_PROXY_GERMANY]
    CommandsHandler = None

    @staticmethod
    def send_request(method, params, custom_error_text=''):
        proxy_index = 0

        for a in range(TgWorker.REQUESTS_MAX_ATTEMPTS):
            try:
                response = TgWorker.SESSION.post(url=creds.TG_API_URL + method, proxies=TgWorker.PROXIES[proxy_index],
                                             json=params, timeout=TgWorker.REQUESTS_TIMEOUT)

                if response:
                    json = response.json()

                    if json['ok']:
                        return json
                    else:
                        logging.error('TG bad response %s : Attempt: %s, Called: %s : Request params: %s',
                                      a, json, custom_error_text, params)
                else:
                    logging.error('TG response failed%s : Attempt: %s, Called: %s : Request params: %s',
                                  a, response.text, custom_error_text, params)

            except requests.exceptions.ProxyError:
                logging.error('Proxy #{} got connection error.'.format(proxy_index))

                if proxy_index < (len(TgWorker.PROXIES) - 1):
                    proxy_index += 1
                    logging.info('Trying proxy #{}'.format(proxy_index))
                else:
                    logging.error('All proxies got connection problems. Request failed')

            except Exception as e:
                logging.error('Sending TG api request %s', e)

        return {}
    
    @staticmethod
    def send_message(chat_id, message_object, formatting='Markdown'):
        message_object['chat_id'] = chat_id
        message_object['parse_mode'] = formatting
        return TgWorker.send_request('sendMessage', message_object, 'Message sending')

    @staticmethod
    def send_photo_by_url(chat_id, url):
        message_object = {
            'chat_id': chat_id,
            'photo': url
        }
        return TgWorker.send_request('sendPhoto', message_object, 'Photo sending')

    @staticmethod
    def send_mediagroup_by_url(chat_id, photos_url_list, caption, formatting='Markdown'):
        message_object = {
            'chat_id': chat_id,
            'media': [],
        }

        for ph_url in photos_url_list:
            message_object['media'].append({'type': 'photo', 'media': ph_url})

        if len(photos_url_list) > 0:
            message_object['media'][0]['caption'] = caption
            message_object['media'][0]['parse_mode'] = formatting

        return TgWorker.send_request('sendMediaGroup', message_object, 'Photo media group sending')

    @staticmethod
    def handle_user_command(user, message):
        try:
            TgWorker.CommandsHandler.handle_command(message)
        except Exception as e:
            logging.error('Handling command: %s', e)

    @staticmethod
    def handle_message(message):
        user_id = message['from']['id']
        chat_id = message['chat']['id']

        # has user been already cached?-
        if TgWorker.USERS.has_user(user_id):
            user = TgWorker.USERS.get_user(user_id)

            if chat_id != user.get_chat_id():
                user._chat_id = chat_id

            if user.is_authorized():
                TgWorker.handle_user_command(user, message)
            else:
                try:
                    provided_password = message['text']

                    if provided_password == creds.GLOBAL_AUTH_PASSWORD:
                        TgWorker.USERS.authorize(user_id, provided_password)
                    else:
                        logging.error('Invalid password authorization attempt, user: ' + user_id)
                        raise Exception()
                except Exception:
                    TgWorker.send_message(chat_id, {'text': TextSnippets.AUTHORIZATION_UNSUCCESSFUL})
                else:
                    TgWorker.send_message(chat_id, {'text': TextSnippets.AUTHORIZATION_SUCCESSFUL})
                    TgWorker.send_message(chat_id, {'text': TextSnippets.BOT_HELP_TEXT})

        else:
            TgWorker.send_message(chat_id, {'text': TextSnippets.REQUEST_PASS_MESSAGE})
            TgWorker.USERS.add_user(user_id, User())

    @staticmethod
    def handle_update(update):
        try:
            if TgWorker.MESSAGE_UPDATE_TYPE in update:
                TgWorker.handle_message(update[TgWorker.MESSAGE_UPDATE_TYPE])
            else:
                raise Exception('Unknown update type: %s' % update)
        except Exception as e:
            logging.error('Handling TG response update: %s', e)

    @staticmethod
    def base_response_handler(json_response):
        try:
            if json_response['result']:
                logging.info(json_response)

            max_update_id = TgWorker.GET_UPDATES_PARAMS['offset']
            updates = json_response['result']
            for update in updates:
                cur_update_id = update['update_id']
                if cur_update_id > max_update_id:
                    max_update_id = cur_update_id

                # TODO: thread for each user?
                # TgWorker.handle_update(update)

            if updates:
                TgWorker.GET_UPDATES_PARAMS['offset'] = max_update_id + 1

        except Exception as e:
            logging.error('Base TG response exception handler: %s', e)

    # entry point
    @staticmethod
    def run():
        TgWorker.USERS.load_user_store()

        while True:
            response = TgWorker.send_request('getUpdates', TgWorker.GET_UPDATES_PARAMS, 'Main getting updates')

            # prevent logs spamming in case of network problems
            if not response:
                time.sleep(TgWorker.GLOBAL_LOOP_ERROR_TIMEOUT)

            # don't handle requests for now
            TgWorker.base_response_handler(response)
            # TODO: multithreading timer for updates?
            TgWorker.USERS.update_user_store()
