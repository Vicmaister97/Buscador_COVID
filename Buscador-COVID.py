#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Autor: Víctor García Carrera victorgarciacarrera@gmail.com
	Descarga el contenido del buscador de google con un término
	de búsqueda concreto y guarda el NUMERO DE RESULTADOS
"""

import sys
from math import *
from random import *

""" Ejemplo obtenido de: https://www.edureka.co/blog/web-scraping-with-python/ """

from selenium import webdriver
from BeautifulSoup import BeautifulSoup
import pandas as pd

import string
import time
from datetime import datetime

from concurrent.futures import ProcessPoolExecutor


def main():

	""" Establecemos el path al chromedriver"""
	driver = webdriver.Chrome("/bin/chromedriver")

	""" LINEAS PARA DESHABILITAR EL CONTROL DE GOOGLE: "Chrome is being controlled by automated test software" """
	chrome_options = webdriver.ChromeOptions(); 
	chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'disable-infobars']);
	driver = webdriver.Chrome(options=chrome_options);
	
	""" Lista con el numero de resultados por termino de busqueda """
	resultados = []

	"""busquedas = ["*.es"]"""
	""" Lista con las búsquedas a realizar en Google """
	busquedas = ["*.es", "coronavirus *.es", "crisis * coronavirus *.es", "calma * coronavirus *.es", "esperanza * coronavirus *.es" ,  
					"pánico * coronavirus *.es", "miedo * coronavirus *.es", "ansiedad * coronavirus *.es", "terror * coronavirus *.es",       
					"inseguridad * coronavirus*.es", "enfado * coronavirus *.es", "rabia * coronavirus *.es", "ira * coronavirus *.es" , 
					"alegría * coronavirus *.es", "tristeza * coronavirus *.es", "sorpresa * coronavirus *.es", "alivio * coronavirus *.es",
					"desconfianza * coronavirus *.es", "incertidumbre * coronavirus *.es", "sanidad * coronavirus *.es", "aislamiento * coronavirus *.es", 
					"cuarentena * coronavirus *.es", "solidaridad * coronavirus *.es", "cooperación * coronavirus *.es", "protección * coronavirus *.es",
					"irresponsable * coronavirus *.es", "polític* * coronavirus *.es", "polític* * irresponsable* * coronavirus *.es", "medic* * coronavirus *.es",
					"cura * coronavirus *.es", "abastecimiento * coronavirus *.es", "alimentos crisis * coronavirus *.es", "alimentos * coronavirus *.es",   
					"aislamiento * coronavirus *.es", "memes * coronavirus *.es", "bromas * coronavirus *.es", "chistes * coronavirus *.es", 
					"alarma * coronavirus *.es", "gratitud * coronavirus *.es", "aplausos * coronavirus *.es", "agradecimiento * coronavirus *.es",
					"vacuna * coronavirus *.es", "mortalidad * coronavirus *.es", "muerte * coronavirus *.es"]
	
	"""SECUENCIAL!!"""
	""" Seleccionamos uno a uno los términos a buscar para obtener su número de resultados """
	"""for termino in busquedas:
		res = buscar(termino)

		resultados.append(str(res))
		"""

	"""PARALELO!!!!"""
	executor = ProcessPoolExecutor(4)

	resultados = list(executor.map(buscar, busquedas))

	driver.close()


	""" Escribimos en un fichero BUSQUEDA *.es: NUMERO DE RESULTADOS: 500"""
	ahora = datetime.now()
	nombre = str(ahora.day) + "-" + str(ahora.month) + "-" + str(ahora.year) + ".txt"
	"""if (ahora.hour < 14 and ahora.hour > 2):
		nombre += " Morning" + ".txt"
	else:
		nombre += " Noche" + ".txt"
	"""
	f = open(nombre, "w+")
	f.write("***\tArchivo con el número de resultados obtenidos por término de búsqueda en GOOGLE\t***")
	f.write("\n***\tFECHA: " + str(ahora) + "\t***\n\n")
	f.write("TÉRMINO DE BÚSQUEDA\t\tNÚMERO APROXIMADO DE RESULTADOS\n")

	for j in range(0, len(resultados)):
		linea = "\n" + busquedas[j] + "\t\t" + resultados[j]
		f.write(linea)

	f.close()


def buscar(termino):

	""" Establecemos el path al chromedriver"""
	driver = webdriver.Chrome("/bin/chromedriver")

	""" LINEAS PARA DESHABILITAR EL CONTROL DE GOOGLE: "Chrome is being controlled by automated test software" """
	chrome_options = webdriver.ChromeOptions(); 
	chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'disable-infobars']);
	driver = webdriver.Chrome(options=chrome_options);

	""" Creamos el link de búsqueda con el término correspondiente """
	link = "https://www.google.com/search?q=" + termino
	print("\n" + link)

	""" Establecemos un tiempo entre las búsquedas para evitar CAPTCHA de Google """
	wait = random()*2
	time.sleep(wait)

	""" Abrimos la URL con la búsqueda """
	driver.get(link)


	""" Buscamos por tags, en nuestro caso, queremos buscar el tag con <div id="result-stats"> """
	content = driver.page_source
	soup = BeautifulSoup(content)
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
	print str(num)

	driver.close()

	""" Devolvemos el número de resultados de buscar el termino """
	return num


if __name__ == '__main__':
	main()
