# MySQL Navigator Xport
# Database: pytasserver
# root@localhost

# CREATE DATABASE pytasserver;
# USE pytasserver;

#
# Table structure for table 'channels'
#

# DROP TABLE IF EXISTS channels;
CREATE TABLE `channels` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` text NOT NULL,
  `founder` text,
  `mutes` text,
  `operators` text,
  `topic` text,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

#
# Table structure for table 'users'
#

# DROP TABLE IF EXISTS users;
CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` text NOT NULL,
  `password` text NOT NULL,
  `playtime` int(11) NOT NULL,
  `accesslevel` tinyint(4) NOT NULL,
  `bot` tinyint(4) NOT NULL,
  `banned` tinyint(4) NOT NULL,
  `casename` text,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=609 DEFAULT CHARSET=latin1;

