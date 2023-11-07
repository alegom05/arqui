import socket,time
from threading import Thread

puerto=1234
direccion='localhost'

def receiving(sock):
    global aux
    while True:
        aux=0
        msg=s.recv(1024).decode()
        if msg!='end':
            dataReceived.append(msg)
            aux=1
            time.sleep(0.0001)
        else:
            aux=2
            break

def processing():
    i=0
    NcompCosteElevado=0
    NcompCosteElevado100=0
    NcompCosteBajo=0
    while True:
        if aux==1:
            time.sleep(0.01)
            dataFiltered=dataReceived[i].split(';')
            cantidad=int(dataFiltered[3])
            costoTotal=cantidad*float(dataFiltered[5])
            if costoTotal>=75:
                clasificacionCosto='Costo elevado'
                NcompCosteElevado+=cantidad
                if int(dataFiltered[4])>100:
                    NcompCosteElevado100+=cantidad
            elif costoTotal>=50:
                clasificacionCosto='Costo alto'
            elif costoTotal>=25:
                clasificacionCosto='Costo regular'
            else:
                clasificacionCosto='Costo bajo'
                NcompCosteBajo+=cantidad
            print(f"---------------Nombre: {dataFiltered[1]}---------------\nCosto total: {costoTotal}\nClasificación por costo: {clasificacionCosto}\nNúmero de componentes con costo elevado: {NcompCosteElevado}\nNúmero de componentes con costo elevado y con peso mayor a 100g: {NcompCosteElevado100}\nNúmero de componentes con costo bajo: {NcompCosteBajo}")
            i+=1
        elif aux==2:
            break

if __name__=='__main__':
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while True:
        try:
            s.connect((direccion,puerto))
            break
        except ConnectionRefusedError:
            pass
    try:
        dataReceived=[]
        threadReceiving=Thread(target=receiving,args=(s,))
        threadProcessing=Thread(target=processing,args=())
        threadReceiving.start()
        threadProcessing.start()
        threadReceiving.join()
        threadProcessing.join()
    except KeyboardInterrupt:
        s.close()



