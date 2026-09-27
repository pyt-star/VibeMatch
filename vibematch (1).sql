-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 21, 2026 at 02:12 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vibematch`
--

-- --------------------------------------------------------

--
-- Table structure for table `active_sessions`
--

CREATE TABLE `active_sessions` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `login_time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `active_sessions`
--

INSERT INTO `active_sessions` (`id`, `username`, `login_time`) VALUES
(2, 'devam123', '2026-04-20 12:44:58');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `username` varchar(15) NOT NULL,
  `password` varchar(15) NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`username`, `password`, `email`) VALUES
('manish', '12345', ''),
('devam123', '12345', 'devampithadia13@gmail.com'),
('manish', 'manish123', 'devampithadia13@gmail.com'),
('devam2', '12345', 'devampithadia13@gmail.com'),
('devam2', '12345', 'devampithadia13@gmail.com'),
('devam2', '12345', 'devampithadia13@gmail.com'),
('jal', '12345', 'jalajhmehta@gmail.com'),
('TinyKing', 'raj12345', 'rajchudasama2008@gmail.com'),
('rajmakwana', 'raj12345', 'raj@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE `sessions` (
  `session_id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `start_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `final_sentiment` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sessions`
--

INSERT INTO `sessions` (`session_id`, `username`, `start_time`, `final_sentiment`) VALUES
(1, 'devam123', '2026-04-21 05:32:35', 'Negative'),
(2, 'devam123', '2026-04-21 05:34:03', 'Positive'),
(3, 'devam123', '2026-04-21 08:43:38', NULL),
(4, 'devam123', '2026-04-21 08:47:36', NULL),
(5, 'devam123', '2026-04-21 08:48:05', NULL),
(6, 'devam123', '2026-04-21 08:50:30', NULL),
(7, 'devam123', '2026-04-21 08:51:03', NULL),
(8, 'devam123', '2026-04-21 08:51:59', NULL),
(9, 'devam123', '2026-04-21 08:52:19', NULL),
(10, 'devam123', '2026-04-21 08:52:36', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `session_responses`
--

CREATE TABLE `session_responses` (
  `id` int(11) NOT NULL,
  `session_id` int(11) DEFAULT NULL,
  `question` text DEFAULT NULL,
  `response` text DEFAULT NULL,
  `sentiment` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `session_responses`
--

INSERT INTO `session_responses` (`id`, `session_id`, `question`, `response`, `sentiment`) VALUES
(1, 1, 'How has your day been going so far?', 'it is going good', 'Positive'),
(2, 1, 'What made you feel the happiest today?', 'when i ate burger', 'Neutral'),
(3, 1, 'Did anything stress or bother you today?', 'my marks did bothered me', 'Negative'),
(4, 1, 'How are you feeling right now?', 'i am feeling low', 'Negative'),
(5, 1, 'How would you describe your day in one sentence?', 'it is going boring', 'Negative'),
(6, 2, 'How has your day been going so far?', 'is going my day is going good', 'Positive'),
(7, 2, 'What made you feel the happiest today?', 'when I received my cloud computing marks', 'Neutral'),
(8, 2, 'Did anything stress or bother you today?', 'i scored low in machine learning', 'Negative'),
(9, 2, 'How are you feeling right now?', 'i am feeling okay', 'Positive'),
(10, 2, 'How would you describe your day in one sentence?', 'it is going good', 'Positive');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `active_sessions`
--
ALTER TABLE `active_sessions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`session_id`);

--
-- Indexes for table `session_responses`
--
ALTER TABLE `session_responses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `session_id` (`session_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `active_sessions`
--
ALTER TABLE `active_sessions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `sessions`
--
ALTER TABLE `sessions`
  MODIFY `session_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `session_responses`
--
ALTER TABLE `session_responses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `session_responses`
--
ALTER TABLE `session_responses`
  ADD CONSTRAINT `session_responses_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `sessions` (`session_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
