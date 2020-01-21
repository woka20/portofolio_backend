-- MySQL dump 10.16  Distrib 10.1.41-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: REAL_DATABASE
-- ------------------------------------------------------
-- Server version	10.1.41-MariaDB-0+deb9u1

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('99a78476b8f2');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `belanja`
--

DROP TABLE IF EXISTS `belanja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `belanja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `kurir` varchar(10) DEFAULT NULL,
  `ongkir` int(11) DEFAULT NULL,
  `total_harga` int(11) DEFAULT NULL,
  `payment` varchar(20) DEFAULT NULL,
  `bukti_pembayaran` blob,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `belanja_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `produk` (`id`),
  CONSTRAINT `belanja_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `konsumen` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `belanja`
--

LOCK TABLES `belanja` WRITE;
/*!40000 ALTER TABLE `belanja` DISABLE KEYS */;
/*!40000 ALTER TABLE `belanja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `konsumen`
--

DROP TABLE IF EXISTS `konsumen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `konsumen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_name` varchar(100) DEFAULT NULL,
  `client_password` varchar(1000) DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `telp` varchar(13) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `kota` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `konsumen`
--

LOCK TABLES `konsumen` WRITE;
/*!40000 ALTER TABLE `konsumen` DISABLE KEYS */;
/*!40000 ALTER TABLE `konsumen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produk`
--

DROP TABLE IF EXISTS `produk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produk` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipe` varchar(10) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `nama_produk` varchar(100) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `harga` int(11) DEFAULT NULL,
  `stok` int(11) DEFAULT NULL,
  `berat` int(11) DEFAULT NULL,
  `gambar` varchar(200) DEFAULT NULL,
  `preview_1` varchar(200) DEFAULT NULL,
  `preview_2` varchar(200) DEFAULT NULL,
  `preview_3` varchar(200) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produk`
--

LOCK TABLES `produk` WRITE;
/*!40000 ALTER TABLE `produk` DISABLE KEYS */;
INSERT INTO `produk` VALUES (1,'Premium',NULL,'RG Zeta Gundam','Real Grade',200000,1,2000,'https://ecs7.tokopedia.net/img/cache/700/product-1/2016/10/12/5073375/5073375_f47b7bd2-9e1a-4752-ab41-e425bdc25608.jpg','https://ecs7.tokopedia.net/img/cache/700/product-1/2016/10/12/5073375/5073375_678799bd-4bfc-438d-9ec0-b98738f6ed07.jpg','https://ecs7.tokopedia.net/img/cache/700/product-1/2016/10/12/5073375/5073375_f3ca3060-758d-4e25-a2dc-d758bb70ac4c.jpg','https://ecs7.tokopedia.net/img/cache/700/product-1/2016/10/12/5073375/5073375_30f8d79d-5c4f-4a65-be0b-44e61a4a4c4a.jpg','- RG Series A New undergone into new, 10th bullet is memorable Zeta Gundam!- RG series that appeared to commemorate the 30th anniversary of Gundam. Two years from the start-up series. Of GunplaAs its 10th anniversary of RG series you should aggregating the technology that can have, the pursuit of real, finallyZeta Gundam appeared.','2020-01-20 15:58:36',NULL,NULL);
/*!40000 ALTER TABLE `produk` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-01-20 19:50:12
