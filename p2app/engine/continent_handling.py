"""File that consists of functions to handle continent events"""
import sqlite3
import p2app.events.continents
from p2app.events.continents import Continent
def start_continent_search(event, connection):
    """Searches database for values"""
    if event.continent_code() is not None and event.name() is not None:
        query = "SELECT * FROM continent WHERE continent_code = ? and name = ?;"
        cursor = connection.execute(query, (event.continent_code(), event.name()))
    elif event.continent_code() is None and event.name() is not None:
        query = "SELECT * FROM continent WHERE name = ?;"
        cursor = connection.execute(query, (event.name(),))
    elif event.continent_code() is not None and event.name() is None:
        query = "SELECT * FROM continent WHERE continent_code = ?;"
        cursor = connection.execute(query, (event.continent_code(),))
    data = cursor.fetchall()
    cursor.close()
    cont_list = []
    for values in data:
        cont = Continent(values[0], values[1], values[2])
        cont_class = p2app.events.ContinentSearchResultEvent(cont)
        cont_list.append(cont_class)
    return cont_list

def load_continent(event, connection):
    """Loads continent"""
    try:
        query = "SELECT * FROM continent WHERE continent_id = ?;"
        cursor = connection.execute(query, (event.continent_id(),))
        data = cursor.fetchone()
        cursor.close()
        cont_list = []
        cont = Continent(data[0], data[1], data[2])
        cont_class = p2app.events.ContinentLoadedEvent(cont)
        cont_list.append(cont_class)
        return cont_list
    except:
        return p2app.events.ErrorEvent(message = "Something Has Gone Wrong, Please Try Again")

def new_continent(event, connection):
    """Creates new continent"""
    query = "SELECT continent_id FROM continent ORDER BY continent_id DESC LIMIT 1;"
    cursor = connection.execute(query)
    last_row_continent_id = cursor.fetchone()
    last_row_continent_id = last_row_continent_id[0]
    cursor.close()
    last_row_continent_id += 1
    edit_query = "INSERT INTO continent (continent_id, continent_code, name) VALUES(?, ?, ?);"
    continent_named_tuple = event.continent()
    try:
        connection.execute(edit_query, (last_row_continent_id, continent_named_tuple.continent_code, continent_named_tuple.name))
        connection.commit()
        new_cont = Continent(last_row_continent_id, continent_named_tuple.continent_code, continent_named_tuple.name)
        new_cont_class = p2app.events.ContinentSavedEvent(new_cont)
        return new_cont_class
    except sqlite3.IntegrityError:
        return p2app.events.SaveContinentFailedEvent(reason="There is a continent with that code already!")

def edit_continent(event, connection):
    """Edits a selected continent in UI"""
    edit_query = "UPDATE continent SET continent_code = ?, name = ? WHERE continent_id = ?;"
    continent_named_tuple = event.continent()
    try:
        connection.execute(edit_query, (continent_named_tuple.continent_code, continent_named_tuple.name, continent_named_tuple.continent_id))
        connection.commit()
        new_cont = Continent(continent_named_tuple.continent_id, continent_named_tuple.continent_code, continent_named_tuple.name)
        new_cont_class = p2app.events.ContinentSavedEvent(new_cont)
        return new_cont_class
    except sqlite3.IntegrityError:
        return p2app.events.SaveContinentFailedEvent(reason='There is a continent with that code already!')