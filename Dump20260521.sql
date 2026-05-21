CREATE DATABASE  IF NOT EXISTS `ev_charging_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ev_charging_db`;
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: ev_charging_db
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `BookingID` int NOT NULL,
  `BookingDate` date DEFAULT NULL,
  `ChargingDuration` int DEFAULT NULL,
  `ArrivalStatus` varchar(20) DEFAULT NULL,
  `VehicleID` int DEFAULT NULL,
  `SlotID` int DEFAULT NULL,
  PRIMARY KEY (`BookingID`),
  KEY `idx_booking_vehicle` (`VehicleID`),
  KEY `idx_booking_slot` (`SlotID`),
  CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`VehicleID`) REFERENCES `vehicle` (`VehicleID`),
  CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`SlotID`) REFERENCES `charging_slot` (`SlotID`),
  CONSTRAINT `booking_chk_1` CHECK ((`ChargingDuration` > 0)),
  CONSTRAINT `booking_chk_2` CHECK ((`ArrivalStatus` in (_utf8mb4'Arrived',_utf8mb4'No-Show')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` VALUES (401,'2026-01-09',60,'Arrived',101,301),(402,'2026-01-09',90,'Arrived',102,302),(410,'2026-01-17',60,'Arrived',106,303),(411,'2026-01-11',60,'Arrived',103,305),(412,'2026-01-11',90,'Arrived',105,306),(413,'2026-01-12',60,'Arrived',107,307),(414,'2026-01-12',60,'No-Show',108,308),(415,'2026-04-08',60,'Arrived',101,309),(416,'2026-04-17',2,'Arrived',101,309),(417,'2026-04-16',1,'Arrived',101,310);
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `check_slot_availability` BEFORE INSERT ON `booking` FOR EACH ROW BEGIN

DECLARE slot_status VARCHAR(20);

SELECT SlotStatus INTO slot_status
FROM CHARGING_SLOT
WHERE SlotID = NEW.SlotID;

IF slot_status = 'Booked' THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Error: Slot already booked';
END IF;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `charging_operator`
--

DROP TABLE IF EXISTS `charging_operator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `charging_operator` (
  `OperatorID` int NOT NULL,
  `OperatorName` varchar(100) NOT NULL,
  `ContactDetails` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`OperatorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `charging_operator`
--

LOCK TABLES `charging_operator` WRITE;
/*!40000 ALTER TABLE `charging_operator` DISABLE KEYS */;
INSERT INTO `charging_operator` VALUES (1,'EV Power Ltd','contact@evpower.com'),(2,'ChargeGrid India','support@chargegrid.com');
/*!40000 ALTER TABLE `charging_operator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `charging_slot`
--

DROP TABLE IF EXISTS `charging_slot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `charging_slot` (
  `SlotID` int NOT NULL,
  `ConnectorType` varchar(50) DEFAULT NULL,
  `StartTime` datetime DEFAULT NULL,
  `EndTime` datetime DEFAULT NULL,
  `SlotStatus` varchar(20) DEFAULT NULL,
  `StationID` int DEFAULT NULL,
  PRIMARY KEY (`SlotID`),
  KEY `StationID` (`StationID`),
  CONSTRAINT `charging_slot_ibfk_1` FOREIGN KEY (`StationID`) REFERENCES `charging_station` (`StationID`),
  CONSTRAINT `charging_slot_chk_1` CHECK ((`SlotStatus` in (_utf8mb4'Available',_utf8mb4'Booked')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `charging_slot`
--

LOCK TABLES `charging_slot` WRITE;
/*!40000 ALTER TABLE `charging_slot` DISABLE KEYS */;
INSERT INTO `charging_slot` VALUES (301,'Type-2','2026-01-10 10:00:00','2026-01-10 11:00:00','Booked',201),(302,'CCS','2026-01-10 11:00:00','2026-01-10 12:00:00','Booked',202),(303,'Fast','2026-01-20 10:00:00','2026-01-20 11:00:00','Booked',203),(305,'Type-2','2026-01-11 10:00:00','2026-01-11 11:00:00','Booked',201),(306,'CCS','2026-01-11 11:00:00','2026-01-11 12:30:00','Booked',201),(307,'Type-2','2026-01-12 09:00:00','2026-01-12 10:00:00','Booked',202),(308,'Fast','2026-01-12 10:00:00','2026-01-12 11:00:00','Available',202),(309,'CCS','2026-01-18 09:00:00','2026-01-18 10:30:00','Available',203),(310,'Fast','2026-01-18 10:30:00','2026-01-18 11:30:00','Available',203);
/*!40000 ALTER TABLE `charging_slot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `charging_station`
--

DROP TABLE IF EXISTS `charging_station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `charging_station` (
  `StationID` int NOT NULL,
  `StationName` varchar(100) DEFAULT NULL,
  `City` varchar(50) DEFAULT NULL,
  `Location` varchar(100) DEFAULT NULL,
  `MaxPowerCapacity` int DEFAULT NULL,
  `ThresholdPower` int DEFAULT NULL,
  `OperatorID` int DEFAULT NULL,
  PRIMARY KEY (`StationID`),
  KEY `OperatorID` (`OperatorID`),
  KEY `idx_station_city` (`City`),
  CONSTRAINT `charging_station_ibfk_1` FOREIGN KEY (`OperatorID`) REFERENCES `charging_operator` (`OperatorID`),
  CONSTRAINT `charging_station_chk_1` CHECK ((`MaxPowerCapacity` > 0)),
  CONSTRAINT `charging_station_chk_2` CHECK ((`ThresholdPower` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `charging_station`
--

LOCK TABLES `charging_station` WRITE;
/*!40000 ALTER TABLE `charging_station` DISABLE KEYS */;
INSERT INTO `charging_station` VALUES (201,'DelhiEVCharge Station','Delhi','Connaught Place',500,100,1),(202,'MumbaiEVCharge Station','Mumbai','Andheri East',600,150,1),(203,'BangaloreCharge Hub','Bangalore','Indiranagar',550,120,2);
/*!40000 ALTER TABLE `charging_station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ev_owner`
--

DROP TABLE IF EXISTS `ev_owner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ev_owner` (
  `OwnerID` int NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Phone` varchar(15) NOT NULL,
  `City` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`OwnerID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ev_owner`
--

LOCK TABLES `ev_owner` WRITE;
/*!40000 ALTER TABLE `ev_owner` DISABLE KEYS */;
INSERT INTO `ev_owner` VALUES (1,'Armaan Malik','armaan@gmail.com','9876543210','Delhi'),(2,'Neha Sharma','neha@gmail.com','9123456780','Mumbai'),(3,'Vk','idk@gmail.com','9810348102','Blr'),(4,'Rahul Mehta','rahul@gmail.com','9876501234','Delhi'),(5,'Priya Singh','priya@gmail.com','9812345678','Mumbai');
/*!40000 ALTER TABLE `ev_owner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grid_authority`
--

DROP TABLE IF EXISTS `grid_authority`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grid_authority` (
  `GridID` int NOT NULL,
  `AuthorityName` varchar(100) DEFAULT NULL,
  `Region` varchar(50) DEFAULT NULL,
  `ContactInfo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`GridID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grid_authority`
--

LOCK TABLES `grid_authority` WRITE;
/*!40000 ALTER TABLE `grid_authority` DISABLE KEYS */;
INSERT INTO `grid_authority` VALUES (1,'National Power Grid','North','grid@power.gov'),(2,'South Power Grid','South','southgrid@power.gov');
/*!40000 ALTER TABLE `grid_authority` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintenance_request`
--

DROP TABLE IF EXISTS `maintenance_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maintenance_request` (
  `RequestID` int NOT NULL,
  `RequestDate` date DEFAULT NULL,
  `RequestType` varchar(50) DEFAULT NULL,
  `ApprovalStatus` varchar(20) DEFAULT NULL,
  `StationID` int DEFAULT NULL,
  `VendorID` int DEFAULT NULL,
  PRIMARY KEY (`RequestID`),
  KEY `StationID` (`StationID`),
  KEY `VendorID` (`VendorID`),
  CONSTRAINT `maintenance_request_ibfk_1` FOREIGN KEY (`StationID`) REFERENCES `charging_station` (`StationID`),
  CONSTRAINT `maintenance_request_ibfk_2` FOREIGN KEY (`VendorID`) REFERENCES `vendor` (`VendorID`),
  CONSTRAINT `maintenance_request_chk_1` CHECK ((`ApprovalStatus` in (_utf8mb4'Pending',_utf8mb4'Approved',_utf8mb4'Rejected')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenance_request`
--

LOCK TABLES `maintenance_request` WRITE;
/*!40000 ALTER TABLE `maintenance_request` DISABLE KEYS */;
INSERT INTO `maintenance_request` VALUES (801,'2026-01-08','Charger Repair','Approved',201,701),(802,'2026-01-10','Routine Check','Approved',202,702),(803,'2026-01-12','Connector Issue','Rejected',203,703),(804,'2026-01-15','Software Update','Approved',201,702),(805,'2026-04-07','Routine Check','Pending',201,703);
/*!40000 ALTER TABLE `maintenance_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `PaymentID` int NOT NULL,
  `EnergyConsumed` int DEFAULT NULL,
  `Amount` decimal(10,2) DEFAULT NULL,
  `PaymentStatus` varchar(20) DEFAULT NULL,
  `PaymentTime` datetime DEFAULT NULL,
  `BookingID` int DEFAULT NULL,
  PRIMARY KEY (`PaymentID`),
  UNIQUE KEY `BookingID` (`BookingID`),
  KEY `idx_payment_status` (`PaymentStatus`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`BookingID`) REFERENCES `booking` (`BookingID`),
  CONSTRAINT `payment_chk_1` CHECK ((`EnergyConsumed` >= 0)),
  CONSTRAINT `payment_chk_2` CHECK ((`Amount` >= 0)),
  CONSTRAINT `payment_chk_3` CHECK ((`PaymentStatus` in (_utf8mb4'Success',_utf8mb4'Failure')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (501,20,400.00,'Success','2026-01-10 11:05:00',401),(502,25,500.00,'Success','2026-04-05 02:04:57',411),(503,30,600.00,'Success','2026-04-05 02:04:57',412),(504,20,400.00,'Success','2026-04-05 02:04:57',413),(505,28,560.00,'Success','2026-04-05 16:23:12',410),(506,24,480.00,'Success','2026-04-05 17:09:08',402),(507,20,400.00,'Success','2026-04-08 20:35:04',415),(508,50,1000.00,'Success','2026-04-17 05:22:57',414),(509,50,1000.00,'Success','2026-04-17 05:41:26',416),(510,50,1000.00,'Success','2026-04-17 06:10:11',417);
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `power_allocation`
--

DROP TABLE IF EXISTS `power_allocation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `power_allocation` (
  `AllocationID` int NOT NULL,
  `AllocatedPower` int DEFAULT NULL,
  `AvailablePower` int DEFAULT NULL,
  `LastUpdated` datetime DEFAULT NULL,
  `StationID` int DEFAULT NULL,
  `GridID` int DEFAULT NULL,
  PRIMARY KEY (`AllocationID`),
  KEY `StationID` (`StationID`),
  KEY `GridID` (`GridID`),
  CONSTRAINT `power_allocation_ibfk_1` FOREIGN KEY (`StationID`) REFERENCES `charging_station` (`StationID`),
  CONSTRAINT `power_allocation_ibfk_2` FOREIGN KEY (`GridID`) REFERENCES `grid_authority` (`GridID`),
  CONSTRAINT `power_allocation_chk_1` CHECK ((`AllocatedPower` >= 0)),
  CONSTRAINT `power_allocation_chk_2` CHECK ((`AvailablePower` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `power_allocation`
--

LOCK TABLES `power_allocation` WRITE;
/*!40000 ALTER TABLE `power_allocation` DISABLE KEYS */;
INSERT INTO `power_allocation` VALUES (601,300,240,'2026-04-17 06:20:47',201,1),(602,350,250,'2026-04-05 02:39:38',202,2),(603,320,220,'2026-04-05 02:39:38',203,2);
/*!40000 ALTER TABLE `power_allocation` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `power_threshold_alert` BEFORE UPDATE ON `power_allocation` FOR EACH ROW BEGIN
    DECLARE threshold INT;

    SELECT ThresholdPower INTO threshold
    FROM charging_station
    WHERE StationID = NEW.StationID;

    IF NEW.AvailablePower < threshold THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Warning: Power below safe threshold';
    END IF;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `vehicle`
--

DROP TABLE IF EXISTS `vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle` (
  `VehicleID` int NOT NULL,
  `RegistrationNumber` varchar(20) NOT NULL,
  `VehicleType` varchar(50) DEFAULT NULL,
  `BatteryCapacity` int DEFAULT NULL,
  `OwnerID` int DEFAULT NULL,
  PRIMARY KEY (`VehicleID`),
  UNIQUE KEY `RegistrationNumber` (`RegistrationNumber`),
  KEY `idx_vehicle_owner` (`OwnerID`),
  CONSTRAINT `vehicle_ibfk_1` FOREIGN KEY (`OwnerID`) REFERENCES `ev_owner` (`OwnerID`),
  CONSTRAINT `vehicle_chk_1` CHECK ((`BatteryCapacity` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle`
--

LOCK TABLES `vehicle` WRITE;
/*!40000 ALTER TABLE `vehicle` DISABLE KEYS */;
INSERT INTO `vehicle` VALUES (101,'DL01EV1234','Sedan',60,1),(102,'MH02EV5678','SUV',75,2),(103,'DL03EV9999','Hatchback',50,4),(105,'MH05EV4321','SUV',65,5),(106,'KA01EV2222','SUV',70,3),(107,'DL09EV8888','Sedan',55,1),(108,'MH12EV1111','Hatchback',45,2);
/*!40000 ALTER TABLE `vehicle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendor`
--

DROP TABLE IF EXISTS `vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendor` (
  `VendorID` int NOT NULL,
  `OrganizationName` varchar(100) DEFAULT NULL,
  `ContactDetails` varchar(100) DEFAULT NULL,
  `AuthorizationDoc` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`VendorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendor`
--

LOCK TABLES `vendor` WRITE;
/*!40000 ALTER TABLE `vendor` DISABLE KEYS */;
INSERT INTO `vendor` VALUES (701,'PowerTech Pvt Ltd','support@chargetech.com','AUTH_CERT_001'),(702,'ChargeFix Solutions','support@chargefix.com','AUTH_CERT_002'),(703,'EV Maintenance Co','help@evmaint.com','AUTH_CERT_003');
/*!40000 ALTER TABLE `vendor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'ev_charging_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-21 15:09:52
