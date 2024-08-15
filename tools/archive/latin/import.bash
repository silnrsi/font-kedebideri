#!/bin/bash

ar=$PWD/tools/archive/latin
glyphnames=$HOME/script/smithplus/etc/glyph_names/glyph_names.csv
shimenkan=$HOME/script/plrd/fonts/shimenkan-local/kedebideri/Shimenkan
andika=$HOME/script/latn/fonts/andika/source/masters/Andika

pushd source
for weight in Regular
do
    ufo=Kedebideri-${weight}.ufo
    
    # main import
    scale="--scale 1.033333"
    glyphs=$ar/shimenkan-${weight}.csv
    latin=${shimenkan}-${weight}.ufo
    psfgetglyphnames -i $ar/import.txt -a $glyphnames $latin $glyphs
    psfcopyglyphs --rename rename --unicode usv $scale -s $latin -i $glyphs -l $glyphs.log $ufo

    # supplemental import
    scale="--scale .488281" # 1000/2048
    glyphs=$ar/andika-${weight}.csv
    latin=${andika}-${weight}.ufo
    psfgetglyphnames -i $ar/import.txt -a $glyphnames $latin $glyphs
    psfcopyglyphs --rename rename --unicode usv $scale -s $latin -i $glyphs -l $glyphs.log $ufo

    # cleanup
    psfrenameglyphs -i $ar/rename.csv $ufo
    psfsetunicodes -i $ar/encode.csv $ufo
    $HOME/script/tools/anchor-keep.py only $ar/anchors.json $ufo
    $HOME/script/tools/fix-spaces.py $ufo
    $ar/cleanup.py $ufo
    psfsetmarkcolors -i $ar/import.txt -u -c g_light_gray $ufo
    psfsetmarkcolors -i $ar/imported.txt -c g_light_gray $ufo

    # check
    ls -l $ufo/glyphs/*copy?.glif
    composites $ufo
done
popd
