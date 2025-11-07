import glob, os

def wait_file(Arquivo):
    # Padrão para buscar o arquivo de download mais recente
    pattern = f'{os.path.join(os.path.expanduser("~"), "Downloads")}\\{Arquivo}*.*'
    matching_files = glob.glob(pattern)

    # Filtra apenas arquivos .xls e .xlsx e ordena pela data de modificação
    matching_files = [f for f in matching_files if f.endswith(('.xls', '.xlsx'))]
    matching_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # Se encontrou algum arquivo, tenta ler
    # ... restante do seu código que encontra o arquivo baixado

    if matching_files: 
        latest_matching_file = matching_files[0]
        return latest_matching_file
        # print(latest_matching_file)
    
    return f'{os.path.join(os.path.expanduser("~"), "Downloads")}\\{Arquivo}.xls'
# ff=wait_file("Associados")
# print(ff)





def zerobreaker():
    
    Arquivo=wait_file("ExtratoAssociado")
    tamanho_bytes = os.path.getsize(Arquivo)
    return tamanho_bytes


