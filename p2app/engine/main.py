# p2app/engine/main.py
#
# ICS 33 Spring 2023
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.
import sqlite3
import p2app.events.database
import p2app.engine.continent_handling
import p2app.engine.country_handling
import p2app.engine.region_handling


class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self.connection = None



    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""

        # This is a way to write a generator function that always yields zero values.
        # You'll want to remove this and replace it with your own code, once you start
        # writing your engine, but this at least allows the program to run.

        # Beginning UI Event Handling
        if isinstance(event, p2app.events.OpenDatabaseEvent):
            try:
                """This try block using duck typing to check if the database has the right tables"""
                connection = sqlite3.connect(event.path())
                connection.execute("PRAGMA foreign_keys = ON")
                cursor = connection.execute("SELECT * FROM continent WHERE name = 'Europe';")
                dats = cursor.fetchone()
                cursor.close()
                if dats[1] != 'EU':
                    yield p2app.events.DatabaseOpenFailedEvent(reason='Database is not Correct!')
                cursor = connection.execute("SELECT * FROM country WHERE nax`x`me = 'Egypt';")
                dats = cursor.fetchone()
                cursor.close()
                if dats[1] != 'EG':
                    yield p2app.events.DatabaseOpenFailedEvent(reason='Database is not Correct!')
                cursor = connection.execute("SELECT * FROM region WHERE name = 'Queensland';")
                dats = cursor.fetchone()
                cursor.close()
                if dats[3] != 'Queensland':
                    yield p2app.events.DatabaseOpenFailedEvent(reason='Database is not Correct!')
                self.connection = connection
                yield p2app.events.database.DatabaseOpenedEvent(event.path())
            except sqlite3.OperationalError:
                """Catches the exception where the database doesn't match"""
                yield p2app.events.DatabaseOpenFailedEvent(reason='Database is not Correct!')
            except sqlite3.DatabaseError:
                """Catches the exception where the path leads to a file and not a database"""
                yield p2app.events.DatabaseOpenFailedEvent(reason='Found something that is not a Database!')
        if isinstance(event, p2app.events.QuitInitiatedEvent):
            """Ends application/UI"""
            yield p2app.events.EndApplicationEvent()
        if isinstance(event, p2app.events.CloseDatabaseEvent):
            """Closes database"""
            yield p2app.events.DatabaseClosedEvent()

        # Continent Event Handling
        if isinstance(event, p2app.events.StartContinentSearchEvent):
            event_list = p2app.engine.continent_handling.start_continent_search(event, self.connection)
            yield from event_list
        if isinstance(event, p2app.events.LoadContinentEvent):
            event_list = p2app.engine.continent_handling.load_continent(event, self.connection)
            yield from event_list
        if isinstance(event, p2app.events.SaveNewContinentEvent):
            new_event = p2app.engine.continent_handling.new_continent(event, self.connection)
            yield new_event
        if isinstance(event, p2app.events.SaveContinentEvent):
            edit_event = p2app.engine.continent_handling.edit_continent(event, self.connection)
            yield edit_event

        # Country-related Event Handling
        if isinstance(event, p2app.events.StartCountrySearchEvent):
            event_list = p2app.engine.country_handling.start_country_search(event, self.connection)
            yield from event_list

        if isinstance(event, p2app.events.LoadCountryEvent):
            event_list = p2app.engine.country_handling.load_country(event, self.connection)
            yield from event_list

        if isinstance(event, p2app.events.SaveNewCountryEvent):
            new_event = p2app.engine.country_handling.new_country_event(event, self.connection)
            yield new_event

        if isinstance(event, p2app.events.SaveCountryEvent):
            new_event = p2app.engine.country_handling.edit_country_event(event, self.connection)
            yield new_event

        #Region-related Event Handling
        if isinstance(event, p2app.events.StartRegionSearchEvent):
            event_list = p2app.engine.region_handling.start_region_search(event, self.connection)
            yield from event_list

        if isinstance(event, p2app.events.LoadRegionEvent):
            event_list = p2app.engine.region_handling.load_region(event, self.connection)
            yield from event_list

        if isinstance(event, p2app.events.SaveNewRegionEvent):
            new_event = p2app.engine.region_handling.new_region_event(event, self.connection)
            yield new_event

        if isinstance(event, p2app.events.SaveRegionEvent):
            new_event = p2app.engine.region_handling.edit_region_event(event, self.connection)
            yield new_event