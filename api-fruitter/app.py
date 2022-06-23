from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from flask import Flask, jsonify, request

app = Flask(__name__)
id_paciente = 0
id_receta = 0


# CONECTAR A CLUSTER
def connect_cluster():
    contact_points = ['cassandra_node_1', 'cassandra_node_2', 'cassandra_node_3']
    port = 9042
    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
    cluster = Cluster(contact_points=contact_points, port=port, auth_provider= auth_provider)
    session = cluster.connect()
    print(session.execute('SELECT * FROM patient.paciente'))
    return session

# CREAR RECETA
@app.route('/create', methods=['POST'])
def create():
    receta = {
        "nombre": request.json['nombre'],
        "apellido": request.json['apellido'],
        "rut": request.json['rut'],
        "email": request.json['email'],
        "fecha_nacimiento": request.json['fecha_nacimiento'],
        "comentario": request.json['comentario'],
        "farmacos": request.json['farmacos'],
        "doctor": request.json['doctor']
    }

    rows = session.execute(
        """
        SELECT * FROM patient.paciente WHERE rut = %s
        """, receta["rut"]
    )

    id_cliente = 0

    if rows[0] is None:
        session.execute(
            """
            INSERT INTO patient.paciente (id, nombre, apellido, rut, email, fecha_nacimiento)
            VALUES (%d, %s, %s, %s, %s, %s)
            """, (id_paciente, receta["nombre"], receta["apellido"], receta["rut"], receta["email"], receta["fecha_nacimiento"])
        )
        id_cliente = id_paciente
        id_paciente = id_paciente + 1
    else:
        id_cliente = session.execute(
            """
            SELECT id FROM patient.paciente WHERE %s = rut LIMIT 1
            """, receta["rut"]
        )

    session.execute(
        """
        INSERT INTO recets.recetas (id, id_paciente, comentario, farmaco, doctor)
        VALUES (%d, %d, %s, %s, %s)
        """, (id_receta, id_cliente, receta["comentario"], receta["farmacos"], receta["doctor"])
    )

    id_receta = id_receta + 1

    print("----------------RECETAS----------------")
    rows = session.execute('SELECT * FROM recets.recetas')

    for row in rows:
        print(row)

    print("----------------PACIENTES----------------")
    rows = session.execute('SELECT * FROM patient.paciente')

    for row in rows:
        print(row)

    return jsonify({"message": "ok"})

# EDITA RECETA
@app.route('/edit', methods=['POST'])
def edit():
    receta = {
        "id": request.json['id'],
        "comentario": request.json['comentario'],
        "farmacos": request.json['farmacos'],
        "doctor": request.json['doctor']
    }

    session.execute(
        """
        UPDATE recets.recetas
        SET comentario = %s, farmaco = %s, doctor = %s
        WHERE id = %d
        """, (receta["comentario"], receta["farmacos"], receta["doctor"], receta["id"])
    )

    rows = session.execute('SELECT * FROM recets.recetas')

    for row in rows:
        print(row)
    
    return jsonify({"message": "ok"})
    
# ELIMINA RECETA
@app.route('/delete', methods=['POST'])
def delete():
    receta = {
        "id": request.json['id']
    }

    session.execute(
        """
        DELETE
        FROM recets.recetas
        WHERE id = %d
        """, receta['id']
    )

    rows = session.execute('SELECT * FROM recets.recetas')

    for row in rows:
        print(row)
    
    return jsonify({"message": "ok"})

# CONEXIÓN API A CLUSTER
session = connect_cluster()

if __name__ == '__main__':
    app.run(debug=True, port=5000)