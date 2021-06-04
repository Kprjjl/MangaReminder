import sqlite3
from datetime import datetime

db_file = "/database/mangadb.db"
fields = {'name', 'link', 'current_ch', 'recent_ch', 'interval', 'upDate'}
fieldtypes = {
    'name': 'str or None',
    'link': 'str or None',
    'current_ch': 'float, int or None',
    'recent_ch': 'float, int or None',
    'interval': 'int or None',
    'upDate': 'str or None'
}
# might need: function that checks proper date format (YYYY-MM-DD?)
# need: checker if name already exists


def check_details(details):
    # check if details is None or is a dictionary
    try:
        keys = details.keys()
    except AttributeError:
        return "Passed parameter is not a dict"  # TypeError

    if {*keys} <= fields:
        return "Keys are not fieldnames."  # KeyError

    # Type Check
    for key in keys:
        if details[key] is None:
            continue

        datatype = type(details[key])
        if key in ['name', 'link', 'upDate'] and datatype is str:
            continue
        elif key in ['current_ch', 'recent_ch'] and datatype in [float, int]:
            continue
        elif key == 'interval' and datatype is int:
            continue
        return f"{key} must be of type {fieldtypes[key]}."  # TypeError

    # Date Format Check

    return True


def new_manga(name, details=None):
    connect = sqlite3.connect(db_file)
    cursor = connect.cursor()

    cursor.execute("INSERT INTO Manga (name) VALUES (?)", (name,))

    connect.commit()
    connect.close()

    if details is not None:
        update_details(details)

    # if details is not None and type(details) is dict:
    # try:
    #     keys = details.keys()
    # except AttributeError:
    #     return

    # required_keys = {'link', 'current_ch', 'recent_ch', 'interval', 'upDate'}
    # if (required_keys <= keys) is False:
    #     return "Wrong details passed."

    # accepted_keys = {'name', 'link', 'current_ch', 'recent_ch', 'interval', 'upDate'}
    # if {*keys} <= accepted_keys:
    #     return "Wrong details passed."

    # not_null_keys = []
    # for key in details:
    #     if details[key] is not None:
    #         not_null_keys.append(key)

    # query = ""
    # for key in not_null_keys:
    #     # query += f"UPDATE Manga SET {key} = ? WHERE name = ?;"
    #     query += f" {key} = ?,"
    # query = "UPDATE Manga SET" + query[:-1] + " WHERE name = ?;"
    #
    # not_null_keys.append(name)
    # upd_params = tuple(not_null_keys)
    #
    # cursor.execute(query, upd_params)

    # upd_params = [(key, details[key], name) for key in not_null_keys]
    # cursor.executemany("UPDATE Manga SET ? = ? WHERE name = ?", upd_params)


# ---------UPDATING----------
def update_name(name, new_name):
    connect = sqlite3.connect(db_file)
    cursor = connect.cursor()
    cursor.execute("UPDATE Manga SET name = ? WHERE name = ?", (new_name, name))
    connect.commit()
    connect.close()


def update_details(details):
    # check
    check = check_details(details)
    if not check:
        return check
    # required 'name' key
    try:
        name = details['name']
    except KeyError:
        return "No 'name' key passed in dict."

    # check if all keys are fieldnames
    keys = details.keys()
    if {*keys} <= fields:
        return "Wrong details passed."

    upd_params = [(key, details[key], name) for key in keys]

    connect = sqlite3.connect(db_file)
    cursor = connect.cursor()

    cursor.executemany("UPDATE Manga SET ? = ? WHERE name = ?", upd_params)

    connect.commit()
    connect.close()


# def upd_link(link):
#     pass
#
#
# def upd_current_ch(current_ch):
#     pass
#
#
# def upd_recent_ch(recent_ch):
#     pass
#
#
# def upd_interval(interval):
#     pass
#
#
# def upd_update(up_date):
#     pass
# -------------------------------
# ---------DELETING-----------
def del_manga(name):
    connect = sqlite3.connect(db_file)
    cursor = connect.cursor()
    cursor.execute("DELETE FROM Manga WHERE name = ?", (name,))
    connect.commit()
    connect.close()
# ---------------------------


def list_manga():
    pass
