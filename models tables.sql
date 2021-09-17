create database biblioteca_flask;
use biblioteca_flask;

CREATE TABLE Libros (
id INT(6) AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
autor VARCHAR(100) NOT NULL,
disponibilidad boolean
);

CREATE TABLE Usuarios (
id INT(6) AUTO_INCREMENT PRIMARY KEY,
nombre_completo VARCHAR(100) NOT NULL,
libros_en_uso VARCHAR(100) NOT NULL
);

CREATE TABLE prestamos (
id Int(6) PRIMARY KEY,
id_libro Int(6),
id_usuario Int(6),
nombre_libro VARCHAR(100) NOT NULL,
nombrecompleto_usuario VARCHAR(100) NOT NULL
);