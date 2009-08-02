-- phpMyAdmin SQL Dump
-- version 3.2.0.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generato il: 02 ago, 2009 at 10:42 PM
-- Versione MySQL: 5.0.75
-- Versione PHP: 5.2.6-3ubuntu4.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Database: `pytasserver`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `channels`
--

CREATE TABLE IF NOT EXISTS `channels` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` text NOT NULL,
  `founder` text,
  `accountmutes` text,
  `ipmutes` text NOT NULL,
  `operators` text,
  `topic` text,
  `password` varchar(24) NOT NULL default '*',
  `accountbans` text NOT NULL,
  `ipbans` text NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

-- --------------------------------------------------------

--
-- Struttura della tabella `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` text NOT NULL,
  `password` text NOT NULL,
  `playtime` int(11) NOT NULL,
  `accesslevel` tinyint(4) NOT NULL,
  `bot` tinyint(4) NOT NULL,
  `banned` tinyint(4) NOT NULL,
  `casename` text,
  `lastlogin` int(20) NOT NULL default '0',
  `registrationdate` int(20) NOT NULL default '0',
  `lastip` varchar(16) NOT NULL default '127.0.0.1',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=610 ;
