-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: yaofangsafety
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `drugs`
--

DROP TABLE IF EXISTS `drugs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drugs` (
  `drug_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `manufacturer` varchar(100) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock` int NOT NULL,
  `code` varchar(50) DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `last_updated_by` varchar(50) DEFAULT NULL,
  `total_sold` int DEFAULT '0',
  `sold_since_restock` int DEFAULT '0',
  PRIMARY KEY (`drug_id`),
  UNIQUE KEY `drug_id` (`drug_id`),
  UNIQUE KEY `code` (`code`),
  CONSTRAINT `drugs_chk_1` CHECK ((`stock` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drugs`
--

LOCK TABLES `drugs` WRITE;
INSERT INTO `drugs` VALUES (1,'Amoxicillin','HealthCo',6.98,100,'D001','2025-05-30 15:22:53','Cici',5,0),(2,'Amoxicillin','HealthCo',8.50,80,'D002','2025-06-06 03:34:28','manager1',18,0),(3,'Vitamin C','Pharma Co',9.99,105,'D003','2025-05-30 02:55:37','manager1',1,1),(7,'Ibuprofen','PharmaX',6.50,50,'D004','2025-05-30 14:56:01','Cici',2,2),(8,'Ibuprofen','MediCare Ltd.',6.75,120,'D005','2025-05-30 14:35:25','manager1',1,1),(9,'Cetirizine','AllergyRelief Co.',4.20,95,'D006','2025-04-16 02:06:40','manager1',5,5),(10,'Aspirin','HealthPlus',3.99,145,'D007','2025-04-15 06:53:21','manager1',5,5),(12,'Loratadine','AllerGen Pharma',5.10,75,'D009','2025-04-15 06:53:21','manager1',10,10),(13,'Azithromycin','AntibioTech',12.00,80,'D010','2025-05-30 02:55:58','manager1',55,0),(14,'Omeprazole','DigestWell',7.45,90,'D011','2025-05-29 15:44:54','manager1',5,5),(15,'Simvastatin','CardioHealth',10.25,100,'D012','2025-04-15 06:53:50','manager1',9,9),(16,'Levothyroxine','ThyroMed',6.85,100,'D013','2025-05-29 15:45:10','manager1',5,5),(17,'Losartan','PressureEase',8.60,70,'D014','2025-04-15 06:53:21','manager1',10,10),(18,'Furosemide','Diurex Labs',5.40,75,'D015','2025-04-15 06:53:21','manager1',0,0),(19,'Prednisone','ImmunoCorp',11.20,60,'D016','2025-06-02 03:41:17','manager1',5,0),(20,'Atorvastatin','LipidoCare',9.80,100,'D017','2025-04-15 06:53:21','manager1',0,0),(21,'Clopidogrel','AntiClot Pharma',13.60,54,'D018','2025-04-15 06:53:21','manager1',1,1),(22,'Alprazolam','CalmMed Inc.',4.90,60,'D019','2025-04-15 06:53:21','manager1',10,10),(24,'Hydrochlorothiazide','WaterRegulate',6.60,80,'D021','2025-04-15 06:53:21','manager1',5,5),(25,'Montelukast','BreathEZ Pharma',7.75,79,'D022','2025-04-15 06:53:21','manager1',1,1),(26,'Tramadol','PainRelief Corp.',9.99,20,'D023','2025-06-04 12:47:38','manager1',55,0),(27,'Ranitidine','AcidAway',5.35,98,'D024','2025-04-15 06:53:21','manager1',2,2);
UNLOCK TABLES;

--
-- Table structure for table `operation_log`
--

DROP TABLE IF EXISTS `operation_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operation_log` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `operation_type` enum('add','update','delete','restock') NOT NULL,
  `drug_id` bigint DEFAULT NULL,
  `drug_name` varchar(255) DEFAULT NULL,
  `description` text,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operation_log`
--

LOCK TABLES `operation_log` WRITE;
INSERT INTO `operation_log` VALUES (1,'manager1','update',26,'Tramadol','Updated drug \'Tramadol\': price=9.99, stock=20, manufacturer=\'PainRelief Corp.\', code=\'D023\'','2025-06-04 12:47:38'),(2,'manager1','update',2,'Amoxicillin','Updated drug \'Amoxicillin\': price=8.5, stock=80, manufacturer=\'HealthCo\', code=\'D002\'','2025-06-06 03:34:28');
UNLOCK TABLES;

--
-- Table structure for table `sales`
--

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales` (
  `sale_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `drug_id` bigint unsigned NOT NULL,
  `seller_id` bigint unsigned NOT NULL,
  `quantity` int NOT NULL,
  `sale_time` datetime DEFAULT NULL,
  PRIMARY KEY (`sale_id`),
  UNIQUE KEY `sale_id` (`sale_id`),
  KEY `fk_sales_drug` (`drug_id`),
  KEY `fk_sales_seller` (`seller_id`),
  CONSTRAINT `fk_sales_drug` FOREIGN KEY (`drug_id`) REFERENCES `drugs` (`drug_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_sales_seller` FOREIGN KEY (`seller_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `sales_chk_1` CHECK ((`quantity` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales`
--

LOCK TABLES `sales` WRITE;
INSERT INTO `sales` VALUES (1,2,3,10,'2025-04-15 09:57:49'),(2,26,3,55,'2025-04-15 15:17:54'),(3,13,3,55,'2025-04-15 15:23:11'),(5,1,3,1,'2025-05-17 14:56:41'),(6,2,3,1,'2025-05-17 14:56:50'),(7,1,3,1,'2025-05-17 15:01:46'),(8,2,3,1,'2025-05-17 15:05:04'),(9,1,3,1,'2025-05-21 13:42:51'),(10,1,3,1,'2025-05-21 13:49:30'),(11,10,3,1,'2025-05-23 02:03:38'),(12,9,3,1,'2025-05-23 02:03:39'),(13,8,3,1,'2025-05-23 02:03:40'),(14,7,3,1,'2025-05-23 02:03:41'),(15,15,3,1,'2025-05-23 02:03:42'),(16,24,3,1,'2025-05-23 02:03:45'),(17,21,3,1,'2025-05-23 02:03:46'),(18,10,3,1,'2025-05-23 11:27:42'),(19,9,3,1,'2025-05-23 11:27:42'),(20,10,13,1,'2025-05-27 02:17:11'),(21,12,13,1,'2025-05-27 02:17:11'),(22,12,13,1,'2025-05-27 02:20:19'),(23,10,13,1,'2025-05-27 02:20:19'),(24,10,3,1,'2025-05-28 15:01:47'),(26,24,3,1,'2025-05-28 15:12:49'),(28,27,3,1,'2025-05-28 15:12:49'),(30,22,3,7,'2025-05-28 15:41:18'),(33,27,3,1,'2025-05-28 15:41:18'),(35,15,3,1,'2025-05-28 15:41:18'),(36,14,3,1,'2025-05-28 15:41:18'),(37,15,3,1,'2025-05-28 15:43:04'),(38,17,3,1,'2025-05-29 08:17:12'),(39,19,3,5,'2025-05-29 08:17:57'),(40,14,3,4,'2025-05-29 16:29:24'),(41,15,3,6,'2025-05-29 16:29:24'),(42,16,3,5,'2025-05-29 16:29:24'),(43,17,3,9,'2025-05-29 16:29:24'),(44,22,3,3,'2025-05-29 16:29:24'),(45,7,3,1,'2025-05-29 16:32:47'),(46,12,3,1,'2025-05-29 16:34:18'),(47,1,3,1,'2025-05-29 18:48:08'),(48,2,3,1,'2025-05-29 18:49:14'),(49,3,3,1,'2025-05-29 22:39:20'),(50,25,3,1,'2025-05-29 22:44:24'),(59,12,3,2,'2025-06-04 09:38:30'),(60,9,3,3,'2025-06-04 20:46:52'),(61,2,3,5,'2025-06-06 11:30:41'),(62,12,3,5,'2025-06-06 20:51:26'),(63,24,3,3,'2025-06-06 20:51:26');
UNLOCK TABLES;

--
-- Table structure for table `sales_log`
--

DROP TABLE IF EXISTS `sales_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `drug_id` bigint unsigned NOT NULL,
  `drug_name` varchar(255) NOT NULL,
  `manufacturer` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `quantity` int NOT NULL,
  `total_price` decimal(10,2) GENERATED ALWAYS AS ((`price` * `quantity`)) STORED,
  `sale_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_log`
--

LOCK TABLES `sales_log` WRITE;
INSERT INTO `sales_log` (`id`, `drug_id`, `drug_name`, `manufacturer`, `price`, `quantity`, `sale_time`) VALUES (1,2,'Amoxicillin','HealthCo',8.50,10,'2025-04-15 09:57:49'),(2,26,'Tramadol','PainRelief Corp.',9.99,55,'2025-04-15 15:17:54'),(3,13,'Azithromycin','AntibioTech',12.00,55,'2025-04-15 15:23:11'),(4,1,'Amoxicillin','HealthCo',6.98,1,'2025-05-17 14:56:41'),(5,2,'Amoxicillin','HealthCo',8.50,1,'2025-05-17 14:56:50'),(6,1,'Amoxicillin','HealthCo',6.98,1,'2025-05-17 15:01:46'),(7,2,'Amoxicillin','HealthCo',8.50,1,'2025-05-17 15:05:04'),(8,1,'Amoxicillin','HealthCo',6.98,1,'2025-05-21 13:42:51'),(9,1,'Amoxicillin','HealthCo',6.98,1,'2025-05-21 13:49:30'),(10,10,'Aspirin','HealthPlus',3.99,1,'2025-05-23 02:03:38'),(11,9,'Cetirizine','AllergyRelief Co.',4.20,1,'2025-05-23 02:03:39'),(12,8,'Ibuprofen','MediCare Ltd.',6.75,1,'2025-05-23 02:03:40'),(13,7,'Ibuprofen','PharmaX',6.50,1,'2025-05-23 02:03:41'),(14,15,'Simvastatin','CardioHealth',10.25,1,'2025-05-23 02:03:42'),(15,24,'Hydrochlorothiazide','WaterRegulate',6.60,1,'2025-05-23 02:03:45'),(16,21,'Clopidogrel','AntiClot Pharma',13.60,1,'2025-05-23 02:03:46'),(17,10,'Aspirin','HealthPlus',3.99,1,'2025-05-23 11:27:42'),(18,9,'Cetirizine','AllergyRelief Co.',4.20,1,'2025-05-23 11:27:42'),(19,10,'Aspirin','HealthPlus',3.99,1,'2025-05-27 02:17:11'),(20,12,'Loratadine','AllerGen Pharma',5.10,1,'2025-05-27 02:17:11'),(21,12,'Loratadine','AllerGen Pharma',5.10,1,'2025-05-27 02:20:19'),(22,10,'Aspirin','HealthPlus',3.99,1,'2025-05-27 02:20:19'),(23,10,'Aspirin','HealthPlus',3.99,1,'2025-05-28 15:01:47'),(24,24,'Hydrochlorothiazide','WaterRegulate',6.60,1,'2025-05-28 15:12:49'),(25,27,'Ranitidine','AcidAway',5.35,1,'2025-05-28 15:12:49'),(26,22,'Alprazolam','CalmMed Inc.',4.90,7,'2025-05-28 15:41:18'),(27,27,'Ranitidine','AcidAway',5.35,1,'2025-05-28 15:41:18'),(28,15,'Simvastatin','CardioHealth',10.25,1,'2025-05-28 15:41:18'),(29,14,'Omeprazole','DigestWell',7.45,1,'2025-05-28 15:41:18'),(30,15,'Simvastatin','CardioHealth',10.25,1,'2025-05-28 15:43:04'),(31,17,'Losartan','PressureEase',8.60,1,'2025-05-29 08:17:12'),(32,19,'Prednisone','ImmunoCorp',11.15,5,'2025-05-29 08:17:57'),(33,14,'Omeprazole','DigestWell',7.45,4,'2025-05-29 16:29:24'),(34,15,'Simvastatin','CardioHealth',10.25,6,'2025-05-29 16:29:24'),(35,16,'Levothyroxine','ThyroMed',6.85,5,'2025-05-29 16:29:24'),(36,17,'Losartan','PressureEase',8.60,9,'2025-05-29 16:29:24'),(37,22,'Alprazolam','CalmMed Inc.',4.90,3,'2025-05-29 16:29:24'),(38,7,'Ibuprofen','PharmaX',6.50,1,'2025-05-29 16:32:47'),(39,12,'Loratadine','AllerGen Pharma',5.10,1,'2025-05-29 16:34:18'),(40,1,'Amoxicillin','HealthCo',6.98,1,'2025-05-29 18:48:08'),(41,2,'Amoxicillin','HealthCo',8.50,1,'2025-05-29 18:49:14'),(42,3,'Vitamin C','Pharma Co',9.99,1,'2025-05-29 22:39:20'),(43,25,'Montelukast','BreathEZ Pharma',7.75,1,'2025-05-29 22:44:24'),(64,12,'Loratadine','AllerGen Pharma',5.10,2,'2025-06-04 09:38:30'),(65,9,'Cetirizine','AllergyRelief Co.',4.20,3,'2025-06-04 20:46:52'),(66,2,'Amoxicillin','HealthCo',8.50,5,'2025-06-06 11:30:41'),(67,12,'Loratadine','AllerGen Pharma',5.10,5,'2025-06-06 20:51:26'),(68,24,'Hydrochlorothiazide','WaterRegulate',6.60,3,'2025-06-06 20:51:26');
UNLOCK TABLES;

--
-- Table structure for table `user_logs`
--

DROP TABLE IF EXISTS `user_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_logs` (
  `log_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `action` text,
  `log_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`),
  UNIQUE KEY `log_id` (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_logs`
--

LOCK TABLES `user_logs` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `total_sales_amount` decimal(10,2) DEFAULT '0.00',
  `cert_fingerprint` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `username` (`username`),
  CONSTRAINT `users_chk_1` CHECK ((`role` in (_utf8mb4'admin',_utf8mb4'manager',_utf8mb4'seller')))
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
INSERT INTO `users` VALUES (1,'admin1','adminpass','admin','2025-04-14 13:28:05',0.00,'f9e8da621cea8d181609ab19c51965bd8ae08622f68f912d11aa9e6df98a7d8b'),(2,'manager1','managerpass','manager','2025-04-14 13:28:05',0.00,NULL),(3,'seller1','sellerpass','seller','2025-04-14 13:28:05',625.96,NULL),(5,'Sally','pbkdf2:sha256:260000$hbddsrB5ISB679ZQ$74d418cabc6c5cd84c19b0d8c2f11608cae8bebff58668a40782f47489711f6f','admin','2025-04-15 15:18:51',0.00,'f9e8da621cea8d181609ab19c51965bd8ae08622f68f912d11aa9e6df98a7d8b'),(6,'Lucy','pbkdf2:sha256:260000$Kjj1mnOcc5C33zrg$84556a4a1a03d23de287b62563597e62467cf2be5207a61341a0fc40f9d5f33d','manager','2025-04-15 15:19:08',0.00,NULL),(7,'Jenny','pbkdf2:sha256:260000$xhlamcz1nNGStVTp$18984ef6dedd4851265d3fc7eb51e70cf83e9c17812cd6b54908aa71802ea752','seller','2025-04-15 15:19:18',0.00,NULL),(8,'Jack','pbkdf2:sha256:260000$OxAOuBvjCWca4YZN$cd694a53b055e2ceb39e17b960fa0a4c9e73dbc1964900548766b4064ed7637c','seller','2025-04-16 02:07:59',0.00,NULL),(9,'Joe','pbkdf2:sha256:260000$AyJnuUqM6p8SJLE4$7eefda54e3c126e9848ed16bf5c9813d1e4fc0051a206babcca26861404e3dc2','seller','2025-04-16 02:08:08',0.00,NULL),(10,'Nick','pbkdf2:sha256:260000$ecWV5hGc1LNwpz1c$72360fa05c34565ac0430a869b95d8d788e065e719a8f06d100caa3dc5e9c7ab','admin','2025-04-16 02:08:20',0.00,'f9e8da621cea8d181609ab19c51965bd8ae08622f68f912d11aa9e6df98a7d8b'),(11,'Smart','pbkdf2:sha256:260000$Ctwu7ZKD6W4TyOwr$909d7bf53a9bca04e525d87419f538262fb0fff287f47781e2e20dfa41e38860','seller','2025-04-16 02:08:34',0.00,NULL),(12,'Stella','pbkdf2:sha256:260000$Z8nISeTAa4lVZamY$9a7ceaa52e7f4ecf04cb503e81b18f6ea66d7c65488f37fbba64184a01d6e42e','manager','2025-04-16 02:18:18',0.00,NULL),(13,'Summer','pbkdf2:sha256:260000$L6qT8ThkWojZtF8B$02c62452f13e6952b5fd59cdc83421a1e95a255c521eb74d9f2c0dc4e8dcbd3b','seller','2025-05-23 11:48:56',18.18,NULL),(14,'Cici','pbkdf2:sha256:260000$1rpEzoQnodHD4CQn$559730bed6001fc40e5c247bd734e4ba976e2f22fb1bf3110433677363e60773','manager','2025-05-30 14:36:38',0.00,NULL);
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-06 21:43:57
