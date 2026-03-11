**Технічний опис завдання**

```
☝ У цьому домашньому завданні ви повинні додати функціонал збереження адресної книги на диск та відновлення з диска.\n
```

Для цього ви маєте вибрати`pickle`протокол серіалізації / десеріалізації даних та реалізувати методи, які дозволять зберегти всі дані у файл і завантажити їх із файлу.

**Головна мета**— щоб застосунок не втрачав даних після виходу із застосунку та при запуску відновлював їх із файлу. Повинна зберігатися адресна книга, з якою ми працювали минулого разу.

Реалізуйте функціонал для збереження стану`AddressBook`у файл при закритті програми та відновлення стану при її запуску.

**Приклади коду, які стануть у пригоді:**

**Серіалізація з**`pickle`

```
import pickle\n\ndef save_data(book, filename=\"addressbook.pkl\"):\n    with open(filename, \"wb\") as f:\n        pickle.dump(book, f)\n\ndef load_data(filename=\"addressbook.pkl\"):\n    try:\n        with open(filename, \"rb\") as f:\n            return pickle.load(f)\n    except FileNotFoundError:\n        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено\n
```

**Інтеграція збереження та завантаження в основний цикл**

```
def main():\n    book = load_data()\n\n    # Основний цикл програми\n\n    save_data(book)  # Викликати перед виходом з програми\n
```

```
Ці приклади допоможуть вам у реалізації домашнього завдання.\n
```

**Критерії оцінювання:**

1. Реалізовано протокол серіалізації / десеріалізації даних за допомогою`pickle`.
2. Усі дані повинні зберігатися при виході з програми.
3. При новому сеансі адресна книга, яка була при попередньому запуску, повинна бути в застосунку.

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

1. Install `uv` (if it isn’t already):
   ```sh
   pip install uv
   ```
2. Sync the development dependencies:
   ```sh
   uv sync --only-dev
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


## Test coverage 📊

We use `pytest-cov` to measure test coverage and upload the results to
[Codecov](https://codecov.io/) every time the CI workflow runs. A badge showing
the current coverage percentage is available at the top of this README:

[![Coverage Status](https://codecov.io/gh/${{ github.repository }}/branch/main/graph/badge.svg)](https://codecov.io/gh/${{ github.repository }})

To enable uploads you should add a `CODECOV_TOKEN` secret in your repository
settings—public repos do not strictly require it, but it's good practice.
