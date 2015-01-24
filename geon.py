#!/usr/bin/env python
# -*- coding: utf-8 -*-
#GEOLOCALIZADOR  v1.1 
#codificada por arthas1000 para SL4A 
#shiftshell@gmail.com
#correciones jeanlocos@gmail.com
#basado en el script de cmartorella@edge-security.com geoedge v0.2
#disponible  aqui : http://www.edge-security.com/soft/geoedge.py 
#AGREGADO SOPORTE DE VOZ 
#AGREGADO SOPORTE PARA PLATAFORMA ANDROID
#AGREGADO LOG DE BUSQUEDAS
#AGREGADO FECHADO Y LOCALIZACION GPS ACTUAL
import sys
import re
import httplib
import android
import string
#~ import time
from datetime import datetime 
#vaciamos el archivo 
consultas= open('direccion.txt','wt+')
consultas.close()
#nuestra hermosa ayuda 
def manifesto():
	arriba = 'Instrucciones'
	ayudita = 'escribe la IP o el HOST '
	droid.dialogCreateAlert(arriba , ayudita)
	droid.dialogSetPositiveButtonText('(_p..q_)'+'\n'+'||||')
	#  
	# (_p..q_)
	#   ||||
	
	droid.dialogShow()
	response = droid.dialogGetResponse().result

#solicitamos la pagina web 
def solicitud ():
	paginaweb = droid.dialogGetInput('DATOS', 'Escriba la direccion web:', None).result
	contenido =paginaweb
	direccion = open('direccion.txt','wt+')
	direccion.write(contenido)
	direccion.close()
	droid.ttsSpeak('almacenando')
	#vibra al terminar 
	result = droid.vibrate()
 
def buscando():
#creamos titulos apantalladores
	title1 = 'Procesando '
	message1 = 'geolocalizando'
	droid.ttsSpeak(title1)
#un spinner para dar emocion 
	droid.dialogCreateSpinnerProgress(title1,message1)
	droid.dialogShow()
	time.sleep(1)
	droid.dialogDismiss()
	
def informacion():
	paginaweb =open('direccion.txt','rt+')
	host = paginaweb.read()
	
	try:
		
		h = httplib.HTTP("www.geoiptool.com")
		h.putrequest('GET',"/es/?IP="+ host )
		h.putheader('Host', 'www.geoiptool.com')
		h.putheader('User-agent', 'Internet Explorer 8.0 ')
		h.endheaders()
		returncode, returnmsg, headers = h.getreply()
		response=h.file.read()
		
		res=re.compile("<td align=\"left\" class=\"arial_bold\">.*</td>")
		results=res.findall(response)
		res=[]
		for x in results:
			x=x.replace("<td align=\"left\" class=\"arial_bold\">","")
			x=x.replace("</td>","")
			res.append(x)
		a = "IP/Host: "+res[0]
		country=re.sub("<.*nk\">","",res[1])
		country=country.replace("</a>","")
		country=re.sub("<.*middle\" >","",country)
		b = "Pais: " + country + ","+ res[2]
		city=re.sub("<.*nk\">","",res[3])
		city=city.replace("</a>","")
		c = "Ciudad: " + city + ","+ res[4]
		d = "Coordenadas: " + res[8] + ","+res[7]
		
		wiki = open('log.txt','a+')
		wiki.write(host)
		wiki.write(a)
		wiki.write(b)
		wiki.write(c)
		wiki.write(d)
		wiki.write('\n')	
		wiki.close()
		arriba4 = 'tus datos son'
		droid.ttsSpeak(arriba4)
		mensaje ='\n' + a + '\n' + b + '\n' + c + '\n' + d 
		droid.dialogCreateAlert(arriba4, mensaje)
		droid.dialogSetPositiveButtonText('yeeah')
		droid.dialogShow()
		response = droid.dialogGetResponse().result	

	except:
		arriba3 = 'ERROR'
		ayudita3 = 'Revisa tus conexiones '
		droid.ttsSpeak(ayudita3)
		droid.dialogCreateAlert(arriba3 , ayudita3)
		droid.dialogSetPositiveButtonText('KO')
		droid.dialogShow()
		response = droid.dialogGetResponse().result		

def datosgenerales():
#almacen datos de usuario 
	fechado = open('log.txt','a+')
	fecha = datetime.now()
	ip_val = droid.wifiGetConnectionInfo().result[ 'ip_address' ]
	it = iter (format(ip_val, '08x' ))
	octets = [ int(a+b,16) for a,b in zip (it,it)]
	octets.reverse()
	ip = '.' .join( str(o) for o in octets)
	fechado.write('tu ip : '+str(ip)+'\n')
	fechado.write(str(fecha))
	fechado.write('\n \n')	
	fechado.close()
	droid.notify('Datos obtenidos','tu ip :'+ ip + 'fecha :'+str(fecha))
	
if __name__ == '__main__':
	droid = android.Android()
	manifesto()
	solicitud()
	buscando()
	informacion()
	datosgenerales()
	

