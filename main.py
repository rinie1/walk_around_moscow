import telebot
from telebot import types
import openpyxl
import random

bot = telebot.TeleBot('')
sheet_num = 0
id_place = ''

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Дальше➡️', callback_data='next'))
    bot.send_message(message.chat.id, f'👋Привет, <b>{message.from_user.first_name}</b>! Этот бот поможет тебе найти интересные и \
запоминающиеся места в Москве! Здесь ты сможешь увидеть достопримечательности любого района, а также построить маршрут для \
своей прогулки🚶', parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f'<b>❓Дополнительная информация</b>\n\
Этот Бот поможет вам сделать ваши прогулки по Москве более интересными и насыщенными! Здесь вы \
сможете найти интересные места во всех районах Москвы, а также составить маршрут вашей прогулки.\n\
<b>⌨️Команды для работы с Ботом</b>\n/help - <em>дополнительная информация о Боте</em>\n/main - <em>основное меню</em>\n\
<b>📕Контакты</b>\nАвтор: @rinie1\nПо всем вопросам - @rinie1', parse_mode='html')

@bot.message_handler(commands=['main'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('⁉️Найти случайное место', callback_data='random')
    btn2 = types.InlineKeyboardButton('🔍Стандартный поиск', callback_data='find')
    markup.row(btn1, btn2)
    btn3 = types.InlineKeyboardButton('🗺️Посмотреть маршрут', callback_data='route')
    markup.row(btn3)
    bot.send_message(message.chat.id, f'😀Добро пожаловать в главное меню! Выберите то, что вас интересует.\n\
Функция <em>"Случайное место"</em> находит абсолютно случайное место в Москве и показывает всю информацию о нём.\n\
Функция <em>"Стандартный поиск"</em> позволяет найти место исходя из заданных параметров: расположение, район, тематика места.\n\
Фунция <em>"Посмотреть маршрут"</em> показывает тот маршрут, который вы построили, а также позволяет взаимодействовать с ним.\n\
Дополнительная информация - /help.', parse_mode='html', reply_markup=markup)

okrug = None

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'next':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Начать', callback_data='main'))
        bot.send_message(callback.message.chat.id, 'Если вы готовы начать работу с ботом, то \
нажмите на кнопку ниже. Если вы хотите получить дополнительную информацию, то введите команду /help.', reply_markup=markup)
    elif callback.data == 'main':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('⁉️Найти случайное место', callback_data='random')
        btn2 = types.InlineKeyboardButton('🔍Стандартный поиск', callback_data='find')
        markup.row(btn1, btn2)
        btn3 = types.InlineKeyboardButton('🗺️Посмотреть маршрут', callback_data='route')
        markup.row(btn3)
        bot.send_message(callback.message.chat.id, f'😀Добро пожаловать в главное меню! Выберите то, что вас интересует.\n\
Функция <em>"Случайное место"</em> находит абсолютно случайное место в Москве и показывает всю информацию о нём.\n\
Функция <em>"Стандартный поиск"</em> позволяет найти место исходя из заданных параметров: расположение, район, тематика места.\n\
Фунция <em>"Посмотреть маршрут"</em> показывает тот маршрут, который вы построили, а также позволяет взаимодействовать с ним.\n\
Дополнительная информация - /help.', parse_mode='html', reply_markup=markup)
    elif callback.data == 'random':
        sheet_num_rand = random.randint(0, 3)
        rand = random.randint(1, 20)
        book = openpyxl.open('data/places.xlsx', read_only=True)
        sheetr = book.worksheets[sheet_num_rand]
        for row in range(1, sheetr.max_row + 1):
            if sheetr[row][0].value == rand:
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('Найти еще одно случайное место', callback_data='random')
                markup.row(btn1)
                btn2 = types.InlineKeyboardButton('Выход в главное меню', callback_data='main')
                markup.row(btn2)
                file = open(f'data/{sheetr[row][4].value}', 'rb')
                bot.send_photo(callback.message.chat.id, file)
                bot.send_message(callback.message.chat.id, f'<b>{sheetr[row][1].value}</b>\n{sheetr[row][5].value}\
\n\nСсылка на <b>Яндекс Карты</b> - {sheetr[row][3].value}', parse_mode='html')
                bot.send_message(callback.message.chat.id, 'Выберите следующее действие:', reply_markup=markup)

    elif callback.data == 'route':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Преснесенский', callback_data='presnesenskiy')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton('Арбат', callback_data='arbat')
        btn3 = types.InlineKeyboardButton('Тверской', callback_data='tverskoy')
        markup.row(btn2, btn3)
        bot.send_message(callback.message.chat.id, f'Выберите район в котором вы хотите увидеть <em>маршрут</em>:', parse_mode='html', reply_markup=markup)

    elif callback.data == 'presnesenskiy':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Арбат', callback_data='arbat')
        btn2 = types.InlineKeyboardButton('Тверской', callback_data='tverskoy')
        markup.row(btn1, btn2)
        btn3 = types.InlineKeyboardButton('Выход', callback_data='main')
        markup.row(btn3)
        bot.send_message(callback.message.chat.id, f'<b>Маршрут для прогулки по этому району:</b>\n1. Москва-Сити\n\
2.Экспоцентр\n3. Парк Красная Пресня\n4. Дом Правительства\n5. Посольство США\n6. Высотка на Кудринской площади\n7. Планетарий\n\
Ссылка на маршрут - https://yandex.ru/maps?rtext=55.749588%2C37.535299~55.752184%2C37.545725~55.753783%2C37.551703~55.755485%2C37.573745~55.755392%2C37.578757~55.758986%2C37.581710~55.761433%2C37.582910&rtt=pd', parse_mode='html', reply_markup=markup)
    elif callback.data == 'arbat':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Преснесенский', callback_data='presnesenskiy')
        btn2 = types.InlineKeyboardButton('Тверской', callback_data='tverskoy')
        markup.row(btn1, btn2)
        btn3 = types.InlineKeyboardButton('Выход', callback_data='main')
        markup.row(btn3)
        bot.send_message(callback.message.chat.id, f'<b>Маршрут для прогулки по этому району:</b>\n1. Министерство инстранных дел\n\
2. Музей-квартира Пушкина\n3. Театр Вахтангова\n4. Памятник Н.В. Гоголю\n5. Музей Книги\nСсылка на маршут - https://yandex.ru/maps?rtext=55.746016%2C37.583217~55.747733%2C37.585773~55.749501%2C37.591844~55.747679%2C37.595235~55.747064%2C37.599660~55.750936%2C37.600579~55.749375%2C37.608622~55.751845%2C37.610066&rtt=pd', parse_mode='html', reply_markup=markup)
    elif callback.data == 'tverskoy':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Арбат', callback_data='arbat')
        btn2 = types.InlineKeyboardButton('Преснесенский', callback_data='presnesenskiy')
        markup.row(btn1, btn2)
        btn3 = types.InlineKeyboardButton('Выход', callback_data='main')
        markup.row(btn3)
        bot.send_message(callback.message.chat.id, f'<b>Маршрут для прогулки по этому району:</b>\n1. Московский Кремль\n\
2. Храм Василия Блаженного\n3. ГУМ\n4. Большой Театр\n5. Совет Федерации\n6. Триумфальный сквер\n7. Спасский Собор\n\
Ссылка на маршрут - https://yandex.ru/maps?rtext=55.751518%2C37.619414~55.752920%2C37.622612~55.756738%2C37.615613~55.759740%2C37.619428~55.768028%2C37.613674~55.772446%2C37.604645~55.789048%2C37.592052&rtt=pd', parse_mode='html', reply_markup=markup)

    elif callback.data == 'find':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('ЦАО', callback_data='cao')
        btn2 = types.InlineKeyboardButton('ЮАО', callback_data='yao')
        btn3 = types.InlineKeyboardButton('ЮЗАО', callback_data='yzao')
        markup.row(btn1, btn2, btn3)
        btn4 = types.InlineKeyboardButton('ЗАО', callback_data='zao')
        btn5 = types.InlineKeyboardButton('СЗАО', callback_data='szao')
        btn6 = types.InlineKeyboardButton('САО', callback_data='sao')
        markup.row(btn4, btn5, btn6)
        btn7 = types.InlineKeyboardButton('СВАО', callback_data='svao')
        btn8 = types.InlineKeyboardButton('ВАО', callback_data='vao')
        btn9 = types.InlineKeyboardButton('ЮВАО', callback_data='yvao')
        markup.row(btn7, btn8, btn9)
        file = open('data/okrug.gif', 'rb')
        bot.send_photo(callback.message.chat.id, file)
        bot.send_message(callback.message.chat.id, 'Выберите административный округ', reply_markup=markup)

    elif callback.data == 'cao' or callback.data == callback.data == 'yao' or callback.data == 'yzao' or \
    callback.data == 'zao' or callback.data == 'szao' or callback.data == 'sao' \
    or callback.data == 'svao' or callback.data == 'vao' or callback.data == 'yvao':
        file = open('data/district.jpg', 'rb')
        bot.send_photo(callback.message.chat.id, file)
        if callback.data == 'cao':
            bot.send_message(callback.message.chat.id, 'Отлично! Вы выбрали Центральный административный округ!\
Теперь выбрете район! Для этого введите <em>название района</em> из этого списка: \n1. Китай-Город\n2. Арбат\n3. Хамовники\
\n4. Якиманка\n5. Рязанский\n6. Таганский\n7. Басманный\n8. Красно-Сельский\n9. Мещанский\n10. Тверской\n11. Преснесенский\n12. Сити\
\nЕсли вам не важен район, то введите <b>Любой</b>\n\n<em>Например:\nВаше сообщение: Нагорный\nПравильный вариант✅\nВаше сообщение: 1. Нагорный\nНеправильный вариант❌</em>', parse_mode='html')
            global sheet_num
            sheet_num = 0
        elif callback.data == 'yao':
            bot.send_message(callback.message.chat.id, 'Отлично! Вы выбрали Южный административный округ!\
Теперь выбрете район! Для этого введите <em>название района</em> из этого списка:\n1. Даниловский\n2. Донской\n\
3. ЗИЛ\n4. Нагорный\n5. Нагатино-Садовники\n6. Нагатинский Затон\n\
7. Коломенское\n8. Москворечье-Сабурово\n9. Чертаново\n10. Царицино\n\
11. Бирюлево\n12. Орехово-Борисово\n13. Братеево\n\
14. Зябликово\nЕсли вам не важен район, то введите <b>Любой</b>\n\n\
<em>Например:\nВаше сообщение: Нагорный\nПравильный вариант✅\nВаше сообщение: 1. Нагорный\nНеправильный вариант❌</em>', parse_mode='html')
            sheet_num = 1
        elif callback.data == 'yzao':
            bot.send_message(callback.message.chat.id, 'Отлично! Вы выбрали Юго-Западный административный округ!\
Теперь выбрете район! Для этого введите <em>название района</em> из этого списка:\n1. Гагаринский\n2. Академический\n\
3. Котловка\n4. Ломоносовский\n5. Черемушки\n6. Зюзино\n7. Обручевский\n8. Коньково\n9. Бицевский Лесопарк\n10. Теплый Стан\n\
11. Ясенево\n12. Северное Бутово\n13. Южное Бутово\nЕсли вам не важен район, то введите <b>Любой</b>\n\n\
<em>Например:\nВаше сообщение: Нагорный\nПравильный вариант✅\nВаше сообщение: 1. Нагорный\nНеправильный вариант❌</em>', parse_mode='html')
            sheet_num = 2
        elif callback.data == 'zao':
            bot.send_message(callback.message.chat.id, 'Отлично! Вы выбрали Западный административный округ!\
Теперь выбрете район! Для этого введите <em>название района</em> из этого списка:\n1. Филевский парк\n2. Дорогомилово\n\
3. Раменки\n4. МГУ\n5. Фили-Давыдково\n6. Проспект Вернадского\n7. Крылатское\n8. Кунцево\n9. Можайский\n10. Тропарево-Никулино\n\
11. Солнцево\n12. Ново-Переделкино\nЕсли вам не важен район, то введите <b>Любой</b>\n\n\
<em>Например:\nВаше сообщение: Нагорный\nПравильный вариант✅\nВаше сообщение: 1. Нагорный\nНеправильный вариант❌</em>', parse_mode='html')
            sheet_num = 3
        elif callback.data == 'szao':
            bot.send_message(callback.message.chat.id, 'Отлично! Вы выбрали Северо-Западный административный округ!\
Теперь выбрете район! Для этого введите <em>название района</em> из этого списка:\n1. Хорошево-Мневники\n2. Щукино\n3. Строгино\n\
4. Покровское-Стрешнево\n5. Южное Тушино\n6. Митино\n7. Северное Тушино\n8. Куркино\n9. Молжаниновский\nЕсли вам не важен район, то введите <b>Любой</b>\n\n\
<em>Например:\nВаше сообщение: Нагорный\nПравильный вариант✅\nВаше сообщение: 1. Нагорный\nНеправильный вариант❌</em>', parse_mode='html')
            sheet_num = 4
        elif callback.data == 'sao':
            bot.send_message(callback.message.chat.id, 'Отлично! Вы выбрали Северо-Западный административный округ!\
Теперь выбрете район! Для этого введите <em>название района</em> из этого списка:\n1. Беговой\n2. Хорошевский\n3. Савеловский\n\
4. Аэропорт\n5. Сокол\n6. Тимирязевский\n7. Коптево\n8. Войковский\n9. Головинский\n10. Дегунино\n11. Дмитровский\n12. Ховрино\n13. Левобережный\n\
Если вам не важен район, то введите <b>Любой</b>\n\n<em>Например:\nВаше сообщение: Нагорный\nПравильный вариант✅\n\
Ваше сообщение: 1. Нагорный\nНеправильный вариант❌</em>', parse_mode='html')
            sheet_num = 5
        elif callback.data == 'svao':
            bot.send_message(callback.message.chat.id, 'Отлично! Вы выбрали Северо-Западный административный округ!\
Теперь выбрете район! Для этого введите <em>название района</em> из этого списка:\n1. Марьина Роща\n2. Алексеевский\n3. Останкинский\n\
4. Бутырский\n5. ВДНХ\n6. Шереметьевский\n7. Ростокино\n8. Свиблово\n9. Отрадное\n10. Бабушкинский\n11. Ярославский\n12. Лосиный Остров\n\
13. Медведково\n14. Алтуфьевский\n15. Бибирево\n16. Лианозово\n17. Северный\n18. Марфино\n\
Если вам не важен район, то введите <b>Любой</b>\n\n<em>Например:\nВаше сообщение: Нагорный\nПравильный вариант✅\n\
Ваше сообщение: 1. Нагорный\nНеправильный вариант❌</em>', parse_mode='html')
            sheet_num = 6
        elif callback.data == 'vao':
            bot.send_message(callback.message.chat.id, 'Отлично! Вы выбрали Северо-Западный административный округ!\
Теперь выбрете район! Для этого введите <em>название района</em> из этого списка:\n1. Сокольники\n2. Богородское\n3. Преображенское\n\
4. Метрогородок\n5. Соколиная гора\n6. Гольяново\n7. Измайлово\n8. Перово\n9. Ивановское\n10. Новогиреево\n11. Парк Кусково\n\
12. Вешняки\n13. Новокосино\n14. Косино-Ухтомский\n\
Если вам не важен район, то введите <b>Любой</b>\n\n<em>Например:\nВаше сообщение: Нагорный\nПравильный вариант✅\n\
Ваше сообщение: 1. Нагорный\nНеправильный вариант❌</em>', parse_mode='html')
            sheet_num = 7
        elif callback.data == 'yvao':
            bot.send_message(callback.message.chat.id, 'Отлично! Вы выбрали Северо-Западный административный округ!\
Теперь выбрете район! Для этого введите <em>название района</em> из этого списка:\n1. Лефортово\n2. Нижегородский\n3. Южно-Портовый\n\
4. Печатники\n5. Текстильщики\n6. Рязанский\n7. Кузьминки\n8. Выхино-Жулебино\n9. Люблино\n10. Марьино\n11. Капотня\n\
Если вам не важен район, то введите <b>Любой</b>\n\n<em>Например:\nВаше сообщение: Нагорный\nПравильный вариант✅\n\
Ваше сообщение: 1. Нагорный\nНеправильный вариант❌</em>', parse_mode='html')
            sheet_num = 8

        @bot.message_handler(content_types=['text'])
        def district(message):
            dis = message.text.strip().lower()
            book = openpyxl.open('data/places.xlsx', read_only=True)
            global sheet_num
            sheet = book.worksheets[sheet_num]
            count = 0
            if dis != 'любой':
                for row in range(1, sheet.max_row + 1):
                    if sheet[row][2].value == dis:
                        bot.send_message(message.chat.id, f'{sheet[row][0].value} - {sheet[row][1].value}.')
                        count += 1
            elif dis == 'любой':
                for row in range(1, sheet.max_row+1):
                    bot.send_message(message.chat.id, f'{sheet[row][0].value} - {sheet[row][1].value}.\nРайон - {sheet[row][2].value.capitalize()}')
                    count += 1
            if count == 0:
                bot.send_message(message.chat.id, 'Вы ввели неправильное название района. Попробуйте еще раз!')
            else:
                bot.send_message(message.chat.id, 'Перед каждым местом написано число - это его <b>уникальное ID</b>.\
Если вы хотите узнать более подробную информацию о месте, то введите его ID.', parse_mode='html')
                bot.register_next_step_handler(message, place)

        @bot.message_handler(content_types=['text'])
        def place(message):
            id_place = message.text.strip().lower()
            book = openpyxl.open('data/places.xlsx', read_only=True)
            global sheet_num
            sheet = book.worksheets[sheet_num]
            count = 0
            for row in range(1, sheet.max_row+1):
                if id_place == str(sheet[row][0].value):
                    file = open(f'data/{sheet[row][4].value}', 'rb')
                    bot.send_photo(message.chat.id, file)
                    bot.send_message(message.chat.id, f'<b>{sheet[row][1].value}</b>\n{sheet[row][5].value}\
\n\nСсылка на <b>Яндекс Карты</b> - {sheet[row][3].value}', parse_mode='html')
                    count = 1
            if count == 0 and id_place != 'стоп':
                bot.send_message(message.chat.id, 'Вы ввели неправильное ID. Попробуйте еще раз!')
                bot.register_next_step_handler(message, place)
            elif count == 1:
                bot.send_message(message.chat.id, 'Если вы хотите прекратить вводить ID мест, то введите <b>Стоп</b>. \
Если вы хотите посмотреть дополнительную информацию по другим местам из списка, то введите их ID.', parse_mode='html')
                bot.register_next_step_handler(message, place)
            elif id_place == 'стоп':
                bot.send_message(message.chat.id, 'Отлично! Вы вернулись назад. \
Для того, чтобы выйти в главное меню, введите  /main')



bot.polling(none_stop=True)