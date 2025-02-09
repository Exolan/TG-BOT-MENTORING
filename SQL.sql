drop database N;

create database N;

use N;

create table categories (
    category_id int primary key auto_increment,
    category_name varchar(100) not null
);

create table themes (
    theme_id int primary key auto_increment,
    category_id int not null,
    theme_name varchar(100) not null unique,
    theme_text text null,
    theme_vector json null,
    theme_file_url text null,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

create table subthemes (
	subtheme_id int primary key auto_increment,
    theme_id int not null,
    subtheme_name varchar(100) not null,
    subtheme_text text not null,
    subtheme_vector json null,
    subtheme_file_url text null,
    FOREIGN KEY (theme_id) REFERENCES themes(theme_id)
);
