#!/usr/bin/env python3
__doc__ = '''generate ftml tests from glyph_data.csv and UFO'''
__url__ = 'https://github.com/silnrsi/font-arab-tools'
__copyright__ = 'Copyright (c) 2018-2025 SIL Global  (https://www.sil.org)'
__license__ = 'Released under the MIT License (https://opensource.org/licenses/MIT)'
__author__ = 'Bob Hallissy'

import re
from silfont.core import execute
import silfont.ftml_builder as FB
from palaso.unicode.ucd import get_ucd, loadxml
from collections import OrderedDict
from itertools import permutations


argspec = [
    ('ifont', {'help': 'Input UFO'}, {'type': 'infont'}),
    ('output', {'help': 'Output file ftml in XML format', 'nargs': '?'}, {'type': 'outfile', 'def': '_out.ftml'}),
    ('-i','--input', {'help': 'Glyph info csv file'}, {'type': 'incsv', 'def': 'glyph_data.csv'}),
    ('-f','--fontcode', {'help': 'letter to filter for glyph_data'},{}),
    ('--prevfont', {'help': 'font file of previous version'}, {'type': 'filename', 'def': None}),
    ('-l','--log', {'help': 'Set log file name'}, {'type': 'outfile', 'def': '_ftml.log'}),
    ('--langs', {'help':'List of bcp47 language tags', 'default': None}, {}),
#    ('--rtl', {'help': 'enable right-to-left features', 'action': 'store_true'}, {}),
    ('--norendercheck', {'help': 'do not include the RenderingUnknown check', 'action': 'store_true'}, {}),
    ('-t', '--test', {'help': 'name of the test to generate', 'default': None}, {}),
    ('-s','--fontsrc', {'help': 'font source: "url()" or "local()" optionally followed by "|label"', 'action': 'append'}, {}),
    ('--scale', {'help': 'percentage to scale rendered text (default 100)'}, {}),
    ('--ap', {'help': 'regular expression describing APs to examine', 'default': '.'}, {}),
    ('-w', '--width', {'help': 'total width of all <string> column (default automatic)'}, {}),
    ('--xsl', {'help': 'XSL stylesheet to use'}, {}),
    ('--ucdxml', {'help': 'File with UCD XML data for chars in the pipeline'}, {}),
]


def joinGoupSortKey(uid:int):
    return joinGroupKeys.get(get_ucd(uid, 'jg'), 99) * 0x20000 + uid

ageToFlag = 17.0
ageColor = '#FFC8A0'      # light orange -- marks if there is a char from above Unicode version or later
missingColor = '#FFE0E0'  # light red -- mark if a char is missing from UFO
newColor = '#F0FFF0'      # light green -- mark if char is not in previous version (if --prevFont supplied)
backgroundLegend =  'Background colors: ' \
                    'light red: a character is missing from UFO; else ' + \
                    f'light orange: includes a character from Unicode version {ageToFlag} or later; else ' + \
                    'light green: a character is new in this version of the font'

def doit(args):
    logger = args.logger

    if args.ucdxml:
        # Update UCD module with data for relevant pipeline chars 
        loadxml(args.ucdxml)

    # A note about args.fontcode:
    # In most applications we blindly pass this to FTMLbuilder so that, in the case the user has provided `absGlyphList.csv` 
    # (or something similar) as the input CSV file, FTMLBuilder will be able to filter out the records appropriately. 
    # Of course this parameter is unneeded in cases where a project-specific `glyph_data.csv` file is provided as input, and 
    # in fact will cause an error in FTMLBuilder because processing of args.fontcode requires a `Fonts` column in the csv file.

    # However, in this app args.fontcode can serve two purposes: 
    #    - filtering records from absGlyphList.csv (as above)
    #    - deciding what tests or test data to include in generated ftml file.
    # Thus, in this app, it is permissible to provide args.fontcode even though project specific glyph_data.csv (rather than 
    # absGlyphList.csv) is supplied as input. So we must be careful not to send user-supplied args.fontcode to FTMLBuilder if
    # the input csv has no `Fonts` column. Whew.

    try:
        whichfont = args.fontcode.strip().lower()   # This will be used within this app to select appropriate tests and data
    except AttributeError:
        whichfont = ''
    
    if len(whichfont) > 1:
                logger.log('fontcode must be a single letter', 'S')

    # Read input csv
    builder = FB.FTMLBuilder(logger, incsv=args.input, 
                             fontcode=args.fontcode if 'Fonts' in args.input.firstline else None,  # see comments above
                             font=args.ifont, ap=args.ap, langs=args.langs)

    # Per ABS-3017, we want users to be able to override any and all language-specific behaviors by
    # setting relevant CV features. This typically involves adding an additional CV value whose behavior
    # is to reset glyphs back to their defaults.  To make sure these get tested, we need to increment the maxval
    # of some of the features (those where the glyph_data.csv doesn't explicitly list this extra value):
    for tag in ('cv12', 'cv44', 'cv54', 'cv70', 'cv72', 'cv78', 'cv82'):
        try:
            builder.features[tag].maxval += 1
        except KeyError:
            # It's okay if this font doesn't have this feature.
            pass
    
    # Override default base (25CC) for displaying combining marks
    builder.diacBase = 0x25CC   # dotted circle


    def basenameSortKey(uid:int):
        return builder.char(uid).basename.lower()

    # Initialize FTML document:
    test = args.test or "AllChars (NG)"  # Default to AllChars
    widths = None
    if args.width:
        try:
            width, units = re.match(r'(\d+)(.*)$', args.width).groups()
            if len(args.fontsrc):
                width = int(round(int(width)/len(args.fontsrc)))
            widths = {'string': f'{width}{units}'}
            logger.log(f'width: {args.width} --> {widths["string"]}', 'I')
        except:
            logger.log(f'Unable to parse width argument "{args.width}"', 'W')
    # split labels from fontsource parameter
    fontsrc = []
    labels = []
    for sl in args.fontsrc:
        try:
            s, l = sl.split('|',1)
            fontsrc.append(s)
            labels.append(l)
        except ValueError:
            fontsrc.append(sl)
            labels.append(None)
    ftml = FB.FTML(test, logger, comment=backgroundLegend, rendercheck=not args.norendercheck, fontscale=args.scale,
                   widths=widths, xslfn=args.xsl, fontsrc=fontsrc, fontlabel=labels)

    if args.prevfont is not None:
        try:
            from fontTools.ttLib import TTFont
            font = TTFont(args.prevfont)
            prevCmap = font.getBestCmap()
        except:
            logger.log(f'Unable to open previous font {args.prevfont}', 'S')


    def setBackgroundColor(uids):
        # We can only set one background color, so the order of these corresponds to importance of the info.
        # (e.g., if the char is missing from the UFO then that has to be fixed first.)
        # If this order is changed, then update the backgroundLegend accordingly.

        # if any uid in uids is missing from the UFO, set test background color to missingColor
        if any(uid in builder.uidsMissingFromUFO for uid in uids):
            ftml.setBackground(missingColor)
        # else if any uid in uids has Unicode age >= ageToFlag, then set the test background color to ageColor
        elif max(map(lambda x: float(get_ucd(x, 'age')), uids)) >= ageToFlag:
            ftml.setBackground(ageColor)
        # else if any uid was not in previous version of ttf (if supplied), set to newColor:
        elif args.prevfont and any(uid not in prevCmap for uid in uids):
            ftml.setBackground(newColor)
        else:
            ftml.clearBackground()

    # Some lists shared used by multiple tests:
    # all lam-like:
    lamlist = sorted(filter(lambda uid: get_ucd(uid, 'jg') == 'Lam', builder.uids()))
    # all alef-like except high-hamza-alef:
    aleflist = sorted(filter(lambda uid: get_ucd(uid, 'jg') == 'Alef' and uid != 0x0675, builder.uids()))

#--------------------------------
# AllChars test
#--------------------------------

    if test.lower().startswith("allchars"):
        # all chars that should be in the font:
        saveDiacBase = builder.diacBase
        ftml.startTestGroup('Encoded characters')
        for uid in sorted(builder.uids()):
            if uid < 32: continue
            c = builder.char(uid)
            setBackgroundColor((uid,))
            builder.diacBase = 0x0644 if uid == 0x10EFC  else saveDiacBase  # Special base for alefOverlay
            for featlist in builder.permuteFeatures(uids=(uid,)):
                ftml.setFeatures(featlist)
                builder.render((uid,), ftml)
            ftml.clearFeatures()
            if len(c.langs):
                for langID in builder.allLangs:
                    ftml.setLang(langID)
                    builder.render((uid,), ftml)
                ftml.clearLang()
        builder.diacBase = saveDiacBase

#--------------------------------
# Diacritic test
#--------------------------------

    if test.lower().startswith("diac"):
        # Diac attachment:

        doLongTest = 'short' not in test.lower()

        # Representative base and diac chars:
        if doLongTest:
            repDiac = list(filter(lambda x: x in builder.uids(), (0x0300, 0x0301, 0x0304, 0x0307)))
            repBase = list(filter(lambda x: x in builder.uids(), (0x16EA0, 0x16EA3, 0x16EA7, 0x16EAF, 0x16EB6, 0x16EBB, 0x16EBE, 0x16EC2, 0x16ECA, 0x16ED1)))
        else:
            repDiac = list(filter(lambda x: x in builder.uids(), (0x0300, 0x0301, 0x0304, 0x0307)))
            repBase = list(filter(lambda x: x in builder.uids(), (0x16EA0, 0x16EA3, 0x16EA7, 0x16EAF, 0x16EB6, 0x16EBB, 0x16EBE, 0x16EC2, 0x16ECA, 0x16ED1)))


        ftml.startTestGroup('All Beria Erfe diacritics on all (vowel) bases')
        for uid in sorted(builder.uids()):
            # ignore non-ABS marks
            if uid < 0x300 or uid in range(0xFE00, 0xFE10): continue
            c = builder.char(uid)
            if c.general == 'Mn' and uid != 0x10EA0:  # all combining marks except alefoverlay (which isn't general purpose)
                for base in repBase:
                    setBackgroundColor((uid,base))
                    for featlist in builder.permuteFeatures(uids=(uid,base)):
                        ftml.setFeatures(featlist)
                        builder.render((base,uid), ftml, keyUID=uid, addBreaks=False, dualJoinMode=2)
                        if doLongTest:
                            if uid != 0x0300: # if not shadda
                                # include shadda, in either order:
                                builder.render((base, uid, 0x0300), ftml, keyUID=uid, addBreaks=False, dualJoinMode=2)
                                builder.render((base, 0x0300, uid), ftml, keyUID=uid, addBreaks=False, dualJoinMode=2)
                            if diac != 0x0301:  # If not superscript alef
                                # include superscript alef, in either order:
                                builder.render((uid, diac, 0x0301), ftml, addBreaks=False, dualJoinMode=2)
                                builder.render((uid, 0x0301, diac), ftml, addBreaks=False, dualJoinMode=2)
                    ftml.clearFeatures()
                ftml.closeTest()


#--------------------------------
#  Classes test
#--------------------------------

    if test.lower().startswith('classes'):
        zwj = chr(0x200D)
        lsb = '' # chr(0xF130)
        rsb = '' # chr(0xF131)

        glyphsSeen = set()

        uids = sorted(filter(lambda uid: builder.char(uid).general == 'Lo' and uid > 255, builder.uids()))
        uids = sorted(uids, key=joinGoupSortKey)
        for uid in uids:
            c = chr(uid)
            thischar = builder.char(uid)
            label = 'U+{:04X}'.format(uid)
            for featlist in builder.permuteFeatures(uids=(uid,)):
                gname = thischar.basename
                if len(featlist) == 1 and featlist[0] is not None:
                    # See if we can find an alternate glyph name:
                    feat = '{}={}'.format(featlist[0][0], featlist[0][1])
                    gname = thischar.altnames.get(feat,gname)
                if gname not in glyphsSeen:
                    glyphsSeen.add(gname)
                    comment = gname
                    ftml.setFeatures(featlist)
                    ftml.addToTest(    uid, lsb +       c       + rsb, label, comment) #isolate
                    if get_ucd(uid, 'jt') == 'D':
                        ftml.addToTest(uid, lsb +       c + zwj + rsb)  # initial
                        ftml.addToTest(uid, lsb + zwj + c + zwj + rsb)  # medial
                    if get_ucd(uid, 'jt') in ('R', 'D'):
                        ftml.addToTest(uid, lsb + zwj + c       + rsb)  # final
            ftml.clearFeatures()
            ftml.closeTest()


    ftml.writeFile(args.output)

def cmd() : execute("UFO",doit,argspec)
if __name__ == "__main__": cmd()
