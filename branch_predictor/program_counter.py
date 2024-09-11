from trace import Trace

# Clase de contador de programa que permite aumentar el pc
# Crea el pc apartir de un archivo trace
# El pc salta aleatoriamente
class ProgramCounter:
    def __init__(self,trace_name):
        self.__trace = Trace(trace_name)
        self.__current_pc = self.__trace[0]
    
    @property
    def address(self):
        return self.__current_pc[0]
    
    @property
    def history(self):
        return self.__current_pc[1]
    
    def next(self):
        self.__current_pc = next(self.__trace)
        return self.__current_pc
