import re
import pandas as pd
from bs4 import BeautifulSoup


def unparser(filepather = "Associados.xls", header = 0):
    # Lê o arquivo HTML
    # --- ANTIGO (comentado p/ time dev): forçava latin-1 quando header=0 (falsy),
    #     corrompendo acentos UTF-8 -> ex: UBERLÂNDIA virava UBERLÃ\x82NDIA ---
    # with open(filepather, "r", encoding="utf-8" if header else 'latin-1') as f:
    # # with open(filepather, "r", encoding="utf-8") as f:
    #     html = f.read()
    # --- NOVO: estes ".xls" são HTML em UTF-8; lê bytes e decodifica UTF-8
    #     (fallback latin-1 só se não for UTF-8 válido) ---
    with open(filepather, "rb") as f:
        raw = f.read()
    try:
        html = raw.decode("utf-8")
    except UnicodeDecodeError:
        html = raw.decode("latin-1")

    # Função para substituir sequências de dois ou mais espaços por um marcador que indica a quantidade
    def replace_spaces(match):
        num_spaces = len(match.group(0))
        return f"___SPACE_{num_spaces}___"

    # Substitui todas as ocorrências de dois ou mais espaços
    html_modified = re.sub(r" {2,}", replace_spaces, html)

    # Faz o parsing do HTML com BeautifulSoup
    soup = BeautifulSoup(html_modified, "html5lib")
    html_str = str(soup)

    # Lê a tabela do HTML modificado
    # df = pd.read_html(html_str, header=header)[0]
    df = pd.read_html(html_str, header=0)[0]

    # Função para restaurar os espaços a partir do marcador
    def restore_spaces(text):
        return re.sub(r"___SPACE_(\d+)___", lambda m: " " * int(m.group(1)), text)

    if not header: 
        # Aplica a restauração para todas as células que forem do tipo string
        df = df.applymap(lambda x: restore_spaces(x) if isinstance(x, str) else x)
    else:
        #Passar colunas nos parametros nome razao, associado comprador/vendedor
        # df["Associado Comprador"] = df["Associado Comprador"].apply(restore_spaces)
        # df["Associado Vendedor"] = df["Associado Vendedor"].apply(restore_spaces)

        df["COMPRADOR"] = df["COMPRADOR"].apply(restore_spaces)
        df["VENDEDOR"] = df["VENDEDOR"].apply(restore_spaces)

    # print(df.iloc[0])
    return df

# unparser()

