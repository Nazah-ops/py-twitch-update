import logging as logger
import os
import ssl

from integrations.youtube import upload
from utils.compose_video import generate_short_format_video
from utils.globals import clean_work_dir
from utils.mongo import close_mongo_client

# Configurazione del logger per registrare messaggi con timestamp in un formato leggibile.
logger.basicConfig(format="[%(asctime)s] - %(message)s", level=logger.INFO,
                   datefmt='%Y-%m-%d %H:%M:%S')

# ATTENZIONE: Disabilitazione della verifica SSL.
# Necessario perché l'API di Pexel restituisce un errore durante la verifica SSL.
# Questo workaround è rischioso e dovrebbe essere evitato in produzione.
ssl._create_default_https_context = ssl._create_unverified_context  # type: ignore


def main():
    logger.info('Starting video making process')

    # Pulisce la directory di lavoro rimuovendo file temporanei o non necessari.
    # Questo aiuta a mantenere un ambiente pulito per l'elaborazione successiva
    clean_work_dir()
    logger.info("Workspace directory cleaned")

    # Genera il video breve, il titolo e le parole chiave.
    # La funzione restituisce il path dove e' stato memorizzato il video.
    video, title = generate_short_format_video()
    logger.info("Video produced: %s", title)

    # Controlla se l'ambiente è di produzione. Se sì, carica il video.
    # In ambienti non di produzione (es. sviluppo), il video non viene caricato.
    if os.environ.get('ENV') == "PROD":
        upload(file=video, title=title)
        logger.info(
            "Uploading video to platform in PROD environment: %s", title)
    else:
        logger.info("Not uploaded to youtube, enviroment is: %s",
                    os.environ.get('ENV'))

    # Chiude il client MongoDB per liberare risorse.
    # Utile per garantire che non ci siano connessioni aperte dopo l'esecuzione.
    close_mongo_client()
    logger.info("MongoDB client closed successfully")


if __name__ == "__main__":
    main()

# NOTE TO SELF
# per convertire un AVI pesante per l'into a un mov -> ffmpeg -i Editor.avi -map 0 -c:v png -c:a copy output.mov
