-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Sep 13, 2018 at 01:11 PM
-- Server version: 5.7.23-0ubuntu0.18.04.1
-- PHP Version: 7.2.7-0ubuntu0.18.04.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inventory_management`
--

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

CREATE TABLE `location` (
  `location_id` int(11) NOT NULL,
  `location_name` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `location`
--

INSERT INTO `location` (`location_id`, `location_name`) VALUES
(1, 'Mumbai'),
(2, 'Delhi'),
(3, 'New_Delhi'),
(4, 'Chennai'),
(5, 'Bangalore'),
(6, 'Hyderabad'),
(7, 'Kolkata'),
(8, 'Ahmedabad'),
(11, 'Mirzapur'),
(12, 'Nagpur'),
(13, 'Pune'),
(19, 'Navi_Mumbai'),
(21, 'Kundapura'),
(22, 'Kozhikode');

-- --------------------------------------------------------

--
-- Table structure for table `locationinventory`
--

CREATE TABLE `locationinventory` (
  `locationinventory_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `Mumbai` int(11) DEFAULT '0',
  `Delhi` int(11) DEFAULT '0',
  `New_Delhi` int(11) DEFAULT '0',
  `Chennai` int(11) DEFAULT '0',
  `Bangalore` int(11) DEFAULT '0',
  `Hyderabad` int(11) DEFAULT '0',
  `Kolkata` int(11) DEFAULT '0',
  `Ahmedabad` int(11) DEFAULT '0',
  `Mirzapur` int(11) DEFAULT '0',
  `Nagpur` int(11) DEFAULT '0',
  `Pune` int(11) DEFAULT '0',
  `Navi_Mumbai` int(11) DEFAULT '0',
  `Kundapura` int(11) DEFAULT '0',
  `Kozhikode` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `locationinventory`
--

INSERT INTO `locationinventory` (`locationinventory_id`, `user_id`, `Mumbai`, `Delhi`, `New_Delhi`, `Chennai`, `Bangalore`, `Hyderabad`, `Kolkata`, `Ahmedabad`, `Mirzapur`, `Nagpur`, `Pune`, `Navi_Mumbai`, `Kundapura`, `Kozhikode`) VALUES
(1, 1, 0, 0, 65, 78, 1465, 0, 152, 0, 0, 0, 0, 0, 0, 0),
(2, 1, 37, 6, 489, 1, 6, 5, 0, 5, 0, 0, 5, 0, 0, 15),
(3, 1, 5, 3, 1, 3, 3, 3, 3, 3, 52, 6, 489, 1, 6, 5),
(4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(5, 1, 15, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(7, 1, 48, 52, 6, 475, 1, 6, 5, 0, 5, 0, 0, 5, 0, 0),
(8, 1, 46, 46, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(9, 1, 13, 12, 12, 12, 12, 12, 12, 12, 0, 0, 0, 0, 0, 0),
(10, 1, 20, 20, 20, 20, 20, 20, 20, 20, 0, 0, 0, 0, 0, 0),
(11, 2, 12, 12, 12, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(12, 2, 12, 12, 12, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(13, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(14, 2, 212, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(15, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(16, 2, 456, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(17, 2, 456, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `product_id` int(11) NOT NULL,
  `product_name` varchar(60) NOT NULL,
  `product_quantity` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`product_id`, `product_name`, `product_quantity`, `user_id`) VALUES
(1, 'Product 1', 1760, 1),
(2, 'Product 2', 569, 1),
(3, 'Product 3', 583, 1),
(4, 'Product 4', 0, 1),
(5, 'Product 5', 45, 1),
(6, 'Product 6', 0, 1),
(7, 'Product 7', 597, 1),
(8, 'Product 8', 92, 1),
(9, 'Product 9', 97, 1),
(10, 'Product 10', 160, 1),
(11, 'Product 11', 60, 2),
(12, 'Product 12', 60, 2),
(13, 'Product 13', 0, 2),
(14, 'Product 14', 224, 2),
(15, 'Product 15', 2, 2),
(16, 'Product 16', 456, 2),
(17, 'Product 17', 461, 2);

-- --------------------------------------------------------

--
-- Table structure for table `productmovement`
--

CREATE TABLE `productmovement` (
  `productmovement_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `product_name` varchar(60) NOT NULL,
  `from_location_name` varchar(60) NOT NULL,
  `to_location_name` varchar(60) NOT NULL,
  `product_quantity` int(11) NOT NULL,
  `timestamp` date NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `productmovement`
--

INSERT INTO `productmovement` (`productmovement_id`, `product_id`, `product_name`, `from_location_name`, `to_location_name`, `product_quantity`, `timestamp`, `user_id`) VALUES
(1, 3, 'Product 3', 'New_Delhi', 'Mumbai', 2, '2018-09-13', 1),
(3, 7, 'Product 7', 'Chennai', 'Mumbai', 14, '2018-09-13', 1),
(5, 5, 'Product 5', 'Delhi', 'Mumbai', 15, '2018-09-13', 1),
(7, 2, 'Product 2', 'Mumbai', 'Kozhikode', 15, '2018-09-13', 1);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `user_email` varchar(60) NOT NULL,
  `user_password` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `user_name`, `user_email`, `user_password`) VALUES
(1, 'himanshu', 'himanshuwarekar@yahoo.com', '$2b$12$IjFgSnAJCdxQrksUSbTq9Oox7YzBx4Q0WdcRM3FJaLP5CAJ4H9O8i');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `location`
--
ALTER TABLE `location`
  ADD PRIMARY KEY (`location_id`);

--
-- Indexes for table `locationinventory`
--
ALTER TABLE `locationinventory`
  ADD PRIMARY KEY (`locationinventory_id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `productmovement`
--
ALTER TABLE `productmovement`
  ADD PRIMARY KEY (`productmovement_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `location`
--
ALTER TABLE `location`
  MODIFY `location_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;
--
-- AUTO_INCREMENT for table `locationinventory`
--
ALTER TABLE `locationinventory`
  MODIFY `locationinventory_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
--
-- AUTO_INCREMENT for table `productmovement`
--
ALTER TABLE `productmovement`
  MODIFY `productmovement_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
