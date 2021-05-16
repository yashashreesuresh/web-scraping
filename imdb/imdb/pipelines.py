# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class SQLlitePipeline:
    # Function is executed during the start of spider
    def open_spider(self, spider):
        try:
            self.connection = sqlite3.connect("imdb.db")
            self.cursor = self.connection.cursor()

            command = """
                CREATE TABLE top_rated_movies (
                    Title TEXT,
                    Rating TEXT,
                    Release_date TEXT,
                    Genre TEXT,
                    Duration TEXT,
                    Movie_url TEXT
                )"""

            self.cursor.execute(command)
            self.connection.commit()

        except sqlite3.OperationalError:
            pass


    # Function is executed during the end of spider
    def close_spider(self,spider):
        self.connection.close()


    # Function is exectued after each item is scraped (after making each request)
    def process_item(self, item, spider):
        command = """INSERT INTO top_rated_movies (Title, Rating, Release_date, Genre, Duration, Movie_url)
            VALUES (?, ?, ?, ?, ?, ?)"""

        self.cursor.execute(
            command,
            (item.get("title"), item.get("rating"), item.get("release-date"), item.get("genre"), item.get("duration"), item.get("movie-url"))
        )

        self.connection.commit()
        return item
