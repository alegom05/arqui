from multiprocessing import Process
import time

CUENTA = 50_000_000

def cuenta(n):
    while n > 0:
        n -= 1


if __name__ == "__main__":
    inicio = time.perf_counter()
    p1 = Process(target=cuenta, args=(CUENTA // 2,))
    p2 = Process(target=cuenta, args=(CUENTA // 2,))
    p1.start()
    p2.start()

    p1.join()
    p2.join()
    fin = time.perf_counter()

    print(f"Tiempo de ejecucion multiproceso: {fin - inicio} segundos")