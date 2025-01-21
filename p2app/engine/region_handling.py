"""File that consists of functions to handle region events"""
import sqlite3
import p2app.events.regions
from p2app.events.regions import Region

def start_region_search(event, connection):
    """Searches database for region values"""
    conditions = []
    values = []
    if event.region_code() is not None:
        conditions.append(f"region_code = ?")
        values.append(event.region_code())

    if event.local_code() is not None:
        conditions.append(f"local_code = ?")
        values.append(event.local_code())

    if event.name() is not None:
        conditions.append(f"name = ?")
        values.append(event.name())

    where = " AND ".join(conditions)
    edit_query = f"SELECT * FROM region"
    if where:
        edit_query += " WHERE " + where
    print(edit_query)
    cursor = connection.execute(edit_query, values)
    data = cursor.fetchall()
    cursor.close()
    reg_list = []
    for values in data:
        reg = Region(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7])
        reg_class = p2app.events.RegionSearchResultEvent(reg)
        reg_list.append(reg_class)
    return reg_list

def load_region(event, connection):
    """Loads Selected Region from UI"""
    try:
        edit_query = "SELECT * FROM region WHERE region_id = ?;"
        cursor = connection.execute(edit_query, (event.region_id(),))
        data = cursor.fetchone()
        cursor.close()
        reg_list = []
        reg = Region(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        reg_class = p2app.events.RegionLoadedEvent(reg)
        reg_list.append(reg_class)
        return reg_list
    except:
        return p2app.events.ErrorEvent(message="Something Has Gone Wrong, Please Try Again")

def new_region_event(event, connection):
    "Creates New Region"
    query = "SELECT region_id FROM region ORDER BY region_id DESC LIMIT 1;"
    cursor = connection.execute(query)
    last_row_continent_id = cursor.fetchone()
    last_row_continent_id = last_row_continent_id[0]
    cursor.close()
    last_row_continent_id += 1
    edit_query = "INSERT INTO region (region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
    reg_t = event.region()
    try:
        connection.execute(edit_query, (last_row_continent_id, reg_t.region_code, reg_t.local_code, reg_t.name, reg_t.continent_id, reg_t.country_id, reg_t.wikipedia_link, reg_t.keywords))
        connection.commit()
        new_reg = Region(last_row_continent_id, reg_t.region_code, reg_t.local_code, reg_t.name, reg_t.continent_id, reg_t.country_id, reg_t.wikipedia_link, reg_t.keywords)
        new_reg_class = p2app.events.RegionSavedEvent(new_reg)
        return new_reg_class
    except sqlite3.IntegrityError:
        return p2app.events.SaveRegionFailedEvent(reason="Region Cannot Be Saved, Make Sure Country And Continent Exist!")

def edit_region_event(event, connection):
    """Edits a selected region in UI"""
    edit_query = "UPDATE region SET region_code = ?, local_code = ?, name = ?, continent_id = ?, country_id = ?, wikipedia_link = ?, keywords = ? WHERE region_id = ?"
    reg_t = event.region()
    try:
        connection.execute(edit_query, (reg_t.region_code, reg_t.local_code, reg_t.name, reg_t.continent_id, reg_t.country_id, reg_t.wikipedia_link, reg_t.keywords, reg_t.region_id))
        connection.commit()
        new_reg = Region(reg_t.region_id, reg_t.region_code, reg_t.local_code, reg_t.name, reg_t.continent_id, reg_t.country_id, reg_t.wikipedia_link, reg_t.keywords)
        new_reg_class = p2app.events.RegionSavedEvent(new_reg)
        return new_reg_class
    except sqlite3.IntegrityError:
        return p2app.events.SaveRegionFailedEvent(reason="Region Cannot Be Saved, Make Sure Country And Continent Exist!")