ALTER TABLE channels ADD password VARCHAR(24) NOT NULL DEFAULT '*';
ALTER TABLE users ADD lastlogin int(20) NOT NULL DEFAULT 0;
ALTER TABLE users ADD registrationdate int(20) NOT NULL DEFAULT 0;
ALTER TABLE users ADD lastip VARCHAR(16) NOT NULL DEFAULT '127.0.0.1';