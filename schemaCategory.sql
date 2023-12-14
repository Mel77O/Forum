-- schema.sql


CREATE TABLE `grps` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `category` varchar(500) NOT NULL DEFAULT '',
  `hashtag` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;


CREATE TABLE `catusers` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `grp_id` int NOT NULL,
  `tags` varchar(500) NOT NULL DEFAULT '',
  `date` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB ;


CREATE VIEW catusers_view AS
  SELECT catusers.id,
    catusers.tags,
    catusers.date,
    grps.category,
    grps.hashtag
  FROM catusers
  INNER JOIN grps ON catusers.grp_id = grps.id;


DELIMITER $$$
CREATE PROCEDURE create_catuser(
  IN p_category varchar(500),
  IN p_hashtag varchar(500),
  IN p_tags varchar(500),
  IN p_date varchar(100)
)
BEGIN
  DECLARE p_grp_id INT;
  DECLARE p_catuser_id INT;
  INSERT INTO grps (category, hashtag)
    VALUES (p_category, p_hashtag);
  SET p_grp_id = LAST_INSERT_ID();
  INSERT INTO catusers (grp_id, tags, date)
    VALUES (p_grp_id, p_tags, p_date);
  SET p_catuser_id = LAST_INSERT_ID();
  SELECT p_catuser_id AS id;
END$$$
DELIMITER ;


DELIMITER $$$
CREATE PROCEDURE update_catuser(
  IN p_id INT,
  IN p_category varchar(500),
  IN p_hashtag varchar(500),
  IN p_tags varchar(500),
  IN p_date varchar(100)
)
BEGIN
  UPDATE grps
    INNER JOIN catusers ON grps.id = catusers.grp_id
    SET category = p_category,
      hashtag = p_hashtag
    WHERE catusers.id = p_id;
  UPDATE catusers
    SET tags = p_tags,
      date = p_date
    WHERE id = p_id;
  SELECT p_id AS id;
END$$$
DELIMITER ;


DELIMITER $$$
CREATE PROCEDURE delete_catuser(
  IN p_id INT
)
BEGIN
  DELETE grp.* FROM grps
  INNER JOIN catusers ON grps.id = catusers.grp_id
  WHERE catusers.id = p_id;
  DELETE FROM catusers
  WHERE id = p_id;
  SELECT id FROM catusers
  WHERE id = p_id;
END$$$
DELIMITER ;