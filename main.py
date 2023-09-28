from time import sleep
from Scraper_Inapi import Scraper_Inapi
from utility_functions import get_registros

from TEST_VALUES import REGISTER_TEST 

def main():
    """
    instrucciones del programa principal
    """
    lista_registros = get_registros()

    scraper = Scraper_Inapi()
    scraper.fetch("/Marca/BuscarMarca.aspx")
    for registro in lista_registros:
        scraper.buscador_register(registro) 
        sleep(3)
        scraper.lista_de_aciertos()
    
    scraper.end_scraper()
    

if __name__ == "__main__":
    main()