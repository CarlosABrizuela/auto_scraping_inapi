from selenium import webdriver
from AbstractScraper import AbstractScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from sys import exception

class Scraper_Inapi(AbstractScraper):
    def __init__(self):
        """
        cargar las configuraciones
        """
        super().__init__("https://ion.inapi.cl")
        self.data = []
        self.actual_register = None

    def fetch(self, url):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window() #
        full_url = self.base_url+url
        self.driver.get(full_url)

    def buscador_register(self, register_number):
        """
        Ingresa un nuevo numero de registro para la busqueda
        """
        self.actual_register = register_number
        input_register = self.driver.find_element(by=By.ID, value="txtRegistro")
        input_register.clear()
        # print(self.actual_register)
        input_register.send_keys(self.actual_register)
        sleep(1)
        
        self.wait_to_load(20)
        submit_button = self.driver.find_element(by=By.ID, value="btnBuscarMarca")
        submit_button.click()

    def to_json(self):
        """
        Guardar los datos en un json file
        """
        pass

    def wait_to_load(self, time):
        """
        espera a que el elemento que bloquea la pantalla mientras carga desaparezca
        """
        try:
            WebDriverWait(self.driver, time).until(EC.invisibility_of_element_located((By.ID, "loadingBackground")))

        except exception:
            print(exception) 
