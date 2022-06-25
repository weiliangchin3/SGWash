-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 13, 2021 at 02:32 PM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `customer`
--
CREATE DATABASE IF NOT EXISTS `customer` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `customer`;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `custID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `mobile` char(8) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `vType` varchar(255) NOT NULL,
  `carplate` varchar(255) NOT NULL,
  `verified` tinyint(1) NOT NULL DEFAULT '0',
  `bookingStatus` varchar(255) NOT NULL DEFAULT 'Available',
  `TelegramID` varchar(255) NOT NULL,
  PRIMARY KEY (`custID`)
) ENGINE=MyISAM AUTO_INCREMENT=5716 DEFAULT CHARSET=utf8;
--
-- Database: `jobrequest`
--
CREATE DATABASE IF NOT EXISTS `jobrequest` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `jobrequest`;

-- --------------------------------------------------------

--
-- Table structure for table `job_request`
--

DROP TABLE IF EXISTS `job_request`;
CREATE TABLE IF NOT EXISTS `job_request` (
  `recordID` int(11) NOT NULL AUTO_INCREMENT,
  `custID` int(11) NOT NULL,
  `vAddress` varchar(255) NOT NULL,
  `postal` varchar(6) NOT NULL,
  `description` varchar(255) NOT NULL,
  `bookingType` varchar(255) NOT NULL,
  `serviceType` varchar(255) NOT NULL,
  `cost` decimal(5,2) NOT NULL,
  `bookDatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `washerID` int(11) DEFAULT NULL,
  `status` varchar(255) NOT NULL DEFAULT 'open',
  `receiptID` varchar(255) NOT NULL,
  `carplate` varchar(255) NOT NULL,
  PRIMARY KEY (`recordID`)
) ENGINE=MyISAM AUTO_INCREMENT=177 DEFAULT CHARSET=utf8;
--
-- Database: `ticket`
--
CREATE DATABASE IF NOT EXISTS `ticket` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `ticket`;

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
CREATE TABLE IF NOT EXISTS `ticket` (
  `tixID` int(1) DEFAULT NULL,
  `custID` int(1) DEFAULT NULL,
  `recordID` int(1) DEFAULT NULL,
  `date_submit` varchar(10) DEFAULT NULL,
  `time_submit` varchar(5) DEFAULT NULL,
  `receiptID` varchar(27) DEFAULT NULL,
  `description` varchar(19) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `image_URL` varchar(255) DEFAULT NULL,
  `amount` int(1) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`tixID`, `custID`, `recordID`, `date_submit`, `time_submit`, `receiptID`, `description`, `status`, `image_URL`, `amount`) VALUES
(2, 1, 2, '20/03/2021', '14:00', 'ch_1IfPDNImR2bGEHhXJNUvmhOj', 'scratched bonnet', 'open', 'https://firebasestorage.googleapis.com/v0/b/fil-flutter-f31f2.appspot.com/o/ticketImages%2F20032021-1400-1.jpeg?alt=media&token=a069f12e-ec25-44f2-8616-4e7652f49c05', 6),
(3, 2, 3, '20/03/2021', '15:00', 'ch_1IcZIiImR2bGEHhXxJoSljdc', 'broken side mirrors', 'open', 'https://firebasestorage.googleapis.com/v0/b/fil-flutter-f31f2.appspot.com/o/ticketImages%2F20032021-1500-2.jpeg?alt=media&token=47c20393-0ff5-4fe9-9e7d-48a6f963e4b2', 9),
(4, 3, 4, '20/03/2021', '13:05', 'ch_1IcY0WImR2bGEHhX7KMw72r6', 'scratched door', 'open', 'https://firebasestorage.googleapis.com/v0/b/fil-flutter-f31f2.appspot.com/o/ticketImages%2F20032021-1305-3.jpeg?alt=media&token=21499f0b-b6e8-428b-a1f0-87f0392a60b8', 9),
(5, 4, 5, '20/03/2021', '12:00', 'ch_1IfP8xImR2bGEHhXU78bCvJd', 'broken windshield', 'open', 'https://firebasestorage.googleapis.com/v0/b/fil-flutter-f31f2.appspot.com/o/ticketImages%2F20032021-1200-4.jpeg?alt=media&token=cb25c5d8-3ed4-44aa-ba06-944ef914b9cf', 6),
(6, 5, 6, '20/03/2021', '16:00', 'ch_1Iec2IImR2bGEHhXJn57GRjq', 'broken headlights', 'open', 'https://firebasestorage.googleapis.com/v0/b/fil-flutter-f31f2.appspot.com/o/ticketImages%2F20032021-1600-5.jpeg?alt=media&token=fef5695b-bd39-4dbf-b986-bc3e413f7e0d', 9);
--
-- Database: `washer`
--
CREATE DATABASE IF NOT EXISTS `washer` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `washer`;

-- --------------------------------------------------------

--
-- Table structure for table `washer`
--

DROP TABLE IF EXISTS `washer`;
CREATE TABLE IF NOT EXISTS `washer` (
  `washerID` int(255) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `mobile` char(10) NOT NULL,
  `numWashes` int(5) NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`washerID`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `washer`
--

INSERT INTO `washer` (`washerID`, `name`, `email`, `password`, `mobile`, `numWashes`, `status`) VALUES
(1, 'john', 'john@gmail.com', '123', '56748567', 62, 'available'),
(2, 'may', 'may@gmail.com', '345', '89675931', 15, 'available');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
