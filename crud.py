import sqlite3
from datetime import date

# might need: function that checks proper date format (YYYY-MM-DD?)
# need: checker if name already exists


# new ideas
class Manga:
    db_file = "/database/mangadb.db"
    fields = {'name', 'link', 'current_ch', 'recent_ch', 'interval', 'upDate', 'ongoing'}
    fieldtypes = {
        'name': 'str or None',
        'link': 'str or None',
        'current_ch': 'float, int or NoneType',
        'recent_ch': 'float, int or NoneType',
        'interval': 'int or NoneType',
        'upDate': 'datetime.date or NoneType',
        'ongoing': 'integer (1 or 0) or boolean'
    }

    def __init__(self, name=None, link=None, current_ch=None, recent_ch=None, interval=None,
                 up_date=None, ongoing=None, details=None):
        self.name = None
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
                'upDate': up_date,
                'ongoing': ongoing
            }
        self.update_details(details)

    def update_details(self, details):
        # check
        self.check_details(details)
        # required 'name' key
        if self.name is None:
            return "No 'name' attribute."

        keys = details.keys()
        for key in keys:
            if key == 'name':
                self.name = details[key]
            elif key == 'link':
                self.link = details[key]
            elif key == 'current_ch':
                self.current_ch = details[key]
            elif key == 'recent_ch':
                self.recent_ch = details[key]
            elif key == 'interval':
                self.interval = details[key]
            elif key == 'upDate':
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

        if {*keys} <= Manga.fields:
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
            elif key == 'upDate' and datatype is date:
                continue
            elif key == 'ongoing' and datatype in [int, bool]:
                continue
            raise TypeError(f"{key} must be of type {Manga.fieldtypes[key]}.")  # TypeError

        # ongoing format check
        if details['ongoing'] is not None:
            if isinstance(details['ongoing'], int):
                if details['ongoing'] not in (1, 0):
                    raise ValueError("'ongoing' detail must be boolean or integer (1 or 0 only).")

    def details(self):
        return {
            'name': self.name,
            'link': self.link,
            'current_ch': self.current_ch,
            'recent_ch': self.recent_ch,
            'interval': self.interval,
            'upDate': self.up_date
        }


# Create
def new_manga(manga):
    is_manga_obj(manga)

    connect = sqlite3.connect(Manga.db_file)
    cursor = connect.cursor()

    cursor.execute("""
        INSERT INTO Manga (name, link, current_ch, recent_ch, interval, upDate) 
        VALUES (?, ?, ?, ?, ?, ?)
        """, (manga.name, manga.link, manga.recent_ch, manga.current_ch, manga.interval, manga.up_date))

    connect.commit()
    connect.close()


# Read
def get_manga(name):
    pass


# Update
def update_manga(manga):
    try:
        details = manga.details()
    except AttributeError:
        raise TypeError("Must pass a Manga object.")
    if manga.name is None:
        raise AttributeError("Manga object must have attribute 'name'.")

    upd_params = [(key, details[key], details['name']) for key in details.keys()]

    connect = sqlite3.connect(Manga.db_file)
    cursor = connect.cursor()

    cursor.executemany("UPDATE Manga SET ? = ? WHERE name = ?", upd_params)

    connect.commit()
    connect.close()


def rename_manga(name, new_name):
    if not if_manga_exists(name):
        return f"No manga with name {name} in storage."

    connect = sqlite3.connect(Manga.db_file)
    cursor = connect.cursor()
    cursor.execute("UPDATE Manga SET name = ? WHERE name = ?", (new_name, name))
    connect.commit()
    connect.close()
    return f"{name} renamed to {new_name}."


# Delete
def del_manga(name):
    if not if_manga_exists(name):
        return f"No manga with name {name} in storage."

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

# -------OLD IDEAS---------
# db_file = "/database/mangadb.db"
# fields = {'name', 'link', 'current_ch', 'recent_ch', 'interval', 'upDate'}
# fieldtypes = {
#     'name': 'str or None',
#     'link': 'str or None',
#     'current_ch': 'float, int or None',
#     'recent_ch': 'float, int or None',
#     'interval': 'int or None',
#     'upDate': 'str or None'
# }

# def check_details(details):
#     # check if details is None or is a dictionary
#     try:
#         keys = details.keys()
#     except AttributeError:
#         return "Passed parameter is not a dict"  # TypeError
#
#     if {*keys} <= fields:
#         return "Keys are not fieldnames."  # KeyError
#
#     # Type Check
#     for key in keys:
#         if details[key] is None:
#             continue
#
#         datatype = type(details[key])
#         if key in ['name', 'link', 'upDate'] and datatype is str:
#             continue
#         elif key in ['current_ch', 'recent_ch'] and datatype in [float, int]:
#             continue
#         elif key == 'interval' and datatype is int:
#             continue
#         return f"{key} must be of type {fieldtypes[key]}."  # TypeError
#
#     # Date Format Check
#
#     return True


# def new_manga(name, details=None):
#     connect = sqlite3.connect(db_file)
#     cursor = connect.cursor()
#
#     cursor.execute("INSERT INTO Manga (name) VALUES (?)", (name,))
#
#     connect.commit()
#     connect.close()
#
#     if details is not None:
#         update_details(details)


# ---------UPDATING----------
# def update_name(name, new_name):
#     connect = sqlite3.connect(db_file)
#     cursor = connect.cursor()
#     cursor.execute("UPDATE Manga SET name = ? WHERE name = ?", (new_name, name))
#     connect.commit()
#     connect.close()


# def update_details(details):
#     # check
#     check = check_details(details)
#     if not check:
#         return check
#     # required 'name' key
#     try:
#         name = details['name']
#     except KeyError:
#         return "No 'name' key passed in dict."
#
#     # check if all keys are fieldnames
#     keys = details.keys()
#     if {*keys} <= fields:
#         return "Wrong details passed."
#
#     upd_params = [(key, details[key], name) for key in keys]
#
#     connect = sqlite3.connect(db_file)
#     cursor = connect.cursor()
#
#     cursor.executemany("UPDATE Manga SET ? = ? WHERE name = ?", upd_params)
#
#     connect.commit()
#     connect.close()
# -------------------------------


# ---------DELETING-----------
# def del_manga(name):
#     connect = sqlite3.connect(db_file)
#     cursor = connect.cursor()
#     cursor.execute("DELETE FROM Manga WHERE name = ?", (name,))
#     connect.commit()
#     connect.close()
# ---------------------------
# def list_manga():
#     pass
