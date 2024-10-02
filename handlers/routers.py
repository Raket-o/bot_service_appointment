"""Модуль регистрации хендлеров пользователя."""
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import any_state
from aiogram.types import ContentType

from handlers.custom_handlers.actioins_users.calendar_change_month import (
    calendar_change_month,
)
from handlers.custom_handlers.actioins_users.delete_recordings import (
    delete_recordings_1,
    delete_recordings_2,
)
from handlers.custom_handlers.actioins_users.service_appointment import (
    service_appointment_1,
    service_appointment_2,
    service_appointment_3,
)
from handlers.custom_handlers.actioins_users.service_cancel import service_cancel
from handlers.custom_handlers.actioins_users.view_recordings import view_recordings
from handlers.custom_handlers.actions_with_admin.admin_menu import admin_menu
from handlers.custom_handlers.actions_with_admin.confirm_yes_no import confirm_yes_no
from handlers.custom_handlers.actions_with_admin.del_all_rec_day import (
    del_all_record_day_1,
    del_all_record_day_2,
    del_all_record_day_3,
)
from handlers.custom_handlers.actions_with_admin.del_rec_day import del_record_day_1
from handlers.custom_handlers.actions_with_admin.del_user import delete_user
from handlers.custom_handlers.actions_with_admin.reserve_day import (
    reserve_day_1,
    reserve_day_2,
    reserve_day_3,
)
from handlers.custom_handlers.actions_with_admin.search_client import (
    search_client_1,
    search_client_2,
)
from handlers.custom_handlers.actions_with_admin.sending_messages import (
    sending_message_1,
    sending_message_2,
    sending_message_3,
    sending_message_4,
)
from handlers.custom_handlers.actions_with_admin.un_block_user import unblocked_user
from handlers.custom_handlers.actions_with_admin.view_clients import view_clients
from handlers.custom_handlers.actions_with_admin.view_rec import view_rec
from handlers.custom_handlers.actions_with_admin.viewing_recordings_day import (
    viewing_recordings_day_1,
    viewing_recordings_day_2,
)
from handlers.custom_handlers.actions_with_admin.weekend import weekend
from handlers.default_heandlers.cancel import cancel_handler
from handlers.default_heandlers.start import start_command
from states.states import ServiceDateState


def register_routers(router: Router):
    """
    Функция register_routers. Зарегистрирует хендлеры пользователя.
    """
    router.message.register(start_command, CommandStart())
    router.callback_query.register(start_command, F.data.startswith("start_command="))

    router.message.register(cancel_handler, Command('cancel'))
    router.message.register(cancel_handler, F.text.casefold() == "cancel")

    router.callback_query.register(calendar_change_month, F.data.startswith("calendar_change_month="))

    router.message.register(delete_recordings_1, ServiceDateState.service_delete)
    router.message.register(delete_recordings_2, ServiceDateState.service_delete_conf)

    router.callback_query.register(service_appointment_1, F.data.startswith("calendar_day_"))
    router.message.register(service_appointment_2, ServiceDateState.service_time)
    router.message.register(service_appointment_3, F.content_type == ContentType.CONTACT, any_state)

    router.message.register(service_cancel, ServiceDateState.service_cancel)

    router.callback_query.register(view_recordings, F.data.startswith("view_recordings="))

    router.callback_query.register(admin_menu, F.data == "admin_menu")

    router.callback_query.register(confirm_yes_no, F.data.startswith("confirm_yes_no"))

    router.callback_query.register(delete_user, F.data.startswith("del_user="))

    router.callback_query.register(reserve_day_1, F.data == "reserve_day")
    router.callback_query.register(reserve_day_2, F.data.startswith("reserve_day_2"))
    router.callback_query.register(reserve_day_3, F.data.startswith("reserve_day="))

    router.callback_query.register(del_all_record_day_1, F.data == "del_all_record_day")
    router.callback_query.register(del_all_record_day_2, F.data.startswith("del_all_record_day_2"))
    router.callback_query.register(del_all_record_day_3, F.data.startswith("del_all_record_day="))

    router.callback_query.register(del_record_day_1, F.data.startswith("rec_del_with_day"))

    router.callback_query.register(search_client_1, F.data == "search_client")
    router.message.register(search_client_2, ServiceDateState.search_client)

    router.callback_query.register(sending_message_1, F.data == "sending_message")
    router.callback_query.register(sending_message_2, F.data.startswith("sending_message_2"))
    router.message.register(sending_message_3, ServiceDateState.mailing_for_day)
    router.callback_query.register(sending_message_4, F.data == "sending_message_3")

    router.callback_query.register(unblocked_user, F.data.startswith("blocked="))

    router.callback_query.register(view_clients, F.data == "view_clients")

    router.callback_query.register(viewing_recordings_day_1, F.data == "viewing_recordings_day")
    router.callback_query.register(viewing_recordings_day_2, F.data.startswith("view_recs_day"))

    router.callback_query.register(weekend, F.data == "weekend")

    router.callback_query.register(view_rec, F.data.startswith("view_rec_client="))
