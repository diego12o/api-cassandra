
# Api Cassandra

## Instalación 
Para poder utilizar la API se debe emplear el siguiente comando:
```
docker-compose up -d
```
Esto levantará 4 dockers: 3 con la imagen de bitnami Cassandra y 
Otro que contiene a la API. En este punto se debe esperar a que él
Servicio de la API pueda ser utilizado. Esto se puede ver en los logs
del contenedor de la API donde se debe obtener........
```
Insertar logs de cuando se encuentra lista la API
```
## Modo de uso

Para este desarrollo se implementan 2 tablas en función del problema propuesto. 
Estas son _paciente_ que se encuentra dentro del keyspace _patient_ y 
 _recetas_ que se encuentra en _recets_.
La API ofrece 4 servicios: ver el contenido de las tablas, crear receta, editarla y eliminarla.

### Ver tablas 
El primero se encuentra en la ruta _/see\_tables_ y al realizar un reques 
del tipo post en esta, se despliega un JSON con el nombre de las tablas como llaves. 
Los valores de ellas son unos arreglos donde se muestra el contenido de cada tabla.

```
http.localhost:5000/see_tables      [POST]
```
### Crear recetas 
El segundo crea recetas, para esto necesitan la siguiente información:
```
{
"nombre": "Melon",
"apellido": "Musk",
"rut": "1",
"email": "Xmelon_muskX@fruitter.com",
"fecha_nacimiento": "28/06/1971",
"comentario": "Amigdalitis",
"farmacos": "Paracetamol",
"doctor": "El Waton de la Fruta" }
```
Esta información se mandará a la siguiente ruta:

```
http.localhost:5000/create      [POST]
```
### Editar recetas

Para editar una receta se necesitará la siguiente información:
```
{
"id": 1,
"comentario ": " Amigdalitis aguda ",
"farmacos ": " Paracetamol con aguita ",
"doctor ": "El Waton de la Fruta "
}
```
Esta información se mandará a la siguiente ruta:
```
http.localhost:5000/edit     [POST]
```
### Eliminar recetas
Finalmente para poder eliminar una receta necesitara la siguiente información:
```
{
"id": 1
}
```

Esta informacion se mandara a la siguiente ruta:
```
http.localhost:5000/delete     [POST]
```

## Preguntas y Respuestas


#### 1. Explique la arquitectura que Cassandra maneja. Cuando se crea el cluster ¿Cómo los nodos se conectan? ¿Qué ocurre cuando un cliente realiza una petición a uno de los nodos? ¿Qué ocurre cuando uno de los nodos se desconecta? ¿La red generada entre los nodos siempre es eficiente? ¿Existe balanceo de carga?
#### 2. Cassandra posee principalmente dos estrategias para mantener redundancia en la replicación de datos. ¿Cuáles son estos? ¿Cuál es la ventaja de uno sobre otro? ¿Cuál utilizaría usted para en el caso actual y por qué? Justifique apropiadamente su respuesta.
#### 3. Teniendo en cuenta el contexto del problema ¿Usted cree que la solución propuesta es la correcta? ¿Qué ocurre cuando se quiere escalar en la solución? ¿Qué mejoras implementaría? Oriente su respuesta hacia el Sharding (la replicación/distribución de los datos) y comente una estrategia que podría seguir para ordenar los datos.
