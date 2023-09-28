ruta_base = 'C:/Users/LNKIZ/Desktop/Test python/proyecto/auto_scraping_inapi'
ruta_rel = '/files/register_number_list.txt'
ruta_full = ruta_base + ruta_rel
# print(ruta_full)

def get_registros():
    """
    Abre el archivo de registros y devuelve la lista
    """
    with open(ruta_full) as f_registros:
        lista_registros = f_registros.read().split("\n")
        return lista_registros
