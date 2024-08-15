#!/usr/bin/python3

import fontParts.world as fontparts
import sys

# Open UFO
ufo = sys.argv[1]
font = fontparts.OpenFont(ufo)

# Modify UFO
cgj = 0x034F
vs = range(0xFE00, 0xFE0F+1)
mn = [cgj] + list(vs)
dotted_circle = 0x25CC
latn = (0x0060, 0x00A8, 0x00AF, 0x00B4, 0x00B8, 0x02C6, 0x02C7, 0x02D8, 0x02DB, 0x02D9, 0x02DA, 0x02DC, 0x02DD)

for glyph in font:
    if glyph.unicode in mn:
        glyph.appendAnchor('_none', (0, 0))
    if glyph.unicode == dotted_circle:
        for anchor in glyph.anchors:
            if anchor.name == 'aboveLC':
                glyph.appendAnchor('U', (anchor.x, anchor.y + 50))
    if glyph.unicode in latn:
        for anchor in glyph.anchors:
            if anchor.name.startswith('_'):
                glyph.removeAnchor(anchor)

# Save UFO
font.changed()
font.save()
font.close()
