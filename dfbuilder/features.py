from abc import ABC, abstractmethod
import numpy as np
import pandas as pd

class Feature(ABC):
    def __init__(self, name:str, alias:str=None, *args, **kwargs):
        self.name = name
        self.alias = alias

    
    @abstractmethod
    def compute(self, data):
        pass

class Field(Feature):
    def compute(self, data):
        return data[[self.name]]


