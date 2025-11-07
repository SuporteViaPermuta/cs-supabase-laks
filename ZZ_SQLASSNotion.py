import  warnings, pandas as pd, requests
warnings.simplefilter(action='ignore', category=UserWarning)

# from notion_client import Client
# Configurações de conexão
# Inicialize o cliente do Notion com o token da sua integração
# notion = Client(auth="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")


def Get_Notion(database_id="21d36fd59cd88047a835f8d688c71910", token="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", includes="*"):
    """
    Busca todos os dados de uma database do Notion e retorna um DataFrame.
    Compatível com qualquer versão da API.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    has_more = True
    next_cursor = None
    results = []

    while has_more:
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        payload = {"page_size": 100}
        if next_cursor:
            payload["start_cursor"] = next_cursor

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        results.extend(data["results"])
        has_more = data.get("has_more", False)
        next_cursor = data.get("next_cursor")

    # Converte propriedades em dicionário simples
    all_rows = []
    for item in results:
        props = item["properties"]
        row = {"id": item["id"]}
        for key, val in props.items():
            t = val["type"]
            v = val.get(t)
            if v is None:
                row[key] = ""
            elif t in ("title", "rich_text"):
                row[key] = v[0]["plain_text"] if v else ""
            elif t == "select":
                row[key] = v["name"] if v else ""
            elif t == "multi_select":
                row[key] = ", ".join([x["name"] for x in v])
            elif t == "date":
                row[key] = v["start"] if v else ""
            elif t == "number":
                row[key] = v
            elif t == "checkbox":
                row[key] = v
            elif t == "people":
                # pega todos os nomes das pessoas associadas
                # row[key] = ", ".join([p.get("name", "") for p in v]) if v else ""

                # pega só o primeiro nome (ou e-mail) do campo de pessoas
                if v and len(v) > 0: row[key] = v[0].get("name", "")
                # if v and len(v) > 0: row[key] = v[0].get("person", {}).get("email", "")
            else:
                row[key] = str(v)
        all_rows.append(row)

    df = pd.DataFrame(all_rows)

    if includes != "*" and isinstance(includes, list):
        df = df[includes]

    return df

# df = Get_Notion()
# df = Get_Notion(includes=[ "id", "CPF ou CNPJ", "Associado", "Status", "Data de Cadastro", "Responsável"])


# # print(df.iloc[0])
# df.to_excel("NotionF.xlsx", index=False)



def BATCH_Update_Notion(data_list=[], token="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"):
    """
    Atualiza múltiplos registros (páginas) na database do Notion,
    com suporte aos tipos: title, select, date e rich_text.
    """

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    updated_count = 0

    for data in data_list:
        # print(data)
        page_id = data.pop("id", None)
        if not page_id:
            print(" X Registro sem 'id', pulando...")
            continue
        # Montar propriedades conforme tipo de cada campo
        properties = {}

        for key, value in data.items():
            if key == "Associado":  # campo tipo title
                properties[key] = {
                    "title": [{"text": {"content": str(value or "")}}]
                }

            elif key == "Data de Cadastro":  # campo tipo date
                properties[key] = {
                    "date": {"start": str(value) if value else None}
                }

            elif key == "Status":  # campo tipo select
                properties[key] = {
                    "select": {"name": str(value)} if value else None
                }

            elif key == "CPF ou CNPJ":  # campo tipo rich_text
                properties[key] = {
                    "rich_text": [{"text": {"content": str(value or "")}}]
                }

            else:
                # Fallback genérico
                properties[key] = {
                    "rich_text": [{"text": {"content": str(value or '')}}]
                }

        payload = {"properties": properties}

        # sleep(20)

        # Enviar PATCH para o Notion
        url = f"https://api.notion.com/v1/pages/{page_id}"
        response = requests.patch(url, headers=headers, json=payload)

        if response.status_code == 200:
            updated_count += 1
            # print('ok')
        else:
            print(f"Erro ao atualizar {page_id}: {response.status_code} - {response.text}")

    print(f"{updated_count} registros atualizados com sucesso no Notion!")
