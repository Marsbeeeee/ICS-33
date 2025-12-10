from p2app.events import *


def region_related_events(engine, event):
    # User initiates a search for regions
    if isinstance(event, StartRegionSearchEvent):
        try:
            region_code = event.region_code()
            local_code = event.local_code()
            name = event.name()
            rows = engine.db_connection.execute(
                'SELECT * '
                'FROM region '
                'WHERE region_code = ? OR local_code = ? OR name = ?',
                (region_code, local_code, name)
            ).fetchall()
            for row in rows:
                if row:
                    yield RegionSearchResultEvent(Region(*row))
        except Exception as e:
            yield ErrorEvent(f'Failed to fetch region related event: {e}')

    # User loads a region from the database to edit it
    elif isinstance(event, LoadRegionEvent):
        try:
            row = engine.db_connection.execute(
                'SELECT * '
                'FROM region '
                'WHERE region_id = ? ',
                (event.region_id(),)
            ).fetchone()
            if row:
                yield RegionLoadedEvent(Region(*row))
        except Exception as e:
            yield ErrorEvent(f'Failed to fetch region related event: {e}')

    # User saves a new region into the database
    elif isinstance(event, SaveNewRegionEvent):
        region = event.region()
        try:
            region_dict = {key: value for key, value in region._asdict().items()}
            del region_dict['region_id']
            cursor = engine.db_connection.execute(
                'INSERT INTO region(region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords)'
                'VALUES (:region_code, :local_code, :name, :continent_id, :country_id, :wikipedia_link, :keywords)',
                region_dict
            )
            engine.db_connection.commit()
            region_id = cursor.lastrowid
            yield RegionSavedEvent(Region(region_id, *region_dict.values()))
        except Exception as e:
            yield SaveRegionFailedEvent(f'Failed to save region related event: {e}')

    # User saves a modified region into the database
    elif isinstance(event, SaveRegionEvent):
        region = event.region()
        try:
            region_lst = list(region)[1:]
            engine.db_connection.execute(
                'UPDATE region '
                'SET region_code = ?, local_code = ?, '
                'name = ?, continent_id = ?, country_id = ?, wikipedia_link = ?, keywords = ? '
                'WHERE region_id = ? ',
                region_lst + [region.region_id]
            ).fetchone()
            engine.db_connection.commit()
            yield RegionSavedEvent(Region(region.region_id, *region_lst))
        except Exception as e:
            yield SaveRegionFailedEvent(f'Failed to save region related event: {e}')