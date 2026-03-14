[![Python Version](https://img.shields.io/badge/python-3.13.7-blue.svg)](https://www.python.org/)
[![Github Actions - CI](https://github.com/neoversity-ai-ml/project-group-20/actions/workflows/ci.yml/badge.svg)](https://github.com/neoversity-ai-ml/project-group-20/actions/workflows/ci.yml)
[![Codecov Coverage](https://codecov.io/gh/neoversity-ai-ml/project-group-20/graph/badge.svg?token=A26ZHG7CU6)](https://codecov.io/gh/neoversity-ai-ml/project-group-20)
[![CodeFactor](https://www.codefactor.io/repository/github/neoversity-ai-ml/project-group-20/badge)](https://www.codefactor.io/repository/github/neoversity-ai-ml/project-group-20)

![Made with VHS](./demo/demo.gif)

---

### Чек-ліст виконання проєкту

#### Основні вимоги

**Зберігання та управління контактами**
- ✅ Додавання нових контактів із іменами, адресами, номерами телефонів, електронною поштою та днями народження
- ✅ Пошук контактів за різними критеріями (наприклад, за іменем)
- ✅ Редагування та видалення контактів
- ✅ Виведення списку контактів, у яких день народження через задану кількість днів від поточної дати
- ✅ Валідація номера телефону та електронної пошти під час додавання або редагування контакту

**Зберігання та управління нотатками**
- ✅ Можливість додавання текстових нотаток
- ✅ Пошук, редагування та видалення нотаток

**Зберігання даних**
- ✅ Всі дані (контакти, нотатки) повинні зберігатися на жорсткому диску у папці користувача
- ✅ Помічник може бути перезапущений без втрати даних

#### Додаткові вимоги

> 💡 Ви також можете розширити/змінити функціонал проєкту на свій розсуд. Ми пропонуємо додаткове ускладнене завдання, для тих хто реалізує основний функціонал.
>
> Персональний помічник повинен додатково вміти:
> 1. Додавати в нотатки "теги", ключові слова, що описують тему та предмет запису;
> 2. Здійснювати пошук та сортування нотаток за ключовими словами (тегами);
>
> _Додаткове завдання не обов’язкове, його можна виконувати за власним бажанням. Зверніть увагу на те, що ви можете отримати 10 балів за реалізацію додаткового функціоналу, описаного нижче в Чек-листі виконання проєкту (додаткові вимоги)_

**Зберігання та управління нотатками**
- ✅ Додавання "тегів" до нотаток
- ✅ Пошук та сортування нотаток за "тегами"

**Інтелектуальний аналіз**
- ✅ Помічник повинен вгадувати, що хоче від нього користувач, на основі введеного тексту та пропонувати найближчу команду для виконання

---

### Running the Bot

There are two primary ways to run the address book bot.

#### As a module

You can run the bot directly as a Python module from the root of the project. This is useful for quick tests without a full installation.

```sh
uv run python -m run
```

#### As an installed script

For more convenient, system-wide access, you can install the project as a command-line tool. This uses the `[project.scripts]` entry in `pyproject.toml` to create an executable script.

1.  **Install the package in editable mode:**
    ```sh
    uv pip install -e .
    ```

2.  **Run the bot from anywhere:**
    ```sh
    uv run address-book-bot
    ```

---

## Code quality and CI

This repository uses [ruff](https://github.com/ruff-rs/ruff) as a combined linter
and formatter. A `pre-commit` configuration lives in
`.pre-commit-config.yaml` and invokes `ruff check --fix` and `ruff format` on all
Python files. The GitHub Actions workflow (`.github/workflows/ci.yml`) executes
the same hooks inside an `uv` environment every time there is a push or pull
request against `main`.

### Getting started

The project uses [uv](https://github.com/astral-sh/uv) to manage dependencies,
including development tools. To prepare your local environment:

1. Install `uv` using [getting started guide](https://docs.astral.sh/uv/getting-started/installation/).
2. Sync dependencies:
   ```sh
   uv sync
   ```
3. Install the git hook:
   ```sh
   uv run pre-commit install
   ```
4. Run the checks manually (optional / first time):
   ```sh
   uv run pre-commit run --all-files
   ```

After this, the `pre-commit` hooks will automatically run on every commit and
any style violations will also show up in the CI workflow.


### Running tests

To run the test suite, use the following command:
```sh
uv run pytest
```

Run tests for a specific file or test-case:
```sh
uv run pytest tests/test_models.py
uv run pytest tests/test_models.py::test_get_upcoming_birthdays
```

To run tests and see the coverage report in the terminal:
```sh
uv run pytest --cov
```

## Test coverage 📊

We use `pytest-cov` to measure test coverage and upload the results to
[Codecov](https://codecov.io/) every time the CI workflow runs.

![Codecov Coverage Graph](https://codecov.io/gh/neoversity-ai-ml/project-group-20/graphs/sunburst.svg?token=A26ZHG7CU6)
