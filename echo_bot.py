import telebot
from telebot import types
import os
import json
import threading
import time
from datetime import datetime
from instagrapi import Client
import signal


# Crea un'istanza del client Instagram
cl = Client()

data_file = 'immagini/photos_data.json'

# Lista per memorizzare i dati delle foto
photos_data = []

class PostProgrammati:
    def __init__(self, file_path, future_datetime, chat_id, caption, media_type):
        self._file_path = file_path
        self._future_datetime = future_datetime
        self._chat_id = chat_id
        self._caption = caption
        self._media_type = media_type

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        self._file_path = file_path

    @property
    def future_datetime(self):
        return self._future_datetime

    @future_datetime.setter
    def future_datetime(self, future_datetime):
        self._future_datetime = future_datetime

    @property
    def chat_id(self):
        return self._chat_id

    @chat_id.setter
    def chat_id(self, chat_id):
        self._chat_id = chat_id

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, caption):
        self._caption = caption

    @property
    def media_type(self):
        return self._media_type

    @media_type.setter
    def media_type(self, media_type):
        self._media_type = media_type

    def caricaPost(self):
        # Carica il file
        image_path = self.file_path
        caption = self.caption
        media_type = self.media_type
        if media_type == 'post':
            if image_path.endswith('.mp4'):
                cl.video_upload(image_path, caption)
                with open(image_path, 'rb') as video:
                    bot.send_video(self.chat_id, video, caption="Post video caricato con successo!")
            else:
                cl.photo_upload(image_path, caption)
                with open(image_path, 'rb') as photo_file:
                    bot.send_photo(self.chat_id, photo_file, caption="Post foto caricato con successo!")
        elif media_type == 'storia':
            if image_path.endswith('.mp4'):
                cl.video_upload_to_story(image_path, caption)
                with open(image_path, 'rb') as video:
                    bot.send_video(self.chat_id, video, caption="Storia video caricato con successo!")
            else:
                cl.photo_upload_to_story(image_path, caption)
                with open(image_path, 'rb') as photo_file:
                    bot.send_photo(self.chat_id, photo_file, caption="Storia foto caricato con successo!")
        
        os.remove(image_path)
        print("Media caricato con successo!")
        save_photos_data()

class Utente:
    def __init__(self, IG_USERNAME, IG_PASSWORD):
        self._IG_USERNAME = IG_USERNAME
        self._IG_PASSWORD = IG_PASSWORD

    @property
    def IG_USERNAME(self):
        return self._IG_USERNAME

    @IG_USERNAME.setter
    def IG_USERNAME(self, IG_USERNAME):
        self._IG_USERNAME = IG_USERNAME

    @property
    def IG_PASSWORD(self):
        return self._IG_PASSWORD

    @IG_PASSWORD.setter
    def IG_PASSWORD(self, IG_PASSWORD):
        self._IG_PASSWORD = IG_PASSWORD

class Bot:
    def __init__(self):
        self.API_TOKEN = '7700145055:AAGqxka9kBvRXY9QTG0isGXSlYFq_LtzXfw'

bot_instance = Bot()
bot = telebot.TeleBot(bot_instance.API_TOKEN)

# Funzione per gestire il comando /fine
@bot.message_handler(commands=['fine'])
def handle_fine_command(message):
    bot.reply_to(message, "Chiusura del programma...")
    save_photos_data()
    os.kill(os.getpid(), signal.SIGINT)

# Funzione per caricare i dati dal file JSON
def load_photos_data():
    global photos_data
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            content = f.read().strip()
            if content:  # Verifica se il file non è vuoto
                data = json.loads(content)
                for item in data:
                    post = PostProgrammati(
                        file_path=item['file_path'],
                        future_datetime=datetime.strptime(item['future_datetime'], '%Y-%m-%d %H:%M'),
                        chat_id=item['chat_id'],
                        caption=item['caption'],
                        media_type=item['media_type']
                    )
                    photos_data.append(post)

# Funzione per salvare i dati nel file JSON
def save_photos_data():
    data = []
    for post in photos_data:
        data.append({
            'file_path': post.file_path,
            'future_datetime': post.future_datetime.strftime('%Y-%m-%d %H:%M'),
            'chat_id': post.chat_id,
            'caption': post.caption,
            'media_type': post.media_type,
        })
    with open(data_file, 'w') as f:
        json.dump(data, f)

# Funzione per gestire il comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Benvenuto! Per favore, inviami il tuo username di Instagram.")
    bot.register_next_step_handler(message, ask_password)

def ask_password(message):
    username = message.text
    bot.send_message(message.chat.id, "Grazie! Ora, per favore, inviami la tua password di Instagram.")
    bot.register_next_step_handler(message, lambda m: show_options(m, username))

def show_options(message, username):
    global cl
    password = message.text
    utente = Utente(username, password)
    
    try:
        cl.login(utente.IG_USERNAME, utente.IG_PASSWORD)
    except Exception as e:
        bot.send_message(message.chat.id, f"Errore di connessione: {str(e)}. Per favore, riprova.")
        bot.send_message(message.chat.id, "Per favore, inviami il tuo username di Instagram.")
        bot.register_next_step_handler(message, ask_password)
        return

    # Creazione di una tastiera personalizzata
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('/insta')
    itembtn2 = types.KeyboardButton('/programmati')
    itembtn3 = types.KeyboardButton('/elimina')
    markup.add(itembtn1, itembtn2, itembtn3)

    # Inviare un messaggio con la tastiera personalizzata
    bot.send_message(message.chat.id, "Benvenuto! Scegli un'opzione:", reply_markup=markup)

# Funzione per gestire il comando /insta
@bot.message_handler(commands=['insta'])
def handle_insta_command(message):
    bot.reply_to(message, "Per favore, invia una foto o un video con la data e l'ora future nel formato 'YYYY-MM-DD HH:MM'.")
    bot.register_next_step_handler(message, process_media)

def process_media(message):
    # Controlla se il messaggio contiene una foto o un video
    if message.content_type in ['photo', 'video']:
        # Chiedi all'utente di inviare la data e l'ora
        bot.reply_to(message, "Perfetto! Ora, per favore, inviami la data e l'ora future nel formato 'YYYY-MM-DD HH:MM'.")
        bot.register_next_step_handler(message, lambda m: ask_datetime(m, message))
    else:
        bot.reply_to(message, "Per favore, invia solo una foto o un video.")
        bot.register_next_step_handler(message, process_media)

def ask_datetime(media_message, original_message):
    try:
        future_datetime = datetime.strptime(media_message.text, '%Y-%m-%d %H:%M')
        if future_datetime <= datetime.now():
            bot.reply_to(media_message, "La data e l'ora devono essere maggiori della data e dell'ora attuali. Per favore, riprova.")
            bot.register_next_step_handler(media_message, lambda m: ask_datetime(m, original_message))
        else:
            # Chiedi all'utente se vuole pubblicare un post o una storia
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            itembtn1 = types.KeyboardButton('Post')
            itembtn2 = types.KeyboardButton('Storia')
            markup.add(itembtn1, itembtn2)
            bot.reply_to(media_message, "Vuoi pubblicare un post o una storia?", reply_markup=markup)
            bot.register_next_step_handler(media_message, lambda m: ask_caption(m, original_message, future_datetime))
    except ValueError:
        bot.reply_to(media_message, "Formato data non valido. Usa 'YYYY-MM-DD HH:MM'. Per favore, riprova.")
        bot.register_next_step_handler(media_message, lambda m: ask_datetime(m, original_message))

def ask_caption(media_message, original_message, future_datetime):
    media_type = media_message.text.lower()
    if media_type not in ['post', 'storia']:
        bot.reply_to(media_message, "Per favore, scegli tra 'Post' o 'Storia'.")
        bot.register_next_step_handler(media_message, lambda m: ask_caption(m, original_message, future_datetime))
        return

    bot.reply_to(media_message, "Per favore, inviami una didascalia per la foto o il video.")
    bot.register_next_step_handler(media_message, lambda m: save_media(m, original_message, future_datetime, media_type))

def save_media(caption_message, original_message, future_datetime, media_type):
    caption = caption_message.text
    file_id = None
    file_type = None

    # Controlla se il messaggio è una foto o un video
    if original_message.content_type == 'photo':
        file_id = original_message.photo[-1].file_id  # -1 per ottenere la foto con la risoluzione più alta
        file_type = 'photo'
    elif original_message.content_type == 'video':
        file_id = original_message.video.file_id
        file_type = 'video'

    # Ottieni informazioni sul file
    file_info = bot.get_file(file_id)

    # Percorso per salvare la foto o video
    download_dir = 'immagini/photos'  # Cambia il nome della cartella se necessario

    # Crea la cartella se non esiste
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Imposta il percorso di download in base al tipo di file
    if file_type == 'photo':
        extension = 'jpg'
    else:
        extension = 'mp4'
    
    download_path = os.path.join(download_dir, f"file_{caption_message.message_id}.{extension}")

    # Scarica il file
    downloaded_file = bot.download_file(file_info.file_path)

    # Salva il file sul tuo computer
    with open(download_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    # Crea un oggetto PostProgrammati e aggiungilo alla lista
    post = PostProgrammati(
        file_path=download_path,
        future_datetime=future_datetime,
        chat_id=original_message.chat.id,
        caption=caption,
        media_type=media_type
    )
    photos_data.append(post)

    # Salva i dati in un file JSON
    save_photos_data()

    # Invia la tastiera personalizzata con i comandi /insta, /programmati e /elimina
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('/insta')
    itembtn2 = types.KeyboardButton('/programmati')
    itembtn3 = types.KeyboardButton('/elimina')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(original_message.chat.id, "Scegli un'opzione:", reply_markup=markup)

    # Rispondi all'utente che la foto o video è stato salvato
    bot.reply_to(caption_message, f"Foto/Video salvato come {download_path} con data e ora future: {future_datetime.strftime('%Y-%m-%d %H:%M')} e didascalia: '{caption_message.text}'")

# Funzione per gestire il comando /programmati
@bot.message_handler(commands=['programmati'])
def handle_programmati_command(message):
    if not photos_data:
        bot.reply_to(message, "Non ci sono post o storie programmati.")
    else:
        for post in photos_data:
            bot.send_message(message.chat.id, f"File: {post.file_path}\nData e ora: {post.future_datetime.strftime('%Y-%m-%d %H:%M')}\nDidascalia: {post.caption}\nTipo: {post.media_type}")

# Funzione per gestire il comando /elimina
@bot.message_handler(commands=['elimina'])
def handle_elimina_command(message):
    if not photos_data:
        bot.reply_to(message, "Non ci sono post o storie programmati.")
    else:
        bot.reply_to(message, "Ecco i post e le storie programmati. Scrivi il numero del file che vuoi eliminare:")
        for post in photos_data:
            file_name = os.path.basename(post.file_path)
            file_number = file_name.split('_')[1].split('.')[0]
            bot.send_message(message.chat.id, f"Numero: {file_number}\nFile: {post.file_path}\nData e ora: {post.future_datetime.strftime('%Y-%m-%d %H:%M')}\nDidascalia: {post.caption}\nTipo: {post.media_type}")
        bot.register_next_step_handler(message, elimina_post)

def elimina_post(message):
    file_number = message.text
    post_to_delete = next((post for post in photos_data if os.path.basename(post.file_path).split('_')[1].split('.')[0] == file_number), None)
    if post_to_delete:
        try:
            os.remove(post_to_delete.file_path)
        except OSError as e:
            bot.reply_to(message, f"Errore durante l'eliminazione del file: {str(e)}")
            return
        photos_data.remove(post_to_delete)
        save_photos_data()
        bot.reply_to(message, f"Il post o la storia con numero {file_number} è stato eliminato.")
    else:
        bot.reply_to(message, "Numero del file non trovato. Per favore, riprova.")
        bot.register_next_step_handler(message, elimina_post)

def check_future_dates():
    while True:
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M')
        for post in photos_data:
            if post.future_datetime.strftime('%Y-%m-%d %H:%M') == current_datetime:
                post.caricaPost()
                photos_data.remove(post)
                save_photos_data()
        time.sleep(60)  # Controlla ogni minuto

# Carica i dati all'avvio del bot
load_photos_data()

# Avvia il thread per controllare le date future
threading.Thread(target=check_future_dates, daemon=True).start()

# Avvia il bot
bot.polling()