#!/usr/bin/env python
from socket import AF_INET, SOCK_DGRAM
import datetime
import time
import socket
import struct
from threading import Thread

servidores_ntp = [
	"0.uk.pool.ntp.org",    # Londres(Reino Unido)
	"1.es.pool.ntp.org",    # Madrid (España)
	"0.us.pool.ntp.org",    # Nueva York(Estados Unidos)
	"0.hk.pool.ntp.org",    # Hong Kong
	"0.jp.pool.ntp.org"     # Tokyo(Japón)
]

"""
Función: get_ntp_time
Descripción: Imprime la  fecha-hora actual en un país determinado
Entrada: Cualquiera de las URLs definidas en la lista servidores_ntp
Salida: Retorna la fecha-hora(timestamp) en formato datetime.datetime, también la imprime
IMPORTANTE: NO modifique esta funcion 
"""
def get_ntp_time(host):
	timezone_dict = {'uk': ['UK', 0 * 3600], 'es': ['España', 1 * 3600],
	                 'hk': ['Hong Kong', 8 * 3600], 'jp': ['Japón', 9 * 3600],
	                 'us': ['Estados Unidos', -5*3600]}
	key = ''
	port = 123
	buf = 1024
	address = (host, port)
	msg = b'\x1b' + 47 * b'\0'

	# reference time (in seconds since 1900-01-01 00:00:00)
	TIME1970 = 2208988800  # 1970-01-01 00:00:00
	# connect to server
	client = socket.socket(AF_INET, SOCK_DGRAM)
	client.sendto(msg, address)
	msg, address = client.recvfrom(buf)
	t = struct.unpack("!12I", msg)[10]
	t -= TIME1970
	client.close()

	for each_key in timezone_dict:
		if each_key in host:
			key = each_key
			break
	print(f"Hora en {timezone_dict[key][0]}: {datetime.datetime.utcfromtimestamp(t + timezone_dict[key][1])}")
	return datetime.datetime.utcfromtimestamp(t + timezone_dict[key][1])

def sinThreads(servidores):
	masCercano=999999
	for i in range(len(servidores_ntp)):
		hora=int(str(get_ntp_time(servidores_ntp[i])).split(':')[0].split(' ')[1])
		if hora>=8:
			hora-=24
		if 8-hora<=masCercano:
			masCercano=8-hora
			posicion=i
	return int(posicion==0)*'UK'+int(posicion==1)*'España'+int(posicion==2)*'Estados Unidos'+int(posicion==3)*'Hong Kong'+int(posicion==4)*'Japón'

def aux(posicion):
	hora=int(str(get_ntp_time(servidores_ntp[posicion])).split(':')[0].split(' ')[1])
	lista[posicion]=8-(hora+int(hora>=8)*-24)

def conThreads(servidores):
	global lista
	lista=[0,0,0,0,0]
	threadHora=[0,0,0,0,0]
	masCercano=999999
	for j in range(4):
		for i in range(len(servidores)):
			if j==0:
				threadHora[i]=Thread(target=aux,args=(i,))
			if j==1:
				threadHora[i].start()
			if j==2:
				threadHora[i].join()
			if j==3:
				if lista[i]<=masCercano:
					masCercano=lista[i]
					posicion=i
	return int(posicion==0)*'UK'+int(posicion==1)*'España'+int(posicion==2)*'Estados Unidos'+int(posicion==3)*'Hong Kong'+int(posicion==4)*'Japón'

if __name__ == '__main__':
	ticSinThreads=time.perf_counter()
	winner=sinThreads(servidores_ntp)
	tocSinThreads=time.perf_counter()
	print(f"El país cuya bolsa de valores está más próxima a abrir es {winner} y el tiempo empleado en esta prueba sin Threading es de {tocSinThreads-ticSinThreads} segundos.")
	ticConThreads=time.perf_counter()
	winner=conThreads(servidores_ntp)
	tocConThreads=time.perf_counter()
	print(f"El país cuya bolsa de valores está más próxima a abrir es {winner} y el tiempo empleado en esta prueba con Threading es de {tocConThreads-ticConThreads} segundos.")
	if tocConThreads-ticConThreads<tocSinThreads-ticSinThreads:
		print("La implemetanción con Threads fue más rápida.")
	else:
		print("La implemetanción sin Threads fue más rápida.")