import pickle


def save_data(book, filename="addressbook.pkl"):
    """Saves the address book to a file."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl", default_factory=None):
    """Loads the address book from a file."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError as e:
        if default_factory is not None:
            return default_factory()
        else:
            raise e
