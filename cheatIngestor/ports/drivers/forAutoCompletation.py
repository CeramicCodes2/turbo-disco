from abc import ABC,abstractmethod
from cheatIngestor.models.template import Technique
class ForAutoComplete:
    @classmethod
    def searchCoincidence(self,keyword:str):
        ...