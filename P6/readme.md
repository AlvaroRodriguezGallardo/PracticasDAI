Aquí voy a subir unos apuntes del proceso de despliegue de la aplicación por si tengo que volver atrás y repetir el proceso.

1- Crear archivo ``docker-compose-prod.yml``: Dentro de la carpeta del proyecto ponemos el archivo con lo siguiente 

```
version: '3.7'

services:
  django_gunicorn:
    volumes:
      - static:/static
    env_file:
      - .env
    build:
      context: .
    ports:
      - "8000:8000"
  nginx:
    build: ./nginx
    volumes:
      - static:/static
    ports:
      - "80:80"
    depends_on:
      - django_gunicorn

volumes:
  static:
```

2- Modificar el resto de archivos de manera que se incluyan las cosas que hay en este [git](https://github.com/dotja/django-docker-compose) (por ahora no meterse en las carpetas, solo los archivos, aunque el .env aún no lo he usado).

3- Hay que tener instalado ``docker-compose`` (ya lo teníamos instalado) y ``docker-machine`` (este no lo teníamos, se instala con [estos pasos](https://github.com/dotja/django-docker-compose), aunque redirije a la página de docker-desktop, así que no sé si va incluido con docker-desktop, así que por ahora supongo que lo tengo también).En Windows hacer con git bash, pero parece que para la terminal en general no se hace.

4- Ahora estoy trabajando en Ubuntu, pero para Mac y Windows hay que instalar también Docker Toolbox. Para windows meterse [aquí](https://docker-docs.uclv.cu/toolbox/toolbox_install_windows/)

5- Ejecutar ``docker-compose version`` y ``docker-machine version``. Debe salir como que está instalado, así que deduzco que tengo que instalar docker-machine porque no va implícito en Docker Desktop. He encontrado esta [página](https://gdevillele.github.io/machine/install-machine/) que explica mejor los pasos para instalar docker-machine, y al menos ya me funciona ``docker-machine version``.

6- A partir de ahora es importante tener la estructura del proyecto con todo escrito para poder continuar con el despliegue.

7- Ejecuta el comando ``docker-machine create -d virtualbox dev;`` y así creamos una máquina nueva. A mi me ha dado este error 
``
Error with pre-create check: "VBoxManage not found. Make sure VirtualBox is installed and VBoxManage is in the path"
``

Así que habrá que instalar VirtualBox si no está instalado, y añadir el PATH. Como estoy en Ubuntu, esto último lo haría como ``export PATH=$PATH:/ruta/a/virtualbox``.

8- Si conseguimos que no haya errores en lo de antes, ejecutamos ``eval $(docker-machine env dev)`` que sirve para que cualquier comando docker se comunique con el daemon (creo). Después, con ``docker-machine ls`` vemos si todo ha ido bien. En la página que estoy siguiendo aparece 

| NAME | ACTIVE | DRIVER      | STATE   | URL                       | SWARM | DOCKER   | ERRORS |
|------|--------|-------------|---------|---------------------------|-------|----------|--------|
| dev  | -      | virtualbox  | Running | tcp://192.168.99.100:2376 |       | v18.09.3 |        |

