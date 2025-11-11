from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from Personalizados import  InputDater, Dropdown
from Awaiter import wait_file, zerobreaker
import os

def BaixaTudo(Acesso="dudauberaba", Unidade='Uberaba', Days="90"):
    # Days = os.getenv('Days') or 0

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    # Navegação anônima (sem pop-ups do perfil)
    # options.add_argument("--incognito") 

    # Ignorarcertificados
    options.add_argument("--ignore-certificate-errors")

    # Desativa extensões e infobars
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")

    # Desativa plugins e outros recursos de mídia
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-popup-blocking")

    # Desativa sandbox e uso intensivo de recursos (útil em ambientes com poucos recursos)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.add_argument("--disable-blink-features=AutomationControlled")  # Remove detecção de automação
    options.add_argument("--disable-popup-blocking")  # Desativa bloqueio de pop-ups
    options.add_argument("--allow-running-insecure-content")  # Allow insecure content
    options.add_argument("--unsafely-treat-insecure-origin-as-secure=http://associadovp.laks.net.br")  # Replace example.com with your site's domain

    # Desabilita o carregamento de imagens
    prefs0 = {"profile.managed_default_content_settings.images": 2}

    prefs  = {
        "profile.managed_default_content_settings.images": 2,
        "download.default_directory": f'{os.path.join(os.path.expanduser("~"), "Downloads")}',  # Define a pasta de downloads
        "download.prompt_for_download": False,  # Baixar sem perguntar
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,  # Desativa proteção contra arquivos inseguros
        "safebrowsing.disable_download_protection": True,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False

    }
    options.add_experimental_option("prefs", prefs)
    # options.set_preference("permissions.default.image", 2)

    navegador = webdriver.Chrome(options=options)

    link = 'https://associadovp.laks.net.br/'


    # Acesso = os.getenv('Acesso') or "adm.curitiba@viapermuta.com.br"
    # Unidade = os.getenv('Unidade') or "Curitiba"


    navegador.get(link)
    sleep(1)  # É recomendável evitar sleeps fixos e usar o WebDriverWait quando possível
    navegador.find_element(By.NAME, "usu_login").send_keys(Acesso)
    sleep(1)
    navegador.find_element(By.NAME, "usu_senha").send_keys("123456")
    sleep(1)
    navegador.find_element(By.CLASS_NAME, "btn-warning").click()

    # Espera até que um elemento indicando que o login foi bem-sucedido esteja visível
    WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-category")))
    # quit()
    navegador.get("https://associadovp.laks.net.br/franquia/cadastro-associados")

    #WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()=' Exportar extrato do associado']")))
    WebDriverWait(navegador, 100).until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-backdrop")))

    tmp = wait_file("Associados")
    # print(tmp); print("1111")
    #Baixa Arquivo
    icone_exportar_excel = navegador.find_element(By.XPATH, "//i[@title='Exportar para Excel']")
    icone_exportar_excel.click()
    # print("qwet")
    while tmp == wait_file("Associados"):
        # print(tmp); print(wait_file("Associados"));
        # print("AzZZ");
        sleep(1)
    print("passou")


    ###Baixa Saldo:
    # Espera até que um elemento indicando que o login foi bem-sucedido esteja visível
    WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-category")))

    navegador.get("https://associadovp.laks.net.br/franquia/relatorio-saldo-associados")
    #WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "text-center clickable")))

    WebDriverWait(navegador, 100).until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-backdrop")))
    sleep(2)  # Novamente, preferir WebDriverWait a sleep


    tmp = wait_file("Saldo Associados")
    # print(tmp)

    #Baixa Arquivo
    icone_exportar_excel = navegador.find_element(By.XPATH, "//button[text()=' Exportar relatório para Excel']")
    icone_exportar_excel.click()

    while tmp == wait_file("Saldo Associados"):
        sleep(1)
    print("passou")
    # sleep(15 if Unidade == 'Uberaba' else 10)

    #####################################################################################################
    #####################################################################################################
    

    ###Baixa Negociações:
    #$$ Baixa a Lista de Negociações tb:
    # Espera até que um elemento indicando que o login foi bem-sucedido esteja visível
    WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-category")))

    navegador.get("https://associadovp.laks.net.br/franquia/negociacoes")

    '''//////////////////////////////          PYAUTOGUI => InputDater          ///////////////////////////'''
    from datetime import datetime, timedelta

    diaz = 180
    diaz = int(Days) or 90
    # meses = 
    # while not zerobreaker():
    while 1:

        # WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()=' Exportar extrato do associado']")))
        WebDriverWait(navegador, 100).until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-backdrop")))

        """ NEW COMEÇA AQUI """

        # Localizar o elemento <span> pelo texto exato
        navegador.find_element(By.XPATH, "//span[text()='Aplique os filtros para alterar o extrato']").click(); sleep(1)



        Inicio = (datetime.now() - timedelta(days=diaz-1)).strftime("%d/%m/%Y") # .replace('/','') #Baixa o meio ano
        Fim = (datetime.now() - timedelta(days=diaz-30)).strftime("%d/%m/%Y") #.replace('/','')
        # Inicio = (datetime.now() - timedelta(days=diaz)).strftime("%d/%m/%Y") # .replace('/','') #Baixa o meio ano
        # Fim = (datetime.now() - timedelta(days=diaz-29)).strftime("%d/%m/%Y") #.replace('/','') # Assim vai até ontem, o que pode ser até melhor

        # Início index=0 ordem do array de dater's inputs:
        InputDater(navegador=navegador, data=Inicio, index=0, label="Início"); sleep(0.5) #chrome

        # Fim:
        InputDater(navegador=navegador, data=Fim, index=1, label="Fim"); sleep(0.5) #chrome
        
        # botao_buscar = navegador.find_element(By.CLASS_NAME, "fas fa-file-export")
        botao_buscar = navegador.find_element(By.XPATH, "//button[text()=' Buscar']")
        botao_buscar.click()

        # Depois de dar o buscar (search): volta pra backdrop e tem q dar o wait:
        #  
        #WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()=' Exportar extrato do associado']")))
        WebDriverWait(navegador, 200).until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-backdrop"))); sleep(0.5)

        # Search OldFiles:
        tmp = wait_file("negociacoes_filtradas_")

        # Clica pra baixar:
        navegador.find_element(By.XPATH, "//button[text()=' Exportar planilha']").click()

        # Compara com OldFiles em tempo real:
        while tmp == wait_file("negociacoes_filtradas_"):
            sleep(1)
        print("passou")


        diaz-=30 #Iterar antes de ver:

        if diaz<=0:
            break
        """ else:
            diaz-=30 """




    navegador.quit()
    sleep(1)


# CHAMADA:
""" 
Unidades = [{'v':'Uberaba', 'k':"dudauberaba", 'f':'URA1'}, {'v':'Araxa', 'k':"dudaaraxa", 'f':'AAX1'}, {'v':'Curitiba', 'k':'adm.curitiba@viapermuta.com.br', 'f':'CWB2'}, {'v':'Ribeirao_Preto', 'k':"contato.rib1@viapermuta.com.br", 'f':'RIB1'}, {'v':'Uberlandia', 'k':"igor.uberlandia", 'f':'UDIA1'}]


# 1° Etapa Baixa o Associados:

for i in Unidades:
    # print(f"Etapa {i.get('v')}:")
    if i.get('f')=='URA1':
        Unidade = i.get('v')
        Acesso = i.get('k') 

print(Acesso,Unidade)
"""
# BaixaTudo(Acesso, Unidade)








