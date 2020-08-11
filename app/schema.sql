DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS console_permissions;
DROP TABLE IF EXISTS plugins_permissions;
DROP TABLE IF EXISTS user_permissions;
CREATE TABLE user (
    id integer primary KEY AUTOINCREMENT,
    username text unique not null,
    password text not null,
    valid TEXT CHECK (valid in ('Y', 'N')) NOT NULL DEFAULT 'Y',
    first_login TEXT CHECK (first_login in ('Y', 'N')) NOT NULL DEFAULT 'Y'
);
create table console_permissions(
    user_id PRIMARY KEY,
    stop_perm TEXT CHECK (stop_perm in ('Y', 'N')) NOT NULL DEFAULT 'N',
    start_perm TEXT CHECK (start_perm in ('Y', 'N')) NOT NULL DEFAULT 'N',
    execute_cmd TEXT CHECK (execute_cmd in ('Y', 'N')) NOT NULL DEFAULT 'N',
    admin TEXT CHECK (admin in ('Y', 'N')) NOT NULL DEFAULT 'N',
    FOREIGN KEY (user_id) references user (id)
);
create table plugins_permissions(
    user_id PRIMARY KEY,
    upload TEXT CHECK (upload in ('Y', 'N')) NOT NULL DEFAULT 'N',
    remove TEXT CHECK (remove in ('Y', 'N')) NOT NULL DEFAULT 'N',
    edit_config_files TEXT CHECK (edit_config_files in ('Y', 'N')) NOT NULL DEFAULT 'N',
    admin TEXT CHECK (admin in ('Y', 'N')) NOT NULL DEFAULT 'N',
    FOREIGN KEY (user_id) references user (id)
);
create table user_permissions(
    user_id PRIMARY KEY,
    create_user TEXT CHECK (create_user in ('Y', 'N')) NOT NULL DEFAULT 'N',
    assign_perms TEXT CHECK (assign_perms in ('Y', 'N')) NOT NULL DEFAULT 'N',
    change_perms TEXT CHECK (change_perms in ('Y', 'N')) NOT NULL DEFAULT 'N',
    remove_user TEXT CHECK (remove_user in ('Y', 'N')) NOT NULL DEFAULT 'N',
    reset_pwd TEXT CHECK (reset_pwd in ('Y', 'N')) NOT NULL DEFAULT 'N',
    view_users TEXT CHECK (view_users in ('Y', 'N')) NOT NULL DEFAULT 'N',
    pause_user TEXT CHECK (pause_user in ('Y', 'N')) NOT NULL DEFAULT 'N',
    admin TEXT CHECK (admin in ('Y', 'N')) NOT NULL DEFAULT 'N',
    FOREIGN KEY (user_id) references user (id)
);