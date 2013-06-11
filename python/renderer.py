# coding: utf-8

from card import *
from deck import *

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
        feet_classes = ['fa', 'fb', 'fc', 'fd', 'fe']
        sword_classes = ['s1', 's2', 's3', 's4', 's5']
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
                <div class="min-foot orange %s">&#9679;</div>
                <div class="min-sword blue %s">&#9679;</div>
                <div class="trajectory %s-%s"></div>
                <div class="min-trajectory %s-%s"></div>
            </div>
        """ % (
            card_types[card.type],
            card.power,
            ' '.join(map(lambda x: x.capitalize(), fighter.split('_'))),
            fighter,
            feet_classes[card.left_foot],
            feet_classes[card.right_foot],
            sword_classes[card.sword_origin],
            feet_classes[card.left_foot],
            feet_classes[card.right_foot],
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
.foot.fa { left: 3.115cm; top: 4.435cm; }
.foot.fb { left: 1.54cm; top: 5.55cm; }
.foot.fc { left: 4.7cm; top: 5.55cm; }
.foot.fd { left: 2.13cm; top: 7.4cm; }
.foot.fe { left: 4.12cm; top: 7.4cm; }
.sword {
    width: 0.9cm;
    height: 0.9cm;
    position: absolute;
}
.sword img {
    width: 1cm;
    height: 1cm;
}
.sword.s1 { left: 2.19cm; top: 4.82cm; }
.sword.s2 { left: 4.06cm; top: 4.82cm; }
.sword.s3 { left: 1.6cm; top: 6.55cm; }
.sword.s4 { left: 4.65cm; top: 6.55cm; }
.sword.s5 { left: 3.15cm; top: 7.64cm; }
.min-foot {
    position: absolute;
}
.min-foot.fa { left: 0.6cm; top: 1.25cm; }
.min-foot.fb { left: 0.23cm; top: 1.53cm; }
.min-foot.fc { left: 0.993cm; top: 1.53cm; }
.min-foot.fd { left: 0.38cm; top: 1.97cm; }
.min-foot.fe { left: 0.85cm; top: 1.97cm; }
.min-sword {
    position: absolute;
}
.min-sword.s1 { left: 0.36cm; top: 1.33cm; }
.min-sword.s2 { left: 0.85cm; top: 1.33cm; }
.min-sword.s3 { left: 0.25cm; top: 1.75cm; }
.min-sword.s4 { left: 0.99cm; top: 1.75cm; }
.min-sword.s5 { left: 0.6cm; top: 2cm; }
.orange {
    color: orange;
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
    -moz-transform: rotate(72deg);  /* FF3.5+ */
    -o-transform: rotate(72deg);  /* Opera 10.5 */
    -webkit-transform: rotate(72deg);  /* Saf3.1+, Chrome */
    left: 0.6cm;
    top: 4.74cm;
}
.trajectory.s1-s3,
.trajectory.s3-s1 {
    background-image: url('images/short.png');
    left: 1.6cm;
    top: 4.74cm;
}
.trajectory.s1-s4,
.trajectory.s4-s1 {
    background-image: url('images/long.png');
    -moz-transform: rotate(71deg);  /* FF3.5+ */
    -o-transform: rotate(71deg);  /* Opera 10.5 */
    -webkit-transform: rotate(71deg);  /* Saf3.1+, Chrome */
    left: 0.6cm;
    top: 4.74cm;
}
.trajectory.s1-s5,
.trajectory.s5-s1 {
    background-image: url('images/long.png');
    -moz-transform: rotate(-72deg);  /* FF3.5+ */
    -o-transform: rotate(-72deg);  /* Opera 10.5 */
    -webkit-transform: rotate(-72deg);  /* Saf3.1+, Chrome */
    left: 1.9cm;
    top: 3.8cm;
}
.trajectory.s2-s3,
.trajectory.s3-s2 {
    background-image: url('images/long.png');
    left: 1.6cm;
    top: 4.74cm;
}
.trajectory.s2-s4,
.trajectory.s4-s2 {
    background-image: url('images/short.png');
    -moz-transform: rotate(143deg);  /* FF3.5+ */
    -o-transform: rotate(143deg);  /* Opera 10.5 */
    -webkit-transform: rotate(143deg);  /* Saf3.1+, Chrome */
    left: 0.35cm;
    top: 3.8cm;
}
.trajectory.s2-s5,
.trajectory.s5-s2 {
    background-image: url('images/long.png');
    -moz-transform: rotate(144deg);  /* FF3.5+ */
    -o-transform: rotate(144deg);  /* Opera 10.5 */
    -webkit-transform: rotate(144deg);  /* Saf3.1+, Chrome */
    left: 0.35cm;
    top: 3.75cm;
}
.trajectory.s3-s4,
.trajectory.s4-s3 {
    background-image: url('images/long.png');
    -moz-transform: rotate(-144deg);  /* FF3.5+ */
    -o-transform: rotate(-144deg);  /* Opera 10.5 */
    -webkit-transform: rotate(-144deg);  /* Saf3.1+, Chrome */
    left: 1.15cm;
    top: 3.23cm;
}
.trajectory.s3-s5,
.trajectory.s5-s3 {
    background-image: url('images/short.png');
    -moz-transform: rotate(-73deg);  /* FF3.5+ */
    -o-transform: rotate(-73deg);  /* Opera 10.5 */
    -webkit-transform: rotate(-73deg);  /* Saf3.1+, Chrome */
    left: 1.9cm;
    top: 3.78cm;
}
.trajectory.s4-s5,
.trajectory.s5-s4 {
    background-image: url('images/short.png');
    -moz-transform: rotate(-144deg);  /* FF3.5+ */
    -o-transform: rotate(-144deg);  /* Opera 10.5 */
    -webkit-transform: rotate(-144deg);  /* Saf3.1+, Chrome */
    left: 1.1cm;
    top: 3.2cm;
}
.min-trajectory.s1-s2,
.min-trajectory.s2-s1 {
    background-image: url('images/min-short.png');
    -moz-transform: rotate(69deg);  /* FF3.5+ */
    -o-transform: rotate(69deg);  /* Opera 10.5 */
    -webkit-transform: rotate(69deg);  /* Saf3.1+, Chrome */
    left: 0.19cm;
    top: 1.49cm;
}
.min-trajectory.s1-s3,
.min-trajectory.s3-s1 {
    background-image: url('images/min-short.png');
    left: 0.28cm;
    top: 1.53cm;
}
.min-trajectory.s1-s4,
.min-trajectory.s4-s1 {
    background-image: url('images/min-long.png');
    -moz-transform: rotate(71deg);  /* FF3.5+ */
    -o-transform: rotate(71deg);  /* Opera 10.5 */
    -webkit-transform: rotate(71deg);  /* Saf3.1+, Chrome */
    left: 0.18cm;
    top: 1.49cm;
}
.min-trajectory.s1-s5,
.min-trajectory.s5-s1 {
    background-image: url('images/min-long.png');
    -moz-transform: rotate(-72deg);  /* FF3.5+ */
    -o-transform: rotate(-72deg);  /* Opera 10.5 */
    -webkit-transform: rotate(-72deg);  /* Saf3.1+, Chrome */
    left: 0.35cm;
    top: 1.4cm;
}
.min-trajectory.s2-s3,
.min-trajectory.s3-s2 {
    background-image: url('images/min-long.png');
    left: 0.32cm;
    top: 1.5cm;
}
.min-trajectory.s2-s4,
.min-trajectory.s4-s2 {
    background-image: url('images/min-short.png');
    -moz-transform: rotate(143deg);  /* FF3.5+ */
    -o-transform: rotate(143deg);  /* Opera 10.5 */
    -webkit-transform: rotate(143deg);  /* Saf3.1+, Chrome */
    left: 0.15cm;
    top: 1.37cm;
}
.min-trajectory.s2-s5,
.min-trajectory.s5-s2 {
    background-image: url('images/min-long.png');
    -moz-transform: rotate(144deg);  /* FF3.5+ */
    -o-transform: rotate(144deg);  /* Opera 10.5 */
    -webkit-transform: rotate(144deg);  /* Saf3.1+, Chrome */
    left: 0.15cm;
    top: 1.37cm;
}
.min-trajectory.s3-s4,
.min-trajectory.s4-s3 {
    background-image: url('images/min-long.png');
    -moz-transform: rotate(-144deg);  /* FF3.5+ */
    -o-transform: rotate(-144deg);  /* Opera 10.5 */
    -webkit-transform: rotate(-144deg);  /* Saf3.1+, Chrome */
    left: 0.258cm;
    top: 1.31cm;
}
.min-trajectory.s3-s5,
.min-trajectory.s5-s3 {
    background-image: url('images/min-short.png');
    -moz-transform: rotate(-73deg);  /* FF3.5+ */
    -o-transform: rotate(-73deg);  /* Opera 10.5 */
    -webkit-transform: rotate(-73deg);  /* Saf3.1+, Chrome */
    left: 0.33cm;
    top: 1.39cm;
}
.min-trajectory.s4-s5,
.min-trajectory.s5-s4 {
    background-image: url('images/min-short.png');
    -moz-transform: rotate(-144deg);  /* FF3.5+ */
    -o-transform: rotate(-144deg);  /* Opera 10.5 */
    -webkit-transform: rotate(-144deg);  /* Saf3.1+, Chrome */
    left: 0.28cm;
    top: 1.31cm;
}
</style>
"""
