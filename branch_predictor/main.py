from program_counter import ProgramCounter
from pshare import Pshare
from gshare import GSharePredictor
from tui import PredictorTUI

trace = "trace_01"

def main_loop():


    tui = PredictorTUI()
    trace = check_until_valid(tui.choose_trace)

    predictor = check_until_valid(tui.select_predictor)
    sizes = check_until_valid(tui.select_sizes)
    iter = check_until_valid(tui.select_iterations)

    print(f"Simulando con {trace}")
    pc = ProgramCounter(trace)

    predictor = run_predictor(predictor, sizes, iter, pc)

    if(isinstance(predictor, Pshare)):
        bht_table = tui.table_menu("BHT")
        if bht_table:
            display_bht(predictor.bht, bht_table)
    else:
        btb_table = tui.table_menu("BTB")
        if btb_table:
            display_btb(predictor.btb, btb_table)
        
    pht_table = tui.table_menu("PHT")
    if pht_table:
        display_pht(predictor.pht, pht_table)

def check_until_valid(func):
    item = False
    while(not item):
        item = func()
    return item

def run_predictor(predictor, sizes, iter, pc):
   
    match predictor:
        case 1: predictor = run_pshare(sizes, iter, pc)
        case 2: predictor = run_gshare(sizes, iter)
        case _: return False
    return predictor

def run_pshare(sizes, iter, pc):
    
    btb, pht = sizes
    pshare = Pshare(bht_size=pht, pht_size=pht)
    
    correct_predictions = 0
    for i in range(0, iter):
        outcome = pc.jmp
        prediction = pshare.predict(pc.addr)
        if prediction == outcome:
             correct_predictions += 1
        pshare.update(pc.addr, outcome)
        pc.next()
    
    results(correct_predictions, iter, pc)
    return pshare

def results(correct, iterations, pc):
    accuracy = (correct / iterations) * 100
    errors = iterations - correct
    jumps = pc.jumps

    print("\n[Resultados]")
    print(f"Saltos: {jumps}")
    print(f"Tasa: {accuracy} %")
    print(f"Errores: {errors}\n")

def run_gshare(sizes, iter):
    bht, pht = sizes
    gshare = GSharePredictor(trace_name=trace, btb_size=bht, pht_size=pht, iter=iter)
    correct_predictions, pc = gshare.run()
    results(correct_predictions, iter, pc)
    return gshare

def display_bht(table, end):
    print("Branch History Table")

    table = table[:end]
    print("Address | State")
    for idx, row in enumerate(table):
        match row:
            case 0: row = "ST"
            case 1: row = "SN"
            case 2: row = "WT"
            case 3: row = "WN"
            case _: break
        print(f"0x{idx:06x} | {row}")

def display_pht(table,end):
    print("Pattern History Table")
    table = table[:end]
    print("Address | BHR")
    for idx, row in enumerate(table):
        print(f"0x{idx:06x} | 0b{row:010b}")

def display_btb(table,end):
    print("Branch Target Buffer")
    print("Address | Target")
    for i, (address, target) in enumerate(table.buffer.items()): 
        if i >= end: break
        print(f" {hex(address)} | {target}")

if __name__ == "__main__":
    main_loop()
    

