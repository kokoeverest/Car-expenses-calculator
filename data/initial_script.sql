-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema Car Expenses
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Car Expenses
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Car Expenses` ;
USE `Car Expenses` ;

-- -----------------------------------------------------
-- Table `Car Expenses`.`Cars`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Car Expenses`.`Cars` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `Brand` VARCHAR(50) NOT NULL,
  `Model` VARCHAR(45) NOT NULL,
  `Year` INT(11) NOT NULL,
  `Seats` INT(11) NULL DEFAULT 5,
  `Tires` TEXT NULL DEFAULT NULL,
  `Vignette price` FLOAT NULL DEFAULT 87,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `Car Expenses`.`Engines`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Car Expenses`.`Engines` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Capacity` VARCHAR(45) NOT NULL,
  `Power_hp` VARCHAR(45) NOT NULL,
  `Power_kw` VARCHAR(45) NOT NULL,
  `Fuel type` VARCHAR(45) NOT NULL,
  `Emmissions category` VARCHAR(45) NOT NULL,
  `Consumption` FLOAT NULL,
  `Oil capacity` FLOAT NULL,
  `Oil type` VARCHAR(45) NULL DEFAULT '10W40',
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Car Expenses`.`Tires`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Car Expenses`.`Tires` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Prefix` VARCHAR(3) NULL DEFAULT 'R',
  `Width` VARCHAR(45) NOT NULL,
  `Height` VARCHAR(45) NOT NULL,
  `Radius` VARCHAR(45) NOT NULL,
  `Min price` FLOAT NULL DEFAULT 0,
  `Max price` FLOAT NULL DEFAULT 0,
  `Date` DATE NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Car Expenses`.`Fuels`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Car Expenses`.`Fuels` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Fuel type` VARCHAR(45) NOT NULL,
  `Price` FLOAT NULL DEFAULT NULL,
  `Date` DATE NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Car Expenses`.`Taxes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Car Expenses`.`Taxes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `City` VARCHAR(45) NOT NULL,
  `Municipality` VARCHAR(45) NOT NULL,
  `Euro category` VARCHAR(45) NOT NULL,
  `Car year` VARCHAR(45) NOT NULL,
  `Engine power` VARCHAR(45) NOT NULL,
  `Price` FLOAT NULL,
  `Date` DATE NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Car Expenses`.`Insurances`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Car Expenses`.`Insurances` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Car year` VARCHAR(45) NOT NULL,
  `Engine size` VARCHAR(45) NOT NULL,
  `Fuel type` VARCHAR(45) NOT NULL,
  `Engine power` VARCHAR(45) NOT NULL ,
  `Municipality` VARCHAR(45) NOT NULL,
  `Registration` TINYINT NULL DEFAULT 0,
  `Driver age` VARCHAR(45) NULL DEFAULT NULL ,
  `Driver experience` VARCHAR(45) NULL DEFAULT NULL ,
  `Min price` FLOAT NULL DEFAULT 0,
  `Max price` FLOAT NULL DEFAULT 0,
  `Date` DATE NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Car Expenses`.`Cities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Car Expenses`.`Cities` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(100) NOT NULL,
  `Municipality` VARCHAR(145) NOT NULL,
  `Prefix` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Car Expenses`.`Cars_Engines`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Car Expenses`.`Cars_Engines` (
  `Car_id` INT(11) NOT NULL,
  `Engine_id` INT NOT NULL,
  PRIMARY KEY (`Car_id`, `Engine_id`),
  INDEX `fk_Cars_has_Engines_Engines1_idx` (`Engine_id` ASC) VISIBLE,
  INDEX `fk_Cars_has_Engines_Cars_idx` (`Car_id` ASC) VISIBLE,
  CONSTRAINT `fk_Cars_has_Engines_Cars`
    FOREIGN KEY (`Car_id`)
    REFERENCES `Car Expenses`.`Cars` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Cars_has_Engines_Engines1`
    FOREIGN KEY (`Engine_id`)
    REFERENCES `Car Expenses`.`Engines` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `Car Expenses`.`Cars_Tires`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Car Expenses`.`Cars_Tires` (
  `Car_id` INT(11) NOT NULL,
  `Tire_id` INT NOT NULL,
  PRIMARY KEY (`Car_id`, `Tire_id`),
  INDEX `fk_Cars_has_Tires_Tires1_idx` (`Tire_id` ASC) VISIBLE,
  INDEX `fk_Cars_has_Tires_Cars1_idx` (`Car_id` ASC) VISIBLE,
  CONSTRAINT `fk_Cars_has_Tires_Cars1`
    FOREIGN KEY (`Car_id`)
    REFERENCES `Car Expenses`.`Cars` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Cars_has_Tires_Tires1`
    FOREIGN KEY (`Tire_id`)
    REFERENCES `Car Expenses`.`Tires` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `Car Expenses`.`Oils`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Car Expenses`.`Oils` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Oil type` VARCHAR(45) NOT NULL,
  `Min price` FLOAT NOT NULL DEFAULT 0,
  `Max price` FLOAT NOT NULL DEFAULT 0,
  `Date` DATE NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Car Expenses`.`Brake pads`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Car Expenses`.`Brake pads` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Front` TINYINT NULL DEFAULT 0,
  `Rear` TINYINT NULL DEFAULT 0,
  `Min price` FLOAT NOT NULL DEFAULT 0,
  `Max price` FLOAT NOT NULL DEFAULT 0,
  `Date` DATE NOT NULL,
  `Car_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Brake pads_Cars1_idx` (`Car_id` ASC) VISIBLE,
  CONSTRAINT `fk_Brake pads_Cars1`
    FOREIGN KEY (`Car_id`)
    REFERENCES `Car Expenses`.`Cars` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
