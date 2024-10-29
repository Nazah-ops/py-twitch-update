import http.client
import urllib.parse


def download(url, name, headers=None):
    # Parsing dell'URL per ottenere il dominio e il percorso
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path
    
    if headers is None:
        headers = {}
        
    # Connessione al server
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", path, headers=headers)
    response = conn.getresponse()

    # Verifica che la richiesta sia andata a buon fine
    if response.status != 200:
        raise Exception("Errore durante download del url: ", url, response.status, response.reason)
    
    
    with open(name, "wb") as file:
        while True:
            data = response.read(8192)
            if not data:
                break
            file.write(data)
    conn.close()
    return True