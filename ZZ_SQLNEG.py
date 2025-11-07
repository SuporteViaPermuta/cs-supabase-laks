import psycopg2, pandas as pd, warnings
warnings.simplefilter(action='ignore', category=UserWarning)
from datetime import datetime, timedelta
import os
# Days = os.getenv('Days') or 90-1 or 120
# Days = 90 or 89

# Configurações de conexão
db_config = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "Lipidios10$*",
    "host": "db.gumtdqwzdskbjxzijnto.supabase.co",
    "port": "5432",  # Padrão+1 do PostgreSQL porta pública
}

db_config = {
    "dbname": "postgres",
    "user": "postgres.gumtdqwzdskbjxzijnto",
    "password": "Lipidios10$*",
    "host": "aws-0-sa-east-1.pooler.supabase.com",
    "port": "5432",  # Padrão+1 do PostgreSQL porta pública
}

def Get_Postgres(includes=["*"], TableName="z1lista_associados", header=0, Days=90):

    query = f'select {", ".join(includes)} from "{TableName}"'
    # Inicio = (datetime.now() - timedelta(days=int(Days))).strftime("%Y-%m-%d")
    Inicio = (datetime.now() - timedelta(days=int(Days)-1)).strftime("%Y-%m-%d")
    Fim = datetime.now().strftime("%Y-%m-%d")
    
    query+=" WHERE COALESCE(situacao, '') <> 'excluido' "

    if not header:
        query += f"and data >= '{Inicio}'::date and data <= '{Fim}'::date"
    # query += f"WHERE data >= '2024-03-14'::date and data <= '2024-03-14'::date"
    # query = 'select * from "z1lista_associados"'

    conn = psycopg2.connect(**db_config)
    # print(query)
    # Criar um DataFrame com os dados da tabela
    df = pd.read_sql(query, conn)

    # Fechar a conexão
    conn.close()

    # Exibir os dados
    # print(df)
    return df

# Get_Postgres(['nome_fantasia', 'situacao'], "z1lista_associados")



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








def BATCH_SoftDelete_Postgres(TableName="z1lista_associados", Lista_ids=[]):
    """
    Atualiza a coluna 'situacao' para 'excluido' nos registros informados por ID.
    """

    if not Lista_ids:
        print("Nenhum ID fornecido para atualização.")
        return

    # Criar placeholders dinâmicos (%s, %s, %s, ...)
    placeholders = ', '.join(['%s'] * len(Lista_ids))

    # Criar a query de UPDATE em vez de DELETE
    query = f'''
        UPDATE "{TableName}"
        SET situacao = 'excluido'
        WHERE id IN ({placeholders})
    '''

    # Criar conexão com o banco
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Executar a query com os valores da lista
    cursor.execute(query, tuple(Lista_ids))

    # Commit e fechar conexão
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(Lista_ids)} registros marcados como 'excluido' na tabela {TableName}.")









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


