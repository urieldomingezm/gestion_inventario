-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Servidor: db:3306
-- Tiempo de generación: 11-03-2025 a las 16:42:32
-- Versión del servidor: 8.0.41
-- Versión de PHP: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `hotel_inventario`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id` int NOT NULL,
  `nombre` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Laptop', 'Computadoras portátiles'),
(2, 'Monitor', 'Pantallas para computadoras'),
(3, 'Teclado', 'Dispositivos de entrada'),
(4, 'Mouse', 'Dispositivos de entrada'),
(5, 'Impresora', 'Equipos de impresión');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipos`
--

CREATE TABLE `equipos` (
  `id` int NOT NULL,
  `nombre` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_general_ci,
  `numero_serie` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `marca` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modelo` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `categoria_id` int DEFAULT NULL,
  `ubicacion_id` int DEFAULT NULL,
  `fecha_adquisicion` date DEFAULT NULL,
  `fecha_garantia` date DEFAULT NULL,
  `fecha_expericion` date DEFAULT NULL,
  `estado` enum('Operativo','En mantenimiento','Fuera de servicio','Descontinuado') COLLATE utf8mb4_general_ci DEFAULT 'Operativo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `equipos`
--

INSERT INTO `equipos` (`id`, `nombre`, `descripcion`, `numero_serie`, `marca`, `modelo`, `categoria_id`, `ubicacion_id`, `fecha_adquisicion`, `fecha_garantia`, `fecha_expericion`, `estado`) VALUES
(3, 'Prueba 23', 'Teclado inalámbrico', 'SN98765', 'Logitechq', 'K380', 3, 3, '2021-09-20', '2025-02-03', '2025-02-20', 'Operativo'),
(26, 'Laptop HP', 'Laptop de 15 pulgadas para oficina', 'SN12345', 'HP', 'Pavilion 15', 1, 1, '2023-06-10', '2025-02-19', '2025-02-28', 'Operativo'),
(36, 'Impresora HP LaserJet', 'Impresora láser monocromática', 'HP123456789', 'HP', 'LaserJet Pro M404dn', 1, 2, '2023-01-15', '2025-01-15', '2030-01-15', 'Operativo'),
(37, 'Laptop Dell XPS', 'Laptop de alto rendimiento', 'DELL987654321', 'Dell', 'XPS 15', 2, 3, '2022-05-20', '2024-05-20', '2028-05-20', 'Operativo'),
(38, 'Router Cisco', 'Router empresarial', 'CISCO19283746', 'Cisco', 'RV340', 3, 4, '2021-08-10', '2023-08-10', '2026-08-10', 'Operativo'),
(39, 'Monitor Samsung', 'Monitor LED de 24 pulgadas', 'SAMSUNG567890', 'Samsung', 'S24F350FHL', 4, 5, '2023-03-12', '2025-03-12', '2030-03-12', 'Operativo'),
(40, 'Servidor HP ProLiant', 'Servidor para base de datos', 'HPPL123456', 'HP', 'ProLiant DL380', 5, 1, '2020-11-25', '2023-11-25', '2027-11-25', 'En mantenimiento'),
(41, 'Escáner Epson', 'Escáner de documentos', 'EPSON654321', 'Epson', 'WorkForce DS-530', 5, 2, '2021-07-07', '2023-07-07', '2026-07-07', 'Operativo'),
(42, 'Proyector BenQ', 'Proyector HD', 'BENQ789654', 'BenQ', 'MW560', 4, 3, '2022-09-30', '2024-09-30', '2029-09-30', 'Operativo'),
(43, 'Disco Duro Externo', 'Disco duro de 2TB', 'WD123654789', 'Western Digital', 'Elements 2TB', 3, 4, '2022-12-05', '2024-12-05', '2027-12-05', 'Operativo'),
(44, 'Switch TP-Link', 'Switch de 24 puertos', 'TPLINK852741', 'TP-Link', 'TL-SG1024', 2, 5, '2023-04-18', '2025-04-18', '2028-04-18', 'Operativo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `login_usuarios`
--

CREATE TABLE `login_usuarios` (
  `id_usuario` int NOT NULL,
  `usuario_nombre` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `usuario_apellido` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `usuario_password` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `usuario_email` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `usuario_registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `login_usuarios`
--

INSERT INTO `login_usuarios` (`id_usuario`, `usuario_nombre`, `usuario_apellido`, `usuario_password`, `usuario_email`, `usuario_registro`) VALUES
(19, 'asda', 'asdas', '123456', 'uriel@gmail.com', '2025-03-11 15:40:53');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos`
--

CREATE TABLE `movimientos` (
  `id` int NOT NULL,
  `equipo_id` int NOT NULL,
  `tipo` enum('Asignación','Cambio de ubicación','Mantenimiento','Baja') COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_general_ci,
  `fecha_movimiento` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `usuario_responsable` varchar(150) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nueva_ubicacion_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `movimientos`
--

INSERT INTO `movimientos` (`id`, `equipo_id`, `tipo`, `descripcion`, `fecha_movimiento`, `usuario_responsable`, `nueva_ubicacion_id`) VALUES
(3, 3, 'Mantenimiento', 'Revisión de conectividad', '2025-02-06 18:49:37', 'Carlos López', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ubicaciones`
--

CREATE TABLE `ubicaciones` (
  `id` int NOT NULL,
  `nombre` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ubicaciones`
--

INSERT INTO `ubicaciones` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Oficina de computo', 'Ubicacion principal para todo el proceso'),
(2, 'Oficina B', 'Departamento de Contabilidad'),
(3, 'Bodega', 'Almacenamiento de equipos'),
(4, 'Sala de Servidores', 'Ubicación de los servidores principales'),
(5, 'Recepción', 'Área de atención al público');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `equipos`
--
ALTER TABLE `equipos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_serie` (`numero_serie`),
  ADD KEY `categoria_id` (`categoria_id`),
  ADD KEY `ubicacion_id` (`ubicacion_id`);

--
-- Indices de la tabla `login_usuarios`
--
ALTER TABLE `login_usuarios`
  ADD PRIMARY KEY (`id_usuario`);

--
-- Indices de la tabla `movimientos`
--
ALTER TABLE `movimientos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `equipo_id` (`equipo_id`),
  ADD KEY `nueva_ubicacion_id` (`nueva_ubicacion_id`);

--
-- Indices de la tabla `ubicaciones`
--
ALTER TABLE `ubicaciones`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `equipos`
--
ALTER TABLE `equipos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT de la tabla `login_usuarios`
--
ALTER TABLE `login_usuarios`
  MODIFY `id_usuario` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `movimientos`
--
ALTER TABLE `movimientos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `ubicaciones`
--
ALTER TABLE `ubicaciones`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `equipos`
--
ALTER TABLE `equipos`
  ADD CONSTRAINT `equipos_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `equipos_ibfk_2` FOREIGN KEY (`ubicacion_id`) REFERENCES `ubicaciones` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `movimientos`
--
ALTER TABLE `movimientos`
  ADD CONSTRAINT `movimientos_ibfk_1` FOREIGN KEY (`equipo_id`) REFERENCES `equipos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `movimientos_ibfk_2` FOREIGN KEY (`nueva_ubicacion_id`) REFERENCES `ubicaciones` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
