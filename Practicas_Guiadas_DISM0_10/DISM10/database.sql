-- Script SQL para la creación de la BD DISM y tabla Usuarios (Ejercicio 10)
CREATE DATABASE IF NOT EXISTS `dism` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `dism`;

DROP TABLE IF EXISTS `usuarios`;

CREATE TABLE `usuarios` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `edad` VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `edad`) VALUES
(1, 'Sergio', 'sergio@ua.es', '20'),
(2, 'Estela', 'estela@ua.es', '19'),
(3, 'Susana', 'susana@ua.es', '27'),
(4, 'Hugo', 'hugo@ua.es', '21');
