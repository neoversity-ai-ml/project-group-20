from address_book_bot.models import AddressBook
from address_book_bot.utils import input_error, validate_args


@input_error
@validate_args(min_args=1, error_message="Please provide note text.")
def add_note(args, book: AddressBook):
    text = " ".join(args)
    book.add_note(text)
    return "Note added."


def show_notes(_args, book: AddressBook):
    if not book.notes:
        return "No notes found."
    return "\n".join(f"{i}. {note}" for i, note in enumerate(book.notes, 1))


@input_error
@validate_args(min_args=1, max_args=1, error_message="Please provide note number.")
def delete_note(args, book: AddressBook):
    index = int(args[0]) - 1
    book.delete_note(index)
    return "Note deleted."


@input_error
@validate_args(min_args=1, error_message="Please provide a keyword to search for.")
def search_notes(args, book: AddressBook):
    keyword = " ".join(args)
    notes = book.search_notes(keyword)
    if not notes:
        return "No notes found."
    return "\n".join(str(note) for note in notes)


@input_error
@validate_args(min_args=2, error_message="Please provide note number and new text.")
def edit_note(args, book: AddressBook):
    index = int(args[0]) - 1
    new_text = " ".join(args[1:])
    book.edit_note(index, new_text)
    return "Note updated."
