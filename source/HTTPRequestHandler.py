from http.server import BaseHTTPRequestHandler
from urllib import parse
import logging

from .BitrixFieldsAliases import *
from . import Utils
from . import TextSnippets
from .TelegramWorker import TgWorker
from .BitrixWorker import BitrixWorker
from . import creds


class DealUpdatesHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            query = parse.urlparse(self.path).query
            query_components = parse.parse_qs(query, keep_blank_values=True)

            if WEBHOOK_SECRET_ALIAS in query_components \
                    and query_components[WEBHOOK_SECRET_ALIAS][0] == creds.BITRIX_WEBHOOK_SECRET:

                deal_id = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_ID_ALIAS)
                deal_responsible = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_RESPONSIBLE_ALIAS)
                deal_florist = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_FLORIST_ALIAS)
                deal_order = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_ORDER_ALIAS)
                deal_courier = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_COURIER_ALIAS)
                deal_accepted = Utils.prepare_external_field(query_components, WEBHOOK_ACCEPTED_ALIAS)

                deal_message = TextSnippets.DEAL_TEMPLATE.format(deal_id, deal_order, deal_courier,
                                                                 deal_responsible, deal_florist, deal_accepted)

                if deal_id != TextSnippets.FIELD_IS_EMPTY_PLACEHOLDER:
                    photo_urls = BitrixWorker.get_deal_photo_dl_urls(creds.GROUP_CHAT_ID, deal_id)

                    # 1024 symbols of caption only, if more -> need a message
                    if photo_urls:
                        TgWorker.send_mediagroup_by_url(creds.GROUP_CHAT_ID, photo_urls, deal_message)
                    else:
                        TgWorker.send_message(creds.GROUP_CHAT_ID, {'text': deal_message})

        except Exception as e:
            logging.error('HTTP request handling error: %s', e)

