from p2app.events import *

def country_related_events(engine, event):
    # User initiates a search for countries
    if isinstance(event, StartCountrySearchEvent):
        try:
            country_code = event.country_code()
            name = event.name()
            rows = engine.db_connection.execute(
                'SELECT *'
                'FROM country '
                'WHERE country_code = ? OR name = ?',
                (country_code, name)
            ).fetchall()
            for row in rows:
                yield CountrySearchResultEvent(Country(*row))
        except Exception as e:
            yield ErrorEvent(f'Failed to get country related event: {e}')

    # User loads a country from the database to edit it
    elif isinstance(event, LoadCountryEvent):
        try:
            country_id = event.country_id()
            row = engine.db_connection.execute(
                'SELECT *'
                'FROM country '
                'WHERE country_id = ?',
                (country_id,)
            ).fetchone()
            if row:
                yield CountryLoadedEvent(Country(*row))
        except Exception as e:
            yield ErrorEvent(f'Failed to load country related event: {e}')

    # User saves a new country into the database
    elif isinstance(event, SaveNewCountryEvent):
        country = event.country()
        try:
            country_dict = {key: value for key, value in country._asdict().items()}
            del country_dict['country_id']
            cursor = engine.db_connection.execute(
                'INSERT INTO country (country_code, name, continent_id, wikipedia_link, keywords) '
                'VALUES (:country_code, :name, :continent_id, :wikipedia_link, :keywords)',
                country_dict
            )
            engine.db_connection.commit()
            new_id = cursor.lastrowid
            yield CountrySavedEvent(Country(new_id, *country_dict.values()))
        except Exception as e:
            yield SaveCountryFailedEvent(f'Failed to save country related event: {e}')

    # User saves a modified country into the database
    elif isinstance(event, SaveCountryEvent):
        country = event.country()
        try:
            country_lst = list(country)[1:]
            engine.db_connection.execute(
                'Update country '
                'Set country_code = ?, name = ?, continent_id = ?, wikipedia_link = ?, keywords = ? '
                'WHERE country_id = ? ',
                country_lst + [country.country_id]
            )
            engine.db_connection.commit()
            yield CountrySavedEvent(Country(country.country_id, *country_lst))
        except Exception as e:
            yield SaveCountryFailedEvent(f'Failed to save country related event: {e}')