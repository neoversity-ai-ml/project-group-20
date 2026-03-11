from models import AddressBook, Record
from data_loading import save_data, load_data


def input_error(func):
    """Decorator to handle common input errors."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command format. Please provide all necessary arguments."
    return inner


def parse_input(user_input):
    """Parses user input into a command and arguments."""
    cmd, *args = user_input.split()
    return cmd.lower(), *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact changed."
    raise KeyError


@input_error
def show_phone(args, book: AddressBook):
    name, = args
    record = book.find(name)
    if record:
        return '; '.join(p.value for p in record.phones)
    raise KeyError


def show_all(book: AddressBook):
    if not book.data:
        return "No contacts found."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    raise KeyError


@input_error
def show_birthday(args, book: AddressBook):
    name, = args
    record = book.find(name)
    if record and record.birthday:
        return str(record.birthday)
    if record:
        return "Birthday not set for this contact."
    raise KeyError


def birthdays(book: AddressBook):
    """Shows contacts with birthdays in the upcoming week."""
    birthdays_by_day = book.get_upcoming_birthdays()
    if not birthdays_by_day:
        return "No upcoming birthdays in the next week."

    output = []
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    for day in week_days:
        if birthdays_by_day[day]:
            output.append(f"{day}: {', '.join(birthdays_by_day[day])}")

    return "\n".join(output) if output else "No upcoming birthdays in the next week."

def add_email(args, book: AddressBook):
    name, email = args
    record = book.find(name)
    if record:
        record.add_email(email)
        return "Email added."
    raise KeyError

def show_email(args, book: AddressBook):
    name, = args
    record = book.find(name)
    if record and record.email:
        return str(record.email)
    if record:
        return "Email not set for this contact."
    raise KeyError

def main():
    """Main function to run the assistant bot."""

    book = load_data(default_factory=AddressBook)
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        elif command == "email":
            print(add_email(args, book))
        elif command == "show-email":
            print(show_email(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
