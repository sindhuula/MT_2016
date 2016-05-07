#!/bin/bash

installdir="./ding"
#installdir=/usr/share/trans

# test for existence of lynx and awk
for PROG in lynx awk
do
command -v $PROG >/dev/null 2>&1 || { echo >&2 "Program $PROG is required but it's not installed.  Aborting."; exit 1; }
done

function download { 
echo "downloading "$2
cat /dev/null>$2
for letter in a b c d e f g h i j k l m n o p q r s t u v w x y z 0
do
lynx -width=1000 -nolist -underscore -dump -assume_charset=utf-8 -display_charset=utf-8 "http://en.wiktionary.org/w/index.php?title=$1-$letter&printable=yes" |\
awk '/::/ {gsub(/[\ ]+/, " "); gsub(/^[\ ]/, ""); print;}'>>$2 
done
}

for lang in es it pt fr nl de fi no sv cs hu pl ru ja arb cmn fa hi vi el he tr ko bg ro ca sh da
do
WIKIPATH=User:Matthias_Buchmeier/en-$lang
TARGETPATH=$installdir/en-$lang-enwiktionary.txt
download $WIKIPATH $TARGETPATH
done

for lang in es it fr fi pt
do
WIKIPATH=User:Matthias_Buchmeier/$lang-en
TARGETPATH=$installdir/$lang-en-enwiktionary.txt
download $WIKIPATH $TARGETPATH
done
