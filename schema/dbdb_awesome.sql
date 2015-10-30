/*
SQLyog Ultimate v11.11 (64 bit)
MySQL - 5.6.14 : Database - ebdb_awesome
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`ebdb_awesome` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `ebdb_awesome`;

/*Table structure for table `blogs` */

DROP TABLE IF EXISTS `blogs`;

CREATE TABLE `blogs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `summary` varchar(200) DEFAULT NULL,
  `content` text NOT NULL,
  `category_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

/*Data for the table `blogs` */

insert  into `blogs`(`id`,`user_id`,`title`,`summary`,`content`,`category_id`,`created_at`) values (1,1,'bottle笔记','bottle笔记','static/files/bottle笔记.md',1,'2015-10-29 16:56:51'),(2,1,'python-对象生存周期问题','python-对象生存周期问题','static/files/python-对象生存周期问题.md',1,'2015-10-30 09:31:09'),(3,1,'centos快速搭建ftp服务器','centos快速搭建ftp服务器asasas','static/files/centos快速搭建ftp服务器.md',5,'2015-10-29 17:00:30'),(4,1,'python-微信公众平台','python-微信公众平台','static/files/python-微信公众平台.md',1,'2015-10-30 09:29:56'),(6,1,'centos快速搭建ftp服务器','centos快速搭建ftp服务器','static/files/centos快速搭建ftp服务器.md',1,'2015-10-29 07:43:14'),(7,1,'python-rsa模块','python-rsa模块','static/files/python-rsa模块.md',1,'2015-10-30 01:37:47'),(8,1,'python-pymongo模块','python-pymongo模块','static/files/python-pymongo模块.md',1,'2015-10-30 02:05:02');

/*Table structure for table `category` */

DROP TABLE IF EXISTS `category`;

CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

/*Data for the table `category` */

insert  into `category`(`id`,`name`,`user_id`) values (1,'python',1),(5,'java',1),(6,'php',1);

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `admin` int(1) DEFAULT '0' COMMENT '管理员-1，普通-0',
  `name` varchar(50) DEFAULT NULL,
  `image` varchar(500) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

/*Data for the table `users` */

insert  into `users`(`id`,`email`,`password`,`admin`,`name`,`image`,`created_at`) values (1,'269614597@qq.com','f148f4f9d03f8c1ca52d45db8b538bb8',1,'admin',NULL,'2015-10-27 08:09:32');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
