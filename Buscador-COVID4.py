# coding=utf-8

""" Autor: Víctor García Carrera victorgarciacarrera@gmail.com
	Descarga el contenido del buscador de google con un término
	de búsqueda concreto y guarda el NUMERO DE RESULTADOS
"""

import sys
from math import *
from random import *

""" Ejemplo obtenido de: https://www.edureka.co/blog/web-scraping-with-python/ """

from selenium import webdriver
#from selenium.webdriver.common.keys import keys		#The Keys class provide keys in the keyboard like RETURN, F1, ALT etc.

from bs4 import BeautifulSoup		#Libreria bs4 version ultima BeautifulSoup4
import pandas as pd

import string
import time
from datetime import datetime
import numpy as np

from concurrent.futures import ProcessPoolExecutor

POOLSIZE = 10


#@#@#@@ VER OTROS __MOTORES__ de BUSQUEDA (no navegadores, que solo es para visualizacion y navegar)
### HACER LOS DRIVERS COMO UNA CLASE (con sus atributos y metodos) para utilizarla en ambos lados!!!

""" ### FALTA HACER LISTA DE DRIVERS (meter @|FIREFOX|@) +
	###		+ CALCULO DE RESULTADOS (estadisticas, valorar con desviacion respecto a la media...)
	### 	+ INSPECCIONAR/MEDIR + DATOS como tiempo de respuesta, enlaces (expresiones regulares)
	
"""

#@#@#@#@#@ PONER MEJOR EL START TIME (despues de inicializar listas) y 2 para los 2 drivers #@#@#@#@#@

def main():

	# Declaramos la var global POOLSIZE que indica el tamanio del pool de procesos
	global POOLSIZE

	# Lista donde guardamos los drivers que utilizamos para las busquedas
	driver_list = []

	# Driver1 CHROME
	chrome_options = webdriver.ChromeOptions();
	chrome_options.add_argument('--headless');		# EJECUCION EN BACKGROUND, invisible

	""" LINEAS PARA DESHABILITAR EL CONTROL DE GOOGLE: "Chrome is being controlled by automated test software" """
	#@#@#@@ chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'disable-infobars']);
	
	driver1 = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options,
								service_args=['--verbose', '--log-path=/tmp/chromedriver.log']);
	
	# Driver2 FIREFOX
	firefox_options = webdriver.FirefoxOptions()
	firefox_options.add_argument('--headless')
	"""
	firefoxOptions.setAcceptInsecureCerts(true);
    firefoxOptions.setLogLevel(FirefoxDriverLogLevel.TRACE);
	"""
	driver2 = webdriver.Firefox(executable_path="/usr/bin/geckodriver", options=firefox_options)

	# Aniadimos los drivers para realizar las busquedas
	driver_list.append(driver1)
	driver_list.append(driver2)

	print("\n***\tINICIALIZADOS DRIVER\t***\n")
	
	""" Variables de busquedas y resultados """	
	busquedas_groups = []		#  Lista con las busquedas agrupadas
	resultados_groups = []		#  Lista con los resultados agrupados

	# Listas por cada BUSCADOR de los resultados obtenidos
	resultados1 = []		# Resultados de Google
	resultados2 = []		# Resultados de Yahoo

	resultados1_orden = []		# Lista con los resultados ordenados de GOOGLE
	resultados2_orden = []		# Lista con los resultados ordenados de GOOGLE

	#resultados_list = []		#  Lista con el numero de resultados por driver de los terminos de busqueda
	#resultados = []				

	#@#@#@@#@@#@#@ 		IMP!!! LEER DE FICHERO LAS BUSQUEDAS		#@#@#@@#@@#@#@
	""" Lista(array numpy) con las búsquedas a realizar en Google """
	busquedas = np.array( ["*.es", "coronavirus *.es", "crisis * coronavirus *.es", "calma * coronavirus *.es", "esperanza * coronavirus *.es" ,  
					"pánico * coronavirus *.es", "miedo * coronavirus *.es", "ansiedad * coronavirus *.es", "terror * coronavirus *.es",       
					"inseguridad * coronavirus*.es", "enfado * coronavirus *.es", "rabia * coronavirus *.es", "ira * coronavirus *.es" , 
					"alegría * coronavirus *.es", "tristeza * coronavirus *.es" , "sorpresa * coronavirus *.es", "alivio * coronavirus *.es",
					"desconfianza * coronavirus *.es", "incertidumbre * coronavirus *.es", "sanidad * coronavirus *.es", "aislamiento * coronavirus *.es", 
					"cuarentena * coronavirus *.es", "solidaridad * coronavirus *.es", "cooperación * coronavirus *.es", "protección * coronavirus *.es",
					"irresponsable * coronavirus *.es", "polític* * coronavirus *.es", "polític* * irresponsable* * coronavirus *.es", "medic* * coronavirus *.es",
					"cura * coronavirus *.es", "abastecimiento * coronavirus *.es", "alimentos crisis * coronavirus *.es", "alimentos * coronavirus *.es",   
					"aislamiento * coronavirus *.es", "memes * coronavirus *.es", "bromas * coronavirus *.es", "chistes * coronavirus *.es", 
					"alarma * coronavirus *.es", "gratitud * coronavirus *.es", "aplausos * coronavirus *.es", "agradecimiento * coronavirus *.es",
					"vacuna * coronavirus *.es", "mortalidad * coronavirus *.es", "muerte * coronavirus *.es"] )
	

	# REORGANIZAMOS LA LISTA DE BÚSQUEDA PARA AGRUPAR LOS TÉRMINOS EN FUNCION DE POOLSIZE!!!
	init_len = len(busquedas)
	print("NUMERO BUSQUEDAS: " + str(init_len))
	groups = ceil(init_len/POOLSIZE)		# Agrupamos los términos para minimizar los lanzamientos del pool que son costosos
	print(str(groups))
	# EJEMPLO: len(busquedas)=44, POOLSIZE=10, groups=5, para mantener que haya 10 grupos de busquedas
	"""busquedas_groups = np.array_split(busquedas, groups)
	print busquedas_groups"""

	
	# Recorremos la lista de búsquedas agrupando por terminos
	for pos in range(0,init_len):
		if pos%groups==0:
			terms = []
		terms.append(busquedas[pos])
		if pos%groups==(groups-1) or pos==(init_len-1):	# Hemos llenado un grupo de terminos
			busquedas_groups.append(terms)

	# Obtemos el array de búsquedas con subarrays agrupados para mejorar la búsqueda
	print("\n\n")
	print(busquedas_groups)
	print(len(busquedas_groups))
	print("\n\nBREAK\n\n")
	
	"""SECUENCIAL!!"""
	""" Seleccionamos uno a uno los términos a buscar para obtener su número de resultados """
	"""for termino in busquedas:
		res = buscar(termino)

		resultados.append(str(res))
		"""

	"""PARALELO!!!!"""
	executor = ProcessPoolExecutor(POOLSIZE)

	print("\n***\tCOMENZAMOS BUSQUEDA\t***\n")

	try:
		resultados_groups = list(executor.map(buscar, busquedas_groups))

	except concurrent.futures.process.BrokenProcessPool as e:		# Si falla alguna búsqueda
		print('could not start new tasks: {}'.format(e))

	for driver in driver_list:
		# Cierra todas las ventanas de búsqueda y finaliza correctamente la sesión WebDriver
		driver.quit()


	print("\n***\tFIN BUSQUEDA, ORDENAR RESULTADOS\t***\n")


	# Recorremos la lista de resultados agrupando por drivers
	for pos in range(0,len(resultados_groups)):
		resultados1.append(resultados_groups[pos][0])	# Pertenece al primer driver
		resultados2.append(resultados_groups[pos][1])	# Pertenece al segundo driver


	print(resultados1)
	print("\n\nBREAK2\n\n")
	print(resultados2)
	print("\n\n")

	# Quitamos los grupos de resultados Y CALCULAMOS LA SUMA TOTAL DE TIEMPOS DE BUSQUEDA por grupo
	tiempo1_total = 0
	for arr in resultados1:
		# Quitamos el ultimo elemento de cada grupo de resultados que contiene el TIEMPO
		tiempo_parcial = arr.pop()
		tiempo1_total+=tiempo_parcial

		for res in arr:
			resultados1_orden.append(res)

	# Sacamos el tiempo medio de busqueda por grupo
	tiempo1_media = tiempo1_total/len(resultados1)

	tiempo2_total = 0
	for arr in resultados2:
		# Quitamos el ultimo elemento de cada grupo de resultados que contiene el TIEMPO
		tiempo_parcial = arr.pop()
		tiempo2_total+=tiempo_parcial

		for res in arr:
			resultados2_orden.append(res)

	# Sacamos el tiempo medio de busqueda por grupo
	tiempo2_media = tiempo2_total/len(resultados2)

	print(resultados1_orden)
	print("\n\nBREAK3\n\n")
	print(resultados2_orden)

	#print("\nTIEMPO1_TOT" + str(tiempo1_total) + "\n")
	#print("\nTIEMPO2_TOT" + str(tiempo2_total) + "\n")

	""" Escribimos en un fichero BUSQUEDA *.es: NUMERO DE RESULTADOS: 500"""
	ahora = datetime.now()
	nombre = str(ahora.day) + "-" + str(ahora.month) + "-" + str(ahora.year) + "_v4_" + "GOOGLE" + ".txt"
	"""if (ahora.hour < 14 and ahora.hour > 2):
		nombre += " Morning" + ".txt"
	else:
		nombre += " Noche" + ".txt"
	"""
	buscador = "GOOGLE"
	res = resultados1_orden
	tiempoTOT = tiempo1_total
	tiempoGRUPO = tiempo1_media

	for i in range(2):
		if i==1:
			buscador = "FIREFOX"
			res = resultados2_orden
			tiempoTOT = tiempo2_total
			tiempoGRUPO = tiempo2_media
			nombre = str(ahora.day) + "-" + str(ahora.month) + "-" + str(ahora.year) + "_v4_" + "FIREFOX" + ".txt"

		f = open(nombre, "w+")
		f.write("***\tBuscador v4.0 \t Archivo con el número de resultados obtenidos por término de búsqueda en " + buscador + "\t***")
		f.write("\n***\tFECHA: " + str(ahora) + "\t***\n\n")
		f.write("TÉRMINO DE BÚSQUEDA\t\tNÚMERO APROXIMADO DE RESULTADOS\n")

		for j in range(0, len(res)):
			linea = "\n" + busquedas[j] + "\t\t" + str(res[j])
			f.write(linea)

		f.write("\n\nTIEMPO DE BUSQUEDA(secuencial): " + str(tiempoTOT))
		# Escribimos el tiempo medio de busqueda por grupo
		f.write("\n\nTIEMPO MEDIO DE BUSQUEDA(por grupo): " + str(tiempoGRUPO))
		f.close()


def buscar(terminos):

	res = []
	res_driver = []

	# Lista donde guardamos los drivers que utilizamos para las busquedas
	driver_list = []

	# Driver1 CHROME
	chrome_options = webdriver.ChromeOptions();
	chrome_options.add_argument('--headless');		# EJECUCION EN BACKGROUND, invisible

	""" LINEAS PARA DESHABILITAR EL CONTROL DE GOOGLE: "Chrome is being controlled by automated test software" """
	#@#@#@@ chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'disable-infobars']);
	
	driver1 = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options,
								service_args=['--verbose', '--log-path=/tmp/chromedriver.log']);
	
	# Driver2 FIREFOX
	firefox_options = webdriver.FirefoxOptions()
	firefox_options.add_argument('--headless')
	"""
	firefoxOptions.setAcceptInsecureCerts(true);
    firefoxOptions.setLogLevel(FirefoxDriverLogLevel.TRACE);
	"""
	driver2 = webdriver.Firefox(executable_path="/usr/bin/geckodriver", options=firefox_options)

	# Aniadimos los drivers para realizar las busquedas
	driver_list.append(driver1)
	driver_list.append(driver2)

	i = 0

	for driver in driver_list:
		if i==1:
			print("\nCAMBIO DE DRIVER EN LA BUSQUEDA\n\n")
			# En res_driver tenemos los resultados de los terminos en 1 driver
			# Aniadimos al final el tiempo que ha tardado ese driver
			res_driver.append(busqueda_time)
			res.append(res_driver)		# Aniadimos en la lista de resultados finales[res_driver1, res_driver2] 
										#	los resultados del driver1
			res_driver = []
			#tiempos1.append(busqueda_time)
			#print("\nTIEMPOS1: " + str(tiempos1))

		## Inicio TIME
		start_time = time.time()

		for termino in terminos:
			""" Creamos el link de búsqueda con el término correspondiente """
			link = "https://www.google.com/search?q=" + termino
			print("\n" + link)

			""" Establecemos un tiempo entre las búsquedas para evitar CAPTCHA de Google """
			wait = random()
			time.sleep(wait)

			""" Abrimos la URL con la búsqueda """
			driver.get(link)


			""" Buscamos por tags, en nuestro caso, queremos buscar el tag con <div id="result-stats"> """
			content = driver.page_source
			soup = BeautifulSoup(content, "lxml")
			RESULT = soup.find(id ="result-stats")

			""" Obtenemos del texto el número de resultados """
			resu = str(RESULT)
			print("\nRESULT: " + resu)

			""" buscamos el numero de resultados por la cadena de Aproximadamente """
			iniIndex = resu.find("Aproximadamente")
			""" Situamos el indice despues de Aproximadamente, donde va el numero """
			iniIndex += 16
			endIndex = resu.find("resultados")
			num = resu[iniIndex:endIndex]

			#print(num)
			res_driver.append(str(num))

		## busqueda TIME
		busqueda_time = time.time()-start_time
		print("\n*\tTIEMPO BUSQUEDA: " + str(busqueda_time) +"\t*\n")
		i += 1		# Para llevar la cuenta del driver

	# En res_driver tenemos los resultados de los terminos en 2 driver
	# Aniadimos al final el tiempo que ha tardado ese driver
	res_driver.append(busqueda_time)

	# Terminamos de aniadir la info del driver 2
	res.append(res_driver)
	#tiempos2.append(busqueda_time)
	#print("\nTIEMPOS2: " + str(tiempos2))

	""" Cerramos las pestaña abierta """
	for driver in driver_list:
		driver.close()

	""" Devolvemos la lista de resultados finales[res_driver1, res_driver2]"""
	return res


if __name__ == '__main__':
	main()
