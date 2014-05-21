# coding: utf-8

import ktg
from ktg import generator2

deck = generator2.generate(0.3, 0.7, 0.9, 0.3)

print deck.to_json()
