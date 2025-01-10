# Progetto Natale Monsce

## Ispirazione/Obiettivo
Il programma punta a risolvere un problema moderno che ho notato: quando si vuole pubblicare una foto o un video di una serata, ma bisogna aspettare perché si è detto a qualcuno che quella sera non c'era niente. Con questo bot Telegram, si ha la possibilità di programmare post o storie su Instagram che verranno pubblicati automaticamente all'ora e giorno indicati al bot.

## Funzionalità
- Programmazione di post e storie su Instagram.
- Caricamento automatico di foto e video all'ora e data specificate.
- Gestione delle credenziali Instagram tramite interazione con l'utente su Telegram.
- Salvataggio e ripristino dei dati utilizzando file JSON.
- Possibilità di cancellare un post programmato.
- Possibilità di visualizzare tutti i post programmati.
### Come funziona
1. premere /start

2. inviare username e password Instagram (non saranno memorizzate)

3. scegliere tra /insta /programmati /elimina
- /insta: programma una storia o un post su Instagram
- /programmati: visualizza tutti i post programmati
- /elimina: cancella un post programmato

!!vengono postati i post sul account corrente

## Librerie principali
- **Telegram**: `telebot`
- **Instagram**: `instagrapi`

## Requisiti
Assicurati di avere Python installato sul tuo sistema. Puoi installare le dipendenze necessarie utilizzando il file `requirements.txt`.

```sh
pip install -r requirements.txt
```

## File principale
Il file principale da eseguire per avviare il bot è `echo_bot.py`.

## Ambiente virtuale
Si consiglia di utilizzare un ambiente virtuale per gestire le dipendenze del progetto. Ecco come creare e attivare un ambiente virtuale:

1. Crea un ambiente virtuale:
    ```sh
    python -m venv venv
    ```
2. Attiva l'ambiente virtuale:
    - Su Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - Su macOS e Linux:
        ```sh
        source venv/bin/activate
        ```

## Utilizzo
1. Clona il repository o scarica i file del progetto.

2. Installa le dipendenze:
    ```sh
    pip install -r requirements.txt
    ```
3. Esegui il bot:
    ```sh
    python echo_bot.py
    ```
4. Interagisci con il bot su Telegram:
    - Invia il comando `/start` per iniziare.
    - Fornisci il tuo username e password di Instagram.
    - Invia una foto o un video con la data e l'ora future nel formato `YYYY-MM-DD HH:MM`.
    - Scegli se pubblicare un post o una storia.
    - Fornisci una didascalia per la foto o il video.
    - Ulteriori specifiche saranno fornite dal bot in chat

![Screenshot del bot in azione](inutilita/fotoIntroSimpatica.png)

