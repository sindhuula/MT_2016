#INSTPATH=./
INSTPATH=./dictd/
SOURCEPATH=./ding/ 

for PROG in gawk dictfmt
do
command -v $PROG >/dev/null 2>&1 || { echo >&2 "Program $PROG is required but it's not installed.  Aborting."; exit 1; }
done

function compiledict { 
source=$SOURCEPATH$1
target=$INSTPATH$2
database_short=$3
echo "compiling "$2".dict"
gawk -f ding2dictd.awk $source|dictfmt -f \
-s "$database_short" -u "http://en.wiktionary.org/wiki/User:Matthias_Buchmeier" \
--utf8  --columns 0 --without-headword --headword-separator :: $target
dictzip $target.dict
}

for lang in es it pt fr nl de fi no sv cs hu pl ru ja arb cmn hi fa vi el he tr ko bg ro ca sh
do
source=en-$lang-enwiktionary.txt
target=en-$lang-enwiktionary
#echo $source" "$target
compiledict $source $target $target
done

for lang in es it fr fi pt
do
source=$lang-en-enwiktionary.txt
target=$lang-en-enwiktionary
#echo $source" "$target
compiledict $source $target $target
done

