# Apuntes para estudiar DAI

## Tema 1: Bases de datos.

- En una base de datos, las operaciones que se pueden realizar sobre sus elementos los podemos reducir a CRUD: Create, Read, Update y Delete.

- Una arquitectura web por lo general va a estar formada por un cliente y un servidor principalmente, pudiendo añadir una base de datos que se comunica con el servidor, y otra capa de aplicaciín entre la base de datos y el servidor.

- Hay varios tipos de operaciones de persistencia. Son:

    1) Archivos indexados: Siguen un funcionamiento parecido a los diccionarios, a excepción de que se extienden a almacenar cualquier estructura de datos. Es decir, si un diccionario sigue el patrón clave-valor, aquí valor puede ser cualquier estructura de datos. Como ejemplo, si tenemos ``bd`` nuestra base de datos de archivos indexados, si quiero acceder al primer valor hacemos ``bd['uno']`` si la clave fuese 'uno'.

    2) Bases de datos relacionales: Están bien estructuradas, son consistentes y siguen el patrón ASCI. Son escalables verticalmente, y se implementan operaciones sobre las tablas. Se ejecutan en un proceso aparte (excepto SQLite), se puede acceder a la información usando varias claves, y tienen un uso estandarizado. Deberían usarse para operaciones muy importantes, como una compra. SQL es un ejemplo.

    3) Bases de datos no relacionales: Típicamente usadas en Big Data, son veloces, tienen variabilidad y trabaja con grandes volúmenes de datos (las 3 V's). En vez de tablas se usan listas, hashes, u otras estructuras de datos, tal que no sean tan rígidas para hacer operaciones (más dinamicidad en las mismas). Son escalables horizontalmente, y se usan para aplicaciones tales como las redes sociales. Un ejemplo es MongoDB.

    4) Key-Value Store: Usado sobre todo para aplicaciones que no pueden llamar constantemente a memoria, estos datos se almacenan en la caché y se accede a ellos. Otras aplicaciones son a aquellas con distintas velocidades de ejecución, las síncronas,...

**MongoDB**: Es una base de datos no relacional orientada a objetos JSON (BSON). En lugar de tablas se implementan colecciones de objetos, donde cada colección tiene como elementos una serie de documentos, con campo '_id' incluido siempre. Para manejarla en Python, se usa PyMongo, y la ORM se implementa con PyDantic (Object Relation Mapper, se encarga de traducir entre sí datos incompatibles y, en este caso, se usa para traducir estructuras de programación orientada a objetos en estructuras de una base de datos). Además, se implementa un WSGI para comunicar el código en Python con la aplicación del cliente.

## Tema 2: Protocolo HTTP

- Protocolo estándar de comunicación entre cliente y servidor. El cliente es proactivo, envía requests y gestiona las plantillas. El servidor es reactivo, recibe requests y se comunica con la base de datos, implementando la lógica entre los datos.

- Dos formas de comunicarse:
    1) Comunicación síncrona: El cliente envía un request al servidor y para su ejecución hasta que recibe una respuesta.
    2) Comunicación asíncrona: El cliente envía un request al servidor y sigue funcionando, hasta recibir en cierto momento la respuesta del servidor y hacer las operaciones pertinentes.

- Generalmente, el proceso de comunicación cliente-servidor sigue la lógica MVC, que se explica más adelante (aunque puede variar, la forma de funcionar es siempre similar).

- El cliente usa lenguajes como HTML, CSS o JavaScript (y sus extensiones). El servidor se programa con Python (frameworks como Django), PHP o Ruby, entre otros.

- El protocolo HTTP es sin estado. Esto es, el servidor no almacena información sensible del cliente (como contraseñas o cuentas bancarias), si el servidor cae, el cliente asume que no había información suya, si el cliente cae, el servidor no almacena información innecesaria, y si el cliente necesita comunicarse con varios servidores, el almacenamiento y comunicación se hace de forma sincronizada.

- Como hemos dicho, el cliente envía requests al servidor, y el servidor envía responses al cliente. ¿Qué son?:
    1) Request: Se envía al servidor, y es una petición desde el cliente. Tienen tanto una cabecera como un cuerpo. Los verbos principales en HTTP para hacer requests son GET, POST, DELETE y UPDATE (CRUD). En adición,  aunque GET sea Read, y POST sea Create, se pueden usar para obtener datos. Además, son los principales verbos usados para HTTP, con la diferencia de que en GET toda la información de la request va en la URL y en POST, va en el cuerpo de la petición. En consecuencia, si usando HTTP, queremos acceder a ``www.pagina.com``, desde el puerto 80, al recurso almacenado en ``path/al/recurso``, con datos para la petición ``num_pagina=2`` y ``tipo_letra=mi_tipo``:

        -> Con petición GET, la URL es ``http://www.pagina.com:80/path/al/recurso?num_pagina=2&tipo_letra=mi_tipo``
        -> Con petición POST, la URL es ``http://www.pagina.com:80/path/al/recurso``, y en el cuerpo tenemos ``num_pagina=2  tipo_letra=mi_tipo``

    2) Response: La respuesta del servidor a un request, con la información requerida. La estructura es: versión de protocolo + status code + status message + cabeceras.

- HTTP permite el uso de **cookies** y **sesiones**:
    
    - **cookies**: Ficheros de texto que se almacenan en el navegador. Se asocian a cierta funcionalidad, como la autentificación. Son de fácil accceso, por lo que no es seguro usarlos. El nombre entre cookies debe ser distinto.
    
    - **sesiones**: Se almacenan en el servidor, y tienen un tope en el almacenamiento. Pese a ser de fácil acceso, son más seguras que las cookies, pues como funcionalidad añade a estas que se asocien con un token de manera aleatoria.

## Tema 3: Framework MVC

- MVC: Modelo Vista Controlador. Es un paradigma de programación, donde cada tarea se divide entre los tres componentes principales:

    - Modelo: Se comunica con la base de datos y con el controlador. Implementa la lógica entre datos, restricciones,... Forma parte del servidor.
    - Vista: El usuario interactúa con ella, mostrando los resultados de las requests que hace al servidor, rellenando las plantillas. Se comunica con el controlador.
    - Controlador: Atiende las peticiones (requests) del cliente y las procesa, devolviendo una respuesta (response) previamente habiendo hecho una consulta al modelo si hubiese hecho falta.

- En general el proceso es: vista manda una request usando HTTP --> el controlador recibe y procesa la request --> si hiciese falta, el controlador consulta el modelo (base de datos) --> el controlador formaliza una response --> devuelve la response al cliente --> el cliente rellena las plantillas con la información devuelta.

- Un framework para desarrollo web es Django. Implementa el paradigma MTV (similar al MVC), donde M es el modelo (implemntado principalmente en models.py), T es templates (la vista en el MVC, implementado en una carpeta para plantillas) y V es la vista (el controlador en el MVC, implementado en views.py). Hay otros ficheros como urls.py, que gestiona las URLs que puede recibir el servidor, y ejecuta una función en views.py para resolver la request.

- Cuando creamos un proyecto de Django, hay dos carpetas: ``mi_proyecto`` (donde está la configuración, se gestionan algunas URLs, se gestiona la API Restfull si hubiese,...) y ``app`` (donde se implementa el código y se almacenan las plantillas principalmente).

- Hay otros frameworks de desarrollo web, como FastAPI o Flask.

## Tema 4: HTML5 y CSS3.

- A lo largo de la historia de la informática, se han sucedido varias versiones de HTML, llegando a la actual: HTML5. Pese a usarse en muchos navegadores, otros no la soportan. Podemos destacar en HTML5 la introducción de etiquetas semánticas como ``<div>``, etiquetas multimedia como ``<video>`` o ``<canvas>``, el almacenamiento local y el soporte a CSS3 (versión de CSS que soporta componentes como flexbox o grid).

- XML: Lenguaje de marcado. Su versión en HTML es XHTML. Un ejemplo de código en XHTML podría ser el siguiente, puesto que se creó para que fuese fácilmente procesado por navegadores y humanos:

```
<persona>
    <nombre>Álvaro</nombre>
    <apellidos>Rodríguez Gallardo</apellidos>
</persona>
```

- XHTML es más restrictivo que HTML. En XHTML las etiquetas **siempre** son en minúscula, las etiquetas **siempre** deben cerrarse (HTML da cierta libertad para ello) y los atributos **siempre** entre comillas, entre otras características.

- La forma de disponer los elementos es muy variada. Usar el atributo ``display``. Si ``display: block;`` los elementos se apilan a la izquierda de la página, uno sobre otro. Si ``display: inline;``, cada elemento sigue al anterior siempre que haya espacio a su derecha para colocarse.

- En HTML hay jerarquía en etiquetas (relacionado con DOM).

- Hay varios frameworks CSS, que son hojas de estilo previamente hechas para poder ser usadas y personalizar el diseño de una página, haciendo que este sea responsive. Algunos ejemplos son Bootstrap o Tailwind. Sin embargo, son distintos en el sentido que, aunque ambos sean frameworks CSS para un diseño responsive, Bootstrap ofrece componentes previamente construidos, con escasas posibilidades de personalizarlos, por lo que la curva de aprendizaje es menor, y es recomendable usar en páginas donde el diseño no sea el eje central. Por otro lado, Tailwind ofrece utilidades a bajo nivel para construir con ellas componentes, así que la curva de aprendizaje es más lenta, y se debería usar para páginas donde el diseño sea personal.

## Tema 5: Formularios

- Un formulario típico en HTML es el siguiente:

```
<form action="plantilla.html">
    <p>Número</p>
    <input type="text" name="number" />
    <br>
    <input type="submit" "name"="submit" />
</form>
```

- Django permite manejar los formularios de una forma sencilla en ``forms.py``, donde se definen (en la práctica hemos usados estructuras de programación orientada a objetos para ello). Además, permite la validación, relleno de plantillas, gestión de errores y seguridad CSRF, entre otros.

- ¿Cómo se validan? --> Usamos `is_valid()`. Ejemplo:
```
form = miFormulario()
if request.method == 'POST':
    form = miFormulario(data=request.POST)
    if form.is_valid():
        operarConFormulario(form)
        return render(request,'plantilla.html',form)
return render(request,'plantilla.html',form)
```

- Como inciso, es importante saber qué ocurre en todo momento. Por ello, Python ofrece la posibilidad de hacer Logging. Para ello, al iniciar el programa:
```
import logging

logger = logging.getLogger(__name__)

# Uso
logger.info()
logger.error()
...
```

- Si se inicializa para cierto nivel, todos los que hay por debajo de él pueden usarse también, pero no los que hay encima. Si siguiese una jerarquía abuelo->padre->nieto, y configuramos para usar logger.padre, podemos usar logger.nieto, pero no logger.abuelo.

## Tema: 6: Autentificación

- Se usa para poder dar o quitar funcionalidad a la página en función del rol de usuario, o incluso si está o no loggeado. En general, se introduce un nombre de usuario y una contraseña y, si está en la base de datos, se crea una cookie que indica que está loggeado (son distintas cookies entre usuarios), que sirve para saber que está loggeado (o incluso otras pueden crearse para saber su rol). Estas cookies, cuando se cierra sesión, se destruyen (o si se cierra el navegador).

- Django hace uso de un middleware para gestionar lo relativo a la autentificación. Apoyándose en modelos y plantillas para este propósito, permite gestionar más fácilmente el control de sesiones, los roles de usuario o la autorización, entre otros, para que no sea un sufrimiento como en PHP. Se recomienda usar el plugin ``django-allauth``, el cual incluye funcionalidad para redes sociales.

## Tema 7: APIs Restfull

- Primero tenemos que diferenciar dos tipos de páginas (esto es más para el tema de React, pero en las diapositivas lo mete aquí también):

    - MPA (Multi Page Application): Son las clásicas aplicaciones en las cuales cualquier petición que haga el cliente necesita esperar a la respuesta del servidor y volver a recargar la página. Por ejemplo, aquí encontramos peticiones que se hacen con HTML.
    - SPA (Single Page Application): Solamente hace una recarga de la página, que es la necesaria para visualizarla. Todas las modificaciones se hacen con peticiones asíncronas desde JavaScipt, por ejemplo, al servidor, usando bibliotecas como AJAX, o aquellas que usan la extensión de JS, JSX, haciendo uso de React para la interfaz de usuario (más fluida y compleja).

- Volviendo al tema, una API Restfull permite comunicar la aplicación con otros dispositivos como móviles. Se encarga de recibir peticiones HTTP y hacer las consultas u operaciones necesarias. Estas peticiones son sin estado (una petición no recuerda a la anterior), las APIs Restfull devuelven objetos JSON, entre otras características. Además, las peticiones HTTP, aunque siguen el esquema CRUD y usan verbos GET, POST, DELETE y UPDATE, en realidad son peticiones GET, con path distinto a las clásicas peticiones GET. Por ejemplo:

```
Quiero borrar de la base de datos todos los elementos que empiecen por A:

-> Sin API Restfull: POST http://www.pagina.com:80/path/recurso/que/borra/cosas?primera_letra='A'
-> Con API Restfull: dELETE http://www.pagina.es:80/api/borrar/A
```

- A un path de la API se le llama **endpoint**.

- En Django se usan los plugins ``django-ninja`` y ``django-ninja-extra`` para construir una API Restfull. Se puede exigir autentificación para usar la API. En ese caso, podemos incluir un token que debe ser dado para ejecutar un endpoint. Si por ejemplo hacemos una petición AJAX desde un móvil a la API, en la cabecera de la petición debe ir el token.

- Formato JWT: Manera de hacer las peticiones a la API más compacta.

## Temas 8 y 9: DOM y ES6.

- Como hemos dicho, las etiquetas de HTML son jerarquizadas en un árbol (las etiquetas pueden ser de tipo root, atributo,...). Esto se representa en un archivo, el DOM, que se carga en la página. Si se quisiese hacer la página interactiva, se podría usar JavaScript para modificar los nodos de dicho árbol, pudiendo hacer animaciones, peticiones asíncronas,..., sin tener que volver a cargar el DOM para ver los cambios.

- ES6: Versión de JavaScript estandarizada, que incluye NodeJS.

- Se puede usar AJAX para hacer peticiones asíncronas al servidor, y así modificar el DOM sin volver a cargarlo en el navegador. Un ejemplo de uso de AJAX es

```
$.ajax('el/path/para/la/peticion', {
    success(response):
        hacerAlgo(response);
    error(response):
        print("Error en la petición AJAX");
})
```

- Posibilidad de usar funciones flecha (introducidas en ES6). Sintaxis más corta, de fácil comprensión,... Además, son un apoyo importante para jQuery.

- jQuery: Biblioteca que facilita la forma de acceder a los nodos del DOM. Para usarlo, el archivo JS debe empezar con la sintaxis apropiada (parecido a 'cuando se cargue DOM'). Un ejemplo de uso, dado este código HTML, mostrar por pantalla el resultado de una operación hecha en el servidor sin recargar DOM:

```
<buttom text="clickar" class="escucha" />
<p id="mi_id"></p>

```

- La solución sería
```
$document.ready(function) {
    $('.escucha').click(function(event) {
        $.ajax('path/a/la/operacion', {
            success(resp):
                $('#mi_id').text = resp.respuesta;
            error(err):
                console.alert("Error en la operación");
        })
    })
}
```

- ES6 nos da la clase 'Promise' para crear objetos promesa, que permiten gestionar la finalización de peticiones asíncronas al servidor. Se puede complementar con el uso de 'async/ await' para tratar con aquellas que se ven y se comportan como peticiones síncronas pese a no serlo.

- Otras opciones en ES6. Las estructuras de datos son similares a otros lenaguajes. Existe el operador `spread`, escrito como `...`, que por si solo no significa nada aunque el programa lo procese, pero para hacer copias de objetos de manera sencilla, se usan así: mi_copia_objeto = ...objeto (recordar que en Python se asignan punteros).

## Tema 10: React

- Volvemos a las páginas SPA y MPA. Este tema se centra en las SPA.

- React es una librería para interfaces de usuario que proporciona componentes para personalizar la misma. Librería de JavaScript, pero se usa en su extensión JSX, ya que esta permite incrustar código HTML, y React ofrece las componentes en forma de etiquetas.

- Los archivos JSX, al compilarlos, se unifican en `bundle.js`, hecho por Webpack.

- En el clásico MVC, M y C estaban en el servidor y V en el cliente. En el caso de las aplicaciónes SPA, M está en el servidor, C y V en el cliente.

- React usa DOM virtual, por lo que la modificación del DOM es más eficiente que en el caso base.

- Posibilidad de usar "herencia" para modularizar el programa. Un ejemplo es
```
function Producto(){
    return (
        <Imagen></Imagen>
        <Info></Info>
    );
}

function Imagen(){
    return (
        <img src="imagen.png" />
    );
}

function Info(){
    return(
        <p>Un producto</p>
        <p>Precio: 10$ </p>
    )
}
```

- Existen los estados (useState, useEffect) y los eventos:
    - Eventos: Qué se puede hacer sobre una componente.
    - Estados: Información local que almacena una componente. Puede predefinirse antes de ejecución o pedirla al servidor y almacenarla localmente. Existe la posibilidad de pasar a cada componente este información. Por ejemplo:

    ```
    function Producto(){
        imagen = "imagen.png";
        return (
            <Imagen img={imagen} ></Imagen>
        );
    }

    function Imagen(img) {
        return (
            <img src=img />
        );
    }
    ```

## Tema 11: Despliegue

- Cuando hemos creado nuestra aplicación en un entorno de desarrollo, queremos que otras personas lo usen. Hay que cambiar el servidor a uno de producción. En Django también se deben cambiar algunas variables de `settings.py`.

- Se quiere tener una estructura como la siguiente (práctica 6):

```

Cliente <-----> NGINX <--------> Gunicorn <-------> Django

```

- NGINX se usa para servir archivos estáticos, cifrado,..., y hacer peticiones al servidor hechas por el cliente. Estas peticiones las recibe un WSGI, en este caso, Gunicorn.

- WSGI (Gunicorn): Recibe las peticiones del cliente y las comunica con el código Python alojado en el servidor (en este caso, se comunica con Django). Debe configurarse en un archivo aparte.

- Estas virtualizaciones se pueden hacer con Docker, apoyándose en scripts para hacer más simple la instalación, de manera que esta se independiza del entorno de producción.

- Podemos distinguir tres tipos de aplicaciones según qué se despliega:
    - SaaS: Software as a Service. El software se almacena en la nube y el cliente solo debe instalar la aplicación, tal que esta se comunicará con el servidor que será el que haga las operaciones.

    - PaaS: Platform as a Service. Todo el hardware y software necesario para la ejecución del programa es dado al usuario.

    -IaaS: Infraestructure as a Service. Se le da al usuario una infraestructura virtual o física, las IPs para ejecutar el programa,...
