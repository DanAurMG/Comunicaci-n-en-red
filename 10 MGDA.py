import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s')


def consumer(cond, buffer):
    logging.debug('Iniciando hilo consumidor')
    with cond:
        while len(buffer) == 0:
            logging.debug('No hay productos disponibles para el consumidor. Esperando...')
            cond.wait()

        # Consumir un producto
        product = buffer.pop(0)
        logging.debug('Consumido el producto %s. Productos restantes en el buffer: %d', product, len(buffer))
        
        if(input("Teclee S si desea seguir consumiendo productos\n") == "S"):
            product = buffer.pop(0)
            logging.debug('Consumido el producto %s. Productos restantes en el buffer: %d', product, len(buffer))
            


def producer(cond, buffer):
    logging.debug('Iniciando el hilo productor')
    with cond:
        while not stop_condition:
            while len(buffer) >= 10:
                logging.debug('Buffer completo. Esperando a que el consumidor consuma productos...')
                cond.wait()

            # Producir un producto
            product = time.time()  # Aquí puedes reemplazar esto con la lógica de producción real
            buffer.append(product)
            logging.debug('Producido el producto %s. Productos en el buffer: %d', product, len(buffer))

            # Notificar al consumidor
            cond.notify()


condition = threading.Condition()
buffer = []
stop_condition = False

c1 = threading.Thread(name='c1', target=consumer, args=(condition, buffer))
c2 = threading.Thread(name='c2', target=consumer, args=(condition, buffer))
p = threading.Thread(name='p', target=producer, args=(condition, buffer))

c1.start()
time.sleep(2)
c2.start()
time.sleep(2)
p.start()