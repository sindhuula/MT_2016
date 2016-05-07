#!/bin/sh

# script copied and modified/improved from the
# DingMee Translator: http://chrm.info/cms/dingmee-translator
# GNU General Public License either version 3 of the License, or
# (at your option) any later version.

if [ $# -ne 3 ] ; then
    echo "Usage: $0 <DICT1> <DICT2> <OUTPUT-FILE>"
    exit
fi

DICT1=$1
DICT2=$2
OUTPUT=$3

a=0

while read line
    do 
    
# Find in another file
#    lineEN=`echo "$line" | sed "s/\ ::\ .*$//g"`
    lineEN=`echo "$line" | sed "s/\ ::\ .*$//g" | sed "s/\/.*\/\ //"`
    termEN=`echo "$lineEN" | sed "s/\ (.*//g"`
    glossEN=`echo "$lineEN" | sed "s/[^(]*//"`
    lineSOURCE=`echo "$line" | sed "s/.*::\ \(.*$\)/\1/g"`

#    echo "[$lineEN]"
#    echo "[$termEN]"
#    echo "[$glossEN]"
#    echo "[$lineSOURCE]"

    TMP=`echo $lineEN | grep SEE`
    if [ "$TMP" != "" ]; then
        echo "--------- SEE --------"
        echo "[$lineEN]"
        echo "[$lineSOURCE]"
        continue
    fi

# gloss-less entries must be excluded
# as they are poor quality 
# and will match any gloss-entry of the same POS
    if [ "$glossEN" = "" ]; then
        echo "--------- NON-GlOSS ENTRY --------"
        echo "[$lineEN]"
        continue
    fi

#    lineDEST=`grep "$lineEN" $DICT2 | sed "s/.*::\ \(.*$\)/\1/g"`
     lineDEST=`grep "$termEN.*$glossEN" $DICT2 | sed "s/.*::\ \(.*$\)/\1/g"`
     

    if [ "$lineDEST" != "" -a "$lineSOURCE" != "" ]; then
        a=$(($a+1));
        echo $a;
        echo "-------- FOUND --------"
        echo "$lineSOURCE :: $lineDEST" >> $OUTPUT
    fi
done < $DICT1

# Cleanup
cat $OUTPUT | grep -v "SEE:" > ${OUTPUT}.new
cat ${OUTPUT}.new | sort | uniq > $OUTPUT
cat $OUTPUT | grep "::" > ${OUTPUT}.new
mv ${OUTPUT}.new $OUTPUT

echo "Ready. Generated file: $OUTPUT"
