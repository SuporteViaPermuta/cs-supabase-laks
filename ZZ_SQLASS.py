import psycopg2, pandas as pd, warnings
warnings.simplefilter(action='ignore', category=UserWarning)

# Configurações de conexão
db_config = {
    "dbname": "postgres",
    "user": "postgres.gumtdqwzdskbjxzijnto",
    "password": "Lipidios10$*",
    "host": "aws-0-sa-east-1.pooler.supabase.com",
    "port": "6543",  # Padrão+1 do PostgreSQL porta pública
}


def Get_Postgres(includes=["*"], TableName="z1lista_associados"):

    # query = f'select {", ".join(includes)} from associados."{TableName}"'
    query = f'select {", ".join(includes)} from "{TableName}"'
    # query = 'select * from "z1lista_associados"'

    conn = psycopg2.connect(**db_config)

    # Criar um DataFrame com os dados da tabela
    df = pd.read_sql(query, conn)

    # Fechar a conexão
    conn.close()

    # Exibir os dados
    # print(df)
    return df





def BATCH_Create_Postgres(TableName="z1lista_associados", Completo=[]):

    colunas = ", ".join(Completo[0].keys())
    valores_placeholder = ", ".join(["%s"] * len(Completo[0]))

    query = f'INSERT INTO "{TableName}" ({colunas}) VALUES ({valores_placeholder})'

     # Criar a lista de valores
    valores = [tuple(dado.values()) for dado in Completo]  # Gera lista de tuplas com os valores

    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Executar a query para cada linha
    cursor.executemany(query, valores)

    # Commit e fechar conexão
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Dados inseridos com sucesso na tabela {TableName}!")
    return




# DELETAR
def BATCH_Delete_Postgres(TableName="z1lista_associados", Lista_ids=[]):

    # Criar placeholders dinâmicos (%s, %s, %s, ...)
    placeholders = ', '.join(['%s'] * len(Lista_ids))

    # Criar a query com a cláusula IN
    query = f'DELETE FROM "{TableName}" WHERE id IN ({placeholders})'

    # Criar conexão com o banco
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Executar a query com os valores da lista
    cursor.execute(query, tuple(Lista_ids))

    # Commit e fechar conexão
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Linhas deletadas da tabela {TableName} para os IDs: {Lista_ids}")





def BATCH_Update_Postgres(TableName="z1lista_associados", data_list=[]):
    # Criar a conexão com o banco de dados
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    for data in data_list:
        # Remover o campo 'id' dos dados de entrada, para usá-lo na condição WHERE
        id_value = data.pop('id')

        # Gerar a parte SET da query (coluna = valor)
        set_clause = ', '.join([f"{col} = %s" for col in data.keys()])

        # Criar a query de UPDATE
        query = f'UPDATE "{TableName}" SET {set_clause} WHERE id = %s'

        # Executar a query com os valores para atualizar as colunas e o valor de 'id' na condição WHERE
        cursor.execute(query, tuple(data.values()) + (id_value,))

    # Commit e fechar a conexão
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(data_list)} registros atualizados na tabela {TableName}!")



"""

def mudanca_nome_fantasia(ListaSupabase, ListaAssociadosLaks):

    """"""

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
    
    from time import sleep; sleep(100000)

"""