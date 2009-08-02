ALTER TABLE `channels` ADD `accountbans` TEXT NOT NULL DEFAULT ''
ALTER TABLE `channels` ADD `ipbans` TEXT NOT NULL DEFAULT ''
ALTER TABLE `channels` CHANGE `mutes` `accountmutes` TEXT CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL 
ALTER TABLE `channels` ADD `ipmutes` TEXT NOT NULL DEFAULT '' AFTER `accountmutes` 
