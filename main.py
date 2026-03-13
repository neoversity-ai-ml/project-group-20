from data_loading import load_data, save_data
from models import AddressBook, Record
from utils import input_error, validate_args, parse_input
from command_resolvers import CommandResolver, FuzzyCommandResolver


@input_error
@validate_args(
    min_args=2,
    max_args=2,
    error_message="Please provide only contact name and phone number.",
)
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
@validate_args(
    min_args=3,
    max_args=3,
    error_message="Please provide only contact name and existing/new phone numbers.",
)
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact changed."
    raise KeyError


@input_error
@validate_args(
    min_args=1, max_args=1, error_message="Please provide only name to show the phone."
)
def show_phone(args, book: AddressBook):
    (name,) = args
    record = book.find(name)
    if record:
        if record.phones:
            return "; ".join(p.value for p in record.phones)
        else:
            return "No phone numbers found for this contact."
    raise KeyError


def show_all(_args, book: AddressBook):
    if not book.data:
        return "No contacts found."
    return "\n".join(str(record) for record in book.data.values())


@input_error
@validate_args(
    min_args=2, max_args=2, error_message="Please provide only contact name and birthday."
)
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    raise KeyError


@input_error
@validate_args(
    min_args=1, max_args=1, error_message="Please provide only name to show the birthday."
)
def show_birthday(args, book: AddressBook):
    (name,) = args
    record = book.find(name)
    if record and record.birthday:
        return str(record.birthday)
    if record:
        return "Birthday not set for this contact."
    raise KeyError


@input_error
@validate_args(
    min_args=1,
    max_args=1,
    error_message="Please provide the number of days to check for upcoming birthdays.",
)
def birthdays(args, book: AddressBook):
    """Shows contacts with birthdays in the upcoming week."""

    if not args[0].isdigit():
        raise ValueError(
            "Please provide the number of days to check for upcoming birthdays."
        )

    (days,) = args
    days = int(days)

    if days > 365:
        raise ValueError("Days must be a positive number and not exceed 365.")

    birthdays_by_day = book.get_upcoming_birthdays(days)
    if not birthdays_by_day:
        return "No upcoming birthdays during requested period."

    output = []
    for entry in birthdays_by_day:
        d = entry["congratulation_date"]
        output.append(f"{d.strftime('%d.%m.%Y')} {entry['name']} ({d.strftime('%A')})")

    return (
        "\n".join(output) if output else "No upcoming birthdays during requested period."
    )


@input_error
@validate_args(min_args=2, error_message="Please provide name and address: name address.")
def add_address(args, book: AddressBook):
    name, *address_parts = args
    address = " ".join(address_parts)

    record = book.find(name)
    if record:
        record.add_address(address)
        return "Address added."
    raise KeyError


@input_error
@validate_args(min_args=2, max_args=2, error_message="Please provide name and email.")
def add_email(args, book: AddressBook):
    name, email = args
    record = book.find(name)
    if record:
        record.add_email(email)
        return "Email added."
    raise KeyError


@input_error
@validate_args(min_args=1, max_args=1, error_message="Please provide only contact name.")
def show_email(args, book: AddressBook):
    (name,) = args
    record = book.find(name)

    if record:
        email = record.email or "Email not set for this contact."
        return email
    raise KeyError


@input_error
@validate_args(
    min_args=2,
    max_args=2,
    error_message="Please provide only contact name and phone number.",
)
def delete_phone(args, book: AddressBook):
    name, phone = args
    record = book.find(name)

    if record:
        record.remove_phone(phone)
        return f"Phone {phone} removed."
    raise KeyError


@input_error
@validate_args(min_args=1, max_args=1, error_message="Please provide only contact name.")
def delete_email(args, book: AddressBook):
    (name,) = args
    record = book.find(name)

    if record:
        record.remove_email()
        return "Email removed."
    raise KeyError


@input_error
@validate_args(min_args=1, max_args=1, error_message="Please provide only contact name.")
def delete_address(args, book: AddressBook):
    (name,) = args
    record = book.find(name)

    if record:
        record.remove_address()
        return "Address removed."
    raise KeyError


@input_error
@validate_args(
    min_args=1, max_args=1, error_message="Please provide some query to search for."
)
def search_contacts(args, book: AddressBook):
    (query,) = args
    results = book.search(query)

    if not results:
        return "No contacts found."
    return "\n".join(str(record) for record in results)


command_resolver = CommandResolver(
    [
        (r"hi|hey|привіт", ("hello",)),
        (r"quit|break", ("exit", "close")),
        (r"insert|create", ("add Name 1234567890", "add-birthday Name 01.01.1990")),
        (
            r"edit|modify",
            ("change Name 1234567890 1234567891", "add-birthday Name 01.01.1990"),
        ),
        (r"del|delete|remove", ("delete contact", "delete birthday")),
        (r"show|display|list", ("all", "birthdays", "show-birthday Name", "phone Name")),
        (
            r"birth|day",
            ("birthdays", "add-birthday Name 01.01.1990", "show-birthday Name"),
        ),
        (r"find|call|number", ("phone Name", "change Name 1234567890 1234567891")),
    ]
)


fuzzy_resolver = FuzzyCommandResolver(
    {
        "hello": "hello",
        "exit": "exit",
        "close": "close",
        "add": "add Name 1234567890",
        "add-birthday": "add-birthday Name 01.01.1990",
        "change": "change Name 1234567890 1234567891",
        "show-birthday": "show-birthday Name",
        "all": "all",
        "birthdays": "birthdays",
        "phone": "phone Name",
        "add-note": "add-note some text",
        "notes": "notes",
        "find-note": "find-note keyword",
        "edit-note": "edit-note 1 new text",
        "delete-note": "delete-note 1",
    }
)


def hello(_args, _book):
    return "How can I help you?"


@input_error
def add_note(args, book: AddressBook):
    text = " ".join(args)
    book.add_note(text)
    return "Note added."


def show_notes(args, book: AddressBook):
    return book.show_notes()


@input_error
def delete_note(args, book: AddressBook):
    index = int(args[0]) - 1
    book.delete_note(index)
    return "Note deleted."


@input_error
def search_notes(args, book: AddressBook):
    keyword = " ".join(args)
    return book.search_notes(keyword)


@input_error
def edit_note(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError
    index = int(args[0]) - 1
    new_text = " ".join(args[1:])
    book.edit_note(index, new_text)
    return "Note updated."


COMMANDS = {
    "add-note": add_note,
    "show-notes": show_notes,
    "find-note": search_notes,
    "edit-note": edit_note,
    "delete-note": delete_note,
    "hello": hello,
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": show_all,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
    "add-address": add_address,
    "add-email": add_email,
    "show-email": show_email,
    "change-email": add_email,
    "change-address": add_address,
    "delete-phone": delete_phone,
    "delete-email": delete_email,
    "delete-address": delete_address,
    "search": search_contacts,
}


def suggest_command(user_input, command, args):
    return (
        command_resolver.resolve(user_input)
        or fuzzy_resolver.resolve(command.lower(), args)
        or fuzzy_resolver.resolve(user_input, [])
    )


def print_help():
    return """
Available commands:
hello
add <name> <phone>
change <name> <old_phone> <new_phone>
phone <name>
all
add-birthday <name> <DD.MM.YYYY>
show-birthday <name>
birthdays

add-note <text>
notes
find-note <keyword>
edit-note <note_number> <new_text>
delete-note <note_number>

close / exit
""".strip()


def main():
    """Main function to run the assistant bot."""

    book = load_data(default_factory=AddressBook)
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, *args = parse_input(user_input)

        if command in {"close", "exit"}:
            print("Good bye!")
            break

        handler = COMMANDS.get(command)

        if handler:
            print(handler(args, book))
        else:
            fallbacks = suggest_command(user_input, command, args)
            if fallbacks:
                print("Command not found. Did you mean:")
                for fallback in fallbacks:
                    print(f"  {fallback}")
            else:
                print("Invalid command.")

        save_data(book)


if __name__ == "__main__":  # pragma: no cover
    main()
