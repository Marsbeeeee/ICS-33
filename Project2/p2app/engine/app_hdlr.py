import sqlite3
from p2app.events import *

def application_level_events(engine, event):
    if isinstance(event, OpenDatabaseEvent):
        try:
            db_path = event.path()
            engine.db_connection = sqlite3.connect(str(db_path))
            engine.db_connection.execute("PRAGMA foreign_keys = ON")
            yield DatabaseOpenedEvent(db_path)
        except Exception as e:
            yield DatabaseOpenFailedEvent(str(e))

    elif isinstance(event, CloseDatabaseEvent):
        engine.db_connection.close()
        engine.db_connection = None
        yield DatabaseClosedEvent()

    elif isinstance(event, QuitInitiatedEvent):
        yield EndApplicationEvent()