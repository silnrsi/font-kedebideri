### Project status [![Build Status](https://build.palaso.org/app/rest/builds/buildType:Fonts_Kedebideri/statusIcon)](https://build.palaso.org/viewType.html?buildTypeId=Fonts_Kedebideri&guest=1)

Kedebideri is a font for the Beria Erfe script. 

_The Beria Erfe script has received [provisional codepoint assignments](https://www.unicode.org/alloc/Pipeline.html) by the Unicode Technical Committee. The script has not yet been formally accepted and approved for a future version of the Unicode Standard. The Kedebideri font is using the provisional codepoints, but those codepoints can always change. Should those codepoints change, this font would be re-released with the new encoding. Documents would then need converting to use the new codepoints._

For more details about this project, including its design history and acknowledgements see [FONTLOG.txt](FONTLOG.txt).

For copyright and licensing information - including any Reserved Font Names - see [OFL.txt](OFL.txt).

For practical information about using, modifying and redistributing this font see [OFL-FAQ.txt](OFL-FAQ.txt).

## Developer notes

This project uses a UFO-based design and production workflow, with all sources in open formats and a completely open-source build toolkit. For more details see [SIL Font Development Notes](https://silnrsi.github.io/silfontdev/en-US/Introduction.html).

We are not currently accepting contributions of glyph designs or code to this project, but if you are interested in helping with the project please contact us at fonts@sil.org.

The font can be built from source using [smith](https://github.com/silnrsi/smith). This is done via the sequence:
```
    smith distclean
    smith configure
    smith build
```
See all the details in the [SIL Font Development Notes](https://silnrsi.github.io/silfontdev/en-US/Introduction.html).
