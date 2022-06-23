-- Create a keyspace
CREATE KEYSPACE IF NOT EXISTS recets WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '2' };

-- Create a table
CREATE TABLE IF NOT EXISTS recets.recetas (
    id int PRIMARY KEY,
    id_paciente int,
    comentario text,
    farmacos text,
    doctor text
);

-- Create a keyspace
CREATE KEYSPACE IF NOT EXISTS patient WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '3' };

-- Create a table
CREATE TABLE IF NOT EXISTS patient.paciente (
    id int PRIMARY KEY,
    nombre text,
    apellido text,
    rut text,
    email text,
    fecha_nacimiento text
);