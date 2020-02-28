
# Usage: python -B cat_deck.py decks.eka

import importlib
import sys

print(importlib.import_module(sys.argv[1]).deck)
