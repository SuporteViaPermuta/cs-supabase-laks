import psycopg2, pandas as pd, warnings
warnings.simplefilter(action='ignore', category=UserWarning)

db_config = {
    "dbname": "postgres",
    "user": "postgres.gumtdqwzdskbjxzijnto",
    "password": "Lipidios10$*",
    "host": "aws-0-sa-east-1.pooler.supabase.com",
    "port": "5432",  # Padrão+1 do PostgreSQL porta pública
}


def Get_Postgres(includes=["*"], TableName="z1lista_associados"):

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

# Get_Postgres(['nome_fantasia', 'situacao'], "z1lista_associados")

def BATCH_Create_PostgresNULL(TableName="z1lista_associados", Completo=[]):

    # BATCH_SIZE = 200; Values = ''
    # for i in range(0, Completo.__len__(), BATCH_SIZE):
    #     Linha = Completo[i:i + BATCH_SIZE]

    Values = ''
    for Linha in Completo:
        Values+=f"({", ".join(Linha.values())})\n"


    query = f'INSERT INTO {TableName} ({", ".join(Completo[0].keys())})"\n'
    query += 'VALUES\n'
    query += f'{Values}'
    print(query)
    # return


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



def BATCH_Update_PostgresNULL(TableName, Lista_ids, new_values, db_config):
    # Criar conexão com o banco
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Criar placeholders dinâmicos para a lista de IDs e valores
    placeholders = ', '.join(['%s'] * len(Lista_ids))
    set_clause = ', '.join([f"{col} = %s" for col in new_values.keys()])

    # Criar a query de UPDATE
    query = f'UPDATE {TableName} SET {set_clause} WHERE id IN ({placeholders})'

    # Organizar os valores para passar no execute
    values = list(new_values.values()) + Lista_ids

    # Executar a query com os valores
    cursor.execute(query, tuple(values))

    # Commit e fechar a conexão
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Linhas da tabela {TableName} atualizadas para os IDs: {Lista_ids}")







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