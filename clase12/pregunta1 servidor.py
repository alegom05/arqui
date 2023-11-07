import socket,time
from threading import Thread

puerto=1234
direccion='localhost'

def sending(client):
    dataFiltered=data.split("\n")
    for i in range(1,len(dataFiltered)):
        client.send(dataFiltered[i].encode())
        time.sleep(1)

def reading():
    global data
    data=open('PartesDeElectrónica.csv',"r",encoding="latin").read()

if __name__=='__main__':
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((direccion,puerto))
    s.listen()
    try:
        while True:
            c,cAddr=s.accept()
            data=0
            threadLeer=Thread(target=reading,args=())
            threadEnviar=Thread(target=sending,args=(c,))
            threadLeer.start()
            while data==0:
                pass
            threadEnviar.start()
            threadLeer.join()
            threadEnviar.join()
            c.send(b'end')
    except KeyboardInterrupt:
        s.close()

        
    
