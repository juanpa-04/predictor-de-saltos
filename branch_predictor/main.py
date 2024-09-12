from program_counter import ProgramCounter
from pshare import Pshare

# pc = ProgramCounter("trace_01") // Carga trace_01 pc es el primer elemento
# print(pc.jmp) // Imprime si es un salto
# pc.addr // Dirección de pc
# print(pc) // Imprime la dirección de pc actual
# pc.next() // Escoge un nuevo pc depediendo de pc.jmp

pc = ProgramCounter("trace_04")
pshare = Pshare()

correct_predictions = 0
iterations = 10000

for i in range(0, iterations):
    outcome = pc.jmp
    prediction = pshare.predict(pc.addr)

    if prediction == outcome:
        correct_predictions += 1

    #print(f"[{i}]: {pc} {outcome} | {prediction}")
    pshare.update(pc.addr, outcome)
    pc.next()

accuracy = (correct_predictions / iterations) * 100
print(f"{accuracy}%")

