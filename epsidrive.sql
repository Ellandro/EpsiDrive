-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : lun. 20 nov. 2023 à 13:27
-- Version du serveur : 8.0.31
-- Version de PHP : 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `epsidrive`
--

-- --------------------------------------------------------

--
-- Structure de la table `abonnements`
--

DROP TABLE IF EXISTS `abonnements`;
CREATE TABLE IF NOT EXISTS `abonnements` (
  `IDAbonnement` int NOT NULL AUTO_INCREMENT,
  `IDUtilisateur` int DEFAULT NULL,
  `IDCategorie` int DEFAULT NULL,
  `IDOperateur` int DEFAULT NULL,
  `Montant` int DEFAULT NULL,
  PRIMARY KEY (`IDAbonnement`),
  KEY `IDUtilisateur` (`IDUtilisateur`),
  KEY `IDCategorie` (`IDCategorie`),
  KEY `IDOperateur` (`IDOperateur`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `autoecoles`
--

DROP TABLE IF EXISTS `autoecoles`;
CREATE TABLE IF NOT EXISTS `autoecoles` (
  `IDAutoEcole` int NOT NULL AUTO_INCREMENT,
  `NomAutoEcole` varchar(100) DEFAULT NULL,
  `Lieu` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`IDAutoEcole`),
  UNIQUE KEY `NomAutoEcole` (`NomAutoEcole`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `categoriespermis`
--

DROP TABLE IF EXISTS `categoriespermis`;
CREATE TABLE IF NOT EXISTS `categoriespermis` (
  `IDCategorie` int NOT NULL AUTO_INCREMENT,
  `NomCategorie` varchar(20) DEFAULT NULL,
  `Montant` int DEFAULT NULL,
  PRIMARY KEY (`IDCategorie`),
  UNIQUE KEY `NomCategorie` (`NomCategorie`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `commentaires`
--

DROP TABLE IF EXISTS `commentaires`;
CREATE TABLE IF NOT EXISTS `commentaires` (
  `IDCommentaire` int NOT NULL AUTO_INCREMENT,
  `IDUtilisateur` int DEFAULT NULL,
  `IDModule` int DEFAULT NULL,
  `TexteCommentaire` text,
  PRIMARY KEY (`IDCommentaire`),
  KEY `IDUtilisateur` (`IDUtilisateur`),
  KEY `IDModule` (`IDModule`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `cours`
--

DROP TABLE IF EXISTS `cours`;
CREATE TABLE IF NOT EXISTS `cours` (
  `IDCours` int NOT NULL AUTO_INCREMENT,
  `IDModule` int DEFAULT NULL,
  `IDCategorie` int DEFAULT NULL,
  `TitreCours` varchar(100) DEFAULT NULL,
  `Contenu` text,
  PRIMARY KEY (`IDCours`),
  KEY `IDModule` (`IDModule`),
  KEY `IDCategorie` (`IDCategorie`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `documentsutilisateur`
--

DROP TABLE IF EXISTS `documentsutilisateur`;
CREATE TABLE IF NOT EXISTS `documentsutilisateur` (
  `IDDocument` int NOT NULL AUTO_INCREMENT,
  `IDUtilisateur` int DEFAULT NULL,
  `TypeDocument` varchar(50) DEFAULT NULL,
  `NomFichier` varchar(255) DEFAULT NULL,
  `DateTelechargement` datetime DEFAULT NULL,
  PRIMARY KEY (`IDDocument`),
  KEY `IDUtilisateur` (`IDUtilisateur`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `examenfinal`
--

DROP TABLE IF EXISTS `examenfinal`;
CREATE TABLE IF NOT EXISTS `examenfinal` (
  `IDExamen` int NOT NULL AUTO_INCREMENT,
  `IDCategorie` int DEFAULT NULL,
  `NomExamen` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`IDExamen`),
  KEY `IDCategorie` (`IDCategorie`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `modulecategorie`
--

DROP TABLE IF EXISTS `modulecategorie`;
CREATE TABLE IF NOT EXISTS `modulecategorie` (
  `IDModule` int NOT NULL AUTO_INCREMENT,
  `IDCategorie` int NOT NULL,
  PRIMARY KEY (`IDModule`,`IDCategorie`),
  KEY `IDCategorie` (`IDCategorie`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `modulesenseignes`
--

DROP TABLE IF EXISTS `modulesenseignes`;
CREATE TABLE IF NOT EXISTS `modulesenseignes` (
  `IDModule` int NOT NULL AUTO_INCREMENT,
  `NomModule` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`IDModule`),
  UNIQUE KEY `NomModule` (`NomModule`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
CREATE TABLE IF NOT EXISTS `notifications` (
  `IDNotification` int NOT NULL AUTO_INCREMENT,
  `IDUtilisateur` int DEFAULT NULL,
  `TexteNotification` text,
  `Statut` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`IDNotification`),
  KEY `IDUtilisateur` (`IDUtilisateur`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `operateurs`
--

DROP TABLE IF EXISTS `operateurs`;
CREATE TABLE IF NOT EXISTS `operateurs` (
  `IDOperateur` int NOT NULL AUTO_INCREMENT,
  `NomOperateur` varchar(100) DEFAULT NULL,
  `Moyendepaiement` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`IDOperateur`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `questionsexams`
--

DROP TABLE IF EXISTS `questionsexams`;
CREATE TABLE IF NOT EXISTS `questionsexams` (
  `IDQuestionExam` int NOT NULL AUTO_INCREMENT,
  `IDExamen` int DEFAULT NULL,
  `choix1` varchar(255) DEFAULT NULL,
  `choix2` varchar(255) DEFAULT NULL,
  `choix3` varchar(255) DEFAULT NULL,
  `choix4` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`IDQuestionExam`),
  KEY `IDExamen` (`IDExamen`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `questionstest`
--

DROP TABLE IF EXISTS `questionstest`;
CREATE TABLE IF NOT EXISTS `questionstest` (
  `IDQuestion` int NOT NULL,
  `IDTest` int DEFAULT NULL,
  `QuestionTexte` varchar(75) DEFAULT NULL,
  `choix1` varchar(255) DEFAULT NULL,
  `choix2` varchar(255) DEFAULT NULL,
  `choix3` varchar(255) DEFAULT NULL,
  `choix4` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`IDQuestion`),
  KEY `IDTest` (`IDTest`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `rendezvous`
--

DROP TABLE IF EXISTS `rendezvous`;
CREATE TABLE IF NOT EXISTS `rendezvous` (
  `IDRendezVous` int NOT NULL AUTO_INCREMENT,
  `IDUtilisateur` int DEFAULT NULL,
  `IDAutoEcole` int DEFAULT NULL,
  `DateRendezVous` datetime DEFAULT NULL,
  `Lieu` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`IDRendezVous`),
  KEY `IDUtilisateur` (`IDUtilisateur`),
  KEY `IDAutoEcole` (`IDAutoEcole`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `reponsesexamen`
--

DROP TABLE IF EXISTS `reponsesexamen`;
CREATE TABLE IF NOT EXISTS `reponsesexamen` (
  `IDReponse` int NOT NULL AUTO_INCREMENT,
  `IDExamen` int DEFAULT NULL,
  `Resultat` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`IDReponse`),
  KEY `IDExamen` (`IDExamen`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `reponsestest`
--

DROP TABLE IF EXISTS `reponsestest`;
CREATE TABLE IF NOT EXISTS `reponsestest` (
  `IDReponse` int NOT NULL AUTO_INCREMENT,
  `IDTest` int DEFAULT NULL,
  `IDQuestion` int DEFAULT NULL,
  `ReponseCorrect` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`IDReponse`),
  KEY `IDTest` (`IDTest`),
  KEY `IDQuestion` (`IDQuestion`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `roles`
--

DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `IDRole` int NOT NULL AUTO_INCREMENT,
  `NomRole` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`IDRole`),
  UNIQUE KEY `NomRole` (`NomRole`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `scoresexamens`
--

DROP TABLE IF EXISTS `scoresexamens`;
CREATE TABLE IF NOT EXISTS `scoresexamens` (
  `IDScore` int NOT NULL AUTO_INCREMENT,
  `IDReponse` int DEFAULT NULL,
  `IDExamen` int DEFAULT NULL,
  `IDUtilisateur` int DEFAULT NULL,
  PRIMARY KEY (`IDScore`),
  KEY `IDExamen` (`IDExamen`),
  KEY `IDUtilisateur` (`IDUtilisateur`),
  KEY `IDReponse` (`IDReponse`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `scoretest`
--

DROP TABLE IF EXISTS `scoretest`;
CREATE TABLE IF NOT EXISTS `scoretest` (
  `IDScore` int NOT NULL AUTO_INCREMENT,
  `IDTest` int DEFAULT NULL,
  `IDQuestion` int DEFAULT NULL,
  `IDUtilisateur` int DEFAULT NULL,
  `Resultat` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`IDScore`),
  KEY `IDTest` (`IDTest`),
  KEY `IDQuestion` (`IDQuestion`),
  KEY `IDUtilisateur` (`IDUtilisateur`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `testsmodule`
--

DROP TABLE IF EXISTS `testsmodule`;
CREATE TABLE IF NOT EXISTS `testsmodule` (
  `IDTest` int NOT NULL AUTO_INCREMENT,
  `IDModule` int DEFAULT NULL,
  `NomTest` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`IDTest`),
  UNIQUE KEY `NomTest` (`NomTest`),
  KEY `IDModule` (`IDModule`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `utilisateurs`
--

DROP TABLE IF EXISTS `utilisateurs`;
CREATE TABLE IF NOT EXISTS `utilisateurs` (
  `IDUtilisateur` int NOT NULL AUTO_INCREMENT,
  `IDRole` int DEFAULT NULL,
  `Prenom` varchar(50) DEFAULT NULL,
  `Nom` varchar(50) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `MotDePasse` varchar(255) DEFAULT NULL,
  `Photo` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`IDUtilisateur`),
  UNIQUE KEY `Email` (`Email`),
  KEY `IDRole` (`IDRole`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
