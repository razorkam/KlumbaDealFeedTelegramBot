import requests
from . import creds
import logging
import pickle

from .BitrixFieldsAliases import *
from .TelegramWorker import TgWorker
from . import TextSnippets


class BitrixWorker:
    SESSION = requests.session()
    REQUESTS_TIMEOUT = 10
    REQUESTS_MAX_ATTEMPTS = 3
    APP_ACCESS_TOKEN = None
    APP_REFRESH_TOKEN = None
    TOKENS_STORAGE_NAME = 'bitrix_tokens.pickle'

    @staticmethod
    def _send_request(chat_id, method, params=None, custom_error_text='', notify_user=True):
        if params is None:
            params = {}

        for a in range(BitrixWorker.REQUESTS_MAX_ATTEMPTS):
            try:
                response = BitrixWorker.SESSION.post(url=creds.BITRIX_API_URL + method,
                                                     json=params, timeout=BitrixWorker.REQUESTS_TIMEOUT)

                if response and response.ok:
                    json = response.json()

                    if 'result' in json:
                        return json['result']
                    else:
                        error = 'Bitrix bad response %s : Attempt: %s, Called: %s : Request params: %s' \
                                % (a, json, custom_error_text, params)
                        logging.error(error)
                else:
                    error = 'Bitrix response failed - %s : Attempt: %s,  Called: %s : Request params: %s' \
                            % (a, response.text, custom_error_text, params)
                    logging.error(error)

            except Exception as e:
                error = 'Sending Bitrix api request %s' % e
                logging.error(error)

        if notify_user:
            TgWorker.send_message(chat_id, {'text': TextSnippets.ERROR_BITRIX_REQUEST})

        return None

    @staticmethod
    def get_deal_photo_dl_urls(chat_id, deal_id):
        deal = BitrixWorker._send_request(chat_id, 'crm.deal.get', params={'id': deal_id})
        photos_list = []

        # for now, refresh oauth all the times
        BitrixWorker.refresh_oauth()

        if DEAL_BIG_PHOTO_ALIAS in deal:
            for photo in deal[DEAL_BIG_PHOTO_ALIAS]:
                path = photo['downloadUrl'].replace('auth=', 'auth=' + BitrixWorker.APP_ACCESS_TOKEN)
                dl_link = creds.BITRIX_MAIN_PAGE + path
                photos_list.append(dl_link)

        return photos_list

    @staticmethod
    def refresh_oauth():
        logging.info("REFRESHING OAUTH")

        for a in range(BitrixWorker.REQUESTS_MAX_ATTEMPTS):
            try:
                response = BitrixWorker.SESSION.get(
                    url=creds.BITRIX_OAUTH_REFRESH_URL.format(BitrixWorker.APP_REFRESH_TOKEN),
                    timeout=BitrixWorker.REQUESTS_TIMEOUT)

                if response and response.ok:
                    json = response.json()

                    logging.info("GOT OAUTH JSON")
                    logging.info(json)

                    logging.info("ACCESS TOKEN PREV")
                    logging.info( BitrixWorker.APP_ACCESS_TOKEN)
                    logging.info("REFRESH TOKEN PREV")
                    logging.info( BitrixWorker.APP_REFRESH_TOKEN)

                    BitrixWorker.APP_ACCESS_TOKEN = json['access_token']
                    BitrixWorker.APP_REFRESH_TOKEN = json['refresh_token']

                    logging.info("ACCESS TOKEN NEW")
                    logging.info(BitrixWorker.APP_ACCESS_TOKEN)
                    logging.info("REFRESH TOKEN NEW")
                    logging.info(BitrixWorker.APP_REFRESH_TOKEN)

                    BitrixWorker._save_store()
                    return True
                else:
                    logging.error("Error OAUTH refreshing.")
                    logging.error(response)

            except Exception as e:
                error = 'Bitrix OAuth refresh error %s' % e
                logging.error(error)

        return False

    @staticmethod
    def load_tokens_store():
        try:
            with open(BitrixWorker.TOKENS_STORAGE_NAME, 'rb') as store:
                BitrixWorker.APP_ACCESS_TOKEN = pickle.load(store)
                BitrixWorker.APP_REFRESH_TOKEN = pickle.load(store)
        except Exception as e:
            BitrixWorker.APP_ACCESS_TOKEN = creds.BITRIX_FIRST_OAUTH_ACCESS_TOKEN
            BitrixWorker.APP_REFRESH_TOKEN = creds.BITRIX_FIRST_OAUTH_REFRESH_TOKEN
            logging.error('Loading Bitrix store %s', e)

    @staticmethod
    def _save_store():
        try:
            with open(BitrixWorker.TOKENS_STORAGE_NAME, 'wb') as store:
                logging.info("STARTING UPDATE TOKEN STORAGE")
                pickle.dump(BitrixWorker.APP_ACCESS_TOKEN, store)
                pickle.dump(BitrixWorker.APP_REFRESH_TOKEN, store)
                logging.info("TOKEN STORAGE SAVED")
        except Exception as e:
            logging.error('Saving Bitrix store %s', e)
