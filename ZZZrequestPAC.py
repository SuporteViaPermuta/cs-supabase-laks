import requests

def PAC():
    # URL que você quer acessar
    url = "https://webh.whybsc.com.br/webhook/botaopac"

    try:
        # faz o GET
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # dispara exceção em caso de status >=400

        # se for JSON, captura o dict
        data = response.json()
        print("Resposta JSON:", data)

    except requests.exceptions.HTTPError as errh:
        print("HTTP error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Erro de conexão:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout:", errt)
    except requests.exceptions.RequestException as err:
        print("Erro inesperado:", err)

    return
