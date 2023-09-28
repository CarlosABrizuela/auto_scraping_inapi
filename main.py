from time import sleep
from Scraper_Inapi import Scraper_Inapi

from TEST_VALUES import REGISTER_TEST 

def main():
    """
    instrucciones del programa principal
    """
    #leer archivo de configuraciones
    scraper = Scraper_Inapi()
    scraper.fetch("/Marca/BuscarMarca.aspx")

    scraper.buscador_register(REGISTER_TEST)
    sleep(3)
    scraper.lista_de_aciertos()
    
    scraper.end_scraper()
    

if __name__ == "__main__":
    main()