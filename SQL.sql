drop database N;

create database N;

use N;

create table categories (
    category_id int primary key auto_increment,
    category_name varchar(100) not null
);

create table content (
    content_id int primary key auto_increment,
    category_id int not null,
    content_text text,
    content_file_url text,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
