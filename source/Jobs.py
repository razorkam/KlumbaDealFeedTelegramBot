import os
import pathlib

from telegram.ext import CallbackContext
from telegram import InputMediaPhoto, ParseMode

import source.TextSnippets as Txt
import source.BitrixWorker as BW
import source.config as cfg
import source.Utils as Utils
import source.creds as creds
from source.BitrixFieldsAliases import *
from source.BitrixFieldsMappings import *


def deal_equipped(context: CallbackContext):
    query_components = context.job.context
    bot = context.bot

    with BW.OAUTH_LOCK:
        access_token = context.bot_data[cfg.BOT_ACCESS_TOKEN_PERSISTENT_KEY]

        deal_id = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_ID_ALIAS)
        deal_responsible = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_RESPONSIBLE_ALIAS)
        deal_florist = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_FLORIST_ALIAS)
        deal_order = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_ORDER_ALIAS)
        deal_courier = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_COURIER_ALIAS)
        deal_accepted = Utils.prepare_external_field(query_components, WEBHOOK_ACCEPTED_ALIAS)
        deal_sum = Utils.prepare_external_field(query_components, WEBHOOK_SUM_ALIAS)
        deal_date = Utils.prepare_external_field(query_components, WEBHOOK_DATE_ALIAS)
        deal_time = Utils.prepare_external_field(query_components, WEBHOOK_TIME_ALIAS)
        deal_type = Utils.prepare_external_field(query_components, WEBHOOK_TYPE_ALIAS)

        deal_message = Txt.DEAL_TEMPLATE.format(Txt.DEAL_STATE_EQUIPPED, deal_id,
                                                deal_order, deal_courier,
                                                deal_responsible, deal_florist, deal_accepted,
                                                deal_sum, deal_date, deal_time, deal_type)

        if deal_id != Txt.FIELD_IS_EMPTY_PLACEHOLDER:
            photo_urls = BW.get_deal_photo_dl_urls(deal_id, access_token,
                                                   (DEAL_BIG_PHOTO_ALIAS,))

            # 1024 symbols of caption only, if more -> need a message
            if photo_urls:
                media_list = [InputMediaPhoto(media=el) for el in photo_urls]
                media_list[0].caption = deal_message
                media_list[0].parse_mode = ParseMode.MARKDOWN_V2

                bot.send_media_group(chat_id=creds.EQUIPPED_GROUP_CHAT_ID, media=media_list)
            else:
                bot.send_message(chat_id=creds.EQUIPPED_GROUP_CHAT_ID, text=deal_message,
                                 parse_mode=ParseMode.MARKDOWN_V2)


def deal_in_delivery(context: CallbackContext):
    query_components = context.job.context
    bot = context.bot

    with BW.OAUTH_LOCK:
        access_token = context.bot_data[cfg.BOT_ACCESS_TOKEN_PERSISTENT_KEY]

        deal_id = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_ID_ALIAS)
        deal_responsible = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_RESPONSIBLE_ALIAS)
        deal_florist = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_FLORIST_ALIAS)
        deal_order = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_ORDER_ALIAS)
        deal_courier = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_COURIER_ALIAS)
        deal_accepted = Utils.prepare_external_field(query_components, WEBHOOK_ACCEPTED_ALIAS)
        deal_sum = Utils.prepare_external_field(query_components, WEBHOOK_SUM_ALIAS)
        deal_date = Utils.prepare_external_field(query_components, WEBHOOK_DATE_ALIAS)
        deal_time = Utils.prepare_external_field(query_components, WEBHOOK_TIME_ALIAS)
        deal_type = Utils.prepare_external_field(query_components, WEBHOOK_TYPE_ALIAS)

        deal_message = Txt.DEAL_TEMPLATE.format(Txt.DEAL_STATE_DELIVERY, deal_id,
                                                deal_order, deal_courier,
                                                deal_responsible, deal_florist, deal_accepted,
                                                deal_sum, deal_date, deal_time, deal_type)

        if deal_id != Txt.FIELD_IS_EMPTY_PLACEHOLDER:
            photo_urls = BW.get_deal_photo_dl_urls(deal_id, access_token,
                                                   (DEAL_BIG_PHOTO_ALIAS,
                                                    DEAL_CHECKLIST_PHOTO_ALIAS))

            # 1024 symbols of caption only, if more -> need a message
            if photo_urls:
                media_list = [InputMediaPhoto(media=el) for el in photo_urls]
                media_list[0].caption = deal_message
                media_list[0].parse_mode = ParseMode.MARKDOWN_V2

                bot.send_media_group(chat_id=creds.DELIVERY_GROUP_CHAT_ID, media=media_list)
            else:
                bot.send_message(chat_id=creds.DELIVERY_GROUP_CHAT_ID, text=deal_message,
                                 parse_mode=ParseMode.MARKDOWN_V2)


def deal_waiting_for_supply(context: CallbackContext):
    query_components = context.job.context
    bot = context.bot

    deal_id = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_ID_ALIAS)
    deal_order = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_ORDER_ALIAS)
    deal_accepted = Utils.prepare_external_field(query_components, WEBHOOK_ACCEPTED_ALIAS)
    deal_link = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_SITE_LINK_ALIAS)
    deal_date = Utils.prepare_external_field(query_components, WEBHOOK_DATE_ALIAS)
    deal_time = Utils.prepare_external_field(query_components, WEBHOOK_TIME_ALIAS)
    deal_type = Utils.prepare_external_field(query_components, WEBHOOK_TYPE_ALIAS)
    deal_supply_date = Utils.prepare_external_field(query_components, WEBHOOK_SUPPLY_DATE_ALIAS)
    deal_delivery_comment = Utils.prepare_external_field(query_components, WEBHOOK_DELIVERY_COMMENT_ALIAS)
    deal_delivery_type = Utils.prepare_external_field(query_components, WEBHOOK_DELIVERY_TYPE_ALIAS)
    deal_subdivision = Utils.prepare_external_field(query_components, WEBHOOK_SUBDIVISION_ALIAS)

    deal_message = Txt.DEAL_WAITING_FOR_SUPPLY_TEMPLATE.format(deal_id,
                                                               Txt.DEAL_WAITING_FOR_SUPPLY_STUB, deal_order,
                                                               deal_link, deal_date, deal_time, deal_type,
                                                               deal_accepted, deal_delivery_comment, deal_delivery_type,
                                                               deal_subdivision, deal_supply_date)

    if deal_id != Txt.FIELD_IS_EMPTY_PLACEHOLDER:
        photo_stub_path = pathlib.Path(__file__).parent.resolve() / 'data/waiting_for_supply.png'

        with open(photo_stub_path, 'rb') as f:
            bot.send_photo(chat_id=creds.RESERVED_GROUP_CHAT_ID, photo=f,
                           caption=deal_message, parse_mode=ParseMode.MARKDOWN_V2)


def deal_reserved(context: CallbackContext):
    query_components = context.job.context
    bot = context.bot

    deal_id = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_ID_ALIAS)
    deal_order = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_ORDER_ALIAS)
    deal_accepted = Utils.prepare_external_field(query_components, WEBHOOK_ACCEPTED_ALIAS)
    deal_link = Utils.prepare_external_field(query_components, WEBHOOK_DEAL_SITE_LINK_ALIAS)
    deal_is_reserved = Utils.prepare_external_field(query_components, WEBHOOK_IS_RESERVED_ALIAS)
    deal_date = Utils.prepare_external_field(query_components, WEBHOOK_DATE_ALIAS)
    deal_time = Utils.prepare_external_field(query_components, WEBHOOK_TIME_ALIAS)
    deal_type = Utils.prepare_external_field(query_components, WEBHOOK_TYPE_ALIAS)
    deal_delivery_comment = Utils.prepare_external_field(query_components, WEBHOOK_DELIVERY_COMMENT_ALIAS)
    deal_delivery_type = Utils.prepare_external_field(query_components, WEBHOOK_DELIVERY_TYPE_ALIAS)
    deal_subdivision = Utils.prepare_external_field(query_components, WEBHOOK_SUBDIVISION_ALIAS)

    deal_reserved_str = Utils.prepare_external_field(query_components, WEBHOOK_RESERVED_STR_ALIAS) \
        if deal_is_reserved.lower() == DEAL_IS_RESERVED_YES.lower() else Txt.DEAL_NO_RESERVE_NEEDED_STUB

    deal_message = Txt.DEAL_RESERVED_TEMPLATE.format(deal_id,
                                                     deal_reserved_str, deal_order,
                                                     deal_link, deal_date, deal_time, deal_type, deal_accepted,
                                                     deal_delivery_comment, deal_delivery_type, deal_subdivision)

    with BW.OAUTH_LOCK:
        access_token = context.bot_data[cfg.BOT_ACCESS_TOKEN_PERSISTENT_KEY]

        if deal_id != Txt.FIELD_IS_EMPTY_PLACEHOLDER:
            if deal_is_reserved.lower() == DEAL_IS_RESERVED_YES.lower():
                photo_urls = BW.get_deal_photo_dl_urls(deal_id, access_token,
                                                       (DEAL_RESERVE_PHOTO_ALIAS,))

                # 1024 symbols of caption only, if more -> need a message
                if photo_urls:
                    media_list = [InputMediaPhoto(media=el) for el in photo_urls]
                    media_list[0].caption = deal_message
                    media_list[0].parse_mode = ParseMode.MARKDOWN_V2

                    bot.send_media_group(chat_id=creds.RESERVED_GROUP_CHAT_ID, media=media_list)
                else:
                    bot.send_message(chat_id=creds.RESERVED_GROUP_CHAT_ID, text=deal_message,
                                     parse_mode=ParseMode.MARKDOWN_V2)
            else:
                photo_stub_path = pathlib.Path(__file__).parent.resolve() / 'data/no_reserve_needed.png'

                with open(photo_stub_path, 'rb') as f:
                    bot.send_photo(chat_id=creds.RESERVED_GROUP_CHAT_ID, photo=f,
                                   caption=deal_message, parse_mode=ParseMode.MARKDOWN_V2)
