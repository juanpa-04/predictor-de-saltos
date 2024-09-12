def read_trace_file(file_path): #Esta función lee un archivo de traza que contiene direcciones de saltos
    #y si el salto fue tomado o no
    trace = []# Lista para almacenar las tuplas
    with open(file_path, 'r') as file:# Abre el archivo en modo lectura.
        for line in file: #se espera a que tenga dirección y un valor 1 o 0
            address, taken = line.split()
            trace.append((int(address,16),int(taken))) #pasar a hexadecimal
    return trace #lista de tuplas donde cada tupla es una dirección 


# Clase para el predictor Simple Saturating Counter
class SimpleSaturatingCounterPredictor:
    def __init__(self, size=1024):
        # Inicializa el tamaño de la tabla de contadores (1024 entradas)
        self.size = size
        # Cada entrada es un contador de 2 bits, inicializado en 1 (predicción inicial: no tomado, por predicción estatica)
        self.table = [1] * size

    def predict(self, address):
        # El índice de la tabla se calcula usando la dirección de la instrucción
        index = address % self.size
        # Si el valor en la tabla es mayor o igual a 2, predice "Tomado" (True), de lo contrario "No Tomado" (False)
        return self.table[index] >= 2

    def update(self, address, taken):
        # El índice de la tabla se calcula usando la dirección de la instrucción
        index = address % self.size
        # Si el salto fue tomado (taken = True), incrementa el contador hasta un máximo de 3
        if taken:
            self.table[index] = min(self.table[index] + 1, 3)
        # Si el salto no fue tomado, decrementa el contador hasta un mínimo de 0
        else:
            self.table[index] = max(self.table[index] - 1, 0)

    def display(self):
        # Muestra el estado de los primeros 10 valores en la tabla
        print("Estado del contador saturado (10 primeros valores):")
        for i, value in enumerate(self.table[:10]):# Itera sobre los primeros 10 valores de la tabla e imprime el índice y el valor.
            print(f"Index: {i}, Value: {value}")


# Función para probar el predictor Simple Saturating Counter con un archivo de trace
def test_saturating_counter_predictor(trace_file):
    # Leer el archivo trace
    trace_data = read_trace_file(trace_file)

    # Inicializar el predictor
    predictor = SimpleSaturatingCounterPredictor()

    # Variables para contar predicciones correctas
    correct_predictions = 0
    total_predictions = 0

    for address, taken in trace_data:  #Probar el predictor en cada dirección y decisión de salto del archivo de traza.
        total_predictions += 1

        # Hacer la predicción
        prediction = predictor.predict(address)

        # Verificar si la predicción fue correcta
        if prediction == taken:
            correct_predictions += 1

        # Actualizar el predictor
        predictor.update(address, taken)

    # Resultados
    print(f"\nContador simple saturado presición: {correct_predictions / total_predictions * 100:.2f}%")

    # Mostrar el estado del predictor (opcional, para inspeccionar los primeros 10 valores)
    predictor.display()


# Ejecutar la prueba (puedes reemplazar `home/gabriel/E/trace_01` con los archivos trace para probar, yo solo probe con uno, por que tal vez más y me explota la pc)
test_saturating_counter_predictor("/home/gabriel/E/trace_01")
