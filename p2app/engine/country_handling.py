"""File that consists of functions to handle country events"""
import sqlite3
import p2app.events.continents
from p2app.events.countries import Country

def start_country_search(event, connection):
    """Searches database for country values"""
    if event.country_code() is not None and event.name() is not None:
        query = "SELECT * FROM country WHERE country_code = ? and name = ?;"
        cursor = connection.execute(query, (event.country(), event.name()))
    elif event.country_code() is None and event.name() is not None:
        query = "SELECT * FROM country WHERE name = ?;"
        cursor = connection.execute(query, (event.name(),))
    elif event.country_code() is not None and event.name() is None:
        query = "SELECT * FROM country WHERE country_code = ?;"
        cursor = connection.execute(query, (event.country_code(),))
    data = cursor.fetchall()
    cursor.close()
    count_list = []
    for values in data:
        cont = Country(values[0], values[1], values[2], values[3], values[4], values[5])
        cont_class = p2app.events.CountrySearchResultEvent(cont)
        count_list.append(cont_class)
    return count_list

def load_country(event, connection):
    """Loads country"""
    try:
        query = "SELECT * FROM country WHERE country_id = ?;"
        cursor = connection.execute(query, (event.country_id(),))
        data = cursor.fetchone()
        cursor.close()
        cont_list = []
        cont = Country(data[0], data[1], data[2], data[3], data[4], data[5])
        cont_class = p2app.events.CountryLoadedEvent(cont)
        cont_list.append(cont_class)
        return cont_list
    except:
        return p2app.events.ErrorEvent(message="Something Has Gone Wrong, Please Try Again")

def new_country_event(event, connection):
    """Creates a new country"""
    query = "SELECT country_id FROM country ORDER BY country_id DESC LIMIT 1;"
    cursor = connection.execute(query)
    last_row_continent_id = cursor.fetchone()
    last_row_continent_id = last_row_continent_id[0]
    cursor.close()
    last_row_continent_id += 1
    edit_query = "INSERT INTO country (country_id, country_code, name, continent_id, wikipedia_link, keywords) VALUES(?, ?, ?, ?, ?, ?);"
    country_t = event.country()
    if country_t.wikipedia_link is None:
        country_t = Country(country_t.country_id, country_t.country_code, country_t.name, country_t.continent_id, '', country_t.keywords)
    try:
        connection.execute(edit_query, (last_row_continent_id, country_t.country_code, country_t.name, country_t.continent_id, country_t.wikipedia_link, country_t.keywords))
        connection.commit()
        new_count = Country(last_row_continent_id, country_t.country_code, country_t.name, country_t.continent_id, country_t.wikipedia_link, country_t.keywords)
        new_count_class = p2app.events.CountrySavedEvent(new_count)
        return new_count_class
    except sqlite3.IntegrityError:
        return p2app.events.SaveCountryFailedEvent(reason="Country Cannot Be Saved! Make Sure Continent Exists!")

def edit_country_event(event, connection):
    """Edits a selected country in UI"""
    edit_query = "UPDATE country SET country_code = ?, name = ?, continent_id = ?, wikipedia_link = ?, keywords = ? WHERE country_id = ?"
    country_t = event.country()
    if country_t.wikipedia_link is None:
        country_t = Country(country_t.country_id, country_t.country_code, country_t.name, country_t.continent_id, '', country_t.keywords)
    try:
        connection.execute(edit_query, (country_t.country_code, country_t.name, country_t.continent_id,country_t.wikipedia_link, country_t.keywords, country_t.country_id))
        connection.commit()
        new_count = Country(country_t.country_id, country_t.country_code, country_t.name,
                        country_t.continent_id, country_t.wikipedia_link, country_t.keywords)
        new_count_class = p2app.events.CountrySavedEvent(new_count)
        return new_count_class
    except sqlite3.IntegrityError:
        return p2app.events.SaveCountryFailedEvent(reason = "Country Cannot Be Saved! Make Sure Continent Exists!")

