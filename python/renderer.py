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
        text += "Mean power: %f" % deck.mean_power() + "\n"
        text += "Power deviation: %f" % deck.power_deviation() + "\n"
        text += "Mean distance: %f" % deck.mean_distance() + "\n"
        text += "Distance deviation: %f" % deck.distance_deviation()
        return text
    else: return None

def to_html(element):
    if isinstance(element, Card):
        card = element
        feet_classes = ['fa', 'fb', 'fc', 'fd', 'fe']
        text = """
             <div class="card">
                <div class="type">
                    <div class="power">%d</div>
                </div>
                <div class="miniature">
                    <img src="../images/board.png" />
                </div>
                <div class="name">FIGHTER - CARD NAME</div>
                <div class="drawing">
                    <img src="../images/fighter.png" />
                </div>
                <div class="requisite"></div>
                <div class="foot %s">
                    <img src="../images/left_foot.png" />
                </div>
                <div class="foot %s">
                    <img src="../images/right_foot.png" />
                </div>
            </table>
        """ % (
            card.power,
            feet_classes[card.left_foot],
            feet_classes[card.right_foot],
        )
        return CARD_STYLE + text

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
    width: 0.9cm;
    height: 0.9cm;
    border: 0.03cm solid lightgray;
    border-radius: 0.9cm 0.9cm 0.9cm 0.9cm;
    position: absolute;
    left: 0.25cm;
    top: 0.35cm;
}
.type .power {
    font-family: Impact;
    font-size: 0.5cm;
    color: gray;
    margin: 0.15cm 0 0 0.3cm;
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
    filter:  progid:DXImageTransform.Microsoft.BasicImage(rotation=1.57);  /* IE6,IE7 */
    -ms-filter: "progid:DXImageTransform.Microsoft.BasicImage(rotation=1.57)"; /* IE8 */
    width: 6.4cm;
    height: 1cm;
    font-family: Impact;
    font-size: 0.6cm;
    color: gray;
    position: absolute;
    left: -2.37cm;
    top: 4.7cm;
}
.drawing {
    height: 3.8cm;
    width: 4.6cm;
    border: 0.03cm solid lightgray;
    border-radius: 0.3cm;
    position: absolute;
    left: 1.35cm;
    top: 0.35cm;
}
.drawing img {
    height: 3.8cm;
    width: 4cm;
    margin: 0 0 0 0.3cm;
}
.requisite {
    height: 4.2cm;
    width: 4.2cm;
    background-image: url('../images/board.png');
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
.foot.fa {
    left: 3.115cm;
    top: 4.435cm;
}
.foot.fb {
    left: 1.54cm;
    top: 5.55cm;
}
.foot.fc {
    left: 4.7cm;
    top: 5.55cm;
}
.foot.fd {
    left: 2.13cm;
    top: 7.4cm;
}
.foot.fe {
    left: 4.12cm;
    top: 7.4cm;
}
</style>
"""


c = Card()
c.random()
print to_html(c)