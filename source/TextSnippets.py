from . import Commands

REQUEST_PASS_MESSAGE = 'Добро пожаловать в *ленту завершенных заказов Клумба*!\n' \
                               'Введите пароль для дальнейшей работы.\n' \

AUTHORIZATION_SUCCESSFUL = 'Авторизация по паролю пройдена!\n' \
                           'Теперь вы можете использовать возможности бота.'

AUTHORIZATION_UNSUCCESSFUL = 'Авторизация не пройдена. Попробуйте снова.'
UNKNOWN_COMMAND = 'Неизвестная команда. Попробуйте снова.'
UNKNOWN_COMMAND_TYPE = 'Команды должны быть переданы в текстовом виде.'

FILE_LOADING_FAILED = 'Произошла ошибка при загрузке файла. Попробуйте снова.'

BOT_HELP_TEXT = 'Лента завершенных заказов отображает следующую информацию о заказах в реальном времени: \n' \
                '*Номер заказа, Курьер, Ответственный, Что заказано, Флорист, Фото*'

ERROR_BITRIX_REQUEST = 'Произошла ошибка при обращении к серверу. \n' \
                       'Попробуйте снова или подождите некоторое время.'


DEAL_TEMPLATE = \
                'Заказ {}!\n' \
                '*№ заказа:* {}\n' \
                '*Что заказано:* {}\n' \
                '*Курьер:* {}\n' \
                '*Ответственный:* {}\n' \
                '*Флорист:* {}\n' \
                '*Кто принял заказ:* {}\n' \
                '*Сумма:* {}\n' \
                '*Дата:* {}\n' \
                '*Время:* {}\n'
#               '{photo}'


DEAL_STATE_EQUIPPED = 'укомплектован'
DEAL_STATE_DELIVERY = 'в доставке'

FIELD_IS_EMPTY_PLACEHOLDER = 'нет'
