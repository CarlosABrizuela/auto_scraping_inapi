from Scraper_Inapi import Scraper_Inapi

def main():
    """
    instrucciones del programa principal
    """
    #leer archivo de configuraciones
    scraper = Scraper_Inapi()
    scraper.fetch("/Marca/BuscarMarca.aspx")

    scraper.end_scraper()
    

if __name__ == "__main__":
    main()