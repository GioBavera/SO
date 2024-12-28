Aplicación Web hecha en framework flask basado en python alojado en un servidor web apache (ultima versión). Se conecta a un servidor mongoDB para guardar los datos. Todo esto en docker.

Pasos ejecución: 
1. Abrir terminal en la carpeta de este proyecto
2. Ejecutar el comando "Docker-compose up"
3. Una vez iniciado el servidor, entrar en la pagina: http://localhost:80
4. Para apagarlo, hacerlo desde Docker desktop o 'Ctr + C' en la misma terminal anterior.


---------------------------------------------------
=== requirements.txt 
Especifica que cosas adicionales hay que instalar a la hora de iniciar el contenedor. En este caso, flask y pymongo (permite conectar a mongodb).

=== app.py y /templates
Programa principal (backend) que lleva toda la lógica y operaciones con la base de datos. Muestra por medio de las interfaces de Templates. Por defecto, llena la base de datos con 10 juegos de mesa en la base de datos para poder operar. 

=== docker-compose.yml 
Permite levantar un servidor pre configurado con un solo comando, "docker-compose up -d". 

=== Dockerfile
Archivo que contiene las instrucciones para construir la imagen del servidor con flask. Paso a paso de como debe hacerlo. 

=== run.wsgi
Necesario para la configuración de mod_wsgi, el cual actúa como un puente entre Apache y la aplicación Flask. Este archivo le dice a mod_wsgi como iniciar y manejar tu aplicación Flask. mod_wsgi es un modulo de apache que permite ejecutar aplicaciones python. 

=== 000-default.conf
Archivo de configuración del servidor web apache. En dockerfile se establece que este se va a copiar a la dirección correspondiente en el contenedor del servidor. 


