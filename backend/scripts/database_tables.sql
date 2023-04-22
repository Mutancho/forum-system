-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema forumproject
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema forumproject
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `forumproject` DEFAULT CHARACTER SET latin1 ;
USE `forumproject` ;

-- -----------------------------------------------------
-- Table `forumproject`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forumproject`.`categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `is_private` TINYINT(1) NOT NULL DEFAULT '0',
  `locked` TINYINT(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forumproject`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forumproject`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `role` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username` (`username` ASC) ,
  UNIQUE INDEX `email` (`email` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forumproject`.`categorymember`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forumproject`.`categorymembers` (
  `user_id` INT(11) NOT NULL,
  `category_id` INT(11) NOT NULL,
  `read_access` TINYINT(1) NOT NULL DEFAULT '0',
  `write_access` TINYINT(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`, `category_id`),
  INDEX `category_id` (`category_id` ASC) ,
  CONSTRAINT `categorymember_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forumproject`.`user` (`id`),
  CONSTRAINT `categorymember_ibfk_2`
    FOREIGN KEY (`category_id`)
    REFERENCES `forumproject`.`category` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forumproject`.`message`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forumproject`.`messages` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `content` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `sender_id` INT(11) NOT NULL,
  `receiver_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `sender_id` (`sender_id` ASC) ,
  INDEX `receiver_id` (`receiver_id` ASC) ,
  CONSTRAINT `message_ibfk_1`
    FOREIGN KEY (`sender_id`)
    REFERENCES `forumproject`.`user` (`id`),
  CONSTRAINT `message_ibfk_2`
    FOREIGN KEY (`receiver_id`)
    REFERENCES `forumproject`.`user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forumproject`.`topic`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forumproject`.`topics` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `content` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT(11) NULL,
  `category_id` INT(11) NOT NULL,
  `locked` TINYINT(1) NOT NULL DEFAULT '0',
  `best_reply_id` INT(11),
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) ,
  INDEX `category_id` (`category_id` ASC) ,
  INDEX `fk_topic_reply1_idx` (`best_reply_id` ASC) ,
  CONSTRAINT `topic_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forumproject`.`user` (`id`),
  CONSTRAINT `topic_ibfk_2`
    FOREIGN KEY (`category_id`)
    REFERENCES `forumproject`.`category` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_topic_reply1`
    FOREIGN KEY (`best_reply_id`)
    REFERENCES `forumproject`.`reply` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forumproject`.`reply`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forumproject`.`replies` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `content` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT(11) NOT NULL,
  `topic_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) ,
  INDEX `fk_reply_topic1_idx` (`topic_id` ASC) ,
  CONSTRAINT `reply_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forumproject`.`user` (`id`),
  CONSTRAINT `fk_reply_topic1`
    FOREIGN KEY (`topic_id`)
    REFERENCES `forumproject`.`topic` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forumproject`.`replyvote`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forumproject`.`replyvotes` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `reply_id` INT(11) NOT NULL,
  `vote_type` ENUM('upvote', 'downvote') NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `reply_id` (`reply_id` ASC) ,
  INDEX `fk_replyvote_user1_idx` (`user_id` ASC) ,
  CONSTRAINT `replyvote_ibfk_2`
    FOREIGN KEY (`reply_id`)
    REFERENCES `forumproject`.`reply` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_replyvote_user1`
  FOREIGN KEY (`user_id`)
    REFERENCES `forumproject`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;