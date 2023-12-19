# Tasty Bite - API REST

## alu0101438139 - Daniel Felipe Gómez Aristizabal
## alu0101406329 - Facundo José García Gallo


### Referencias

[Anexo 1: Informe Proyecto Final - Tasty Bite]()

[Anexo 2: Manual de usuario de la API y Base de datos TastyBite](https://github.com/facu2002/TastyBiteAPIFlask/blob/main/doc/Manual%20de%20Usuario.pdf)

[Anexo 3: Modelo Entidad- Relación](https://github.com/facu2002/TastyBiteAPIFlask/blob/main/doc/Modelo%20Entidad-Relaci%C3%B3n.pdf)

[Anexo 4: Modelo Relacional](https://github.com/facu2002/TastyBiteAPIFlask/blob/main/doc/Modelo%20Relacional.pdf)

[Anexo 5: Operaciones de consulta sobre la base de datos](https://github.com/facu2002/TastyBiteAPIFlask/blob/main/doc/Consultas%20TastyBite.pdf)


### Organización del proyecto

El proyecto se organiza en tres grandes directorios, uno referente a la base de datos, */bd*, otro referente a la API REST, */api* y el último */doc* que tiene toda la documentación necesaria así como las entregas que se especifican en el enunciado del proyecto. Se ha decidido separar por directorios para facilitar el desarrollo y la ejecución de los scripts de creación de la base de datos y la ejecución de la API REST.

Si profundizamos en el directorio */bd* podemos encontrar dos subdirectorios y dos scripts. Los subdirectorios son */bd/schema* y */bd/data*. El primero de ellos contiene toda la información referente a las tablas de la base de datos, es decir, en este directorio se encuentran todos los scripts que crean cada una de las tablas que mencionamos en el informe. El segundo de ellos contiene los scripts que insertan los datos en las tablas creadas. Por último, los dos scripts que se encuentran en el directorio */bd* son *TastyBite.sql* y *DeleteTastyBite.sql*. El primero es el script general que se encarga de crear la base de datos en su totalidad, para ello se ayuda de los scripts que se encuentran en el subdirectorio */bd/schema*. El segundo de ellos se encarga de eliminar la base de datos creada.

Si nos fijamos en el directorio */api* podemos encontrar un subdirectorio */api/rutas* y dos scripts. Dentro del subdirectorio encontramos todos los scripts que definen el comportamiento de la API REST, es decir, los scripts que definen las rutas y los métodos que se pueden utilizar en cada una de ellas. Los dos scripts que se encuentran en el directorio */api* son *app.py* y *db_connection.py*. El primero de ellos es el script que se encarga de ejecutar la API REST gracias a la utilización de Flask. El segundo de ellos es el script que se encarga de realizar la conexión con la base de datos en PostgreSQL.


Es importante mencionar que antes de ejecutar la API REST es conveniente ejecutar el script encargado de crear la base de datos, *TastyBite.sql*.


### Ejecución scripts PostgreSQL

Para la ejecución del script que crea la base de datos, *TastyBite.sql*, es necesario acceder al prompt de PostgreSQL, con el comando ```sudo -u postgres psql```. A continuación, debemos ejecutar el script con el comando ```\i bd/TastyBite.sql```. Este script será el encargado de llamar a cada uno de los scripts que se encuentran en el subdirectorio y así crear cada una de las relaciones de la base de datos.

En caso de querer eliminar la base de datos creada, debemos ejecutar el script *DeleteTastyBite.sql* con el comando ```\i bd/DeleteTastyBite.sql```.



### Ejecución API REST

Para poder ejecutar la API REST, es importante instalar *Flask* y la biblioteca *psycopg2-binary* en un entorno virtual.

En un principio, con el propósito de asegurar que estamos utilizando la versión correcta de *Python*, ejecutamos el comando ```python3 --version```. Contrastamos que tenemos una versión superior a 3.3. Posteriormente, instalamos la biblioteca necesaria para la creación y gestión de entornos virtuales utilizando ```sudo apt install python3.8-venv```. Esta biblioteca posibilita el mantenimiento de un entorno de desarrollo aislado, evitando conflictos entre las versiones de las bibliotecas.

Con la librería instalada, creamos nuestro entorno virtual denominado *venv* mediante el comando ```python3 -m venv venv```. Este procedimiento garantiza que todas las dependencias específicas de nuestro proyecto se instalaran en un espacio aislado. Para comenzar a trabajar en este entorno virtual, activamos el mismo utilizando el comando ```. venv/bin/activate```. Esto proporciona un indicador claro en el prompt de comandos, confirmando que estamos dentro de nuestro entorno virtual y evitando confusiones con las bibliotecas del sistema.

Seguidamente instalamos *Flask*, mediante el comando ```pip install Flask```. Verificamos que se ha instalado de manera correcta al ejecutar ```flask --version```. Finalmente, instalamos la biblioteca *psycopg2-binary* utilizando ```pip install psycopg2-binary```. Esta biblioteca es fundamental para la interacción con bases de datos *PostgreSQL*, debido a que no requiere compiladores ni bibliotecas externas, simplificando significativamente el proceso.

Una vez tenemos todas las bibliotecas instaladas y nos encontramos dentro del entorno virtual, podemos ejecutar la API REST. Para ello, debemos ejecutar el comando ```flask --app ./api/app.py run```. Este comando ejecuta la API REST en el puerto 5000 y en la dirección de localhost, por lo que para acceder a ella debemos acceder a la dirección *http://localhost:5000/*.

Ahora tenemos la API REST escuchando, lo único que queda es realizar peticiones desde el cliente que queramos, en nuestro caso hicimos uso de *Thunder Client*, gracias a la extensión de Visual Studio Code que permite realizar peticiones HTTP. 