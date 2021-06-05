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


class Manga:
    def __init__(self, name=None, link=None, current_ch=None, recent_ch=None, interval=None,
                 up_date=None):
        self.name = name
        self.link = link
        self.current_ch = current_ch
        self.recent_ch = recent_ch
        self.interval = interval
        self.up_date = up_date


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
