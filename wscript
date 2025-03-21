#!/usr/bin/python3
# this is a smith configuration file

# override the default folders
DOCDIR = ["documentation", "web"]
genout = "generated/"

# set the font name and description
APPNAME = 'Kedebideri'
FAMILY = APPNAME
DESC_SHORT = "Font for the Beria Erfe script"

# Get version and authorship information from Regular UFO (canonical metadata); must be first function call:
getufoinfo('source/masters/' + FAMILY + '-Regular' + '.ufo')

# Set up the FTML tests
# ftmlTest('tools/ftml-smith.xsl')

designspace('source/' + FAMILY + '.designspace',
    target = process('${DS:FILENAME_BASE}.ttf',
       cmd('psfchangettfglyphnames ${SRC} ${DEP} ${TGT}', ['source/masters/${DS:FILENAME_BASE}.ufo'])),
    opentype = fea("generated/${DS:FILENAME_BASE}.fea", master="source/opentype/main.feax", to_ufo = 'True'),
    woff = woff('web/${DS:FILENAME_BASE}.woff',
        metadata=f'../source/{FAMILY}-WOFF-metadata.xml',
        cmd='psfwoffit -m ${SRC[1]} --woff ${TGT} --woff2 ${TGT}2 ${SRC[0]}'
        ),
    pdf = fret(params='-oi')
)
