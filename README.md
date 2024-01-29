# RGU
Royal Game of Ur, een 4.500 jaar oud [spel](https://en.wikipedia.org/wiki/Royal_Game_of_Ur).

## Benodigdheden

1. python 3.6 te vinden op [python.org](https://www.python.org)
2. numpy
```
python -m pip install numpy
```
3. pygame
```
python -m pip install pygame
```

## Uitvoeren
Het uitvoerbare bestand is rgu_gui.py, te vinden in de src directory.
```
python rgu_gui.py
```
## Spelregels:
Het doel van het spel is om als eerste alle stenen van de ene kant naar de andere kant van het bord te brengen volgens onderstaande route. Er wordt met vier dobbelstenen gedobbeld die allemaal een 50/50 kans hebben op 0 of 1, het is vergelijkbaar met het opgooien van 4 muntjes. De waarde van de worp is de som van de dobbelstenen. De mogelijke worpen zijn 0 tot en met 4.

![Route](https://github.com/WillemReynvaan/RGU/blob/master/Royal%20Game%20of%20Ur/src/board_transparent_bg_route.png)

Een speler mag een steen alleen vooruit bewegen. Als een speler landt op een roset, hieronder aangegeven met een oranje vierkant, mag de speler nog een keer gooien.

![Rosetten](https://github.com/WillemReynvaan/RGU/blob/master/Royal%20Game%20of%20Ur/src/board_transparent_bg_rosetten.png)

In de middelste rij, waar de routes van beide spelers overlappen kunnen de spelers elkaar slaan door op een tegenstander te landen, de tegenstander gaat dan terug naar het begin van de route. De roset in de middelste rij, gemarkeerd met een gele ster, is veilig, stenen op die roset kunnen niet geslagen worden. Verder kunnen spelers niet op hun eigen stukken landen.
