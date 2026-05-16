CREATE DATABASE IF NOT EXISTS security;

USE security;

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR (100) NOT NULL,
    email VARCHAR (100)
);

INSERT INTO users (name, email) VALUES (
    "lee", "leepineda@gmail.com"
)

CREATE TABLE roles (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR (24) NOT NULL
);

INSERT INTO roles (role_name) VALUES ("admin"),("editor"),("viewer");

CREATE TABLE user_roles (
    user_id INT,
    role_id INT,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles (role_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
); 

INSERT INTO user_roles VALUES (1,1);