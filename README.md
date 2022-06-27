
# Api Cassandra

Diego Alonso y Diego Riffo

## Instalación 
Para poder utilizar la API se debe emplear el siguiente comando:
```
docker-compose up -d
```
Esto levantará 4 dockers: 3 con la imagen de bitnami Cassandra y 
Otro que contiene a la API. En este punto se debe esperar a que él
Servicio de la API pueda ser utilizado.
Esto se demora aproximadamente
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
```json
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
Uso de una arquitectura de tipo anillo, donde la unidad lógica más pequeña es un nodo. Utiliza la partición de datos para optimizar las consultas. por lo que aprovechan, administran y optimizan el uso del ancho de banda de los demás usuarios de la red.

<p align="center">
  <img src="https://cassandra.apache.org/_/_images/diagrams/apache-cassandra-diagrams-01.jpg">
</p>


Los nodos se conectan con la red Gossip Protocol el cual es un  protocolo que permite diseñar sistemas de comunicaciones distribuidos (P2P) altamente eficientes, seguros y de baja latencia.

<p align="center">
  <img src="https://cassandra.apache.org/_/_images/diagrams/apache-cassandra-diagrams-02.jpg">
</p>


Cuando un cliente realiza una petición un nodo será el coordinador (cualquier nodo en el clúster puede asumir el rol de coordinador.) el cual direccionará esta petición al nodo con el token correcto.

Cassandra admite la noción de un factor de replicación (RF), que describe cuántas copias de sus datos deben existir en la base de datos, la naturaleza distribuida de Cassandra la hace más resistente y eficaz. Esto realmente entra en juego cuando tenemos varias réplicas de los mismos datos. Hacerlo ayuda a que el sistema se auto repare si algo sale mal, esta acción es totalmente automática.

<p align="center">
  <img src="https://cassandra.apache.org/_/_images/diagrams/apache-cassandra-diagrams-05.jpg">
</p>


Cuando hay una red generada por nodo hay que considerar cuántos de esto van a haber debido, en una red peer to peer como lo es Cassandra tener tanto escalamiento horizontal y poco vertical afecta al al rendimiento al navegar entre los dispositivos, por lo que es recomendable balancear el tipo de escalamiento.

Cassandra consta de particionador aleatorio por defecto para equilibrar las particiones de un conjunto de datos de entrada para garantizar que cada nodo de procesamiento reciba una partición de tamaño aproximadamente igual.


#### 2. Cassandra posee principalmente dos estrategias para mantener redundancia en la replicación de datos. ¿Cuáles son estos? ¿Cuál es la ventaja de uno sobre otro? ¿Cuál utilizaría usted para en el caso actual y por qué? Justifique apropiadamente su respuesta.


Las estrategias de redundancia son : SimpleStrategy y NetworkTopologyStrategy

SimpleStrategy: Ésta es usada solo para un solo centro de datos y un rack, la primera réplica en un nodo determinado por el particionador. Las réplicas adicionales se colocan en los siguientes nodos en el sentido de las agujas del reloj en el anillo.

NetworkTopologyStrategy: Clúster implementado en varios centros de datos. Esta estrategia especifica cuántas réplicas desea en cada centro de datos.

NetworkTopologyStrategy es altamente recomendado para la mayoría de las implementaciones porque es mucho más fácil expandirse a múltiples centros de datos cuando lo requiera una futura expansión, SimpleStrategy solamente solamente un centro de datos.

En el caso de la actividad solamente se trabajará con un centro de dato por lo que SimpleStrategy es lo ideal.


#### 3. Teniendo en cuenta el contexto del problema ¿Usted cree que la solución propuesta es la correcta? ¿Qué ocurre cuando se quiere escalar en la solución? ¿Qué mejoras implementaría? Oriente su respuesta hacia el Sharding (la replicación/distribución de los datos) y comente una estrategia que podría seguir para ordenar los datos.
Depende de la escala en la que se quiera realizar el sistema, si es a pequeña escala con tres nodos basta para que funcione bien, al igual que la estrategia de replicación ocupada (SimpleStrategy).

Para escalar la solución se necesitará realizar un aumento de nodos, al igual que un mejoramiento en estos mismos (Escalar vertical y horizontal), sino el rendimiento al trabajar con una gran cantidad de datos se vería perjudicado originando un cuello de botella.

Una solución al problema es aumentar la cantidad de shards (otro data center), ya que con esto se solucionara el problema de rendimiento pudiendo repartir los datos en los distintos shards teniendo un balanceo uniforme. También se tendría que cambiar la estrategia de replicación de datos a SimpleStrategy a NetworkTopolyStrategy.

