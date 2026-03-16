from rich import box
from rich.console import Console
from rich.table import Table

console = Console()


def print_success(msg: str):
    console.print(f"[bold green]{msg}[/bold green]")


def print_error(msg: str):
    console.print(f"[bold red]{msg}[/bold red]")


def print_info(msg: str):
    console.print(f"[yellow]{msg}[/yellow]")


def print_commands_table():
    table = Table(title="Assistant Bot Commands", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    table.add_row("[bold]General[/bold]", "")
    table.add_row("hello", "Greet the bot")
    table.add_row("help", "Show this table")
    table.add_row("close / exit", "Exit the program")

    table.add_section()
    table.add_row("[bold]Contacts[/bold]", "")
    table.add_row("add <name> <phone>", "Add a new contact")
    table.add_row("change <name> <old> <new>", "Change a phone number")
    table.add_row("phone <name>", "Show phone number(s)")
    table.add_row("all", "Show all contacts")
    table.add_row("search <query>", "Search contacts")
    table.add_row("delete-phone <name> <phone>", "Delete a phone")

    table.add_section()
    table.add_row("[bold]Birthday[/bold]", "")
    table.add_row("add-birthday <name> <DD.MM.YYYY>", "Add or update birthday")
    table.add_row("show-birthday <name>", "Show birthday")
    table.add_row("birthdays <days>", "Upcoming birthdays")

    table.add_section()
    table.add_row("[bold]Address & Email[/bold]", "")
    table.add_row("add-address <name> <address>", "Add address")
    table.add_row("change-address <name> <address>", "Change address")
    table.add_row("delete-address <name>", "Delete address")
    table.add_row("add-email <name> <email>", "Add email")
    table.add_row("show-email <name>", "Show email")
    table.add_row("change-email <name> <email>", "Change email")
    table.add_row("delete-email <name>", "Delete email")

    table.add_section()
    table.add_row("[bold]Notes[/bold]", "")
    table.add_row("add-note <text>", "Add a new note")
    table.add_row("show-notes", "Show all notes")
    table.add_row("sort-notes", "Sort and show notes")
    table.add_row("find-note <keyword>", "Search notes by keyword")
    table.add_row("search-tag <tag>", "Search notes by tag")
    table.add_row("edit-note <number> <text>", "Edit a note")
    table.add_row("delete-note <number>", "Delete a note")

    console.print(table)
