CREATE TABLE IF NOT EXISTS threads (
    id_thread integer PRIMARY KEY AUTOINCREMENT,
    category_thread text NOT NULL,
    img_thread text,
    date_thread text NOT NULL,
    name_thread text NOT NULL,
    text_thread text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id_post integer PRIMARY KEY AUTOINCREMENT,
    id_thread_post integer NOT NULL,
    img_post text,
    date_post text NOT NULL,
    text_post text NOT NULL,
    FOREIGN KEY (id_thread_post) REFERENCES threads(id_thread)
);