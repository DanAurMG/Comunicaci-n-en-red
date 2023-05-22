import threading 
 
class CuentaBancaria: 
    def __init__(self): 
        self.balance = 0 
        #self.lock = threading.Lock() 
 
    def depositar(self, cantidad): 
        print('Saldo actual: ', int(self.balance))
        print('Se va a realizar un deposito de: ', cantidad)
        self.balance += cantidad 
 
    def retirar(self, cantidad): 
        print('Saldo actual: ', int(self.balance))
        print('Se va a realizar un retiro de: ', cantidad)
        
        if cantidad <= self.balance: 
            self.balance -= cantidad 
        else: 
            print("No hay suficiente saldo.") 
 
def realizar_transacciones(cuenta, lock): 
    for _ in range(100): 
        with lock:
            cuenta.depositar(10) 
            cuenta.retirar(5) 
 
def main(): 
    lock = threading.Lock()
    cuenta = CuentaBancaria() 
    hilos = [] 
 
    for _ in range(5): 
        hilo = threading.Thread(target=realizar_transacciones, args=(cuenta,lock,)) 
        hilos.append(hilo) 
        hilo.start() 
 
    for hilo in hilos: 
        hilo.join() 
 
    print(f"Saldo final: {cuenta.balance}") 
 
main()
