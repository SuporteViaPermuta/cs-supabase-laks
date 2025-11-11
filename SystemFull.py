from time import sleep

from BaixaTudo import BaixaTudo
from ListaAssUnidade import ListaAssUnidade
from ListaNegUnidade import ListaNegUnidade
from SaldoAssUnidade import SaldoAssUnidade

from Send1Unidade import Send1Unidade
from Send2 import Send2
from Send3 import Send3
from Send4 import Send4

from NP4P import NP4P
from NPC1P import NPC1P
from NP4SP import NP4SP
from NP4SRFV import NP4SRFV

from datetime import datetime
import math

# Datas
inicio = datetime(2019, 1, 1)
inicio = datetime(2018, 1, 1)
hoje = datetime.today()

# Diferença em dias
dias = (hoje - inicio).days

# Primeiro múltiplo de 30 acima
multiplo_30 = math.ceil(dias / 30) * 30

# os.environ["Days"] = "120" # Quantidade de dias subtraidos na tabela de negociação
Days = "90"or"120"or"3660"
Days = str(multiplo_30) or "2700"
Days = "90" or "30"
# print(Days)

# Unidades = [{'v':'Uberaba', 'k':"dudauberaba"}, {'v':'Araxa', 'k':"dudaaraxa"}, {'v':'Curitiba', 'k':'adm.curitiba@viapermuta.com.br'}, {'v':'Ribeirao_Preto', 'k':"contato.rib1@viapermuta.com.br"}, {'v':'Uberlandia', 'k':"igor.uberlandia"}]
Unidades = [{'v':'Uberaba', 'k':"dudauberaba"}, {'v':'Araxa', 'k':"dudaaraxa"}, {'v':'Curitiba', 'k':'adm.curitiba@viapermuta.com.br'}, {'v':'Uberlandia', 'k':"igor.uberlandia"}]


# 1° Etapa Baixa o Associados:

for i in Unidades:
    print(f"Etapa {i.get('v')}:")

    Unidade = i.get('v')
    Acesso = i.get('k') 

    BaixaTudo(Acesso, Unidade, Days); sleep(1)

    #Lista Associados xlsx
    ListaAssUnidade(Unidade); sleep(1)

    #Lista Neg ReverseFiltered: xlsx
    ListaNegUnidade(Unidade, Days); sleep(1)

    #Forma Lista Outros Associados - Unidade
    Send1Unidade(Unidade); sleep(1)

    #Saldo 
    SaldoAssUnidade(Unidade); sleep(1)

 

# 2° Etapa União dos resultados:

#Junta Lista de Associados:
Send3(); sleep(1)

#Junta Lista Reverse de Negociações:
Send2(Days); sleep(1)

# Junta Saldo Associados
Send4(); sleep(1)

print('Fim Etapa 1')
# quit()
# sleep(1000000000) #Intermediária - Exchange nome_fantasia: Send5( # Melhor pelo postgres já q tem q baixar a planilha de qualquer jeito)



#### ETAPA 2 ###

# 1°: Atualizar a Lista de Associados, nela do SUPABASE: Ela q é a planilha principal de gancho para as outras planilhas!!
print('Lista de Associados')
NP4P(); sleep(2)
from ZZ_SQL import update_nome_fantasia; update_nome_fantasia() ## Muda Nome Fantasia na lista de negociações:

from NP4PNotion import NP4PNotion
NP4PNotion()

# sleep(10000)



# 2°: Atualizar a Lista de Negociações, nela do SUPABASE: Ela necessita da Lista de Associados atualizada! Pois tem correlação de lookup com ela!
print('Lista de Negociaçoes')
NPC1P(Days); sleep(2)

# 3°: Atualizar a Lista de Saldo dos Associados, nela do SUPABASE: Ela necessita da Lista de Associados atualizada! Pois tem correlação de lookup com ela!
print('Saldo Associados')
NP4SP(); sleep(2)


# Atualiza as colunas de formulas:
from ZZ_SQL import Formulador
Formulador(); sleep(2)


# Way Back 2:
with open("status.txt", "w") as arquivo:
    arquivo.write("status: terminado")


#Envio PAC
sleep(2)
from ZZZrequestPAC import PAC
PAC()











