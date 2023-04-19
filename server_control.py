import telebot
import paramiko
import time
import configparser
import threading

# Считываем логины и пароли из файла config.ini
config = configparser.ConfigParser()
config.read('./config.ini')

bot = telebot.TeleBot(config.get('telegram', 'token'))

def get_server1():
    try:
        get_server1.__connect
    except AttributeError:
        get_server1.__connect = None
    if not get_server1.__connect or get_server1.__connect.get_transport() or get_server1.__connect.get_transport().is_active():
        get_server1.__connect = paramiko.SSHClient()
        get_server1.__connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        get_server1.__connect.connect(
            config.get('servers', 'server1_ip'), 
            22, 
            config.get('servers', 'username'), 
            password=config.get('servers', 'password1')
        )
    return get_server1.__connect

def get_server2():
    try:
        get_server2.__connect
    except AttributeError:
        get_server2.__connect = None
    if not get_server2.__connect or get_server2.__connect.get_transport() or get_server2.__connect.get_transport().is_active():
        get_server2.__connect = paramiko.SSHClient()
        get_server2.__connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        get_server2.__connect.connect(
            config.get('servers', 'server2_ip'),
            22, 
            config.get('servers', 'username'), 
            password=config.get('servers', 'password2')
        )
    return get_server2.__connect


# создаем обработчик нажатия на кнопку "solana withdraw"
@bot.callback_query_handler(func=lambda call: call.data == 'get_solana_withdraw')
def get_solana_withdraw(call):
    # запрос числа у пользователя
    bot.send_message(call.message.chat.id, 'Введите значение:')
    bot.register_next_step_handler(call.message, process_value)


def process_value(message):
    global value
    try:
        value = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка! Введите число.')
        return
    # формируем команду с использованием переменной value
    command = f'/root/.local/share/solana/install/active_release/bin/solana withdraw-from-vote-account /root/solana/vote-account-keypair_new1.json --authorized-withdrawer "/root/solana/solflare/solflare777777.json" "/root/solana/identity_ex1arey_mainet.json" {value}'
    # выполняем команду на сервере
    stdin, stdout, stderr = get_server1().exec_command(command)
    # получаем вывод команды
    output = stdout.read().decode()
    if output:
        # отправляем результат пользователю
        bot.send_message(message.chat.id, output)
    else:
        output = stderr.read().decode()
        bot.send_message(message.chat.id, f'Команда выполнена, но ничего не вернула. {output}')


# создаем обработчик нажатия на кнопку "solana version"
@bot.callback_query_handler(func=lambda call: call.data == 'get_solana_version')
def get_solana_version(call):
    # задаем команду, которую нужно выполнить на сервере
    command = '/root/.local/share/solana/install/active_release/bin/solana --version'
    # выполняем команду на сервере
    stdin, stdout, stderr = get_server1().exec_command(command)
    # получаем вывод команды
    output = stdout.read().decode()
    if output:
        # отправляем результат пользователю
        bot.send_message(call.message.chat.id, output)
    else:
        output = stderr.read().decode()
        bot.send_message(call.message.chat.id, "Команда выполнена, но ничего не вернула. %s" % output)


# создаем обработчик нажатия на кнопку "go solana binance"
@bot.callback_query_handler(func=lambda call: call.data == 'go_solana_binance')
def go_solana_binance(call):
    # запрос числа у пользователя
    bot.send_message(call.message.chat.id, 'Введите значение:')
    bot.register_next_step_handler(call.message, process_value_3)


def process_value_3(message):
    global value
    try:
        value = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка! Введите число.')
        return
    # формируем команду с использованием переменной value
    command = f'/root/.local/share/solana/install/active_release/bin/solana transfer --from /root/solana/identity_ex1arey_mainet.json 3iX8f64vRsFCzAsbC7N1BdQHjN8dd7fwVzHrQmiCM2nR {value} --fee-payer /root/solana/identity_ex1arey_mainet.json'
    # выполняем команду на сервере
    stdin, stdout, stderr = get_server1().exec_command(command)
    # получаем вывод команды
    output = stdout.read().decode()
    if output:
        # отправляем результат пользователю
        bot.send_message(message.chat.id, output)
    else:
        output = stderr.read().decode()
        bot.send_message(message.chat.id, f'Команда выполнена, но ничего не вернула. {output}')


# создаем обработчик нажатия на кнопку "solana balance"
@bot.callback_query_handler(func=lambda call: call.data == 'get_solana_balance')
def get_solana_balance(call):
    # задаем команду, которую нужно выполнить на сервере
    command = '/root/.local/share/solana/install/active_release/bin/solana balance'
    # выполняем команду на сервере
    stdin, stdout, stderr = get_server1().exec_command(command)
    # получаем вывод команды
    output = stdout.read().decode()
    if output:
        # отправляем результат пользователю
        bot.send_message(call.message.chat.id, output)
    else:
        output = stderr.read().decode()
        bot.send_message(call.message.chat.id, "Команда выполнена, но ничего не вернула. %s" % output)


# создаем обработчик нажатия на кнопку "solana balance vote account"
@bot.callback_query_handler(func=lambda call: call.data == 'solana_balance_vote_account')
def solana_balance_vote_account(call):
    # задаем команду, которую нужно выполнить на сервере
    command = '/root/.local/share/solana/install/active_release/bin/solana balance /root/solana/vote-account-keypair_new1.json'
    # выполняем команду на сервере
    stdin, stdout, stderr = get_server1().exec_command(command)
    # получаем вывод команды
    output = stdout.read().decode()
    if output:
        # отправляем результат пользователю
        bot.send_message(call.message.chat.id, output)
    else:
        output = stderr.read().decode()
        bot.send_message(call.message.chat.id, "Команда выполнена, но ничего не вернула. %s" % output)


# создаем обработчик нажатия на кнопку "solana epoch-info"
@bot.callback_query_handler(func=lambda call: call.data == 'get_solana_epoch')
def get_solana_epoch(call):
    # задаем команду, которую нужно выполнить на сервере
    command = '/root/.local/share/solana/install/active_release/bin/solana epoch-info'
    # выполняем команду на сервере
    stdin, stdout, stderr = get_server1().exec_command(command)
    # получаем вывод команды
    output = stdout.read().decode()
    if output:
        # отправляем результат пользователю
        bot.send_message(call.message.chat.id, output)
    else:
        output = stderr.read().decode()
        bot.send_message(call.message.chat.id, "Команда выполнена, но ничего не вернула. %s" % output)


# создаем обработчик нажатия на кнопку "solana withdraw"
@bot.callback_query_handler(func=lambda call: call.data == 'get_solana_withdraw_2')
def get_solana_withdraw_2(call):
    # запрос числа у пользователя
    bot.send_message(call.message.chat.id, 'Введите значение:')
    bot.register_next_step_handler(call.message, process_value_2)


def process_value_2(message):
    global value
    try:
        value = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка! Введите число.')
        return
    # формируем команду с использованием переменной value
    command = f'/root/.local/share/solana/install/active_release/bin/solana withdraw-from-vote-account /root/solana/vote-account-key_annet.json --authorized-withdrawer "/root/solana/solflare/solflare.json" "/root/solana/mainnet_annet_keypair.json" {value}'
    # выполняем команду на сервере
    stdin, stdout, stderr = get_server2().exec_command(command)
    # получаем вывод команды
    output = stdout.read().decode()
    if output:
        # отправляем результат пользователю
        bot.send_message(message.chat.id, output)
    else:
        output = stderr.read().decode()
        bot.send_message(message.chat.id, f'Команда выполнена, но ничего не вернула. {output}')


# создаем обработчик нажатия на кнопку "solana version"
@bot.callback_query_handler(func=lambda call: call.data == 'get_solana_version_2')
def get_solana_version_2(call):
    # задаем команду, которую нужно выполнить на сервере
    command = '/root/.local/share/solana/install/active_release/bin/solana --version'
    # выполняем команду на сервере
    stdin, stdout, stderr = get_server2().exec_command(command)
    # получаем вывод команды
    output = stdout.read().decode()
    if output:
        # отправляем результат пользователю
        bot.send_message(call.message.chat.id, output)
    else:
        output = stderr.read().decode()
        bot.send_message(call.message.chat.id, "Команда выполнена, но ничего не вернула. %s" % output)


# создаем обработчик нажатия на кнопку "solana balance"
@bot.callback_query_handler(func=lambda call: call.data == 'get_solana_balance_2')
def get_solana_balance_2(call):
    # задаем команду, которую нужно выполнить на сервере
    command = '/root/.local/share/solana/install/active_release/bin/solana balance'
    # выполняем команду на сервере
    stdin, stdout, stderr = get_server2().exec_command(command)
    # получаем вывод команды
    output = stdout.read().decode()
    if output:
        # отправляем результат пользователю
        bot.send_message(call.message.chat.id, output)
    else:
        output = stderr.read().decode()
        bot.send_message(call.message.chat.id, "Команда выполнена, но ничего не вернула. %s" % output)


# создаем обработчик нажатия на кнопку "solana balance vote account"
@bot.callback_query_handler(func=lambda call: call.data == 'solana_balance_vote_account_2')
def solana_balance_vote_account(call):
    # задаем команду, которую нужно выполнить на сервере
    command = '/root/.local/share/solana/install/active_release/bin/solana balance /root/solana/vote-account-key_annet.json'
    # выполняем команду на сервере
    stdin, stdout, stderr = get_server2().exec_command(command)
    # получаем вывод команды
    output = stdout.read().decode()
    if output:
        # отправляем результат пользователю
        bot.send_message(call.message.chat.id, output)
    else:
        output = stderr.read().decode()
        bot.send_message(call.message.chat.id, "Команда выполнена, но ничего не вернула. %s" % output)


# создаем обработчик нажатия на кнопку "solana epoch-info"
@bot.callback_query_handler(func=lambda call: call.data == 'get_solana_epoch_2')
def get_solana_epoch_2(call):
    # задаем команду, которую нужно выполнить на сервере
    command = '/root/.local/share/solana/install/active_release/bin/solana epoch-info'
    # выполняем команду на сервере
    stdin, stdout, stderr = get_server2().exec_command(command)
    # получаем вывод команды
    output = stdout.read().decode()
    if output:
        # отправляем результат пользователю
        bot.send_message(call.message.chat.id, output)
    else:
        output = stderr.read().decode()
        bot.send_message(call.message.chat.id, "Команда выполнена, но ничего не вернула. %s" % output)


# создаем обработчик нажатия на кнопку "go solana binance"
@bot.callback_query_handler(func=lambda call: call.data == 'go_solana_binance_1')
def go_solana_binance_1(call):
    # запрос числа у пользователя
    bot.send_message(call.message.chat.id, 'Введите значение:')
    bot.register_next_step_handler(call.message, process_value_4)


def process_value_4(message):
    global value
    try:
        value = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка! Введите число.')
        return
    # формируем команду с использованием переменной value
    command = f'/root/.local/share/solana/install/active_release/bin/solana transfer --from /root/solana/mainnet_annet_keypair.json 3iX8f64vRsFCzAsbC7N1BdQHjN8dd7fwVzHrQmiCM2nR {value} --fee-payer /root/solana/mainnet_annet_keypair.json'
    # выполняем команду на сервере
    stdin, stdout, stderr = get_server2().exec_command(command)
    # получаем вывод команды
    output = stdout.read().decode()
    if output:
        # отправляем результат пользователю
        bot.send_message(message.chat.id, output)
    else:
        output = stderr.read().decode()
        bot.send_message(message.chat.id, f'Команда выполнена, но ничего не вернула. {output}')


# создаем обработчик команды /kiev
@bot.message_handler(commands=['kiev'])
def start(message):
    # создаем кнопки "solana version" и "solana withdraw" и добавляем их на клавиатуру
    button_version = telebot.types.InlineKeyboardButton(text='solana version', callback_data='get_solana_version')
    button_epoch_info = telebot.types.InlineKeyboardButton(text='solana epoch', callback_data='get_solana_epoch')
    button_go_binance = telebot.types.InlineKeyboardButton(text='transfer to binance', callback_data='go_solana_binance')
    solana_balance_vote_account = telebot.types.InlineKeyboardButton(text='balance vote account', callback_data='solana_balance_vote_account')
    button_balance = telebot.types.InlineKeyboardButton(text='solana balance', callback_data='get_solana_balance')
    button_withdraw = telebot.types.InlineKeyboardButton(text='solana withdraw', callback_data='get_solana_withdraw')

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(button_version, button_balance, )
    keyboard.add(button_epoch_info, button_go_binance)
    keyboard.add(solana_balance_vote_account, button_withdraw)

    # отправляем сообщение с клавиатурой
    bot.send_message(message.chat.id, 'Привет! Выберите действие:', reply_markup=keyboard)


# создаем обработчик команды /makariv
@bot.message_handler(commands=['makariv'])
def start(message):
    # создаем кнопки "solana version" и "solana withdraw" и добавляем их на клавиатуру
    button_version = telebot.types.InlineKeyboardButton(text='solana version', callback_data='get_solana_version_2')
    button_epoch_info = telebot.types.InlineKeyboardButton(text='solana epoch', callback_data='get_solana_epoch_2')
    solana_balance_vote_account = telebot.types.InlineKeyboardButton(text='balance vote account', callback_data='solana_balance_vote_account_2')
    button_balance = telebot.types.InlineKeyboardButton(text='solana balance', callback_data='get_solana_balance_2')
    button_go_binance = telebot.types.InlineKeyboardButton(text='transfer to binance', callback_data='go_solana_binance_1')
    button_withdraw = telebot.types.InlineKeyboardButton(text='solana withdraw', callback_data='get_solana_withdraw_2')

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(button_version, button_balance)
    keyboard.add(button_epoch_info, button_go_binance)
    keyboard.add(solana_balance_vote_account, button_withdraw)

    # отправляем сообщение с клавиатурой
    bot.send_message(message.chat.id, 'Привет! Выберите действие:', reply_markup=keyboard)


def check_connection():
    while True:
        print("In cycle")
        time.sleep(60)


# запускаем бота
bot_thread = threading.Thread(target=bot.polling)
bot_thread.start()

# проверяем соединение
check_connection()

