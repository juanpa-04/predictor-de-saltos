from os import listdir
from pathlib import Path

class Menu:
    def __init__(self, header):
        self.__options = [header]

    def add_option(self, name):
        index = len(self.__options)
        option_name = f"[{index}] {name}"
        self.__options.append(option_name)
    
    def display(self):
        for opt in self.__options:
            print(opt)

    @property
    def opts(self):
        return len(self.__options) - 1

class PredictorTUI:
    def __init__(self):
        pass
    
    def select_predictor(self):
        menu = Menu("Escoger Predictor")
        menu.add_option("PShare")
        menu.add_option("GShare")
        menu.display()

        result = self.__read_input(max = menu.opts)
        if result:
            return result
        else:
            self.__error("Escoger algún item del menu")
            return False
    
    def select_sizes(self):
        menu = Menu("Cambiar tamaños de BTB (default 1024) y PHT (default 1024)")
        menu.add_option("Si")
        menu.add_option("No")
        menu.display()
        
        result = self.__read_input(max = menu.opts)
        if(result == 1):
            btb = self.__read_input(pre_msg="Ingresar BTB")
            pht = self.__read_input(pre_msg="Ingresar PHT")

            btb = 1024 if not btb else btb
            pht = 1024 if not pht else pht

            return (btb, pht)
        elif(result == 2):
            return (1024, 1024)
        else:
            self.__error("Escoger algún item del menu")
            return False
    
    def select_iterations(self):
        i = self.__read_input(pre_msg="Escoger numero de iteraciones (default 1000)")
        i = 1000 if not i else i
        return i

    def __error(self, msg):
        print(f"[Error] {msg}")

    def __read_input(self, max = None, min = 1, pre_msg=""):
        
        if (pre_msg != ""): print(pre_msg)

        user_input = input(f">> ")
        try:
            user_input = int(user_input)
        except:
            return False

        if(max == None and user_input >= 0):
            return user_input
        elif(user_input >= 0 and user_input <= max):
            return user_input
        else:
            return False
    
    def table_menu(self, name):
        menu = Menu(f"Mostrar {name}")
        menu.add_option("Si")
        menu.add_option("No")
        menu.display()

        result = self.__read_input(max = menu.opts)
        if(result == 1):
            filas = self.__read_input(pre_msg="Ingresar número de filas")
            return filas
        elif(result == 2):
            return False
    
    def choose_trace(self):
        menu = Menu(f"Elegir Trace")
        trace_path = Path(__file__).parent.parent / "traces"
        files = listdir(trace_path)
        files.sort()
        for trace in files:
            menu.add_option(trace)
        menu.display()
        result = self.__read_input(max = menu.opts)
        if result:
            return files[result - 1]
        else:
            self.__error("Escoger algún item del menu")
            return False

        
if __name__ == "__main__":
    tui = PredictorTUI()
    predictor = tui.select_predictor()
    sizes = tui.select_sizes()
    iter = tui.select_iterations()
    

