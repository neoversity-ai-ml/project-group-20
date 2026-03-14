from address_book_bot.commands.handlers.contact_handlers import (
    add_address,
    add_birthday,
    add_contact,
    add_email,
    birthdays,
    change_contact,
    delete_address,
    delete_email,
    delete_phone,
    search_contacts,
    show_all,
    show_birthday,
    show_email,
    show_phone,
)
from address_book_bot.commands.handlers.note_handlers import (
    add_note,
    delete_note,
    edit_note,
    search_by_tag,
    search_notes,
    show_notes,
    sort_notes,
)
from address_book_bot.commands.resolvers import CommandResolver, FuzzyCommandResolver

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
        "help": "help",
        "exit": "exit",
        "close": "close",
        "add": "add Name 1234567890",
        "add-birthday": "add-birthday Name 01.01.1990",
        "add-address": "add-address Name 123 Main St",
        "add-email": "add-email Name email@example.com",
        "add-note": "add-note some text",
        "change": "change Name 1234567890 1234567891",
        "change-email": "change-email Name new@example.com",
        "change-address": "change-address Name new address",
        "show-birthday": "show-birthday Name",
        "show-email": "show-email Name",
        "show-notes": "show-notes",
        "all": "all",
        "birthdays": "birthdays",
        "phone": "phone Name",
        "search": "search query",
        "delete-phone": "delete-phone Name 1234567890",
        "delete-email": "delete-email Name",
        "delete-address": "delete-address Name",
        "find-note": "find-note keyword",
        "edit-note": "edit-note 1 new text",
        "delete-note": "delete-note 1",
        "sort-notes": "sort-notes",
        "search-tag": "search-tag any_tag",
    }
)


def hello(_args, _book):
    return "How can I help you?"


def help_command(_args, _book):
    return DESCRIPTION_TEXT


COMMANDS = {
    "add-note": add_note,
    "show-notes": show_notes,
    "find-note": search_notes,
    "edit-note": edit_note,
    "delete-note": delete_note,
    "sort-notes": sort_notes,
    "search-tag": search_by_tag,
    "hello": hello,
    "help": help_command,
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


DESCRIPTION_TEXT = """\
Available commands:

hello                                   - Greet the bot
help                                    - Show available commands
close / exit                            - Exit the program

Contacts:
add <name> <phone>                      - Add a new contact
change <name> <old_phone> <new_phone>   - Change a contact's phone number
phone <name>                            - Show a contact's phone number(s)
all                                     - Show all contacts
search <query>                          - Search contacts by name, phone, email, address, or birthday

add-birthday <name> <DD.MM.YYYY>        - Add or update a contact's birthday
show-birthday <name>                    - Show a contact's birthday
birthdays <days>                        - Show birthdays in the next <days> days

add-address <name> <address>            - Add a contact's address
change-address <name> <new_address>     - Change a contact's address
delete-address <name>                   - Delete a contact's address

add-email <name> <email>                - Add a contact's email
show-email <name>                       - Show a contact's email
change-email <name> <new_email>         - Change a contact's email
delete-email <name>                     - Delete a contact's email

Notes:
add-note <text>                         - Add a new note
show-notes                              - Show all notes
sort-notes                              - Sort all notes and show them
find-note <keyword>                     - Search for notes by keyword
search-tag <tag>                        - Search for notes by tag
edit-note <note_number> <new_text>      - Edit an existing note
delete-note <note_number>               - Delete a note by its number"""
