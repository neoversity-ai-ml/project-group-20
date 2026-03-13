from address_book_bot.models import AddressBook, Record
from address_book_bot.utils import input_error, validate_args


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
