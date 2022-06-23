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
    global id_paciente, id_receta
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
        SELECT * FROM patient.paciente WHERE rut = %s ALLOW FILTERING
        """, receta["rut"]
    )

    id_cliente = 0
    print(rows)
    if len(rows.current_rows) == 0:
        session.execute(
            """
            INSERT INTO patient.paciente ("id", "nombre", "apellido", "rut", "email", "fecha_nacimiento")
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_paciente, receta["nombre"], receta["apellido"], receta["rut"], receta["email"], receta["fecha_nacimiento"])
        )
        id_cliente = id_paciente
        id_paciente = id_paciente + 1
    else:
        result = session.execute(
            """
            SELECT id FROM patient.paciente WHERE rut = %s ALLOW FILTERING
            """, (receta["rut"])
        )
        id_cliente = result[0].id

    print("Hola " + str(id_cliente))
    session.execute(
        """
        INSERT INTO recets.recetas ("id", "id_paciente", "comentario", "farmacos", "doctor")
        VALUES (%s, %s, %s, %s, %s)
        """, (id_receta, id_cliente, receta["comentario"], receta["farmacos"], receta["doctor"])
    )

    id_receta = id_receta + 1

    return jsonify({"message": "ok"})

# EDITA RECETA
@app.route('/edit', methods=['POST'])
def edit():
    global id_paciente, id_receta
    receta = {
        "id": request.json['id'],
        "comentario": request.json['comentario'],
        "farmacos": request.json['farmacos'],
        "doctor": request.json['doctor']
    }

    session.execute(
        """
        UPDATE recets.recetas
        SET comentario = %s, farmacos = %s, doctor = %s
        WHERE id = %s
        """, (receta["comentario"], receta["farmacos"], receta["doctor"], receta["id"])
    )
    
    return jsonify({"message": "ok"})
    
# ELIMINA RECETA
@app.route('/delete', methods=['POST'])
def delete():
    global id_paciente, id_receta
    receta = {
        "id": request.json['id']
    }

    session.execute(
        """
        DELETE
        FROM recets.recetas
        WHERE id = %s
        """, (receta["id"])
    )

    return jsonify({"message": "ok"})

@app.route('/see_tables', methods=['POST'])
def see_tables():
    results = {
        "recetas": [],
        "pacientes": []
    }

    print("----------------RECETAS----------------")
    rows = session.execute('SELECT * FROM recets.recetas')

    for row in rows:
        results["recetas"].append(row)

    print("----------------PACIENTES----------------")
    rows = session.execute('SELECT * FROM patient.paciente')

    for row in rows:
        results["pacientes"].append(row)

    return jsonify(results)


# CONEXIÓN API A CLUSTER
session = connect_cluster()

if __name__ == '__main__':
    app.run(debug=True, port=5000)