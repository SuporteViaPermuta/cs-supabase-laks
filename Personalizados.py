from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep
def InputDater(navegador, data, index, label=""):
    
    data = data.replace('/','')
    # print(data)

    # Aguarda até que os dois inputs estejam presentes na página
    data_inputs = WebDriverWait(navegador, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.form-group input[type='date'].form-control"))
    )

    # rola pro elemento:
    label_element = navegador.find_element(By.XPATH, f"//label[contains(text(), '{label}')]")
    # navegador.execute_script("arguments[0].scrollIntoView();", label_element); sleep(0.5); sleep(0.5)
    navegador.execute_script("arguments[0].scrollIntoView();", data_inputs[index]); sleep(0.5); sleep(0.5)

    if len(data_inputs) >= 2:
        data_inputs = data_inputs[index]

        # Obtém o tamanho e posição do input
    size = data_inputs.size
    # location = data_inputs.location

    # Calcula a posição do canto esquerdo (evita clicar no ícone de calendário)
    offset_x = 5   # Posição um pouco à direita da borda esquerda
    offset_y = size['height'] // 2  # Mantém o clique centralizado na altura

    # Move o cursor até o canto esquerdo e clica
    actions = ActionChains(navegador)
    actions.move_to_element_with_offset(data_inputs, offset_x, offset_y).click().send_keys(data).perform()

    sleep(0.5)
    return




def Dropdown(navegador, label, desiredOption, siblingClass="react-select-container", Letters_minAss=0, hidden=False, index=0, TLE=0):
    # Inicio:

    label_element = navegador.find_element(By.XPATH, f"//label[contains(text(), '{label}')]")

    if label_element and not hidden:
        react_element = label_element.find_element(By.XPATH, f"./following-sibling::div[contains(@class, '{siblingClass}')]")
    else:
        react_element = navegador.find_element(By.XPATH, f"//div[contains(@class, '{siblingClass}')]")
        

    # rola pro elemento:
    navegador.execute_script("arguments[0].scrollIntoView();", react_element)

    actions = ActionChains(navegador, 500+TLE)

    if not Letters_minAss:
        actions.move_to_element(react_element).click().perform()
    else:
        actions.move_to_element(react_element).click().send_keys(desiredOption).perform(); sleep(1)

    # 2. Esperar as opções aparecerem
    opcao_desejada = desiredOption  # Altere para "Não" se quiser essa opção

    opcao_xpath = f"//div[contains(@class, 'react-select__option') and text()='{opcao_desejada}']"
    
    
    opcao_element = WebDriverWait(navegador, 15).until(
        EC.element_to_be_clickable((By.XPATH, opcao_xpath))
    )

    # rola a barra de lista:
    navegador.execute_script("arguments[0].scrollIntoView();", opcao_element)

    # 3. Clicar na opção desejada
    actions.move_to_element(opcao_element).click().perform(); 
    sleep(0.5)

    return