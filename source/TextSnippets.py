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

# Now using: 'equipped', 'in delivery'
DEAL_TEMPLATE = \
                'Заказ {}\\!\n' \
                '*№ заказа:* {}\n' \
                '*Что заказано:* {}\n' \
                '*Курьер:* {}\n' \
                '*Ответственный:* {}\n' \
                '*Флорист:* {}\n' \
                '*Кто принял заказ:* {}\n' \
                '*Сумма:* {}\n' \
                '*Дата:* {}\n' \
                '*Время:* {}\n' \
                '*Тип заказа:* *{}*\n'
#               '{photo}'

# Now using: 'reserved', 'waiting for supply'
DEAL_RESERVED_TEMPLATE = \
                '*№ заказа:* {}\n' \
                '*Что отложено:* {}\n' \
                '*Что заказано:* {}\n' \
                '*Ссылка на заказ:* {}\n' \
                '*Дата:* {}\n' \
                '*Время:* {}\n' \
                '*Тип заказа:* *{}*\n'\
                '*Кто принял заказ:* {}\n'\
                '*Комментарий по доставке:* {}\n'\
                '*Доставка/Самовывоз:* {}\n'\
                '*Подразделение:* {}\n'
#               '{photo}'

DEAL_WAITING_FOR_SUPPLY_STUB = 'Ждет поставки'
DEAL_NO_RESERVE_NEEDED_STUB = 'Резерв не нужен'

# Now using: 'waiting for supply'
DEAL_WAITING_FOR_SUPPLY_TEMPLATE = \
                '*№ заказа:* {}\n' \
                '*Что отложено:* {}\n' \
                '*Что заказано:* {}\n' \
                '*Ссылка на заказ:* {}\n' \
                '*Дата:* {}\n' \
                '*Время:* {}\n' \
                '*Тип заказа:* *{}*\n'\
                '*Кто принял заказ:* {}\n' \
                '*Комментарий по доставке:* {}\n' \
                '*Доставка/Самовывоз:* {}\n' \
                '*Подразделение:* {}\n'\
                '*Дата поставки:* {}\n'
#               '{photo}'


DEAL_UNAPPROVED_TEMPLATE = \
                '*№ заказа:* {}\n\n' \
                '*Что заказано:* {}\n' \
                '*Комментарий клиента:* {}\n' \
                '*Перезвонить клиенту:* {}\n\n' \
                '*Ответственный:* {}\n' \
                '*Флорист:* *{}*\n'\
                '*Кто укомплектовал заказ:* {}\n' \
                '*Дата:* {}\n' \
                '*Время:* {}\n' \
                '*Комментарий по доставке:* {}\n'\
                '*Источник:* {}\n'
#               '{photo}'


DEAL_STATE_EQUIPPED = 'укомплектован'
DEAL_STATE_DELIVERY = 'в доставке'

FIELD_IS_EMPTY_PLACEHOLDER = 'нет'
