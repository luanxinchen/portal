-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: ecust
-- ------------------------------------------------------
-- Server version	5.7.38

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
-- Table structure for table `api_user`
--

DROP TABLE IF EXISTS `api_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) NOT NULL,
  `password` varchar(64) NOT NULL,
  `role` smallint(6) NOT NULL,
  `status` smallint(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `email` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_user`
--

LOCK TABLES `api_user` WRITE;
/*!40000 ALTER TABLE `api_user` DISABLE KEYS */;
INSERT INTO `api_user` VALUES (1,'admin','5c57d096fd1d11b50dfb24aa35823516',1,1,'2024-09-13 15:40:47.000000','2024-09-13 16:31:09.472160','admin@qq.com'),(3,'栾新晨','8a5d629028a5dc5ac0acaa2044a62243',2,1,'2024-09-13 15:40:47.082835','2024-09-13 18:16:40.219916','123123@qq.com');
/*!40000 ALTER TABLE `api_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_contactcategory`
--

DROP TABLE IF EXISTS `api_contactcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_contactcategory` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `sort` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_contactcategory`
--

LOCK TABLES `api_contactcategory` WRITE;
/*!40000 ALTER TABLE `api_contactcategory` DISABLE KEYS */;
INSERT INTO `api_contactcategory` VALUES (1,'IT信息部',1,'2024-09-11 18:36:12.398535','2024-09-12 15:12:51.667839'),(2,'行政部',2,'2024-09-11 18:36:24.735461','2024-09-12 15:13:06.494346'),(3,'财务部',3,'2024-09-12 15:13:04.111165','2024-09-12 15:13:04.111165'),(4,'人事部',4,'2024-09-12 15:13:12.137245','2024-09-12 15:13:12.137245'),(5,'研发部',1,'2024-09-12 15:13:22.570570','2024-09-12 15:13:22.570570');
/*!40000 ALTER TABLE `api_contactcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_contact`
--

DROP TABLE IF EXISTS `api_contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_contact` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `person` varchar(64) NOT NULL,
  `description` varchar(256) NOT NULL,
  `location` varchar(256) NOT NULL,
  `contact_type` smallint(6) NOT NULL,
  `contact_key` varchar(128) DEFAULT NULL,
  `sort` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_contact_category_id_a6c25967_fk_api_contactcategory_id` (`category_id`),
  CONSTRAINT `api_contact_category_id_a6c25967_fk_api_contactcategory_id` FOREIGN KEY (`category_id`) REFERENCES `api_contactcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_contact`
--

LOCK TABLES `api_contact` WRITE;
/*!40000 ALTER TABLE `api_contact` DISABLE KEYS */;
INSERT INTO `api_contact` VALUES (1,'张三','统一账户处理','A栋5楼IT办公室',1,'18888888888',1,'2024-09-12 15:15:59.538687','2024-09-12 15:15:59.538687',1),(2,'李四','网络管理员','信息大楼11楼IT办公室',1,'12312312311',1,'2024-09-12 15:15:59.538687','2024-09-12 15:23:22.629671',1),(3,'王五','机房管理员','A栋5楼IT办公室',1,'16666666666',1,'2024-09-12 15:15:59.538687','2024-09-12 15:21:21.740850',1),(4,'小明','系统运维管理员','信息大楼11楼IT办公室',3,'admin@qq.com',1,'2024-09-12 15:15:59.538687','2024-09-12 15:22:50.891314',1),(8,'王大雷','XXX系统研发负责人','研发中心3楼',3,'dalei.wang@qq.com',1,'2024-09-12 15:15:59.538687','2024-09-12 15:25:47.523902',5),(9,'张三','统一账户处理','A栋5楼IT办公室',1,'18888888888',1,'2024-09-12 15:15:59.538687','2024-09-12 15:15:59.538687',1);
/*!40000 ALTER TABLE `api_contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_sitecategory`
--

DROP TABLE IF EXISTS `api_sitecategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_sitecategory` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `icon` varchar(64) DEFAULT NULL,
  `title` varchar(64) NOT NULL,
  `sort` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_sitecategory`
--

LOCK TABLES `api_sitecategory` WRITE;
/*!40000 ALTER TABLE `api_sitecategory` DISABLE KEYS */;
INSERT INTO `api_sitecategory` VALUES (3,'Star','常用系统',1,'2024-09-12 15:07:00.000000','2024-09-12 15:07:00.000000'),(4,'DataAnalysis','运营相关',3,'2024-09-12 15:07:00.000000','2024-09-12 15:39:47.164040'),(5,'Monitor','研发相关',2,'2024-09-12 15:07:00.000000','2024-09-12 15:39:43.993713'),(6,'Van','交付系统',5,'2024-09-12 15:07:00.000000','2024-09-12 15:07:00.000000'),(7,'User','人事系统',4,'2024-09-12 15:07:00.000000','2024-09-12 15:07:00.000000'),(8,'FirstAidKit','售后系统',6,'2024-09-12 15:07:00.000000','2024-09-12 15:07:00.000000');
/*!40000 ALTER TABLE `api_sitecategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_notification`
--

DROP TABLE IF EXISTS `api_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_notification` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `content` longtext NOT NULL,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `type` smallint(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_notification`
--

LOCK TABLES `api_notification` WRITE;
/*!40000 ALTER TABLE `api_notification` DISABLE KEYS */;
INSERT INTO `api_notification` VALUES (1,'系统维护通知','Gitlab系统将于本周五（10月1日）20:00分开始维护，期间服务不可用，请大家提前提交代码','2024-09-12 00:00:00.000000','2024-10-22 00:00:00.000000',1,2,'2024-09-12 11:34:10.849760','2024-09-12 15:33:43.189237'),(2,'系统维护通知','Gitlab系统已完成维护，服务已恢复','2024-09-12 00:00:00.000000','2024-09-30 00:00:00.000000',1,1,'2024-09-12 15:34:27.223736','2024-09-12 15:35:30.878250');
/*!40000 ALTER TABLE `api_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_site`
--

DROP TABLE IF EXISTS `api_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_site` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `url` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `sort` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `logo` varchar(128) DEFAULT NULL,
  `tips` longtext,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category_id` bigint(20) DEFAULT NULL,
  `maintainer_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_site_category_id_f30f2690_fk_api_sitecategory_id` (`category_id`),
  KEY `api_site_maintainer_id_871af543_fk_api_user_id` (`maintainer_id`),
  CONSTRAINT `api_site_category_id_f30f2690_fk_api_sitecategory_id` FOREIGN KEY (`category_id`) REFERENCES `api_sitecategory` (`id`),
  CONSTRAINT `api_site_maintainer_id_871af543_fk_api_user_id` FOREIGN KEY (`maintainer_id`) REFERENCES `api_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_site`
--

LOCK TABLES `api_site` WRITE;
/*!40000 ALTER TABLE `api_site` DISABLE KEYS */;
INSERT INTO `api_site` VALUES (6,'OA','https://vpn.ecustmde.com:1111/logon/LogonPoint/index.html','协同办公系统',2,1,'oa.png','使用统一账户登录','2024-09-12 15:11:03.284282','2024-09-13 17:39:06.825534',4,3),(7,'Gitlab','https://vpn.ecustmde.com:1111/logon/LogonPoint/index.html','代码托管系统',1,1,'GITLAB.png','使用统一账户登录','2024-09-12 15:11:03.284282','2024-09-14 11:39:29.353376',5,3),(8,'HR','https://vpn.ecustmde.com:1111/logon/LogonPoint/index.html','人事管理系统',1,1,'moka-people.png','使用邮箱登录','2024-09-12 15:11:03.284282','2024-09-14 15:45:54.513290',7,3),(9,'Email','https://vpn.ecustmde.com:1111/logon/LogonPoint/index.html','企业邮箱平台',2,1,'exmail.png','使用学号+密码登录','2024-09-12 15:11:03.284282','2024-09-12 15:39:13.897971',3,1),(10,'统一账户管理系统','https://vpn.ecustmde.com:1111/logon/LogonPoint/index.html','统一账户管理系统',3,1,'selfcare.png','使用统一账户登录','2024-09-12 15:11:03.284282','2024-09-12 15:39:17.111483',3,1),(11,'Jira','https://vpn.ecustmde.com:1111/logon/LogonPoint/index.html','敏捷开发',1,1,'jira.png','使用学号+密码登录','2024-09-12 15:11:03.284282','2024-09-12 15:31:41.559345',5,1),(12,'Confluence','https://vpn.ecustmde.com:1111/logon/LogonPoint/index.html','研发WIKI平台',1,1,'wiki_1oY5GDh.png','使用学号+密码登录','2024-09-12 15:11:03.284282','2024-09-12 15:32:04.464791',5,1),(13,'校外VPN系统','https://vpn.ecustmde.com:1111/logon/LogonPoint/index.html','校外VPN系统',1,1,'logo.png','使用学号+密码登录','2024-09-12 15:11:03.284282','2024-09-12 15:18:58.615039',8,1),(14,'ERP','https://vpn.ecustmde.com:1111/logon/LogonPoint/index.html','ERP系统',1,1,'owncloud.png','使用学号+密码登录','2024-09-12 15:11:03.284282','2024-09-12 15:38:16.009647',4,1),(15,'CRM','https://vpn.ecustmde.com:1111/logon/LogonPoint/index.html','客户关系情报系统',1,1,'Friday.png','使用学号+密码登录','2024-09-12 15:11:03.284282','2024-09-12 15:38:56.929647',4,1),(16,'AIOPS','https://vpn.ecustmde.com:1111/logon/LogonPoint/index.html','智能运维平台',1,1,'clustermanager.png','使用学号+密码登录','2024-09-12 15:11:03.284282','2024-09-12 15:44:03.511285',5,1),(17,'校外VPN系统','https://vpn.ecustmde.com:1111/logon/LogonPoint/index.html','校外VPN系统',1,1,'logo.png','使用学号+密码登录','2024-09-12 15:11:03.284282','2024-09-12 15:19:16.610555',6,1),(18,'校外VPN系统','https://vpn.ecustmde.com:1111/logon/LogonPoint/index.html','校外VPN系统',1,1,'logo.png','使用学号+密码登录','2024-09-12 15:11:03.284282','2024-09-12 15:11:03.284282',3,1);
/*!40000 ALTER TABLE `api_site` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-14 16:15:13
