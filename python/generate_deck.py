# coding: utf-8

import ktg
from ktg import generator2

deck = generator2.generate(0.5, 0.5, 0.9, 0.1)

print deck.to_json()
