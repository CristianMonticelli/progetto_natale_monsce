from instagrapi import Client
from instagrapi.types import StoryMention, UserShort, StoryLink
from instagrapi.story import StoryBuilder

# Credenziali Instagram
USERNAME = 'monscelli'
PASSWORD = '(Progetto1)'

# Crea un'istanza del client Instagram e effettua il login
cl = Client()
cl.login(USERNAME, PASSWORD)

# Carica un video o un'immagine
media_path = 'file_177.jpg'  # Assicurati che il file esista nel percorso specificato

# Ottieni l'ID dell'utente da menzionare
username_to_mention = 'lamontix'
user_id = cl.user_id_from_username(username_to_mention)

# Crea un'istanza di UserShort con l'ID dell'utente
user_short = UserShort(pk=user_id)

# Crea un'istanza di StoryMention con l'oggetto UserShort
mention = StoryMention(user=user_short)

# Costruisci la storia
buildout = StoryBuilder(media_path, 'Didascalia della storia', [mention]).video(15)

# Carica la storia
cl.video_upload_to_story(
    buildout.path,
    "Didascalia della storia",
    mentions=buildout.mentions,
    links=[StoryLink(webUri='https://example.com')]
)