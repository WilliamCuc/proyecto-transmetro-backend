-- Base de datos
CREATE DATABASE transmetro;
USE transmetro;

-- Tabla usuarios
CREATE TABLE usuarios (
  id_usuario INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100),
  apellido VARCHAR(100),
  correo VARCHAR(100),
  contrasena VARCHAR(255),
  rol INT,
  estado BOOLEAN
);

-- Tabla roles
CREATE TABLE roles (
  id_rol INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(50)
);

-- Tabla permisos
CREATE TABLE permisos (
  id_permiso INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100),
  descripcion TEXT
);

-- Tabla roles_permisos
CREATE TABLE roles_permisos (
  id_rol INT,
  id_permiso INT
);

-- Tabla usuarios_roles
CREATE TABLE usuarios_roles (
  id_usuario INT,
  id_rol INT
);

-- Tabla departamentos
CREATE TABLE departamentos (
  id_departamento INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100)
);

-- Tabla municipios
CREATE TABLE municipios (
  id_municipio INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100),
  id_departamento INT
);

-- Tabla estaciones
CREATE TABLE estaciones (
  id_estacion INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100),
  ubicacion TEXT,
  id_municipio INT
);

-- Tabla accesos
CREATE TABLE accesos (
  id_acceso INT PRIMARY KEY AUTO_INCREMENT,
  descripcion VARCHAR(100),
  id_estacion INT
);

-- Tabla guardias
CREATE TABLE guardias (
  id_guardia INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100),
  id_acceso INT
);

-- Tabla parqueos
CREATE TABLE parqueos (
  id_parqueo INT PRIMARY KEY AUTO_INCREMENT,
  id_estacion INT
);

-- Tabla buses
CREATE TABLE buses (
  id_bus INT PRIMARY KEY AUTO_INCREMENT,
  numero_bus VARCHAR(10),
  capacidad INT,
  estado ENUM('activo', 'mantenimiento', 'fuera de servicio'),
  id_parqueo INT
);

-- Tabla pilotos
CREATE TABLE pilotos (
  id_piloto INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100),
  historial_educativo TEXT,
  direccion TEXT,
  telefono VARCHAR(20),
  id_bus INT
);

-- Tabla lineas
CREATE TABLE lineas (
  id_linea INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100),
  distancia_total DECIMAL(10,2)
);

-- Tabla estaciones_lineas
CREATE TABLE estaciones_lineas (
  id_estacion INT,
  id_linea INT
);

-- Tabla rutas
CREATE TABLE rutas (
  id_ruta INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100),
  descripcion TEXT,
  id_linea INT
);

-- Tabla horarios
CREATE TABLE horarios (
  id_horario INT PRIMARY KEY AUTO_INCREMENT,
  id_ruta INT,
  hora_salida TIME,
  hora_llegada TIME
);

-- Tabla boletos
CREATE TABLE boletos (
  id_boleto INT PRIMARY KEY AUTO_INCREMENT,
  id_usuario INT,
  id_ruta INT,
  fecha_compra DATETIME,
  precio DECIMAL(10,2)
);

-- Tabla viajes
CREATE TABLE viajes (
  id_viaje INT PRIMARY KEY AUTO_INCREMENT,
  id_bus INT,
  id_ruta INT,
  id_horario INT,
  fecha DATE,
  estado ENUM('pendiente', 'en curso', 'finalizado')
);

-- Tabla paradas
CREATE TABLE paradas (
  id_parada INT PRIMARY KEY AUTO_INCREMENT,
  id_ruta INT,
  id_estacion INT,
  orden INT
);

-- Tabla distancias_estaciones
CREATE TABLE distancias_estaciones (
  id_origen INT,
  id_destino INT,
  distancia_km DECIMAL(5,2)
);

-- Tabla alertas
CREATE TABLE alertas (
  id_alerta INT PRIMARY KEY AUTO_INCREMENT,
  id_bus INT,
  id_estacion INT,
  tipo ENUM('sobrecupo', 'baja_ocupacion'),
  fecha_hora DATETIME
);

-- Restricción unique para correo en usuarios
ALTER TABLE usuarios
ADD CONSTRAINT uk_usuarios_correo UNIQUE (correo);

-- Restricción unique para numero_bus en buses
ALTER TABLE buses
ADD CONSTRAINT uk_buses_numero_bus UNIQUE (numero_bus);

-- Foreign keys para roles_permisos
ALTER TABLE roles_permisos
ADD CONSTRAINT fk_roles_permisos_rol FOREIGN KEY (id_rol) REFERENCES roles(id_rol),
ADD CONSTRAINT fk_roles_permisos_permiso FOREIGN KEY (id_permiso) REFERENCES permisos(id_permiso);

-- Foreign keys para usuarios_roles
ALTER TABLE usuarios_roles
ADD CONSTRAINT fk_usuarios_roles_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
ADD CONSTRAINT fk_usuarios_roles_rol FOREIGN KEY (id_rol) REFERENCES roles(id_rol);

-- Foreign key para municipios
ALTER TABLE municipios
ADD CONSTRAINT fk_municipios_departamento FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento);

-- Foreign key para estaciones
ALTER TABLE estaciones
ADD CONSTRAINT fk_estaciones_municipio FOREIGN KEY (id_municipio) REFERENCES municipios(id_municipio);

-- Foreign key para accesos
ALTER TABLE accesos
ADD CONSTRAINT fk_accesos_estacion FOREIGN KEY (id_estacion) REFERENCES estaciones(id_estacion);

-- Foreign key para guardias
ALTER TABLE guardias
ADD CONSTRAINT fk_guardias_acceso FOREIGN KEY (id_acceso) REFERENCES accesos(id_acceso);

-- Foreign key para parqueos
ALTER TABLE parqueos
ADD CONSTRAINT fk_parqueos_estacion FOREIGN KEY (id_estacion) REFERENCES estaciones(id_estacion);

-- Foreign key para buses
ALTER TABLE buses
ADD CONSTRAINT fk_buses_parqueo FOREIGN KEY (id_parqueo) REFERENCES parqueos(id_parqueo);

-- Foreign key para pilotos
ALTER TABLE pilotos
ADD CONSTRAINT fk_pilotos_bus FOREIGN KEY (id_bus) REFERENCES buses(id_bus);

-- Foreign keys para estaciones_lineas
ALTER TABLE estaciones_lineas
ADD CONSTRAINT fk_estaciones_lineas_estacion FOREIGN KEY (id_estacion) REFERENCES estaciones(id_estacion),
ADD CONSTRAINT fk_estaciones_lineas_linea FOREIGN KEY (id_linea) REFERENCES lineas(id_linea);

-- Foreign key para rutas
ALTER TABLE rutas
ADD CONSTRAINT fk_rutas_linea FOREIGN KEY (id_linea) REFERENCES lineas(id_linea);

-- Foreign key para horarios
ALTER TABLE horarios
ADD CONSTRAINT fk_horarios_ruta FOREIGN KEY (id_ruta) REFERENCES rutas(id_ruta);

-- Foreign keys para boletos
ALTER TABLE boletos
ADD CONSTRAINT fk_boletos_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
ADD CONSTRAINT fk_boletos_ruta FOREIGN KEY (id_ruta) REFERENCES rutas(id_ruta);

-- Foreign keys para viajes
ALTER TABLE viajes
ADD CONSTRAINT fk_viajes_bus FOREIGN KEY (id_bus) REFERENCES buses(id_bus),
ADD CONSTRAINT fk_viajes_ruta FOREIGN KEY (id_ruta) REFERENCES rutas(id_ruta),
ADD CONSTRAINT fk_viajes_horario FOREIGN KEY (id_horario) REFERENCES horarios(id_horario);

-- Foreign keys para paradas
ALTER TABLE paradas
ADD CONSTRAINT fk_paradas_ruta FOREIGN KEY (id_ruta) REFERENCES rutas(id_ruta),
ADD CONSTRAINT fk_paradas_estacion FOREIGN KEY (id_estacion) REFERENCES estaciones(id_estacion);

-- Foreign keys para distancias_estaciones
ALTER TABLE distancias_estaciones
ADD CONSTRAINT fk_distancias_origen FOREIGN KEY (id_origen) REFERENCES estaciones(id_estacion),
ADD CONSTRAINT fk_distancias_destino FOREIGN KEY (id_destino) REFERENCES estaciones(id_estacion);

-- Foreign keys para alertas
ALTER TABLE alertas
ADD CONSTRAINT fk_alertas_bus FOREIGN KEY (id_bus) REFERENCES buses(id_bus),
ADD CONSTRAINT fk_alertas_estacion FOREIGN KEY (id_estacion) REFERENCES estaciones(id_estacion);