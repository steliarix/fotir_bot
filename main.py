import telebot
from telebot import types
import configure
import wikipedia
import emoji


client = telebot.TeleBot(configure.config['token'])


# Вызов команды /help

@client.message_handler(commands=['get_help', 'help'])
def get_user_help(message):
    client.send_message(message.chat.id, emoji.emojize('Этот бот преднозначен для быстрого поиска по wikipedia! :cowboy_hat_face: \n'
                                         '\n'
                                         'Для начала выберите язык wikipedia :alien: \n'
                                         '\n'
                                         'Выбор языка вызывается командой\n/language\n'
                                         '\n'
                                         'После чего выберите нужный для поиска язык и делайте запрос :alien_monster:'))


# Вызов клавиатуры выбора языка с помощью команды /language

@client.message_handler(commands=['get_lang', 'language'])
def get_search_lang(message):
    markup_inline = types.InlineKeyboardMarkup()
    ru = types.InlineKeyboardButton(text=emoji.emojize('Русский :Russia:'), callback_data='rus')
    uk = types.InlineKeyboardButton(text=emoji.emojize('Ukraine :Ukraine:'), callback_data='ukr')
    en = types.InlineKeyboardButton(text=emoji.emojize('English :United_States:'), callback_data='eng')

    markup_inline.add(ru, uk, en)
    client.send_message(message.chat.id, 'Вберите язык для поиска!', reply_markup=markup_inline)


# Сообщение об успешной смене языка

@client.callback_query_handler(func=lambda call: True)
def ru_search(call):
    if call.data == 'rus':
        wikipedia.set_lang('ru')
        client.send_message(call.message.chat.id, emoji.emojize('Русский язык поиска успешно поставлен! :Russia:'))
    elif call.data == 'ukr':
        wikipedia.set_lang('uk')
        client.send_message(call.message.chat.id, emoji.emojize('Українська мова пошуку успішно поставлена! :Ukraine:'))
    elif call.data == 'eng':
        wikipedia.set_lang('en')
        client.send_message(call.message.chat.id, emoji.emojize('Search English successfully delivered! :United_States:'))


# Вывод информации с wikipedia и ловля ошибок при неизвестном слове

@client.message_handler(content_types=['text'])
def get_text(message):
    try:
        search = wikipedia.summary(message.text)
        client.send_message(message.chat.id, search)
    except wikipedia.exceptions.PageError:
        client.send_message(message.chat.id, 'Попробуй ещё раз!')
    except wikipedia.exceptions.DisambiguationError:
        client.send_message(message.chat.id, 'Попробуй ещё раз!')
    except wikipedia.exceptions.WikipediaException:
        client.send_message(message.chat.id, 'Попробуй ещё раз!')


# Запуск бота

if __name__ == '__main__':
    client.polling(none_stop=True, interval=0)

