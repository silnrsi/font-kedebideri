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
ftmlTest('tools/ftml-smith.xsl', fonts = ['reference/Kedebideri-Regular.ttf'], addfontindex = 1, fontmode = 'collect')

designspace('source/' + FAMILY + '.designspace',
    target = process('${DS:FILENAME_BASE}.ttf',
        cmd('gftools fix-nonhinting -q --no-backup ${DEP} ${TGT}'),
        cmd('psfchangettfglyphnames ${SRC} ${DEP} ${TGT}', ['${source}']),
    ),
    version=VERSION,  # Needed to ensure dev information on version string
    opentype = fea("generated/${DS:FILENAME_BASE}.fea", master="source/opentype/main.feax", to_ufo = 'True'),
    pdf = fret(params='-oi'),
    woff = woff('web/${DS:FILENAME_BASE}.woff',
        metadata=f'../source/{FAMILY}-WOFF-metadata.xml',
        ),
    )
