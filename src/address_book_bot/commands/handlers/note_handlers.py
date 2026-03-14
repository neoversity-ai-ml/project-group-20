from address_book_bot.models import AddressBook
from address_book_bot.utils import input_error


@input_error
def add_note(args, book: AddressBook):
    text = " ".join(args)
    book.add_note(text)
    return "Note added."


def show_notes(_args, book: AddressBook):
    if not book.notes:
        return "No notes found."
    return "\n".join(f"{i}. {note}" for i, note in enumerate(book.notes, 1))


@input_error
def delete_note(args, book: AddressBook):
    index = int(args[0]) - 1
    book.delete_note(index)
    return "Note deleted."


@input_error
def search_notes(args, book: AddressBook):
    keyword = " ".join(args)
    notes = book.search_notes(keyword)
    if not notes:
        return "No notes found."
    return "\n".join(str(note) for note in notes)


@input_error
def edit_note(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError
    index = int(args[0]) - 1
    new_text = " ".join(args[1:])
    book.edit_note(index, new_text)
    return "Note updated."

@input_error
def search_by_tag(args, book: AddressBook):
    if not args:
        return "Please provide a tag."
    tag = args[0]
    notes = book.search_notes_by_tag(tag)
    if not notes:
        return f"No notes found with tag: {tag}"
    return "\n".join(str(note) for note in notes)

@input_error
def sort_notes(args, book: AddressBook):
    if not book.notes:
        return f"No notes found to sort."
    book.sort_notes_by_tags()
    result = []
    for i, note in enumerate(book.notes, 1):
        tags_str = f"[{', '.join(note.tags)}]" if hasattr(note, 'tags') and note.tags else "[no tags]"
        result.append(f"{i}. {tags_str} {note.value}")

    return "\n".join(result)