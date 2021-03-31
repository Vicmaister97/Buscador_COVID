COMPLETAR DESCRIPCIÓN Y EXPLICACIÓN DEL PROGRAMA

Proyecto de búsqueda automatizada y paralelizada en Google de términos relacionados con el COVID para estudio psicológico de la cuarentena (CONCRETAR). Búsqueda automatizada en Python utilizando las librerías Selenium, bs4 y pandas, junto con la librería concurrent.futures para la paralelización en múltiples hilos.

VERSIÓN OFICIAL DEL BUSCADOR: Buscador_COVID3.py
Trabajamos con 4 listas de términos a buscar:
A partir de la lista con todos los términos a buscar (busquedas), que busca los términos emocionales con las palabras "covid-19" y "*.es", creamos otra lista (busquedas2) que contiene los mismos términos, salvo que se sustituye "covid-19" por "coronavirus" (busca con "coronavirus" y "*.es"). Mismo proceso con otra lista (busquedas_site) donde sustituimos "*.es" por "site:*.es" (busca con "covid-19" y "site:*.es"), y con busquedas2_site (busca "coronavirus" y "site:*.es").
Esto lo realizamos para ampliar y mejorar las búsquedas, y poder comparar los resultados con diversos parámetros de búsqueda.

Para cada lista de búsqueda:
Primero se agrupan todos los términos de búsqueda en GRUPOS, creando *tantos grupos como hilos* vayamos a utilizar para paralelizar la ejecución. Tras esto, lanzamos cada hilo de forma paralela, donde cada uno ejecuta la función "buscar". Esta función recibe como argumento de entrada la lista de términos a buscar (el GRUPO de términos que le corresponde a ese hilo), y básicamente lo que hace cada hilo es abrir una ventana (en background) y buscar en Google 1 a 1 cada uno de los términos de su GRUPO.

Obtener el número de resultados para una búsqueda:
Cada uno de los términos se busca en Google (a través de ChromeDriver y Selenium), se obtiene el fichero html de la respuesta, y a partir del mismo recopilamos el dato de "Aproximadamente X resultados (en Y segundos)". Esto se realiza obteniendo del fichero html el Tag correspondiente al atributo con  "id ="result-stats", del cual obtenemos únicamente el número X antes mencionado. Guarda en una lista (resultados_groups) el número X de resultados obtenido con cada término, para posteriormente crear un fichero (uno por cada una de las 4 listas de búsquedas) donde escribir cada término de búsqueda y su número de resultados.
En este fichero además se detalla la versión del buscador utilizada, la fecha y hora de la búsqueda, y el tiempo de búsqueda.

Script para automatizar la ejecución del buscador:
En la primera fase de búsqueda (de marzo a mayo) se tenía que ejecutar manualmente el buscador a las horas establecidas:
- En marzo (hasta mediados de abril) todos los días 2 búsquedas: una a mediodía (11am-12pm) y otra a medianoche(11pm-12am).
- A partir de mediados de abril todas las semanas los días martes, jueves, viernes y domingo. 1 búsqueda a mediodía (a las 11am-12pm).

Para la segunda fase de búsqueda (de diciembre a febrero) se creó un script que se ejecuta como un servicio automático (demonio) en Linux para ejecutar periódicamente la búsqueda, programando qué dias y a qué horas se ejecuta nuestro programa buscador. De esta forma, todos los lunes, miércoles y viernes se encendía de forma automática el ordenador a mediodía para ejecutar las búsquedas.

TIEMPOS DE BÚSQUEDA:
NOTA: Destacar que los datos de tiempos que se detallan a continuación varían según el ordenador utilizado, su procesador, número de CPUs, la conexión a internet...

En esta versión del buscador, la más optimizada, las búsquedas de los aproximadamente 44 términos se realiza en un tiempo medio de unos 25 segundos.



+++ SCRIPT DONDE SE EJECUTA NECESITA CARPETAS DEBUG y check_auto!!!
+ Detallar cómo se han obtenido los resultados

++ BUSQUEDAS EN DOMINIO ESPAÑOL (blabla.es, sitios con IP española)
## WEB DONDE COMENTA LA DIFERENCIA EN LAS BÚSQUEDAS:
	https://sites.google.com/site/recursosdweb20idiomas/google



-.-.-.-.-.- ERRORES(Solucionados) -.-.-.-.-.-

2-6-20		Versiones ChromeDriver y google chrome DEBEN COINCIDIR!	Establecida v83.
		SOL: El Driver de ChromeDriver se descarga en el momento de ejecución (si NO está ya en caché).
			Así siempre es el más reciente y SIN HISTÓRICO
		
??		Ruta correcta a chromedriver
??		El script ejecuta el buscador al iniciarse la sesión (justo después de hacer log in),
		y en ocasiones la conexión a Internet aún no es posible.
		SOL: Ejecutamos un "sleep 30" en el script para que el buscador se ejecute cuando todas las 
			configuraciones iniciales se han llevado a cabo, y tiene conexión a Internet.
??		Las búsquedas fallan debido a que Google detecta que es un programa de web scrapping(bot), y requiere Captcha.
		Esto ocurre cuando se realizan muchas búsquedas en un periodo de tiempo reducido.
		SOL: Volvemos a repetir la búsqueda más tarde, evitando ejecutar el buscador múltiples veces 
			en un mismo periodo de tiempo.
		SOL MEJORADA(falta implementarla): CAMBIAR PROXY(IP) CON CADA BÚSQUEDA! Así Google no detecta que es un bot, 
			puesto que cada búsqueda se realiza desde una IP diferente.
			
			
-.-.-.-.-.- POSIBLES MEJORAS -.-.-.-.-.-
- INCÓGNITO!!! Útil pero no cambia mucho los resultadoos al descargarse el driver en el momento de ejecución 
		(no hay histórico ni usuario previo)
- BUSQUEDA AVANZADA, no da el número aproximado de resultados :(
	https://rockcontent.com/es/blog/resultados-de-otro-pais/
	
- PROXY OCULTAR DIRECCION IP!!!!!!!!!!!!


-.-.-.-.-.- FUENTES(Bibliografía) -.-.-.-.-.-

**** FUNCIONAMIENTO BEAUTIFULSOUP: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

** """ Ejemplo obtenido de: https://www.edureka.co/blog/web-scraping-with-python/ """

*** Ejecución del buscador en BACKGROUND: https://www.guru99.com/selenium-with-htmlunit-driver-phantomjs.html 


** RUN IN BACKGROUND Selenium Chrome~Firefox. https://blog.testproject.io/2018/02/20/chrome-headless-selenium-python-linux-servers/

** RUN IN BACKGROUND!!!!: https://www.quora.com/Can-I-run-selenium-in-background
		- https://en.wikipedia.org/wiki/Xvfb#Screenshot_example

** Lista de browsers headless (en background): https://github.com/dhamaniasad/HeadlessBrowsers
		- https://phantomjs.org/


* Captura pantalla Windows: https://en.wikipedia.org/wiki/Xwd
