# Api Cassandra

## Instalación 

Para poder utilizar la api se debe emplear el siguiente comando:
```
docker-compose up -d
```
Esto levantará 4 dockers: 3 con la imagen de bitnami Cassandra y 
otro que contiene a la api. En este punto se debe esperar a que el
 servicio de la api pueda ser utilizado. Esto se puede ver en los logs
 del contenedor de la api donde se debe obtener........

```
Insertar logs de cuando se encuentra lista la api
```

## Modo de uso

Para este desarrollo se implementan 2 tablas en función del problema propuesto. 
Estas son _paciente_ que se encuentra dentro del keyspace _patient_ y 
 _recetas_ que se encuentra en _recets_.
La api ofrece 4 servicios: ver el contenido de las tablas, crear receta, editarla y eliminarla.
El primero se encuentra en la ruta _/see\_tables_ y al realizar un reques
del tipo post en esta, se despliega un 
json con el nombre de las tablas como llaves. Los valores de ellas son unos arreglos donde
se muestra el contenido de cada tabla.

El segundo 

