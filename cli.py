import crud
from crud import Manga
import argparse
import datetime as dt
# ALL TEMPORARY

fields = ('name', 'link', 'current_ch', 'recent_ch', 'interval', 'up_date', 'ongoing')


def reset_sequence():  # temporary function
    crud.reset_primary_ids()


def create_details():
    details = {}
    keys_to_pop = []
    for key in fields:
        value = input(f"{key}: ")
        if value == '':
            keys_to_pop.append(key)
        elif value in ['None', 'none', 'Null', 'null']:
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

    for key in keys_to_pop:
        details.pop(key)
    return details


def main():
    parser = argparse.ArgumentParser(description="Test crud operations")
    parser.add_argument("--new", help="list new manga", action="store_const", const="new")
    parser.add_argument("--update", help="update existing manga", action="store_const", const="update")
    parser.add_argument("--delete", help="delete existing manga", nargs='+', metavar="manga name")
    parser.add_argument("--rename", help="rename existing manga", nargs='+', metavar="name / new_name")
    parser.add_argument("--get", help="view existing manga details", nargs='+', metavar="manga name")
    parser.add_argument("--list", help="creates list of manga depending on conditions", action="store_const",
                        const="list")
    args = parser.parse_args()

    if args.new == "new":
        print("new")
        details = create_details()
        manga = Manga(details)
        crud.new_manga(manga)
    elif args.update == "update":
        print("update")
        details = create_details()
        manga = Manga(details)
        crud.update_manga(manga)
    elif args.delete is not None:
        print("delete")
        name = ''
        for word in args.delete:
            name += ' ' + word
        crud.del_manga(name.lstrip())
    elif args.rename is not None:
        print("rename")
        slashpos = args.rename.index('/')
        name = ''
        for word in args.rename[:slashpos]:
            name += ' ' + word

        new_name = ''
        for word in args.rename[slashpos + 1:]:
            new_name += ' ' + word

        crud.rename_manga(name.lstrip(), new_name.lstrip())
    elif args.get is not None:
        print("get")
        name = ''
        for word in args.get:
            name += ' ' + word

        row = crud.get_manga(name.lstrip())
        print(f"name: {row['name']}\n"
              f"link: {row['link']}\n"
              f"current_ch: {row['current_ch']}, recent_ch: {row['recent_ch']}\n"
              f"interval: {row['interval']}\n"
              f"up_date: {row['up_date']}\n"
              f"ongoing: {row['ongoing']}")
    elif args.list == "list":
        print("list")
        details = create_details()
        print(crud.list_manga(details))  # <- needs better visualization


if __name__ == "__main__":
    main()
