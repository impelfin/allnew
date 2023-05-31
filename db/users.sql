CREATE TABLE `users` (
  `id` varchar(120) NOT NULL,
  `nickname` varchar(20) NOT NULL,
  `email` varchar(120) NOT NULL,
  `phone` varchar(13) NOT NULL,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
)