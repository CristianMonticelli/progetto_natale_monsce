import telebot
from telebot import types

# Sostituisci <token_string> con il tuo token del bot
TOKEN = '7922807466:AAHGBS-t-9KhuTKN-oc5O39keI4uIitlbmQ'

bot = telebot.TeleBot(TOKEN)

# Funzione per gestire il comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Creazione di una tastiera personalizzata
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    
    # Aggiunta di pulsanti alla tastiera
    itembtn1 = types.KeyboardButton('/insta')
    
    
    # Aggiunta dei pulsanti alla tastiera
    markup.add(itembtn1)

    # Inviare un messaggio con la tastiera personalizzata
    bot.send_message(message.chat.id, "Benvenuto! Scegli un'opzione:", reply_markup=markup)

# Funzione per gestire le risposte degli utenti
@bot.message_handler(func=lambda message: True)
def handle_response(message):
    bot.send_message(message.chat.id, f"Hai scelto: {message.text}")

# Avvio del polling per ricevere messaggi
bot.infinity_polling()