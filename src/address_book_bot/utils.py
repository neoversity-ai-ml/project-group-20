from functools import wraps


def input_error(func):
    """Decorator to handle common input errors."""

    @wraps(func)
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


def validate_args(min_args=None, max_args=None, error_message="Invalid number of arguments."):
    def decorator(func):
        @wraps(func)
        def wrapper(args, *rest, **kwargs):
            argc = len(args)

            if min_args is not None and argc < min_args:
                return error_message
            if max_args is not None and argc > max_args:
                return error_message

            return func(args, *rest, **kwargs)

        return wrapper

    return decorator


def parse_input(user_input):
    """Parses user input into a command and arguments."""
    cmd, *args = user_input.split()
    return cmd.lower(), *args
