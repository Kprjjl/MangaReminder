import sqlite3
import datetime


class Manga:
    db_file = "database/mangadb.db"
    fields = {'name', 'link', 'current_ch', 'recent_ch', 'interval', 'up_date', 'ongoing'}
    fieldtypes = {
        'name': 'str or None',
        'link': 'str or None',
        'current_ch': 'float, int or NoneType',
        'recent_ch': 'float, int or NoneType',
        'interval': 'int or NoneType',
        'up_date': 'datetime.date or NoneType',
        'ongoing': 'integer (1 or 0) or boolean'
    }

    def __init__(self, details=None, name=None, link=None, current_ch=None, recent_ch=None, interval=None,
                 up_date=None, ongoing=None):
        # required name key
        if name is None:
            try:
                self.name = details['name']
            except KeyError:
                raise KeyError("No 'name' key.")
        else:
            self.name = name
        self.link = None
        self.current_ch = None
        self.recent_ch = None
        self.interval = None
        self.up_date = None
        self.ongoing = None

        if details is None:
            details = {
                'name': name,
                'link': link,
                'current_ch': current_ch,
                'recent_ch': recent_ch,
                'interval': interval,
                'up_date': up_date,
                'ongoing': ongoing
            }
        self.update_details(details)

    def update_details(self, details):
        # check
        self.check_details(details)
        # required 'name' attribute
        if self.name is None:
            raise AttributeError("No 'name' attribute.")

        keys = details.keys()
        for key in keys:
            if key == 'name':
                self.name = details[key]
            elif key == 'link':
                if details[key] == '':
                    details[key] = None
                self.link = details[key]
            elif key == 'current_ch':
                self.current_ch = details[key]
            elif key == 'recent_ch':
                self.recent_ch = details[key]
            elif key == 'interval':
                self.interval = details[key]
            elif key == 'up_date':
                self.up_date = details[key]
            elif key == 'ongoing':
                if isinstance(details[key], bool):
                    self.ongoing = int(details[key])
                else:
                    self.ongoing = details[key]

    @staticmethod
    def check_details(details):
        # check if details is None or is a dictionary
        try:
            keys = details.keys()
        except AttributeError:
            raise TypeError("Passed parameter is not a dict")  # TypeError

        if not ({*keys} <= Manga.fields):
            raise KeyError("Keys are not fieldnames.")  # KeyError

        # Type Check
        for key in keys:
            if details[key] is None:
                continue

            datatype = type(details[key])
            if key in ['name', 'link'] and datatype is str:
                continue
            elif key in ['current_ch', 'recent_ch'] and datatype in [float, int]:
                continue
            elif key == 'interval' and datatype is int:
                continue
            elif key == 'up_date' and datatype is datetime.date:
                continue
            elif key == 'ongoing' and datatype in [int, bool]:
                continue
            raise TypeError(f"{key} must be of type {Manga.fieldtypes[key]}.")  # TypeError

        # name check
        if 'name' in details:
            if details['name'] == '':
                raise ValueError("'name' detail must be either NoneType or str that is not empty.")
        # ongoing format check
        elif 'ongoing' in details:
            if details['ongoing'] is not None:
                if isinstance(details['ongoing'], int):
                    if details['ongoing'] not in (1, 0):
                        raise ValueError("'ongoing' detail must be boolean or integer (1 or 0 only).")
        # link format check (using regex) (optional)

    def details(self):
        return {
            'name': self.name,
            'link': self.link,
            'current_ch': self.current_ch,
            'recent_ch': self.recent_ch,
            'interval': self.interval,
            'up_date': self.up_date
        }


# Create
def new_manga(manga):
    is_manga_obj(manga)

    connect = sqlite3.connect(Manga.db_file, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connect.cursor()

    query = "INSERT INTO Manga (name, link, current_ch, recent_ch, interval, up_date, ongoing) VALUES (?, ?, ?, ?, ?," \
            " ?, ?) "
    params = (manga.name, manga.link, manga.current_ch, manga.recent_ch, manga.interval, manga.up_date, manga.ongoing)
    cursor.execute(query, params)

    connect.commit()
    connect.close()


# Read
def get_manga(name):
    if not if_manga_exists(name):
        return f"Manga with name {name} not found."

    connect = sqlite3.connect(Manga.db_file, detect_types=sqlite3.PARSE_DECLTYPES)
    connect.row_factory = sqlite3.Row
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Manga WHERE name = ?", (name,))
    row = cursor.fetchone()

    return dict(row)


def list_manga(details):
    Manga.check_details(details)

    connect = sqlite3.connect(Manga.db_file, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connect.cursor()

    query = "SELECT * FROM Manga WHERE"
    params = []
    for key in details:
        query += f" {key} = ? AND"
        params.append(details[key])
    query = query[:-4]
    params = tuple(params)

    cursor.execute(query, params)
    lst = cursor.fetchall()
    return lst


# Update
def update_manga(manga):
    if not if_manga_exists(manga.name):
        raise Exception(f"Manga with name {manga.name} not found.")
    try:
        details = manga.details()
    except AttributeError:
        raise TypeError("Must pass a Manga object.")
    if manga.name is None:
        raise AttributeError("Manga object must have attribute 'name'.")

    keys = details.keys()
    query = ""
    for key in keys:
        query += f" {key} = :{key},"
    query = "UPDATE Manga SET" + query[:-1] + f" WHERE name = '{manga.name}'"

    connect = sqlite3.connect(Manga.db_file, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connect.cursor()

    cursor.execute(query, details)

    connect.commit()
    connect.close()


def rename_manga(name, new_name):
    if not if_manga_exists(name):
        raise Exception(f"No manga with name {name} in storage.")

    connect = sqlite3.connect(Manga.db_file)
    cursor = connect.cursor()
    cursor.execute("UPDATE Manga SET name = ? WHERE name = ?", (new_name, name))
    connect.commit()
    connect.close()
    return f"{name} renamed to {new_name}."


# Delete
def del_manga(name):
    if not if_manga_exists(name):
        raise Exception(f"No manga with name {name} in storage.")

    connect = sqlite3.connect(Manga.db_file)
    cursor = connect.cursor()
    cursor.execute("DELETE FROM Manga WHERE name = ?", (name,))
    connect.commit()
    connect.close()
    return f"{name} deleted from storage."


# Misc
def is_manga_obj(manga):
    if not isinstance(manga, Manga):
        raise TypeError("Must pass a Manga object.")


def if_manga_exists(name):
    connect = sqlite3.connect(Manga.db_file)
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM Manga WHERE name = ?", (name,))
    manga = cursor.fetchall()
    connect.close()

    return False if len(manga) == 0 else True


# Probably temporary
def reset_primary_ids():
    connect = sqlite3.connect(Manga.db_file)
    cursor = connect.cursor()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'Manga'")
    connect.commit()
    connect.close()
    print("Manga sequence has been reset.")
