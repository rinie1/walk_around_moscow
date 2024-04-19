import telebot
from telebot import types
import openpyxl
import random

bot = telebot.TeleBot('') #bot token
sheet_num = 0
id_place = ''

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Дальше➡️', callback_data='next'))
    bot.send_message(message.chat.id, f'👋Привет, <b>{message.from_user.first_name}</b>! Этот бот поможет тебе найти интересные и \
запоминающиеся места в Москве! Здесь ты сможешь увидеть достопримечательности любого района, а также построить маршрут для \
своей прогулки🚶', parse_mode='html', reply_markup=markup)

@markup.add(types.InlineKeyboardButton('Начать', callback_data='main'))
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
                        bot.send_message(message.chat.id, 'Вы ввели неправильное название района. Попробуйте еще раз! Если вы хотите выйти из поиска, то введите <b>/main</b>.', parse_mode='html')
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
                     count == 1:
                bot.send_message(message.chat.id, 'Если вы хотите прекратить вводить ID мест, то введите <b>Стоп</b>. \
Если вы хотите посмотреть дополнительную информацию по другим местам из списка, то введите их ID.', parse_mode='html')
                bot.register_next_step_handler(message, place)
            elif id_place == 'стоп':
                bot.send_message(message.chat.id, 'Отлично! Вы вернулись назад. \
Для того, чтобы выйти в главное меню, введите  /main')



bot.polling(none_stop=True)
