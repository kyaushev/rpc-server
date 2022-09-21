DROP DATABASE IF EXISTS news_db;
CREATE DATABASE IF NOT EXISTS news_db;
USE news_db;

DROP TABLE IF EXISTS news;

CREATE TABLE news (
    id SERIAL,
    title CHAR(255) COLLATE utf8mb4_unicode_ci,
    body TEXT COLLATE utf8mb4_unicode_ci,
    post_date DATE
) ENGINE = InnoDB;

SELECT 'LOADING news' as 'INFO';
source load_news.dump