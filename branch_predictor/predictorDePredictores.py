from gshare import GSharePredictor
from pshare import Pshare


class MetaPredictor:
    def __init__(self, trace_name, history_bits=10, meta_size=1024, iter = 1000):
        # Inicializar los predictores GShare y PShare
        self.gshare = GSharePredictor(trace_name, history_bits)  
        self.pshare = Pshare(history_bits)  

        # Inicializar el meta-predictor (inicia en estado débil pshare)
        self.meta_predictor = [1] * meta_size  
        self.meta_size = meta_size              
        self.global_history = 0  # Historial global para seleccionar el predictor

        self.iter = iter

    def _get_meta_index(self, pc_addr):
        if isinstance(pc_addr, str):    # Se pregunta si pc_addr es un string
            pc_addr = int(pc_addr, 16)  # Convertir de hexadecimal a entero

        # Se usa el XOR entre la dirección del PC (ya un entero) y el historial global para indexar el MetaPredictor
        return (pc_addr ^ self.global_history) % self.meta_size

    def predict(self, pc_addr):

        # Asegurarse de que pc_addr es un entero
        if isinstance(pc_addr, str):
            pc_addr = int(pc_addr, 16)  # Convertir de hexadecimal a entero

        # Obtener el estado del meta-predictor
        meta_index = self._get_meta_index(pc_addr)
        state = self.meta_predictor[meta_index]

        # Elegir el predictor basado en el estado
        if state <= 1:
            prediction = self.pshare.predict(pc_addr)
            used_predictor = "pshare"
        else:
            prediction = self.gshare.predict(pc_addr)
            used_predictor = "gshare"
        
        print(f"Meta index: {meta_index}, State: {state}, Using: {used_predictor}")  # Debugging
        return prediction, used_predictor, state

    def update(self, pc_addr, actual_outcome, used_predictor, state):

        # Asegurarse de que pc_addr es un entero
        if isinstance(pc_addr, str):
            pc_addr = int(pc_addr, 16)  # Convertir de hexadecimal a entero
            
        # Actualizar el predictor que se usó
        if used_predictor == "gshare":
            self.gshare.update(pc_addr, actual_outcome)
        else:
            self.pshare.update(pc_addr, actual_outcome)

        # Actualizar el meta-predictor basado en el desempeño
        meta_index = self._get_meta_index(pc_addr)
        gshare_pred = self.gshare.predict(pc_addr)
        pshare_pred = self.pshare.predict(pc_addr)

        print(f"gshare_pred: {gshare_pred}, pshare_pred: {pshare_pred}, actual_outcome: {actual_outcome}")  # Debugging

        # Ajustar el estado del meta-predictor basado en el resultado
        if used_predictor == "gshare" and gshare_pred == actual_outcome:
            if state < 3:
                self.meta_predictor[meta_index] += 1
        elif used_predictor == "pshare" and pshare_pred == actual_outcome:
            if state > 0:
                self.meta_predictor[meta_index] -= 1

        # Imprimir el nuevo estado del meta-predictor
        # print(f"Updated Meta index: {meta_index}, New state: {self.meta_predictor[meta_index]}")  # Debugging

        # Actualizar el historial global
        self.global_history = ((self.global_history << 1) | actual_outcome) & ((1 << 10) - 1)

    def run(self):
        correct_predictions = 0
        total_predictions = 0
        while True:
            # Obtener la dirección del PC actual
            pc_addr = self.gshare.pc.addr
            outcome = self.gshare.pc.jmp  # Resultado real del salto

            # Predecir el salto usando el meta-predictor
            prediction, used_predictor, state = self.predict(pc_addr)

            # Verificar si la predicción fue correcta
            is_correct = (prediction == outcome)
            correct_predictions += is_correct
            total_predictions += 1

            # Actualizar el meta-predictor y los predictores
            self.update(pc_addr, outcome, used_predictor, state)

            # Imprimir precisión cada 100 predicciones
            # if total_predictions % 100 == 0:
                # accuracy = correct_predictions / total_predictions * 100
                # print(f"Accuracy after {total_predictions} predictions: {accuracy:.2f}%")

            if total_predictions >= self.iter:
                return (correct_predictions, self.gshare.pc)

# Ejecutar el meta-predictor
if __name__ == "__main__":
    trace_file = "trace_01"  # Archivo de trazas
    predictor = MetaPredictor(trace_file)  # Instancia del MetaPredictor
    predictor.run()  # Ejecuta el predictor
