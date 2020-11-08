from watcher import Watcher
from database_connector import Database


database = Database()
database.initialize()
watcher = Watcher()
watcher.watch("input",
              "incorrect_input")
