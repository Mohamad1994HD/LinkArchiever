import sqlite3
from config import appConfig


def createTBLS(path=None):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE links(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                                        name TEXT NOT NULL
                   );""")

    cursor.execute("""CREATE TABLE tags(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                                        tag TEXT NOT NULL
                   );""")

    cursor.execute("""CREATE TABLE assc(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                                        links_id INTEGER NOT NULL,
                                        tags_id INTEGER NOT NULL,
                                        FOREIGN KEY (links_id) REFERENCES links(id),
                                        FOREIGN KEY (tags_id) REFERENCES tags(id)
                    );""")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    try:
        path = appConfig.db_path
        print path
        createTBLS(str(path))
    except IOError as e:
        print (str(e))
