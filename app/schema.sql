DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS console_permissions;
DROP TABLE IF EXISTS plugins_permissions;
DROP TABLE IF EXISTS user_permissions;
DROP TABLE IF EXISTS valid_keys;
CREATE TABLE user (
    id integer primary KEY AUTOINCREMENT,
    username text unique not null,
    password text not null,
    valid CHAR CHECK (valid in ('Y', 'N')) NOT NULL DEFAULT 'Y',
    first_login CHAR CHECK (first_login in ('Y', 'N')) NOT NULL DEFAULT 'Y'
);
create table console_permissions(
    user_id INTEGER PRIMARY KEY,
    stop_perm CHAR CHECK (stop_perm in ('Y', 'N')) NOT NULL DEFAULT 'N',
    start_perm CHAR CHECK (start_perm in ('Y', 'N')) NOT NULL DEFAULT 'N',
    execute_cmd CHAR CHECK (execute_cmd in ('Y', 'N')) NOT NULL DEFAULT 'N',
    admin CHAR CHECK (admin in ('Y', 'N')) NOT NULL DEFAULT 'N',
    FOREIGN KEY (user_id) references user (id)
);
create table plugins_permissions(
    user_id INTEGER PRIMARY KEY,
    upload CHAR CHECK (upload in ('Y', 'N')) NOT NULL DEFAULT 'N',
    remove CHAR CHECK (remove in ('Y', 'N')) NOT NULL DEFAULT 'N',
    edit_config_files CHAR CHECK (edit_config_files in ('Y', 'N')) NOT NULL DEFAULT 'N',
    admin CHAR CHECK (admin in ('Y', 'N')) NOT NULL DEFAULT 'N',
    FOREIGN KEY (user_id) references user (id)
);
create table user_permissions(
    user_id INTEGER PRIMARY KEY,
    create_user CHAR CHECK (create_user in ('Y', 'N')) NOT NULL DEFAULT 'N',
    assign_perms CHAR CHECK (assign_perms in ('Y', 'N')) NOT NULL DEFAULT 'N',
    change_perms CHAR CHECK (change_perms in ('Y', 'N')) NOT NULL DEFAULT 'N',
    remove_user CHAR CHECK (remove_user in ('Y', 'N')) NOT NULL DEFAULT 'N',
    reset_pwd CHAR CHECK (reset_pwd in ('Y', 'N')) NOT NULL DEFAULT 'N',
    view_users CHAR CHECK (view_users in ('Y', 'N')) NOT NULL DEFAULT 'N',
    pause_user CHAR CHECK (pause_user in ('Y', 'N')) NOT NULL DEFAULT 'N',
    admin CHAR CHECK (admin in ('Y', 'N')) NOT NULL DEFAULT 'N',
    FOREIGN KEY (user_id) references user (id)
);
create table valid_keys (
    id INTEGER PRIMARY KEY,
    user_key VARCHAR (128) NOT NULL,
    creation_date TEXT NOT NULL,
    expiration_date TEXT NOT NULL,
    FOREIGN KEY (id) references user (id)
)