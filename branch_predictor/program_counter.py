from trace import Trace

# Clase de contador de programa que permite aumentar el pc
# Crea el pc apartir de un archivo trace
# El pc salta aleatoriamente
class ProgramCounter:
    def __init__(self,trace_name, initial_pc = 0):
        self.__trace = Trace(trace_name)
        self.__current_pc = self.__trace[initial_pc]
        self.__pc_index = self.__trace.index(self.__current_pc)
        self.__jmp = self.jmp

    def __str__(self):
        return f"{self.__current_pc[0]}"

    def next(self):
        if self.jmp:
            self.__current_pc = next(self.__trace)      # Si hubo jump, buscar otro trace
        else:
            self.__current_pc = self.__trace[self.__pc_index + 1]       # Si no hubo jump, aumenta el pc en 1 ys igue recorriendo el archivo trace
        self.__update_pc_index()
        return self.__current_pc
    
    @property       # Verifica si hubo un jump
    def jmp(self):
        return  True if int(self.__current_pc[1]) else False
    
    @property
    def addr(self):
        return self.__current_pc[0]
    
    def __update_pc_index(self):
        self.__pc_index = self.__trace.index(self.__current_pc)
