from selenium import webdriver
from AbstractScraper import AbstractScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
from selenium.webdriver.common.proxy import Proxy, ProxyType
import json

class Scraper_Inapi(AbstractScraper):
    def __init__(self, config):
        """
        cargar las configuraciones, declaracion de las propiedades
        """
        self.config = config
        super().__init__(self.config["base_url"])
        self.data = []
        self.actual_register = None
    
    def initialize_driver(self):
        chrome_options = webdriver.ChromeOptions()

        proxy_ip_port = self.config['proxy_ip_port']
        if proxy_ip_port:
            proxy = Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = proxy_ip_port
            proxy.ssl_proxy = proxy_ip_port
            chrome_options.add_argument(f"--proxy-server={proxy_ip_port}")

        self.driver = webdriver.Chrome(options=chrome_options)

    def fetch(self, url):
        if not self.driver:
            self.initialize_driver()
        
        self.driver.get(self.get_full_url(url))
    
    def get_full_url(self, url):
        # self.driver = webdriver.Chrome()
        # self.driver.maximize_window() #
        full_url = self.base_url+url
        return full_url

    def buscador_register(self, register_number):
        """
        Ingresa un nuevo numero de registro para la busqueda
        """
        try:
            input_register = self.driver.find_element(by=By.ID, value="txtRegistro")
            submit_button = self.driver.find_element(by=By.ID, value="btnBuscarMarca")
        except NoSuchElementException as e:
            print(f"Elemento no encontrado. ({e.msg})")
            return
        
        self.actual_register = register_number
        input_register.clear()
        input_register.send_keys(self.actual_register)
        sleep(1)
        
        self.wait_to_load(5)
        submit_button.click()
        try:
            return self.existe_registro()
        except Exception as e:
            print(f"Ocurrió un erro con el popup: {e}")
            return False
                
    
    def lista_de_aciertos(self):
        """
        Selecciona los registros de la tabla, si existiesen
        """
        try:
            tablaresult = self.driver.find_element(by=By.ID, value="tblMarcasResult")
            tbodyresult = tablaresult.find_element(by=By.TAG_NAME, value='tbody')
            trresult = tbodyresult.find_elements(by=By.TAG_NAME, value='tr')
        except NoSuchElementException as e:
            print(f"Elemento no encontrado. ({e.msg})")
            return
        
        for fila in trresult:
            # print(fila.get_attribute('outerHTML'))
            fila.click()
            self.detalle_salida()

        self.prepara_buscador()
    
    def detalle_salida(self):
        """
        obtener los datos del detalle y generar la salida
        """
        sleep(2)
        try:
            datosadministrativos = self.driver.find_element(by=By.ID, value="tblInstancias")
            tbody_administrativos = datosadministrativos.find_element(by=By.TAG_NAME, value='tbody')
            tr_instancia = tbody_administrativos.find_elements(by=By.TAG_NAME, value='tr')
        except NoSuchElementException as e:
            print(f"Elemento no encontrado. ({e.msg})")
            return
        lista_instancias = []
        for fila in tr_instancia:
            instancia = {}
            observada_de_fondo = None
            fecha_observada_de_fondo = None
            apelaciones = None
            ipt = None
            col = 0
            celdasinstancias = fila.find_elements(by=By.TAG_NAME, value='td')
            for celda in celdasinstancias:
                try:
                    valor_celda = celda.get_attribute('innerHTML')
                except NoSuchElementException as e:
                    print(f"Elemento no encontrado. ({e.msg})")
                    return
                
                if col ==0:
                    fechainstancia = valor_celda
                if col ==1:
                    # Observada de fondo y fecha de observada de fondo
                    subtexto = "Resolución de observaciones de fondo de marca"
                    existesubtReso = True if valor_celda.count(subtexto)>0 else False
                    observada_de_fondo = existesubtReso
                    fecha_observada_de_fondo = fechainstancia if existesubtReso else None

                    # Apelaciones
                    subtapelaciones = "Recurso de apelacion"
                    existesubtapela = True if valor_celda.count(subtapelaciones)>0 else False
                    apelaciones = existesubtapela

                    # IPT e IPTV
                    subtIPT = "IPT"
                    existesubtIPT = True if valor_celda.count(subtIPT)>0 else False
                    ipt = existesubtIPT

                col +=1
            instancia["Observada_de_fondo"]= observada_de_fondo
            instancia["Fecha_observada_de_fondo"]= fecha_observada_de_fondo
            instancia["Apelaciones"]= apelaciones
            instancia["IPT"]= ipt
            lista_instancias.append(instancia)

        registro = {}
        registro["registro"] = self.actual_register
        registro["instancias"]=lista_instancias
        self.data.append(registro)

    def prepara_buscador(self):
        """
        prepara para buscar en el primer formulario
        """
        try:
            form_buscador = self.driver.find_element(by=By.XPATH, value="//*[@id='ui-id-3']/a")
        except NoSuchElementException as e:
            print(f"Elemento no encontrado. ({e.msg})")
            return
        form_buscador.click()
    
    def to_json(self):
        """
        Guardar los datos en un json file
        """
        with open(self.config["output"], 'w', encoding='utf-8') as json_file:
            json.dump(self.data, json_file, indent=4, ensure_ascii=False)

    def wait_to_load(self, time):
        """
        espera a que el elemento que bloquea la pantalla mientras carga desaparezca
        """
        try:
            WebDriverWait(self.driver, time).until(EC.invisibility_of_element_located((By.ID, "loadingBackground")))

        except TimeoutException as e:
            print(f"No se puede cargar el contenido: {e.msg}") 
            self.wait_to_load(time)
    
    def existe_registro(self):
        """
        checkea si se ha encontrado resultado para el numero de registro.
        """
        sleep(3)
        popup = self.driver.find_element(By.XPATH, value = "/html/body/div[7]")

        if not popup.is_displayed():
            return True
        else:
            print(f"{self.actual_register} No tuvo resultados")
            wait = WebDriverWait(self.driver, 10)
            popup = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]")))
            popup.find_element(By.XPATH, "//button[contains(text(), 'Ok')]").click()
            # elemento_boton = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[3]/div/button")))
            # elemento_boton.click()
            sleep(1)
            return False



"""
Formato de salida:

    [{
        'registro': NRO_REGISTRO, 
        'instancias': [
            {
                'Observada_de_fondo': True/False, 
                'Fecha_observada_de_fondo': Fecha, 
                'Apelaciones': True/False, 
                'IPT': True/False
            }, 
            ...
            ]
    }]
"""