import glob, os

def wait_file(Arquivo):
    # Diretório Downloads universal
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    # Padrão de busca compatível com Windows e Linux
    pattern = os.path.join(downloads_dir, f"{Arquivo}*")

    # Busca arquivos
    matching_files = glob.glob(pattern)

    # Filtra apenas .xls e .xlsx
    matching_files = [f for f in matching_files if f.endswith(('.xls', '.xlsx'))]
    matching_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    if matching_files:
        return matching_files[0]

    # Se não achar nada, retorna caminho padrão
    return os.path.join(downloads_dir, f"{Arquivo}.xls")




def zerobreaker():
    
    Arquivo=wait_file("ExtratoAssociado")
    tamanho_bytes = os.path.getsize(Arquivo)
    return tamanho_bytes



