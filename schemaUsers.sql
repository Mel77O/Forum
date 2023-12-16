
--Create
CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL DEFAULT '',
  `email` varchar(100) NOT NULL DEFAULT '',
  `password` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB ;

--Read
SELECT * FROM users;


-- View
CREATE VIEW user_view AS
SELECT id, username, email
FROM users;

-- Stored Procedure
DELIMITER $$$
CREATE PROCEDURE create_user(
  IN p_email varchar(200),
  IN p_username varchar(100),
  IN p_password varchar(200),
  OUT p_user_id INT
)
BEGIN
    INSERT INTO users (username, email, password)
    VALUES (p_username, p_email, p_password);

    SET p_user_id = LAST_INSERT_ID();
END$$$
DELIMITER ;


DELIMITER $$$
CREATE PROCEDURE update_user(
    IN p_user_id INT,
    IN p_new_username VARCHAR(100),
    IN p_new_email VARCHAR(100),
    IN p_new_password VARCHAR(200)
)
BEGIN
    UPDATE users
    SET
        username = p_new_username,
        email = p_new_email,
        password = p_new_password
    WHERE id = p_user_id;
END$$$
DELIMITER ;


DELIMITER $$$
CREATE PROCEDURE delete_user(
    IN p_user_id INT
)
BEGIN
    DELETE FROM users
    WHERE id = p_user_id;
END$$$
DELIMITER ;