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


"""
"""


DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `check_id` (IN `p_tid` INT)   BEGIN
    DECLARE exist INT DEFAULT 0;
    SELECT COUNT(*) INTO exist FROM post WHERE tid = p_tid;
    IF exist = 1 THEN
        SELECT 1 as message;
    ELSE
        SELECT 0 as message;
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_post` (IN `p_tid` INT)   BEGIN
	DECLARE d_tid INT;
    DECLARE d_title VARCHAR(100);
    DECLARE d_content VARCHAR(200);
    SELECT tid, title, content INTO d_tid, d_title, d_content FROM post WHERE post.tid = p_tid;
    DELETE FROM post WHERE post.tid = p_tid;
    SELECT d_tid AS tid, d_title AS title, d_content AS content;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `save_post` (IN `p_title` VARCHAR(100), IN `p_content` VARCHAR(200))   BEGIN
	DECLARE n INT DEFAULT 0;
	INSERT INTO dbsample.post (title, content)
    VALUES (p_title, p_content);
    
    SELECT tid INTO n FROM post WHERE post.title = p_title;
    
    SELECT `n` as tid;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_post` (IN `p_tid` INT, IN `p_title` VARCHAR(100), IN `p_content` VARCHAR(200))   BEGIN
    UPDATE post
    SET title = p_title, content = p_content
    WHERE tid = p_tid;
    SELECT * FROM post WHERE tid = p_tid;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `post`
--

CREATE TABLE `post` (
  `tid` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `content` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `post`
--

INSERT INTO `post` (`tid`, `title`, `content`) VALUES
(12, 'new title2', 'new content'),
(13, 'new title32', 'new content');

-- --------------------------------------------------------

--
-- Stand-in structure for view `post_view`
-- (See below for the actual view)
--
CREATE TABLE `post_view` (
`tid` int(11)
,`title` varchar(100)
,`content` varchar(200)
);

-- --------------------------------------------------------

-- CREATE TABLE replies
CREATE TABLE `replies` (
  `reply_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `post_id` INT UNSIGNED NOT NULL,
  `user_id` INT UNSIGNED NOT NULL,
  `content` VARCHAR(1000) NOT NULL,
  `reply_date` VARCHAR(100) NOT NULL,
  `likes` INT DEFAULT 0,
  `dislikes` INT DEFAULT 0,
  PRIMARY KEY (`reply_id`),
  FOREIGN KEY (`post_id`) REFERENCES `post`(`tid`),
  FOREIGN KEY (`user_id`) REFERENCES `catusers`(`id`)
) ENGINE=InnoDB;

DELIMITER $$$

-- Procedure to save a new reply
CREATE PROCEDURE save_reply(
  IN p_post_id INT,
  IN p_user_id INT,
  IN p_content VARCHAR(1000),
  IN p_reply_date VARCHAR(100)
)
BEGIN
  -- Insert into replies table
  INSERT INTO replies (post_id, user_id, content, reply_date)
    VALUES (p_post_id, p_user_id, p_content, p_reply_date);
END$$$
DELIMITER ;

--
-- Structure for view `post_view`
--

DROP TABLE IF EXISTS `post_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `post_view`  AS SELECT `post`.`tid` AS `tid`, `post`.`title` AS `title`, `post`.`content` AS `content` FROM `post`;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `post`
--
ALTER TABLE `post`
  ADD PRIMARY KEY (`tid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `post`
--
ALTER TABLE `post`
  MODIFY `tid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
