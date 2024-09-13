
Many questions can be answered by consulting the following FAQ pages. Here are a few sample questions answered in each FAQ:

- [SIL fonts in general](http://software.sil.org/fonts/faq)
    - *How can I type...?*
    - *How can I use font features?*
    - *Will you add support for character...?*
    - *Will you add support for script...?*
    - *WIll you help me...?*

- [The SIL Open Font License (OFL-FAQ)](https://scripts.sil.org/OFL-FAQ_web)
    - *Can I use this font for...?*
    - *Can I modify the font and then include it in...*
    - *If I use the font on a web page do I have to include an acknowledgement?*
    - The full OFL-FAQ.txt is also included in the font package.

Here are a few of the most frequently asked questions specifically regarding Kedebideri:

#### *Where does the name Kedebideri come from?*

Kedebideri means "Let's write!" in the Zaghawa Beria language of Sudan and Chad.

#### *How do you pronounce Kedebideri?*

The emphasis is on the third syllable: keh-deh-BIH-deh-rih (kɛ̀dɛ̀bɪ́dɛ́ɺɪ́).

#### *Since the Beria Erfe script is not officially in the Unicode Standard, what are the problems I might encounter?*

This font is using [provisional codepoint assignments](https://www.unicode.org/alloc/Pipeline.html) given by the Unicode Technical Committee for the Beria Erfe script characters. The script has not yet been formally accepted and approved for a future version of the Unicode Standard. If the codepoints are changed, the Kedebideri font will be updated and re-released. Any documents produced with this current version (v2.000) of the font would then need converting to use the new codepoints. See last question below for more information on converting data.

#### *How is the font different from Zaghawa Beria?*

**Kedebideri** is based on the design of **Zaghawa Beria**. However, **Zaghawa Beria** used a custom encoding. **Kedebideri** uses the provisionally assigned Unicode codepoints. In addition, it contains a basic set of Latin characters. 

#### *What is the source of the Latin glyphs?*

The Latin glyphs in Kedebideri are based on Source Sans Pro at 103% and a weight of CSS 360.

#### *I used the Zaghawa Beria font which was custom encoded. How can I convert my data from the Zaghawa Beria encoding to Unicode?*

Data which was created with the Zaghawa Beria font will not be automatically converted to Unicode by switching fonts. The data must be converted to Unicode using a data conversion routine. See "Text conversion" in [Resources](resources) for information on converting your data.

There is a minimally tested TECKit mapping file available for converting data from the custom encoded Zaghawa Beria font to the provisional Unicode codepoints:

- [ZaghawaBeria2Uni](https://github.com/silnrsi/wsresources/tree/master/scripts/BeriaErfe/legacy/zaghawa-beria/mappings)




