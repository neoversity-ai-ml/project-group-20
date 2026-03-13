#!/usr/bin/env python

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from address_book_bot.main import main  # noqa: E402

if __name__ == "__main__":
    main()
