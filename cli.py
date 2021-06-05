import crud
from crud import Manga
import argparse
import datetime as dt
# ALL TEMPORARY

fields = ('name', 'link', 'current_ch', 'recent_ch', 'interval', 'up_date', 'ongoing')


def create_details():
    details = {}
    for key in fields:
        value = input(f"{key}: ")
        if value == '':
            value = None
        elif key in ['current_ch', 'recent_ch']:
            try:
                value = int(float(value)) if int(float(value)) == float(value) else float(value)
            except ValueError:
                print(value, type(value))
                raise ValueError(f"{key} detail must be int, float or NoneType only.")
        elif key == 'interval':
            try:
                value = int(float(value))  # can't properly deal with inputs like 7.5 yet
            except ValueError:
                raise ValueError("'interval' detail must be int or NoneType only.")
        elif key == 'ongoing':
            try:
                value = int(value)
            except ValueError:
                if value in ['True', 'true', 'T', 't']:
                    value = True
                elif value in ['False', 'false', 'F', 'f']:
                    value = False
                else:
                    raise ValueError("'ongoing' detail must be bool, NoneType, or integer (1 or 0)")
        elif key == 'up_date':
            value = dt.datetime.strptime(value, "%Y-%m-%d")
            value = dt.date(value.year, value.month, value.day)

        details[key] = value
    return details


def new_manga():
    details = create_details()
    manga = Manga(details)
    crud.new_manga(manga)


def update_manga():
    details = create_details()
    manga = Manga(details)
    crud.update_manga(manga)


def main():
    parser = argparse.ArgumentParser(description="Test crud operations")
    parser.add_argument("--new", help="list new manga", action="store_const", const="new")
    parser.add_argument("--update", help="update existing manga", action="store_const", const="update")
    parser.add_argument("--delete", help="delete existing manga", metavar="manga name")
    args = parser.parse_args()

    new_manga()
    if args.new == "new":
        print("new")
        new_manga()
    elif args.update == "update":
        print("update")
        update_manga()
    elif args.delete is not None:
        print("delete")
        crud.del_manga(args.delete)


if __name__ == "__main__":
    main()
