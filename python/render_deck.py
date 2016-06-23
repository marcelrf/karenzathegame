# coding: utf-8

from ktg.card import *
from ktg.deck import *
import sys
import json

def main():
    deck_filename = sys.argv[1]
    with open(deck_filename, 'r') as deck_file:
        deck_json_object = json.loads(deck_file.read())
    deck = Deck(deck_json_object)
    print to_html(deck)

def to_html(element):
    if isinstance(element, Deck):
        deck = element
        text = '<table cellspacing="0" cellpadding="0">'
        for i in range(len(deck.cards)):
            if i % 3 == 0: text += '<tr>'
            text += '<td>' + to_html(deck.cards[i]) + '</td>'
            if i % 3 == 2: text += '</tr>'
            if i % 9 == 8:
                text += (
                    '</table>'
                    '<div class="separator"></div>'
                    '<table cellspacing="0" cellpadding="0">')
        text += "</table>"
        return STYLE + text
    elif isinstance(element, Card):
        card = element
        sword_classes = ['s1', 's2', 's3', 's4']
        text = '<div class="card">'
        if card.type == 'special':
            text = """
                <div class="card">
                    <div class="type special"></div>
                    <div class="power">&nbsp;&nbsp;&nbsp;%d</div>
                    <div class="name">%s - %s</div>
                    <div class="drawing">
                        <img src="images/%s" />
                    </div>
                    <div class="text">%s</div>
                </div>
            """ % (
                card.power,
                card.fighter,
                card.name,
                card.image,
                card.text,
            )
        else:
            text = """
                <div class="card">
                    <div class="type %s"></div>
                    <div class="power">&nbsp;&nbsp;&nbsp;%d</div>
                    <div class="miniature">
                        <img src="images/board.png" />
                        <div class="min-trajectory %s-%s"></div>
                    </div>
                    <div class="name">%s - %s</div>
                    <div class="drawing">
                        <img src="images/%s" />
                    </div>
                    <div class="requisite">
                        <img src="images/board.png" />
                        <div class="trajectory %s-%s"></div>
                    </div>
                </div>
            """ % (
                card.type,
                card.power,
                sword_classes[card.sword_origin],
                sword_classes[card.sword_destiny],
                card.fighter,
                card.name,
                card.image,
                sword_classes[card.sword_origin],
                sword_classes[card.sword_destiny],
            )
        return text

STYLE = """
<style>
.card {
    width: 6.35cm;
    height: 8.89cm;
    border: 0.03cm solid black;
    position: relative;
}
.type {
    width: 1cm;
    height: 1cm;
    position: absolute;
    left: 0.23cm;
    top: 0.35cm;
}
.type.attack {
    background-image: url('images/attack.png');
}
.type.defense {
    background-image: url('images/defense.png');
}
.type.special {
    background-image: url('images/special.png');
}
.power {
    width: 1cm;
    height: 1cm;
    position: absolute;
    left: 0.23cm;
    top: 1.4cm;
    font-family: Impact;
    font-size: 0.5cm;
    line-height: 1.1cm;
    background-image: url('images/power.png');
    opacity: 0.6;
}
.miniature {
    width: 0.9cm;
    height: 0.9cm;
    position: absolute;
    left: 0.33cm;
    top: 2.6cm;
}
.miniature img {
    width: 0.9cm;
    height: 0.9cm;
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
    left: -2.28cm;
    top: 4.7cm;
}
.drawing {
    height: 4.8cm;
    width: 4.4cm;
    border: 0.03cm solid lightgray;
    position: absolute;
    left: 1.47cm;
    top: 0.35cm;
}
.drawing img {
    display: none;
    height: 3.8cm;
    width: 4.6cm;
}
.requisite {
    height: 4.2cm;
    width: 4.4cm;
    position: absolute;
    left: 1.5cm;
    top: 5.7cm;
}
.requisite img {
    height: 2.7cm;
    width: 4.4cm;
    opacity: 0.5;
}
.trajectory,
.min-trajectory {
    background-repeat: no-repeat;
    position: absolute;
}
.trajectory {
    width: 5cm;
    height: 5cm;
    opacity: 0.7;
}
.min-trajectory {
    width: 5cm;
    height: 5cm;
    opacity: 0.8;
}
.trajectory.s1-s2 {
    background-image: url('images/short.png');
    -moz-transform: scale3d(1.2, -0.7, 1);  /* FF3.5+ */
    -o-transform: scale3d(1.2, -0.7, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(1.2, -0.7, 1);  /* Saf3.1+, Chrome */
    left: 0.4cm;
    top: -1.6cm;
}
.trajectory.s1-s3 {
    background-image: url('images/short.png');
    -moz-transform: rotate(90deg) scale3d(0.7, 1, 1);  /* FF3.5+ */
    -o-transform: rotate(90deg) scale3d(0.7, 1, 1);  /* Opera 10.5 */
    -webkit-transform: rotate(90deg) scale3d(0.7, 1, 1);  /* Saf3.1+, Chrome */
    left: -1.3cm;
    top: -0.7cm;
}
.trajectory.s1-s4 {
    background-image: url('images/long.png');
    -moz-transform: scale3d(1.2, -0.7, 1);  /* FF3.5+ */
    -o-transform: scale3d(1.2, -0.7, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(1.2, -0.7, 1);  /* Saf3.1+, Chrome */
    left: 0.5cm;
    top: -1.6cm;
}
.trajectory.s2-s1 {
    background-image: url('images/short.png');
    -moz-transform: scale3d(-1.2, -0.7, 1);  /* FF3.5+ */
    -o-transform: scale3d(-1.2, -0.7, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(-1.2, -0.7, 1);  /* Saf3.1+, Chrome */
    left: -1.0cm;
    top: -1.6cm;
}
.trajectory.s2-s3 {
    background-image: url('images/long.png');
    -moz-transform: scale3d(-1.2, -0.7, 1);  /* FF3.5+ */
    -o-transform: scale3d(-1.2, -0.7, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(-1.2, -0.7, 1);  /* Saf3.1+, Chrome */
    left: -1cm;
    top: -1.6cm;
}
.trajectory.s2-s4 {
    background-image: url('images/short.png');
    -moz-transform: rotate(90deg) scale3d(0.7, -1, 1);  /* FF3.5+ */
    -o-transform: rotate(90deg) scale3d(0.7, -1, 1);  /* Opera 10.5 */
    -webkit-transform: rotate(90deg) scale3d(0.7, -1, 1);  /* Saf3.1+, Chrome */
    left: 0.7cm;
    top: -0.7cm;
}
.trajectory.s3-s1 {
    background-image: url('images/short.png');
    -moz-transform: rotate(90deg) scale3d(-0.7, 1, 1);  /* FF3.5+ */
    -o-transform: rotate(90deg) scale3d(-0.7, 1, 1);  /* Opera 10.5 */
    -webkit-transform: rotate(90deg) scale3d(-0.7, 1, 1);  /* Saf3.1+, Chrome */
    left: -1.3cm;
    top: -1.6cm;
}
.trajectory.s3-s2 {
    background-image: url('images/long.png');
    -moz-transform: scale3d(1.2, 0.7, 1);  /* FF3.5+ */
    -o-transform: scale3d(1.2, 0.7, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(1.2, 0.7, 1);  /* Saf3.1+, Chrome */
    left: 0.4cm;
    top: -0.7cm;
}
.trajectory.s3-s4 {
    background-image: url('images/short.png');
    -moz-transform: scale3d(1.2, 0.7, 1);  /* FF3.5+ */
    -o-transform: scale3d(1.2, 0.7, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(1.2, 0.7, 1);  /* Saf3.1+, Chrome */
    left: 0.4cm;
    top: -0.7cm;
}
.trajectory.s4-s1 {
    background-image: url('images/long.png');
    -moz-transform: scale3d(-1.2, 0.7, 1);  /* FF3.5+ */
    -o-transform: scale3d(-1.2, 0.7, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(-1.2, 0.7, 1);  /* Saf3.1+, Chrome */
    left: -1cm;
    top: -0.7cm;
}
.trajectory.s4-s2 {
    background-image: url('images/short.png');
    -moz-transform: rotate(90deg) scale3d(-0.7, -1, 1);  /* FF3.5+ */
    -o-transform: rotate(90deg) scale3d(-0.7, -1, 1);  /* Opera 10.5 */
    -webkit-transform: rotate(90deg) scale3d(-0.7, -1, 1);  /* Saf3.1+, Chrome */
    left: 0.7cm;
    top: -1.6cm;
}
.trajectory.s4-s3 {
    background-image: url('images/short.png');
    -moz-transform: scale3d(-1.2, 0.7, 1);  /* FF3.5+ */
    -o-transform: scale3d(-1.2, 0.7, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(-1.2, 0.7, 1);  /* Saf3.1+, Chrome */
    left: -1cm;
    top: -0.7cm;
}
.min-trajectory.s1-s2 {
    background-image: url('images/short.png');
    -moz-transform: scale3d(0.25, -0.25, 1);  /* FF3.5+ */
    -o-transform: scale3d(0.25, -0.25, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(0.25, -0.25, 1);  /* Saf3.1+, Chrome */
    left: -1.93cm;
    top: -2.19cm;
}
.min-trajectory.s1-s3 {
    background-image: url('images/short.png');
    -moz-transform: rotate(90deg) scale3d(0.25, 0.25, 1);  /* FF3.5+ */
    -o-transform: rotate(90deg) scale3d(0.25, 0.25, 1);  /* Opera 10.5 */
    -webkit-transform: rotate(90deg) scale3d(0.25, 0.25, 1);  /* Saf3.1+, Chrome */
    left: -2.24cm;
    top: -1.9cm;
}
.min-trajectory.s1-s4 {
    background-image: url('images/long.png');
    -moz-transform: scale3d(0.25, -0.25, 1);  /* FF3.5+ */
    -o-transform: scale3d(0.25, -0.25, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(0.25, -0.25, 1);  /* Saf3.1+, Chrome */
    left: -2.0cm;
    top: -2.3cm;
}
.min-trajectory.s2-s1 {
    background-image: url('images/short.png');
    -moz-transform: scale3d(-0.25, -0.25, 1);  /* FF3.5+ */
    -o-transform: scale3d(-0.25, -0.25, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(-0.25, -0.25, 1);  /* Saf3.1+, Chrome */
    left: -2.15cm;
    top: -2.19cm;
}
.min-trajectory.s2-s3 {
    background-image: url('images/long.png');
    -moz-transform: scale3d(-0.25, -0.25, 1);  /* FF3.5+ */
    -o-transform: scale3d(-0.25, -0.25, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(-0.25, -0.25, 1);  /* Saf3.1+, Chrome */
    left: -2.2cm;
    top: -2.2cm;
}
.min-trajectory.s2-s4 {
    background-image: url('images/short.png');
    -moz-transform: rotate(90deg) scale3d(0.25, -0.25, 1);  /* FF3.5+ */
    -o-transform: rotate(90deg) scale3d(0.25, -0.25, 1);  /* Opera 10.5 */
    -webkit-transform: rotate(90deg) scale3d(0.25, -0.25, 1);  /* Saf3.1+, Chrome */
    left: -1.9cm;
    top: -1.9cm;
}
.min-trajectory.s3-s1 {
    background-image: url('images/short.png');
    -moz-transform: rotate(90deg) scale3d(-0.25, 0.25, 1);  /* FF3.5+ */
    -o-transform: rotate(90deg) scale3d(-0.25, 0.25, 1);  /* Opera 10.5 */
    -webkit-transform: rotate(90deg) scale3d(-0.25, 0.25, 1);  /* Saf3.1+, Chrome */
    left: -2.2cm;
    top: -2.15cm;
}
.min-trajectory.s3-s2 {
    background-image: url('images/long.png');
    -moz-transform: scale3d(0.25, 0.25, 1);  /* FF3.5+ */
    -o-transform: scale3d(0.25, 0.25, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(0.25, 0.25, 1);  /* Saf3.1+, Chrome */
    left: -1.95cm;
    top: -1.85cm;
}
.min-trajectory.s3-s4 {
    background-image: url('images/short.png');
    -moz-transform: scale3d(0.25, 0.25, 1);  /* FF3.5+ */
    -o-transform: scale3d(0.25, 0.25, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(0.25, 0.25, 1);  /* Saf3.1+, Chrome */
    left: -1.95cm;
    top: -1.9cm;
}
.min-trajectory.s4-s1 {
    background-image: url('images/long.png');
    -moz-transform: scale3d(-0.25, 0.25, 1);  /* FF3.5+ */
    -o-transform: scale3d(-0.25, 0.25, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(-0.25, 0.25, 1);  /* Saf3.1+, Chrome */
    left: -2.15cm;
    top: -1.85cm;
}
.min-trajectory.s4-s2 {
    background-image: url('images/short.png');
    -moz-transform: rotate(90deg) scale3d(-0.25, -0.25, 1);  /* FF3.5+ */
    -o-transform: rotate(90deg) scale3d(-0.25, -0.25, 1);  /* Opera 10.5 */
    -webkit-transform: rotate(90deg) scale3d(-0.25, -0.25, 1);  /* Saf3.1+, Chrome */
    left: -1.95cm;
    top: -2.15cm;
}
.min-trajectory.s4-s3 {
    background-image: url('images/short.png');
    -moz-transform: scale3d(-0.25, 0.25, 1);  /* FF3.5+ */
    -o-transform: scale3d(-0.25, 0.25, 1);  /* Opera 10.5 */
    -webkit-transform: scale3d(-0.25, 0.25, 1);  /* Saf3.1+, Chrome */
    left: -2.15cm;
    top: -1.95cm;
}
.text {
    height: 2.3cm;
    width: 3.8cm;
    border: 0.03cm solid lightgray;
    position: absolute;
    left: 1.47cm;
    top: 5.5cm;
    padding: 0.3cm;
    font-size: 12px;
}
.separator {
    height: 1.2cm;
}
</style>
"""

if __name__ == '__main__':
    main()
