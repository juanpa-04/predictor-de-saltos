from program_counter import ProgramCounter                          # Para recibir la lógica del manejo de los trazos y el PC
from BTBPHT import BranchTargetBuffer, PatternHistoryTable           # Para manejar el BTB y la PHT


# Clase encargada del predictor de saltos tipo 'gshare', se eligen 8 bits de historia, como en el ejemplo visto en clase

class GSharePredictor:
    def __init__(self, trace_name, history_bits=8, btb_size=1024, pht_size=1024):
        self.pc = ProgramCounter(trace_name)                           # Inicializa PC desde la clase implementada en program_counter.py
        self.global_history = 0                                    # Inicializa un arreglo para la información global de los saltos
        self.history_bits = history_bits                               # Instancia el tamaño del historial global, se recibe como parámetro pero su valor por defecto es 8
        self.pht = PatternHistoryTable(pht_size)                   # Recibe como atributo el PHT desde BTBPHT.py
        self.btb = BranchTargetBuffer(btb_size)                        # Recibe como atributo el BTB desde BTBPHT.py

    def _get_pht_index(self, pc_addr):                                 # Método para obtener el índice del PHT

        # Asegurarse de que pc_addr es un entero
        if isinstance(pc_addr, str):
            pc_addr = int(pc_addr, 16)  # Convertir de hexadecimal a entero

        #   La manera en la que un predictor de saltos gshare funciona es que compara mediante una XOR la información global que posee
        # vs lo que dicta el PC para tomar la decisión de si hacer el salto o no
        # Lo que retorna este método es el resultado de esa XOR, y lo que se guardará como índice para acceder a la PHT

        return (pc_addr ^ self.global_history) % self.pht.size         # Se usa %self.pht.size para escalar el número resultante de la XOR a uno entre 0 y size-1

    # Método para realizar la predicción del salto
    def predict(self, pc_addr):
        #pc_addr = int(self.pc.addr, 16)                                 # Obtiene la dirección actual del PC en formato entero
        pht_index = self._get_pht_index(pc_addr)                    # Obtiene  el índice para la PHT
        prediction = self.pht.get(pht_index)                            # Obtiene la predicción de la PHT (0-3) 

        # Predicción: Si el valor es 2 o más, predecir 'tomado', sino 'no tomado'
         # Interpretar el valor de la PHT según los 4 estados posibles
        if prediction == 0:
            state = 'strong not taken'
        elif prediction == 1:
            state = 'weak not taken'
        elif prediction == 2:
            state = 'weak taken'
        elif prediction == 3:
            state = 'strong taken'
        return state, pht_index             # pc_addr ya no se retorna ya que se usa como argumento. Retorna el estado e índice de la PHT

    # Método para actualizar los elementos del predictor
    def update(self, correct_outcome, pc_addr, pht_index):
            # Actualiza la PHT con el resultado real del salto
            self.pht.update(pht_index, correct_outcome)

            # Actualiza el historial global (desplaza e inserta el último resultado)
            self.global_history = ((self.global_history << 1) | int(correct_outcome)) & ((1 << self.history_bits) - 1)   
            # Se usa una máscara OR para ignresar el valor del último salto, 1 si fue tomado, 0 si no

            # Si el salto fue tomado, se debe actualizar el BTB
            if correct_outcome:
                target = self.pc.next()[0]  # Obtener la dirección destino/objetivo para el salto 
                self.btb.update(pc_addr, target)

    def run(self):
        correct_predictions = 0             # Contador de predicciones correctas
        total_predictions = 0               # Contador del total de predicciones realizadas

        # Bucle principal para ejecutar las predicciones
        while True:
            
            # Se obtiene la dirección actual del PC
            pc_addr = int(self.pc.addr, 16)  # Convertir la dirección del PC a entero

            # Realiza la predicción usando la función predict (con los 4 estados posibles)
            state, pht_index = self.predict(pc_addr)

            # Determina si la predicción es "taken" o "not taken" en base al estado
            is_taken_pred = state in ['weak taken', 'strong taken']  # true si la predicción fue "tomado"

            # El resultado real del salto, obtenido del PC
            correct_outcome = self.pc.jmp  # Si el salto fue realmente tomado o no (true o false)

            # Compara la predicción con el resultado real
            correct_predictions += (is_taken_pred == correct_outcome)  # Incrementa si la predicción fue correcta
            total_predictions += 1  # Incrementa el total de predicciones realizadas

            # Actualiza la PHT y el BTB en base al resultado real
            self.update(correct_outcome, pc_addr, pht_index)

            # Imprime la precisión cada 100 predicciones
            if total_predictions % 100 == 0:
                accuracy = correct_predictions / total_predictions * 100
                print(f"Accuracy after {total_predictions} predictions: {accuracy:.2f}%")

            # Sal del bucle después de un número fijo de predicciones (valor por defecto: 1k predicciones)
            if total_predictions >= 1000:  # Se puede ajustar este número de acuerdo a las necesidades del usuario
                break


# Ejecutar el predictor si este archivo se corre directamente
if __name__ == "__main__":
    trace_file = "trace_01"  # Nombre del archivo de trazas, se puede cambiar a gusto
    predictor = GSharePredictor(trace_file)  # Instancia de la clase GSharePredictor
    predictor.run()  # Ejecuta el predictor