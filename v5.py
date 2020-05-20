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
## Inicio TIME
start_time = time.time()

def main():

	# Declaramos la var global POOLSIZE que indica el tamanio del pool de procesos
	global POOLSIZE

	# Driver1 CHROME
	chrome_options = webdriver.ChromeOptions();
	chrome_options.add_argument('--headless');		# EJECUCION EN BACKGROUND, invisible

	""" LINEAS PARA DESHABILITAR EL CONTROL DE GOOGLE: "Chrome is being controlled by automated test software" """
	chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'disable-infobars']);
	
	driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options,
								service_args=['--verbose', '--log-path=/tmp/chromedriver.log']);
	
	
	""" Variables de busquedas y resultados """	
	busquedas_groups = []		#  Lista con las busquedas agrupadas
	resultados1_groups = []		#  Lista con los resultados agrupados con el 1er buscador GOOGLE
	resultados2_groups = []		#  Lista con los resultados agrupados con el 2do buscador YAHOO

	# Listas por cada BUSCADOR de los resultados obtenidos
	resultados1 = []		# Resultados de Google
	resultados2 = []		# Resultados de Yahoo

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

	# EJEMPLO: len(busquedas)=44, POOLSIZE=10, groups=5, para mantener que haya <=10 grupos de busquedas
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

	try:
		resultados1_groups = list(executor.map(buscar1, busquedas_groups))

	except concurrent.futures.process.BrokenProcessPool as e:		# Si falla alguna búsqueda
		print('could not start new tasks: {}'.format(e))

	print("\n\nCAMBIO DE BUSCADOR\n\n")

	try:
		resultados2_groups = list(executor.map(buscar2, busquedas_groups))

	except concurrent.futures.process.BrokenProcessPool as e:		# Si falla alguna búsqueda
		print('could not start new tasks: {}'.format(e))

	"""for driver in driver_list:
		# Cierra todas las ventanas de búsqueda y finaliza correctamente la sesión WebDriver
	"""
	driver.quit()

	# Quitamos los grupos de resultados
	for arr in resultados1_groups:
		for res in arr:
			resultados1.append(res)	

	for arr in resultados2_groups:
		for res in arr:
			resultados2.append(res)	

	print(resultados1)
	print("\n\nBREAK2\n\n")
	print(resultados2)

	"""
	resultadosNotOrdered.append(resultados1)
	resultadosNotOrdered.append(resultados2)
	
	for driver_results in resultadosNotOrdered:
		for arr in driver_results
			for res in arr:
				file = int(driver_results[0])
				resultados[file].append(res)

	print("\n\nResultados: " +str(resultados)) """

	""" Escribimos en un fichero BUSQUEDA *.es: NUMERO DE RESULTADOS: 500"""
	#	ahora = datetime.now()
	#	nombre = str(ahora.day) + "-" + str(ahora.month) + "-" + str(ahora.year) + ".txt"
	"""if (ahora.hour < 14 and ahora.hour > 2):
		nombre += " Morning" + ".txt"
	else:
		nombre += " Noche" + ".txt"
	"""
	"""	f = open(nombre, "w+")
	f.write("***\tBuscador v4.0 \t Archivo con el número de resultados obtenidos por término de búsqueda en GOOGLE\t***")
	f.write("\n***\tFECHA: " + str(ahora) + "\t***\n\n")
	f.write("TÉRMINO DE BÚSQUEDA\t\tNÚMERO APROXIMADO DE RESULTADOS\n")

	for j in range(0, len(resultados)):
		linea = "\n" + busquedas[j] + "\t\t" + str(resultados[j])
		f.write(linea)

	f.write("\n\nTIEMPO DE BUSQUEDA: " + str(time.time()-start_time))

	f.close()"""

# BUSQUEDA EN GOOGLE
def buscar1(terminos):

	res = []

	# Driver1 CHROME
	chrome_options = webdriver.ChromeOptions();
	chrome_options.add_argument('--headless');		# EJECUCION EN BACKGROUND, invisible

	""" LINEAS PARA DESHABILITAR EL CONTROL DE GOOGLE: "Chrome is being controlled by automated test software" """
	chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'disable-infobars']);
	
	driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options,
								service_args=['--verbose', '--log-path=/tmp/chromedriver.log']);


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
		soup = BeautifulSoup(content, "html.parser")
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

	""" Cerramos las pestaña abierta """
	driver.close()

	""" Devolvemos la lista de resultados"""
	return res


# BUSQUEDA EN YAHOO
def buscar2(terminos):

	res = []

	# Driver1 CHROME
	chrome_options = webdriver.ChromeOptions();
	chrome_options.add_argument('--headless');		# EJECUCION EN BACKGROUND, invisible

	""" LINEAS PARA DESHABILITAR EL CONTROL DE GOOGLE: "Chrome is being controlled by automated test software" """
	chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'disable-infobars']);
	
	driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options,
								service_args=['--verbose', '--log-path=/tmp/chromedriver.log']);


	for termino in terminos:
		""" Creamos el link de búsqueda con el término correspondiente """
		link = "https://es.search.yahoo.com/search?p=" + termino
		print("\n" + link)

		""" Establecemos un tiempo entre las búsquedas para evitar CAPTCHA de Google """
		wait = random()
		time.sleep(wait)

		""" Abrimos la URL con la búsqueda """
		driver.get(link)


		""" Buscamos por tags, en nuestro caso, queremos buscar el tag con <div id="result-stats"> """
		content = driver.page_source
		#soup = BeautifulSoup(content, "html.parser")
		## NOTA: Podemos mejorar el rendimiento con el parseador lxml, instalado en pip3
		soup = BeautifulSoup(content, "lxml")
		# Busca el tag span que empieza con yui_3... donde esta el numero de resultados
		RESULT = soup.find_all("span", id=re.compile(r"^yui_3_10_0_1"))

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

	""" Cerramos las pestaña abierta """
	driver.close()

	""" Devolvemos la lista de resultados"""
	return res


if __name__ == '__main__':
	main()