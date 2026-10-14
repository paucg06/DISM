-- Script de creacion de BD y tablas para Sistema de Registro Horario
CREATE DATABASE IF NOT EXISTS `dism_registro` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `dism_registro`;

-- Tabla de ApiKey para seguridad optativa
DROP TABLE IF EXISTS `ApiKey`;
CREATE TABLE `ApiKey` (
  `idKey` INT AUTO_INCREMENT PRIMARY KEY,
  `Key` VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla de Trabajos
DROP TABLE IF EXISTS `Trabajos`;
CREATE TABLE `Trabajos` (
  `IdTrabajo` INT PRIMARY KEY,
  `Nombre` VARCHAR(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla de Usuarios
DROP TABLE IF EXISTS `Usuarios`;
CREATE TABLE `Usuarios` (
  `IdUsuario` INT PRIMARY KEY,
  `Nombre` VARCHAR(100) NOT NULL,
  `Usuario` VARCHAR(50) NOT NULL UNIQUE,
  `Clave` VARCHAR(50) NOT NULL,
  `Rol` VARCHAR(20) DEFAULT 'empleado' -- 'admin' o 'empleado'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla de Fichajes
DROP TABLE IF EXISTS `Fichajes`;
CREATE TABLE `Fichajes` (
  `IdFichaje` INT AUTO_INCREMENT PRIMARY KEY,
  `FechaHoraEntrada` DATETIME NOT NULL,
  `FechaHoraSalida` DATETIME DEFAULT NULL,
  `HorasTrabajadas` INT DEFAULT NULL,
  `IdTrabajo` INT NOT NULL,
  `IdUsuario` INT NOT NULL,
  `GeolocalizacionLatitud` FLOAT NOT NULL,
  `GeolocalizacionLongitud` FLOAT NOT NULL,
  CONSTRAINT `fk_fichaje_trabajo` FOREIGN KEY (`IdTrabajo`) REFERENCES `Trabajos` (`IdTrabajo`) ON DELETE CASCADE,
  CONSTRAINT `fk_fichaje_usuario` FOREIGN KEY (`IdUsuario`) REFERENCES `Usuarios` (`IdUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insercion de datos de prueba
INSERT INTO `ApiKey` (`idKey`, `Key`) VALUES
(1, 'dism-secret-key-2026');

INSERT INTO `Trabajos` (`IdTrabajo`, `Nombre`) VALUES
(1, 'Desarrollo Frontend Ionic'),
(2, 'Auditoría de Sistemas Móviles'),
(3, 'Mantenimiento Base de Datos MySQL'),
(4, 'Soporte y Atención al Cliente');

INSERT INTO `Usuarios` (`IdUsuario`, `Nombre`, `Usuario`, `Clave`, `Rol`) VALUES
(1, 'Administrador General', 'admin', 'admin123', 'admin'),
(2, 'Sergio Garcia', 'sergio', '1234', 'empleado'),
(3, 'Estela Martinez', 'estela', '1234', 'empleado'),
(4, 'Susana Gomez', 'susana', '1234', 'empleado'),
(5, 'Hugo Lopez', 'hugo', '1234', 'empleado');

-- Fichajes de ejemplo (Alicante y San Vicente del Raspeig)
INSERT INTO `Fichajes` (`IdFichaje`, `FechaHoraEntrada`, `FechaHoraSalida`, `HorasTrabajadas`, `IdTrabajo`, `IdUsuario`, `GeolocalizacionLatitud`, `GeolocalizacionLongitud`) VALUES
(1, '2026-10-14 08:30:00', '2026-10-14 16:30:00', 8, 1, 2, 38.38735, -0.51238),
(2, '2026-10-14 09:00:00', '2026-10-14 17:00:00', 8, 2, 3, 38.34599, -0.49068);
