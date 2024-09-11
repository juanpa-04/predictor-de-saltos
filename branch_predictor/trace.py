from pathlib import Path
from random import choice

# Cargar archivo tipo trace (del folder traces/)
# Se carga en un lista con cada item de forma (dirección, historia)
# Trace es un iterable y __next__ elige aleatoriamente la siguiente dirección
class Trace:
    def __init__(self, trace_name):
        self.__trace_name = trace_name
        self.__traces = []
        self.__trace_len = 0
        self.__load()
    
    def __iter__(self):
        return iter(self.__traces)

    def __getitem__(self,index):
        return self.__traces[index]

    def __next__(self):
        return choice(self.__traces)

    def __load(self):
        path = Path(__file__).parent.parent / "traces" / self.__trace_name
        with open(path, "r") as file:
            for line in file:
                address, history = line.strip().split()
                self.__traces.append((address, history))
        self.__trace_len = len(self.__traces)

    