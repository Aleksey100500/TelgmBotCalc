import telebot

bot = telebot.TeleBot('5827404162:AAHvRURWQ1W_E0tjeMpriCERnIJ3GQwj0_Y') # взяли токен у ботфазер в телеграмме, он дается
# при создании нового бота

value = ''  # переменная, в которой мы храним текщее значение калкулятора
old_value = '' # переменная, в которой мы храним предыдущее значение калькулятора

# создаем клавиатуру keyboard

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(   telebot.types.InlineKeyboardButton(' ', callback_data='no'), # callback_data то что будет возвращено после нажатия на эту кнопку
                telebot.types.InlineKeyboardButton('C', callback_data='C'),
                telebot.types.InlineKeyboardButton('<=', callback_data='<='),
                telebot.types.InlineKeyboardButton('/', callback_data='/'))

keyboard.row(   telebot.types.InlineKeyboardButton('7', callback_data='7'),
                telebot.types.InlineKeyboardButton('8', callback_data='8'),
                telebot.types.InlineKeyboardButton('9', callback_data='9'),
                telebot.types.InlineKeyboardButton('*', callback_data='*'))

keyboard.row(   telebot.types.InlineKeyboardButton('4', callback_data='4'),
                telebot.types.InlineKeyboardButton('5', callback_data='5'),
                telebot.types.InlineKeyboardButton('6', callback_data='6'),
                telebot.types.InlineKeyboardButton('-', callback_data='-'))

keyboard.row(   telebot.types.InlineKeyboardButton('1', callback_data='1'),
                telebot.types.InlineKeyboardButton('2', callback_data='2'),
                telebot.types.InlineKeyboardButton('3', callback_data='3'),
                telebot.types.InlineKeyboardButton('+', callback_data='+'))

keyboard.row(   telebot.types.InlineKeyboardButton(' ', callback_data='no'),
                telebot.types.InlineKeyboardButton('0', callback_data='0'),
                telebot.types.InlineKeyboardButton(',', callback_data=','),
                telebot.types.InlineKeyboardButton('=', callback_data='='))


# создаем обработчик событий, он будет работать, когда в боте напишем соответствующую команду
@bot.message_handler(commands = ['start', 'calculater'])

#создаем команду боту
def getMessage(message):
    global value
    
    if value == '':
        bot.send_message(message.from_user.id, '0', reply_markup = keyboard)
    else:
        bot.send_message(message.from_user.id, value, reply_markup=keyboard)

    # bot.send_message(message.from_user.id, 'Привет!') #бот отправляет сообщение Привет! на нашу команду /start
    #reply_markup=keyboard мы добавили после приветствия появление клавиатуры, которую мы создали выше

# добавим новый обработчик событий, который будет вызван при нажатии на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value
    data = query.data # тпереь дата это то, что возвращает кнопка или то, чему равен аргумент callback_data

    if data == 'no':
        pass
    elif data =='C':
        value = ''
    elif data == '<=':
        if value != '':
            value = value[:len(value) - 1]
    elif data == '=':
        try:
            value = str(eval(value)) # eval функция калькулятора
        except:
            value = 'Ошибка!'
    else:
        value += data

    if (value != old_value and value != '') or ('0' != old_value and value == ''):

        if value == '':
            bot.edit_message_text(chat_id = query.message.chat.id, message_id = query.message.message_id, text='0', reply_markup=keyboard)
            old_value = '0'
        else:
            bot.edit_message_text(chat_id = query.message.chat.id, message_id = query.message.message_id, text = value, reply_markup=keyboard)
            old_value = value

    if value == 'Ошибка!': value = ''
    
bot.polling(none_stop = False, interval = 0) # запуск и проверка нашего бота, не будет работать пока ничего нет в боте