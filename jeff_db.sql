-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 10, 2022 at 03:26 PM
-- Server version: 8.0.27
-- PHP Version: 8.0.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `jeff_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `prefixes`
--

DROP TABLE IF EXISTS `prefixes`;
CREATE TABLE IF NOT EXISTS `prefixes` (
  `guild_id` varchar(150) NOT NULL,
  `guild_name` varchar(150) DEFAULT NULL,
  `guild_prefix` varchar(45) NOT NULL,
  PRIMARY KEY (`guild_id`),
  UNIQUE KEY `guild_id_UNIQUE` (`guild_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `prefixes`
--

INSERT INTO `prefixes` (`guild_id`, `guild_name`, `guild_prefix`) VALUES
('296015702891167744', 'DE JONGENS MET VLOTTE MONTUURTJES', '#'),
('706152322492923925', 'Bas\'s Depression Chamber', '//'),
('885427295152652289', 'Project', '#'),
('946439345320099841', 'Buurman en Buurman praatschuur', 'jeff');

-- --------------------------------------------------------

--
-- Table structure for table `user_chips`
--

DROP TABLE IF EXISTS `user_chips`;
CREATE TABLE IF NOT EXISTS `user_chips` (
  `user_id` int NOT NULL,
  `user_name` varchar(45) DEFAULT NULL,
  `user_chips` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
