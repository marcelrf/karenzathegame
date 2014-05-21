# coding: utf-8

import ktg
from ktg.card import *
from ktg.deck import *
import sys

def main():
    deck_filename = sys.argv[1]
    deck_file = open(deck_filename, 'r')
    deck_json = deck_file.read()[:-1]
    deck = Deck(deck_json)
    print to_html(deck, sys.argv[2])

def to_text(element):
    if isinstance(element, Card):
        return str(element)
    elif isinstance(element, Deck):
        deck, text = element, ""
        cards = list(deck.cards)
        while len(cards) > 0:
            line_cards = cards[:5]
            card_texts = map(lambda x: str(x).split("\n"), line_cards)
            while len(card_texts[0]) > 0:
                for i in range(5):
                    text += card_texts[i].pop(0)
                text += '\n'
            cards = cards[5:]
        return text
    else: return None

def to_html(element, fighter, style=True):
    if isinstance(element, Card):
        card = element
        card_types = [None, 'attack', 'defense']
        feet_classes = ['fa', 'fb', 'fc', 'fd', 'fnone']
        sword_classes = ['s1', 's2', 's3', 's4']
        text = """
             <div class="card">
                <div class="type %s">
                    <div class="power">%d</div>
                </div>
                <div class="miniature">
                    <img src="images/board.png" />
                </div>
                <div class="name">%s - Card Name</div>
                <div class="drawing">
                    <img src="images/%s.png" />
                </div>
                <div class="requisite"></div>
                <div class="foot %s">
                    <img src="images/left_foot.png" />
                </div>
                <div class="foot %s">
                    <img src="images/right_foot.png" />
                </div>
                <div class="sword %s">
                    <img src="images/sword.png" />
                </div>
                <div class="min-foot orange %s">&#9679;</div>
                <div class="min-foot red %s">&#9679;</div>
                <div class="min-sword blue %s">&#9679;</div>
                <div class="trajectory %s-%s"></div>
                <div class="min-trajectory %s-%s"></div>
            </div>
        """ % (
            card_types[card.type],
            card.power,
            ' '.join(map(lambda x: x.capitalize(), fighter.split('_'))),
            fighter,
            feet_classes[card.left_foot if card.left_foot is not None else 4],
            feet_classes[card.right_foot if card.right_foot is not None else 4],
            sword_classes[card.sword_origin],
            feet_classes[card.left_foot if card.left_foot is not None else 4],
            feet_classes[card.right_foot if card.right_foot is not None else 4],
            sword_classes[card.sword_origin],
            sword_classes[card.sword_origin],
            sword_classes[card.sword_destiny],
            sword_classes[card.sword_origin],
            sword_classes[card.sword_destiny],
        )
        if style: text = CARD_STYLE + text
        return text
    elif isinstance(element, Deck):
        deck = element
        text = '<table cellspacing="0" cellpadding="0">'
        for i in range(len(deck.cards)):
            if i % 3 == 0: text += "<tr>"
            text += "<td>" + to_html(deck.cards[i], fighter, False) + "</td>"
            if i % 3 == 2: text += "</tr>"
        text += "</table>"
        if style: text = CARD_STYLE + text
        return text

CARD_STYLE = """
<style>
.card {
    width: 6.35cm;
    height: 8.89cm;
    border: 0.03cm solid black;
    border-radius: 0.3cm;
    position: relative;
}
.type {
    width: 1cm;
    height: 1cm;
    position: absolute;
    left: 0.19cm;
    top: 0.35cm;
}
.type.attack {
    background-image: url('images/attack.png');
    color: crimson;
}
.type.defense {
    background-image: url('images/defense.png');
    color: green;
}
.type .power {
    font-family: Impact;
    font-size: 0.5cm;
    margin: 0.2cm 0 0 0.4cm;
}
.miniature {
    width: 0.9cm;
    height: 0.9cm;
    position: absolute;
    left: 0.25cm;
    top: 1.4cm;
}
.miniature img {
    width: 1cm;
    height: 1cm;
}
.name {
    -moz-transform: rotate(-90deg);  /* FF3.5+ */
    -o-transform: rotate(-90deg);  /* Opera 10.5 */
    -webkit-transform: rotate(-90deg);  /* Saf3.1+, Chrome */
    width: 6.4cm;
    height: 1cm;
    font-family: Impact;
    font-size: 0.6cm;
    color: gray;
    position: absolute;
    left: -2.38cm;
    top: 4.7cm;
}
.drawing {
    height: 3.8cm;
    width: 4.6cm;
    border: 0.03cm solid lightgray;
    border-radius: 0.3cm;
    background-color: lightgray;
    position: absolute;
    left: 1.35cm;
    top: 0.35cm;
}
.drawing img {
    height: 3.8cm;
    width: 4.6cm;
    opacity: 0.7;
}
.requisite {
    height: 4.2cm;
    width: 4.2cm;
    background-image: url('images/board.png');
    position: absolute;
    left: 1.5cm;
    top: 4.4cm;
}
.foot {
    width: 0.9cm;
    height: 0.9cm;
    position: absolute;
}
.foot img {
    width: 1cm;
    height: 1cm;
}
.foot.fa { left: 3.07cm; top: 4.49cm; }
.foot.fb { left: 1.58cm; top: 6.08cm; }
.foot.fc { left: 4.62cm; top: 6.03cm; }
.foot.fd { left: 3.11cm; top: 7.57cm; }
.foot.fnone { display: none; }
.sword {
    width: 0.9cm;
    height: 0.9cm;
    position: absolute;
}
.sword img {
    width: 1cm;
    height: 1cm;
}
.sword.s1 { left: 2.08cm; top: 4.99cm; }
.sword.s2 { left: 4.12cm; top: 5cm; }
.sword.s3 { left: 2.06cm; top: 7.1cm; }
.sword.s4 { left: 4.17cm; top: 7.1cm; }
.min-foot {
    position: absolute;
}
.min-foot.fa { left: 0.6cm; top: 1.26cm; }
.min-foot.fb { left: 0.25cm; top: 1.65cm; }
.min-foot.fc { left: 0.99cm; top: 1.63cm; }
.min-foot.fd { left: 0.6cm; top: 1.99cm; }
.min-foot.fnone { display: none; }
.min-sword {
    position: absolute;
}
.min-sword.s1 { left: 0.36cm; top: 1.39cm; }
.min-sword.s2 { left: 0.85cm; top: 1.39cm; }
.min-sword.s3 { left: 0.36cm; top: 1.87cm; }
.min-sword.s4 { left: 0.85cm; top: 1.87cm; }
.orange {
    color: orange;
}
.red {
    color: orangered;
}
.blue {
    color: blue;
}
.trajectory,
.min-trajectory {
    background-repeat: no-repeat;
    position: absolute;
}
.trajectory {
    width: 5cm;
    height: 5cm;
    opacity: 0.5;
}
.min-trajectory {
    width: 1cm;
    height: 1cm;
    opacity: 0.8;
}
.trajectory.s1-s2,
.trajectory.s2-s1 {
    background-image: url('images/short.png');
    -moz-transform: rotate(89deg);  /* FF3.5+ */
    -o-transform: rotate(89deg);  /* Opera 10.5 */
    -webkit-transform: rotate(89deg);  /* Saf3.1+, Chrome */
    left: 0.8cm;
    top: 4.46cm;
}
.trajectory.s1-s3,
.trajectory.s3-s1 {
    background-image: url('images/short.png');
    left: 1.5cm;
    top: 4.4cm;
}
.trajectory.s1-s4,
.trajectory.s4-s1 {
    background-image: url('images/long.png');
    -moz-transform: rotate(90deg);  /* FF3.5+ */
    -o-transform: rotate(90deg);  /* Opera 10.5 */
    -webkit-transform: rotate(90deg);  /* Saf3.1+, Chrome */
    left: 0.76cm;
    top: 4.48cm;
}
.trajectory.s2-s3,
.trajectory.s3-s2 {
    background-image: url('images/long.png');
    left: 1.5cm;
    top: 4.4cm;
}
.trajectory.s2-s4,
.trajectory.s4-s2 {
    background-image: url('images/short.png');
    -moz-transform: rotate(178deg);  /* FF3.5+ */
    -o-transform: rotate(178deg);  /* Opera 10.5 */
    -webkit-transform: rotate(178deg);  /* Saf3.1+, Chrome */
    left: 0.65cm;
    top: 3.75cm;
}
.trajectory.s3-s4,
.trajectory.s4-s3 {
    background-image: url('images/short.png');
    -moz-transform: rotate(-90deg);  /* FF3.5+ */
    -o-transform: rotate(-90deg);  /* Opera 10.5 */
    -webkit-transform: rotate(-90deg);  /* Saf3.1+, Chrome */
    left: 1.4cm;
    top: 3.6cm;
}
.min-trajectory.s1-s2,
.min-trajectory.s2-s1 {
    background-image: url('images/min-short.png');
    -moz-transform: rotate(90deg);  /* FF3.5+ */
    -o-transform: rotate(90deg);  /* Opera 10.5 */
    -webkit-transform: rotate(90deg);  /* Saf3.1+, Chrome */
    left: 0.21cm;
    top: 1.44cm;
}
.min-trajectory.s1-s3,
.min-trajectory.s3-s1 {
    background-image: url('images/min-short.png');
    left: 0.26cm;
    top: 1.42cm;
}
.min-trajectory.s1-s4,
.min-trajectory.s4-s1 {
    background-image: url('images/min-long.png');
    -moz-transform: rotate(90deg);  /* FF3.5+ */
    -o-transform: rotate(90deg);  /* Opera 10.5 */
    -webkit-transform: rotate(90deg);  /* Saf3.1+, Chrome */
    left: 0.23cm;
    top: 1.44cm;
}
.min-trajectory.s2-s3,
.min-trajectory.s3-s2 {
    background-image: url('images/min-long.png');
    left: 0.26cm;
    top: 1.42cm;
}
.min-trajectory.s2-s4,
.min-trajectory.s4-s2 {
    background-image: url('images/min-short.png');
    -moz-transform: rotate(180deg);  /* FF3.5+ */
    -o-transform: rotate(180deg);  /* Opera 10.5 */
    -webkit-transform: rotate(180deg);  /* Saf3.1+, Chrome */
    left: 0.23cm;
    top: 1.4cm;
}
.min-trajectory.s3-s4,
.min-trajectory.s4-s3 {
    background-image: url('images/min-short.png');
    -moz-transform: rotate(-90deg);  /* FF3.5+ */
    -o-transform: rotate(-90deg);  /* Opera 10.5 */
    -webkit-transform: rotate(-90deg);  /* Saf3.1+, Chrome */
    left: 0.25cm;
    top: 1.4cm;
}
</style>
"""

if __name__ == '__main__':
    main()