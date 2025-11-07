import pandas as pd, os, warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore")

def mudanca_nome_fantasia(ListaSupabase, ListaAssociadosLaks):

    mudancas_nome = []  # lista de dicionários

    for valor in ListaSupabase:
        # Encontra o item correspondente na ListaAssociadosLaks pelo CNPJ
        associado_laks = next(
            (a for a in ListaAssociadosLaks if a["cnpj_ou_cpf"] == valor["cnpj_ou_cpf"]),
            None
        )

        # Se encontrou o mesmo CNPJ, verifica se o nome_fantasia mudou
        if associado_laks and valor["nome_fantasia"] != associado_laks["nome_fantasia"]:
            mudancas_nome.append({
                "cnpj_ou_cpf": valor["cnpj_ou_cpf"],
                "nome_antigo": valor["nome_fantasia"],
                "nome_novo": associado_laks["nome_fantasia"]
            })

    print(mudancas_nome)

    # Converter lista de dicionários em DataFrame
    df_mudancas = pd.DataFrame(mudancas_nome)

    # Salvar em arquivo Excel
    df_mudancas.to_excel("mudancas_nome.xlsx", index=False)
    
    # from time import sleep; sleep(100000)





