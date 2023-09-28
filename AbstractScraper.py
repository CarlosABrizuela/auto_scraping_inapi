from abc import ABC, abstractmethod

class AbstractScraper(ABC):
    def __init__(self, base_url):
        self.base_url = base_url
        self.driver = None

    @abstractmethod
    def fetch(self, url, **kwargs):
        """
        Realiza una solicitud HTTP a la URL especificada y devuelve la respuesta.

        Args:
            url (str): La URL a la que se realizará la solicitud.
            **kwargs: Argumentos adicionales para personalizar la solicitud (por ejemplo, encabezados, cookies).

        Returns:
            str: El contenido de la respuesta HTTP.
        """
        pass



    @abstractmethod
    def to_json(self, data):
        """
        Convierte los datos extraídos en formato JSON.

        Args:
            data (dict): Un diccionario que contiene los datos extraídos.

        Returns:
            str: Los datos en formato JSON.
        """
        pass