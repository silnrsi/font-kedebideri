#!/bin/bash

# This script rebuilds the algorithmically-generated ftml files. See README.md

# Copyright (c) 2020-2025 SIL Global  (https://www.sil.org)
# Released under the MIT License (https://opensource.org/licenses/

# Assumes we're in the root folder, i.e., font-ramsina

set -e

if [ ! -e OFL.txt ] 
then
	echo "Please cd to root of font project to use this script"
	exit 2
fi

prevfont="references/Kedebideri-Regular.ttf"
prevver="2.0"

commonParams=( \
	--prevfont "$prevfont"  \
	-s "url(../$prevfont)|$prevver"  \
	--ap '_?dia[ABO]$'  \
	--xsl ../tools/ftml.xsl  \
	--scale 200  \
	-i source/glyph_data.csv  \
	-w 75%  \
#	-s "url(../references/Kedebideri-Regular.ttf)|ref"  \
)

echo "Rebuilding ftml files..."
tools/psfgenftml.py -q -t 'AllChars (auto)'                      source/masters/Kedebideri-Regular.ufo  tests/AllChars-auto.ftml        -l tests/logs/AllChars.log         "${commonParams[@]}" -s 'url(../results/Kedebideri-Regular.ttf)|Reg' -s 'url(../results/Kedebideri-Medium.ttf)|Med' -s 'url(../results/Kedebideri-SemiBold.ttf)|seBld' -s 'url(../results/Kedebideri-Bold.ttf)|Bld' -s 'url(../results/Kedebideri-ExtraBold.ttf)|exBld' -s 'url(../results/Kedebideri-Black.ttf)|Blk' &
tools/psfgenftml.py -q -t 'Diac Short (auto)'                    source/masters/Kedebideri-Regular.ufo  tests/Diac-short-auto.ftml      -l tests/logs/DiacTest1-short.log  "${commonParams[@]}" -s 'url(../results/Kedebideri-Regular.ttf)|Reg' -s 'url(../results/Kedebideri-Medium.ttf)|Med' -s 'url(../results/Kedebideri-SemiBold.ttf)|seBld' -s 'url(../results/Kedebideri-Bold.ttf)|Bld' -s 'url(../results/Kedebideri-ExtraBold.ttf)|exBld' -s 'url(../results/Kedebideri-Black.ttf)|Blk' &


wait
echo done.
