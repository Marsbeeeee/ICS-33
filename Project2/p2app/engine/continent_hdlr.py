from p2app.events import *


def continent_related_events(engine, event):
    # User initiates a search for continents
    if isinstance(event, StartContinentSearchEvent):
        code = event.continent_code()
        name = event.name()
        try:
            rows = engine.db_connection.execute(
                'SELECT * '
                'FROM continent '
                'WHERE continent_code = ? OR name = ?',
                (code, name)
            ).fetchall()
            for row in rows:
                continent = Continent(row[0], row[1], row[2])
                yield ContinentSearchResultEvent(continent)
        except Exception as e:
            yield ErrorEvent(f"Failed to get continent related events: {e}")

    # User loads a continent from the database to edit it
    elif isinstance(event, LoadContinentEvent):
        continent_id = event.continent_id()
        try:
            row = engine.db_connection.execute(
                'SELECT * '
                'FROM continent '
                'WHERE continent_id = :continent_id',
                {'continent_id': continent_id}
            ).fetchone()
            continent = Continent(row[0], row[1], row[2])
            if row:
                yield ContinentLoadedEvent(continent)
        except Exception as e:
            yield ErrorEvent(f"Failed to load continent related events: {e}")

    # User saves a new continent into the database
    elif isinstance(event, SaveNewContinentEvent):
        continent = event.continent()
        try:
            cursor = engine.db_connection.execute(
                'INSERT INTO continent (continent_code, name) '
                'VALUES (:continent_code, :name);',
                {'continent_code': continent.continent_code, 'name': continent.name}
            )
            engine.db_connection.commit()
            new_id = cursor.lastrowid
            new_continent = Continent(new_id, continent.continent_code, continent.name)
            yield ContinentSavedEvent(new_continent)
        except Exception as e:
            yield SaveContinentFailedEvent(f'Failed to save continent related event: {e}')

    # User saves a modified continent into the database
    elif isinstance(event, SaveContinentEvent):
        continent = event.continent()
        try:
            engine.db_connection.execute(
                'UPDATE continent '
                'SET name = :name, continent_code = :continent_code WHERE continent_id = :continent_id; ',
                {'name': continent.name, 'continent_code': continent.continent_code, 'continent_id': continent.continent_id}
            )
            engine.db_connection.commit()
            new_continent = Continent(continent.continent_id, continent.continent_code, continent.name)
            yield ContinentSavedEvent(new_continent)
        except Exception as e:
            yield SaveContinentFailedEvent(f'Failed to save continent related event: {e}')