COMPLETAR DESCRIPCIÓN Y EXPLICACIÓN DEL PROGRAMA

+++ SCRIPT DONDE SE EJECUTA NECESITA CARPETAS DEBUG y check_auto!!!
+ Detallar cómo se han obtenido los resultados

++ BUSQUEDAS EN DOMINIO ESPAÑOL (blabla.es, sitios con IP española)
## WEB DONDE COMENTA LA DIFERENCIA EN LAS BÚSQUEDAS:
	https://sites.google.com/site/recursosdweb20idiomas/google



-.-.-.-.-.- ERRORES(Solucionados) -.-.-.-.-.-

2-6-20		Versiones chromedriver y google chrome DEBEN COINCIDIR!	Establecida v83.
		SOL: El Driver de chromedriver se descarga en el momento de ejecución, si no está en caché se descarga.
			Así siempre es el más reciente y SIN HISTÓRICO
		
??		Ruta correcta a chromedriver
??		El script ejecuta el buscador al iniciarse la sesión (justo después de hacer log in), y en ocasiones la conexión a Internet aún no es posible.
		SOL: Ejecutamos un "sleep 30" en el script para que el buscador se ejecute cuando todas las configuraciones iniciales
			se han llevado a cabo, y tiene conexión a Internet.
??		Las búsquedas fallan debido a que Google detecta que es un programa de web scrapping(bot), y requiere Captcha.
		Esto ocurre cuando se realizan muchas búsquedas en un periodo de tiempo reducido.
		SOL: Volvemos a repetir la búsqueda más tarde, evitando ejecutar el buscador múltiples veces en un mismo periodo de tiempo.
		SOL MEJORADA(falta implementarla): CAMBIAR PROXY(IP) CON CADA BÚSQUEDA! Así Google no detecta que es un bot, puesto que cada
			búsqueda se realiza desde una IP diferente.
			
			
-.-.-.-.-.- POSIBLES MEJORAS -.-.-.-.-.-
- INCÓGNITO!!! Útil pero no cambia mucho los resultadoos al descargarse el driver en el momento de ejecución (no hay histórico ni usuario previo)
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
