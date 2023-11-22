-- MariaDB dump 10.19  Distrib 10.11.3-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: salle_concert
-- ------------------------------------------------------
-- Server version	10.11.3-MariaDB-1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `concerts`
--

DROP TABLE IF EXISTS `concerts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `concerts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titre` varchar(50) NOT NULL,
  `artiste` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `tarif` smallint(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `concerts`
--

LOCK TABLES `concerts` WRITE;
/*!40000 ALTER TABLE `concerts` DISABLE KEYS */;
INSERT INTO `concerts` VALUES
(1,'Concert A','Artiste A','2023-12-15',50),
(2,'Concert B','Artiste B','2023-12-20',60),
(3,'Concert C','Artiste C','2023-12-25',40);
/*!40000 ALTER TABLE `concerts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spectateurs`
--

DROP TABLE IF EXISTS `spectateurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spectateurs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `num_tel` int(10) DEFAULT NULL,
  `email` varchar(80) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  `id_concert` int(11) NOT NULL,
  `nb_place_achete` smallint(6) NOT NULL,
  `emplacement` varchar(3) NOT NULL,
  `tarif` smallint(5) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_concert` (`id_concert`),
  CONSTRAINT `spectateurs_ibfk_1` FOREIGN KEY (`id_concert`) REFERENCES `concerts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spectateurs`
--

LOCK TABLES `spectateurs` WRITE;
/*!40000 ALTER TABLE `spectateurs` DISABLE KEYS */;
INSERT INTO `spectateurs` VALUES
(13,'Dupont','Jean',656245856,'jean.dupont@gmail.com','gtrnet',1,2,'A1',50),
(14,'Martin','Sophie',676543210,'sophie.martin@gmail.com','gtrnet',2,1,'B3',70),
(15,'Lefebvre','Pierre',654443333,'pierre.lefebvre@gmail.com','gtrnet',3,4,'C2',40);
/*!40000 ALTER TABLE `spectateurs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-22 14:07:11
