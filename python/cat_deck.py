
from ktg.deck import Deck
import sys
import json

with open(sys.argv[1], 'r') as input_file:
	print Deck(json.loads(input_file.read()))
