from selenium import webdriver
from AbstractScraper import AbstractScraper

class Scraper_Inapi(AbstractScraper):
    def __init__(self):
        """
        cargar las configuraciones
        """
        super().__init__("https://ion.inapi.cl")
        self.data = []
        # self.actual_register = None

    def fetch(self, url):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window() #
        full_url = self.base_url+url
        self.driver.get(full_url)

    def to_json(self):
        """
        Guardar los datos en un json file
        """
        pass
