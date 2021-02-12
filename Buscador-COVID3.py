# coding=utf-8

""" Autor: Víctor García Carrera, victorgarciacarrera@gmail.com
	Descarga el contenido del buscador de google con un término
	de búsqueda concreto y guarda el NUMERO DE RESULTADOS
"""

import sys
from math import *
from random import *

""" Ejemplo obtenido de: https://www.edureka.co/blog/web-scraping-with-python/ """

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.common.keys import keys		#The Keys class provide keys in the keyboard like RETURN, F1, ALT etc.

from bs4 import BeautifulSoup		#Libreria bs4 version ultima BeautifulSoup4
import pandas as pd

import string
import time
from datetime import datetime
import numpy as np

# INTENTAR ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
# Para ver si procesos o threads: https://dev.to/rhymes/how-to-make-python-code-concurrent-with-3-lines-of-code-2fpe

POOLSIZE = 10

""" ### FALTA HACER LISTA DE DRIVERS (meter @|FIREFOX|@) +
	###		+ CALCULO DE RESULTADOS (estadisticas, valorar con desviacion respecto a la media...)
	### 	+ INSPECCIONAR/MEDIR + DATOS como tiempo de respuesta, enlaces (expresiones regulares)
"""

def main():

	global POOLSIZE	

	""" LINEAS PARA DESHABILITAR EL CONTROL DE GOOGLE: "Chrome is being controlled by automated test software" """
	chrome_options = webdriver.ChromeOptions();
	chrome_options.add_argument('--headless');		# EJECUCION EN BACKGROUND

	chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'disable-infobars']);
	
	driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options );
	# ,service_args=['--verbose', '--log-path=/tmp/chromedriver.log' )
	

	""" Lista con el numero de resultados por termino de busqueda """
	resultados = []
	resultados_groups = []
	busquedas_groups = []
	busquedas_groups2 = []
	busquedas = []
	busquedas2 = []

	"""busquedas = ["*.es"]"""
	""" Lista(array numpy) con las búsquedas a realizar en Google """
	busquedas = np.array( ["*.es", "covid-19 *.es", "crisis * covid-19 *.es", "calma * covid-19 *.es", "esperanza * covid-19 *.es" ,  
					"pánico * covid-19 *.es", "miedo * covid-19 *.es", "ansiedad * covid-19 *.es", "terror * covid-19 *.es",       
					"inseguridad * covid-19*.es", "enfado * covid-19 *.es", "rabia * covid-19 *.es", "ira * covid-19 *.es" , 
					"alegría * covid-19 *.es", "tristeza * covid-19 *.es" , "sorpresa * covid-19 *.es", "alivio * covid-19 *.es",
					"desconfianza * covid-19 *.es", "incertidumbre * covid-19 *.es", "sanidad * covid-19 *.es", "aislamiento * covid-19 *.es", 
					"cuarentena * covid-19 *.es", "solidaridad * covid-19 *.es", "cooperación * covid-19 *.es", "protección * covid-19 *.es",
					"irresponsable * covid-19 *.es", "polític* * covid-19 *.es", "polític* * irresponsable* * covid-19 *.es", "medic* * covid-19 *.es",
					"cura * covid-19 *.es", "abastecimiento * covid-19 *.es", "alimentos crisis * covid-19 *.es", "alimentos * covid-19 *.es",   
					"aislamiento * covid-19 *.es", "memes * covid-19 *.es", "bromas * covid-19 *.es", "chistes * covid-19 *.es", 
					"alarma * covid-19 *.es", "gratitud * covid-19 *.es", "aplausos * covid-19 *.es", "agradecimiento * covid-19 *.es",
					"vacuna * covid-19 *.es", "mortalidad * covid-19 *.es", "muerte * covid-19 *.es"] )
	
	# Gestionamos otra lista de términos de búsqueda, buscando coronavirus en vez de covid-19
	for term in busquedas:
		new_term = term.replace('covid-19', 'coronavirus')
		busquedas2.append(new_term)

	print(busquedas2)

	"""busquedas2 = np.array( ["*.es", "coronavirus *.es", "crisis * coronavirus *.es", "calma * coronavirus *.es", "esperanza * coronavirus *.es" ,  
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
	"""


	# REORGANIZAMOS LA LISTA DE BÚSQUEDA PARA AGRUPAR LOS TÉRMINOS EN FUNCION DE POOLSIZE!!!
	init_len = len(busquedas)
	print(init_len)
	groups = ceil(init_len/POOLSIZE)		# Agrupamos los términos para minimizar los lanzamientos del pool que son costosos

	# EJEMPLO: len(busquedas)=40, POOLSIZE=10, groups=4
	"""		busquedas_groups = np.array_split(busquedas, groups)
	print busquedas_groups		"""

	
	# Recorremos la lista de búsquedas agrupando por terminos
	for pos in range(0,init_len):
		if pos%groups==0:
			terms = []
			terms2 = []
		terms.append(busquedas[pos])
		terms2.append(busquedas2[pos])
		if pos%groups==(groups-1) or pos==(init_len-1):	# Hemos llenado un grupo de terminos
			busquedas_groups.append(terms)
			busquedas_groups2.append(terms2)

	# Obtemos el array de búsquedas con subarrays agrupados para mejorar la búsqueda
	#print(busquedas_groups)
	#print(busquedas_groups2)
	
	"""SECUENCIAL!!"""
	""" Seleccionamos uno a uno los términos a buscar para obtener su número de resultados """
	"""for termino in busquedas:
		res = buscar(termino)
		resultados.append(str(res))
		"""

	"""PARALELO!!!!"""

	#### Finalizada INICIALIZACION, pasamos a busqueda

	executor = ProcessPoolExecutor(POOLSIZE)

	for x in range(2):
		if x==0:		# primera busqueda con busquedas_groups con covid-19
			busq = busquedas_groups
			name = "covid-19_"
			search = busquedas
		else:			# segunda busqueda con busquedas_groups2 con coronavirus
			busq = busquedas_groups2
			name = "coronavirus_"
			search = busquedas2

		resultados = []

		## Inicio TIME
		start_time = time.time()

		#timeout=None, chunksize=1000
		resultados_groups = list(executor.map(buscar, busq))

		## Tiempo de busqueda
		busqueda_time = time.time() - start_time

		for arr in resultados_groups:
			for res in arr:
				resultados.append(res)

		print("\n\nResultados: " + str(resultados))

		""" Escribimos en un fichero BUSQUEDA *.es: NUMERO DE RESULTADOS: 500"""
		ahora = datetime.now()
		nombre = name + str(ahora.day) + "-" + str(ahora.month) + "-" + str(ahora.year) + "_v3" + ".txt"
		"""if (ahora.hour < 14 and ahora.hour > 2):
			nombre += " Morning" + ".txt"
		else:
			nombre += " Noche" + ".txt"
		"""
		f = open(nombre, "w+")
		f.write("***\tBuscador v3.0 \t Archivo con el número de resultados obtenidos por término de búsqueda en GOOGLE\t***")
		f.write("\n***\tFECHA: " + str(ahora) + "\t***\n\n")
		f.write("TÉRMINO DE BÚSQUEDA\t\tNÚMERO APROXIMADO DE RESULTADOS\n")

		for j in range(0, len(resultados)):
			linea = "\n" + search[j] + "\t\t" + str(resultados[j])
			f.write(linea)

		f.write("\n\nTIEMPO DE BUSQUEDA(en segundos): " + str(busqueda_time))

		f.close()

	# Cierra todas las ventanas de búsqueda y finaliza correctamente la sesión WebDriver
	driver.quit()



def buscar(terminos):

	#global driver

	res = []

	""" LINEAS PARA DESHABILITAR EL CONTROL DE GOOGLE: "Chrome is being controlled by automated test software" """
	chrome_options = webdriver.ChromeOptions();
	chrome_options.add_argument('--headless');		# EJECUCION EN BACKGROUND

	chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'disable-infobars']);
		
	driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options );
	# , service_args=['--verbose', '--log-path=/tmp/chromedriver.log'] )

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
		res.append(str(num))

	""" Cerramos la pestaña abierta """
	driver.close()

	""" Devolvemos el número de resultados de buscar el termino """
	return res


if __name__ == '__main__':
	main()