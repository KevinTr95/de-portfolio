# Immagine di partenza: Python 3.12 ufficiale, nella versione ridotta
FROM python:3.12-slim

# Fa stampare a Python i messaggi subito, senza tenerli in memoria
ENV PYTHONUNBUFFERED=1

# Crea un utente senza privilegi di amministratore
RUN useradd --create-home appuser

# Cartella di lavoro dentro l'immagine
WORKDIR /app

# Prima le dipendenze, che cambiano raramente
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Poi il codice, che cambia più spesso
COPY ingest.py .

# Da qui in poi, tutto gira come appuser e non come root
USER appuser

# Il comando eseguito all'avvio di ogni container
ENTRYPOINT ["python", "ingest.py"]