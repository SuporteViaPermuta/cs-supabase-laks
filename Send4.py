import pandas as pd, os, warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def Send4():
    # Unidade = os.getenv('Unidade')
    SaldoAssUberaba = pd.read_excel("Saldo_Associados3-Uberaba.xlsx")
    SaldoAssAraxa = pd.read_excel("Saldo_Associados3-Araxa.xlsx")
    SaldoAssCuritiba = pd.read_excel("Saldo_Associados3-Curitiba.xlsx")
    # SaldoAssRibeirao_Preto = pd.read_excel("Saldo_Associados3-Ribeirao_Preto.xlsx")
    SaldoAssUberlandia = pd.read_excel("Saldo_Associados3-Uberlandia.xlsx")
    SaldoAssFranca = pd.read_excel("Saldo_Associados3-Franca.xlsx")  # Franca adicionada
    # AssociadosOutros = pd.read_excel("AssociadosOutros.xlsx")


    # df_total = pd.concat([SaldoAssUberaba, SaldoAssAraxa, SaldoAssCuritiba, SaldoAssRibeirao_Preto, SaldoAssUberlandia], ignore_index=True)
    # Franca adicionada -> linha antiga (sem Franca) comentada logo abaixo:
    # df_total = pd.concat([SaldoAssUberaba, SaldoAssAraxa, SaldoAssCuritiba, SaldoAssUberlandia], ignore_index=True)
    df_total = pd.concat([SaldoAssUberaba, SaldoAssAraxa, SaldoAssCuritiba, SaldoAssUberlandia, SaldoAssFranca], ignore_index=True)

    df_total = df_total.drop_duplicates()

    # Salvar o resultado em um novo arquivo Excel
    if os.path.exists(f'Saldo_Associados3Totais.xlsx'):
        os.remove(f'Saldo_Associados3Totais.xlsx')
        
    df_total.to_excel("Saldo_Associados3Totais.xlsx", index=False)

# Send4()