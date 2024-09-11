# Clase para el BTB (Branch Target Buffer)
class BranchTargetBuffer: #almacena direcciones de salto y sus destinos para prever
    #hacia donde saltar en caso que se tome el salto
    def __init__(self, size=1024):# Inicializa el tamaño del BTB (por defecto 1024 entradas)
        self.size = size # Crea un diccionario vacío donde se almacenarán las direcciones y sus destinos
        self.buffer = {} #un diccionario "buffer" donde se almacenarán las direcciones de salto como claves y destinos como valores

    def lookup(self, address):
        # Busca en el buffer la dirección dada y devuelve el destino si existe, de lo contrario devuelve None
        return self.buffer.get(address, None) # usa get, para devolver el destino si la dirección esta en el buffer, sino da "none"
    
    def update(self, address, target):
        # Si el BTB ha alcanzado su tamaño máximo, elimina la entrada más antigua (primer elemento) y la remplaza con una nueva entrada
        if len(self.buffer) >= self.size:
            self.buffer.pop(next(iter(self.buffer)))  # Elimina la entrada más antigua
        self.buffer[address] = target # Agrega la nueva dirección con su destino en el buffer

    def display(self): # Imprime el estado del BTB, mostrando solo las primeras 10 entradas
        print("Estado BTB (primeras 10 entradas):")
        for i, (address, target) in enumerate(self.buffer.items()): #itera sobre el "buffer" obteniendo las direcciones y destinos
            if i >= 10: break  # Limita la salida a las primeras 10 entradas, esto por que estamos probando
            print(f"Address: {hex(address)}, Target: {target}") #imprime la dirección en hexadecimal y destino
# Clase para el PHT (Pattern History Table)
class PatternHistoryTable: #almacena los salto, saltos tomados o no
    def __init__(self, size=1024): # Inicializa el tamaño de la tabla (por defecto 1024 entradas)
        self.size = size # Crea una tabla con 'size' entradas, todas inicializadas en 0
        self.table = [0] * size #inicia la lista con el numero de entradas que diga "size", todas con valor 0, esto es el historial de predicciones
    def get(self, index):# Devuelve el valor en el índice dado, utilizando el tamaño para asegurar que esté en la tabla
        return self.table[index % self.size] #devuelve el valor en la posición que tiene de parametro

    def update(self, index, taken):# Si el salto fue tomado, incrementa el valor en el índice, con un máximo de 3 (saturación), sino, decreta el valor de la tabla
        if taken:
            self.table[index % self.size] = min(self.table[index % self.size] + 1, 3)
        else:
            self.table[index % self.size] = max(self.table[index % self.size] - 1, 0)

    def display(self):
        # Imprime el estado de la tabla, mostrando solo los primeros 10 valores
        print("Estado PHT(primeros 10 valores):")
        for i, value in enumerate(self.table[:10]): #itera en la tabla
            print(f"Index: {i}, Value: {value}") #imprime el indice y valor correspondiente
            
