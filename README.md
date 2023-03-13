Frontend - 前端， vue

backend - 后端，flask

具体前后端如何运行请进入这两个文件夹查看 readme 文件

数据库建立可以参考位于 backend/readme 中的建议，如果不成功，也可以通过 SQL 语句建立你的数据库：

#### (1) 建立数据库

```sql
CREATE DATABASE `BS` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
```

#### (2) 建表

```sql
CREATE TABLE `image` (
  `id` int NOT NULL AUTO_INCREMENT,
  `address` varchar(250) DEFAULT NULL,
  `task_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_image_address` (`address`),
  KEY `task_id` (`task_id`),
  CONSTRAINT `image_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `task` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `imagetotag` (
  `image_id` int NOT NULL,
  `tag_id` int NOT NULL,
  `x` varchar(20) DEFAULT NULL,
  `x1` varchar(20) DEFAULT NULL,
  `y` varchar(20) DEFAULT NULL,
  `y1` varchar(20) DEFAULT NULL,
  `tag_count` int NOT NULL,
  PRIMARY KEY (`image_id`,`tag_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `imagetotag_ibfk_1` FOREIGN KEY (`image_id`) REFERENCES `image` (`id`),
  CONSTRAINT `imagetotag_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tag` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tag_name` varchar(50) DEFAULT NULL,
  `uuid` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  UNIQUE KEY `ix_tag_tag_name` (`tag_name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `task` (
  `id` int NOT NULL AUTO_INCREMENT,
  `creator_id` int DEFAULT NULL,
  `title` varchar(64) DEFAULT NULL,
  `discription` text,
  `create_time` datetime DEFAULT NULL,
  `finish_time` datetime DEFAULT NULL,
  `IsFinished` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `creator_id` (`creator_id`),
  KEY `ix_task_title` (`title`),
  CONSTRAINT `task_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `location` varchar(64) DEFAULT NULL,
  `about_me` text,
  `member_since` datetime DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_email` (`email`),
  UNIQUE KEY `ix_user_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

