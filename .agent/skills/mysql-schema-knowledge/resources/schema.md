# Database Schema: News Aggregation System

## Overview
MySQL 8 Database containing news scraping, filtering, and social media tracking data.
**Note:** There are no explicit Foreign Keys defined between tables. Relationships are logical (based on URLs/Headlines).

---

## 1. Table: `breaking_news`
High-priority news items with scoring.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Unique identifier |
| `type` | VARCHAR(40) | NOT NULL | Category/Type of news |
| `headline` | VARCHAR(500) | NOT NULL | News title |
| `source` | VARCHAR(25) | NOT NULL | News source name |
| `url` | VARCHAR(600) | NOT NULL | Link to article |
| `score` | INT | NOT NULL | Relevance score |

---

## 2. Table: `featured_news`
Curated list of featured articles.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Unique identifier |
| `title` | VARCHAR(255) | NULLABLE | Article title |
| `url` | VARCHAR(255) | NULLABLE | Link to article |
| `category` | VARCHAR(255) | NULLABLE | Content category |
| `keywords` | VARCHAR(255) | NULLABLE | Comma-separated tags |

---

## 3. Table: `news`
**Main Table.** Core repository of all scraped news articles.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Unique identifier |
| `scrapedate` | DATETIME | NOT NULL, DEFAULT NOW() | When record was created |
| `headline` | VARCHAR(255) | NOT NULL, UNIQUE | Article title |
| `summary` | TEXT | NULLABLE | Article excerpt |
| `source` | VARCHAR(255) | NULLABLE | News source name |
| `keywords` | TEXT | NULLABLE | Extracted keywords |
| `section` | VARCHAR(255) | NULLABLE | Website section |
| `url` | VARCHAR(255) | NULLABLE | Link to article |
| `urlhash` | VARCHAR(255) | UNIQUE | Hash of URL for deduplication |
| `imageurl` | VARCHAR(700) | NULLABLE | Main article image |
| `clusterid` | VARCHAR(255) | NULLABLE | Grouping ID for similar stories |
| `pubdate` | VARCHAR(255) | NULLABLE | Original publication date (string) |
| `featured` | TINYINT | NULLABLE | Flag: Is featured? |
| `clustercount` | TINYINT | NULLABLE | Count of similar stories |
| `new` | TINYINT | NULLABLE | Flag: Is new arrival? |

**Indexes:**
- `UNIQUE` on `headline`
- `UNIQUE` on `urlhash`
- `FULLTEXT` on `headline` (Use for natural language search)

---

## 4. Table: `social_news`
Tracks news shares/posts on social platforms.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Unique identifier |
| `username` | VARCHAR(60) | NOT NULL | Social media handle |
| `user_url` | VARCHAR(60) | NOT NULL | Profile link |
| `created_at` | VARCHAR(26) | NOT NULL | Post timestamp (stored as string) |
| `card_url` | VARCHAR(255) | NOT NULL | Link to the news card |
| `post_url` | VARCHAR(255) | NOT NULL | Link to the social post |

**Indexes:**
- `UNIQUE` composite on (`username`, `card_url`)

---

## Query Guidelines for Agent
1. **Search:** Use `MATCH(headline) AGAINST(...)` for full-text search on the `news` table.
2. **Deduplication:** Check `urlhash` or `headline` uniqueness before inserting into `news`.
3. **Joins:** No enforced Foreign Keys. Join logically on `url` or `headline` if needed, but expect potential mismatches.
4. **Dates:** `news.scrapedate` is DATETIME. `social_news.created_at` is VARCHAR (parse carefully).
5. **Limits:** The `news` table is large (37M+ rows). Always use `LIMIT` and indexed columns (`urlhash`, `headline`) in WHERE clauses.
