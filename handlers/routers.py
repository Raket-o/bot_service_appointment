
# __all__ = ['register_routers']

from aiogram import Router, F
from aiogram.filters import Command, CommandStart, callback_data
from aiogram.types import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state

from handlers.default_heandlers.start import start_command
from handlers.custom_handlers.actioins_users.calendar_next_month import calendar_next_month
from handlers.custom_handlers.actioins_users.delete_recordings import delete_recordings_1, delete_recordings_2
from handlers.custom_handlers.actioins_users.service_appointment import service_appointment_1, service_appointment_2, service_appointment_3
from handlers.custom_handlers.actioins_users.service_cancel import service_cancel
from handlers.custom_handlers.actioins_users.view_recordings import view_recordings
from handlers.custom_handlers.actions_with_admin.admin_menu import admin_menu
from handlers.custom_handlers.actions_with_admin.confirm_yes_no import confirm_yes_no
from handlers.custom_handlers.actions_with_admin.del_user import delete_user
from handlers.custom_handlers.actions_with_admin.reserve_day import reserve_day_1, reserve_day_2, reserve_day_3
from handlers.custom_handlers.actions_with_admin.search_client import search_client_1, search_client_2
from handlers.custom_handlers.actions_with_admin.sending_messages import sending_message_1, sending_message_2, sending_message_3, sending_message_4
from handlers.custom_handlers.actions_with_admin.un_block_user import unblocked_user
from handlers.custom_handlers.actions_with_admin.view_clients import view_clients
from handlers.custom_handlers.actions_with_admin.viewing_recordings_day import viewing_recordings_day_1, viewing_recordings_day_2
from handlers.custom_handlers.actions_with_admin.weekend import weekend
from handlers.default_heandlers.cancel import cancel_handler
from handlers.custom_handlers.actions_with_admin.view_rec import view_rec



from states.states import ServiceDateState


def register_routers(router: Router):
    """
    Зарегистрировать хендлеры пользователя
    """
    router.message.register(start_command, CommandStart())
    router.callback_query.register(start_command, F.data.startswith("start_command="))

    router.message.register(cancel_handler, Command('cancel'))
    router.message.register(cancel_handler, F.text.casefold() == "cancel")


    router.callback_query.register(calendar_next_month, F.data.startswith("calendar_next_month="))

    router.message.register(delete_recordings_1, ServiceDateState.service_delete)
    router.message.register(delete_recordings_2, ServiceDateState.service_delete_conf)

    router.callback_query.register(service_appointment_1, F.data.startswith("calendar_day_"))
    router.message.register(service_appointment_2, ServiceDateState.service_time)
    # router.message.register(service_appointment_3, ContentTypesFilter(content_types=[ContentType.CONTACT]), any_state)
    router.message.register(service_appointment_3, F.content_type == ContentType.CONTACT, any_state)
    router.message.register(service_cancel, ServiceDateState.service_cancel)
    router.callback_query.register(view_recordings, F.data.startswith("view_recordings="))
    router.callback_query.register(admin_menu, F.data == "admin_menu")
    router.callback_query.register(confirm_yes_no, F.data.startswith("confirm_yes_no"))
    router.callback_query.register(delete_user, F.data.startswith("del_user="))
    router.callback_query.register(reserve_day_1, F.data == "reserve_day")
    router.callback_query.register(reserve_day_2, F.data.startswith("reserve_day_2"))
    router.callback_query.register(reserve_day_3, F.data.startswith("reserve_day="))
    router.callback_query.register(search_client_1, F.data == "search_client")
    router.message.register(search_client_2, ServiceDateState.search_client)
    router.callback_query.register(sending_message_1, F.data == "sending_message")
    router.callback_query.register(sending_message_2, F.data.startswith("sending_message_2"))
    router.message.register(sending_message_3, ServiceDateState.mailing_for_day)
    router.callback_query.register(sending_message_4, F.data == "sending_message_3")
    router.callback_query.register(unblocked_user, F.data.startswith("blocked="))
    router.callback_query.register(view_clients, F.data == "view_clients")

    router.callback_query.register(viewing_recordings_day_1, F.data == "viewing_recordings_day")
    router.callback_query.register(viewing_recordings_day_2, F.data.startswith("calendar_viewing_recordings_day"))
    router.callback_query.register(weekend, F.data == "weekend")

    router.callback_query.register(view_rec, F.data.startswith("view_rec_client="))












    # router.message.register(cancel_handler, Command('cancel'))
    # router.message.register(cancel_handler, F.text.casefold() == "cancel")

    # router.callback_query.register(operations_events, F.data == "operations_events"),
    # router.callback_query.register(operations_events, F.data.startswith("operations_events_")),


    # router.message.register(input_name, UserInfoState.user_first_name)





    # router.message.register(operations_events, F.__dict__ == "operations_events")


    # router.message.register(new_GPT_3, Command('new_gpt_3'), any_state)
    #
    # router.callback_query.register(
    #     new_dial_with_prompt, SelectPromptCD.filter(F.flag == '1'))
    #

    # router.message.register(censel_hendler, F.text.casefold().lower() == 'отмена', any_state)
    #
    # # хендлеры диалога
    # router.message.register(type_voice, F.voice, DialogueStates.dialogue)
    # router.message.register(type_file, F.audio, DialogueStates.dialogue)
    # router.message.register(dial_settings, Command('settings'), DialogueStates.dialogue)
    # router.message.register(dialogue, DialogueStates.dialogue)
    # router.callback_query.register(
    #     settings_menu, SettingsCallback.filter(F.flag == '1'), DialogueStates.settings_menu)
    # router.callback_query.register(
    #     transcribe_to_gpt, TranscribeCD.filter(F.flag == '1'), DialogueStates.dialogue)
    # router.message.register(dial_change, DialogueStates.change_2)