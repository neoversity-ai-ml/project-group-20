from address_book_bot.commands.resolvers import CommandResolver, FuzzyCommandResolver
from address_book_bot.commands.handlers.contact_handlers import (
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
    add_address,
    add_email,
    show_email,
    delete_phone,
    delete_email,
    delete_address,
    search_contacts,
)
from address_book_bot.commands.handlers.note_handlers import (
    add_note,
    show_notes,
    search_notes,
    edit_note,
    delete_note,
)


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


DESCRIPTION_TEXT = """\
        Available commands:

        hello                                   - Greet the bot
        close / exit                            - Exit the program

        Contacts:
        add <name> <phone>                      - Add a new contact
        change <name> <old_phone> <new_phone>   - Change a contact's phone number
        phone <name>                            - Show a contact's phone number(s)
        all                                     - Show all contacts
        search <query>                          - Search contacts by name or phone

        add-birthday <name> <DD.MM.YYYY>        - Add a contact's birthday
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
        find-note <keyword>                     - Search for notes by keyword
        edit-note <note_number> <new_text>      - Edit an existing note
        delete-note <note_number>               - Delete a note by its number"""
