#!/bin/bash
# jenga.sh -- kusanya programu ya Swa inayotumia json.swa
#
# Matumizi:
#   SWA=/njia/ya/swa ./jenga.sh faili.swa towe
#
# SWA ni saraka ya hazina ya lugha-swa/swa (chaguo-msingi:
# ~/Projects/compilers/swa). Mara ya kwanza, script hujenga mkusanyaji
# wa Swa (stage2) ndani ya .jenga/ kutoka mbegu.bin ya hazina hiyo;
# baada ya hapo hutumia tena mkusanyaji huo.
#
# `faili.swa` haitakiwi kuhusisha json.swa yenyewe -- script inaiunganisha
# mbele ya faili lako kabla ya kuikusanya (na maktaba za msingi
# kumbukumbu.swa/mfuatano.swa zinatatuliwa na mkusanyaji kutoka hazina
# ya SWA).
set -e

SWA="${SWA:-$HOME/Projects/compilers/swa}"
KIONGOZI="$(cd "$(dirname "$0")" && pwd)"
AKIBA="$KIONGOZI/.jenga"
STAGE2="$AKIBA/stage2"

kama_hakuna_swa() {
    echo "hitilafu: hazina ya Swa haipatikani: $SWA (weka SWA=/njia/ya/swa)" >&2
    exit 1
}
[ -f "$SWA/msingi/mbegu.bin" ] || kama_hakuna_swa

# 1. Jenga mkusanyaji (mara moja tu).
if [ ! -x "$STAGE2" ]; then
    mkdir -p "$AKIBA"
    echo "jenga: kujenga mkusanyaji wa Swa (mara ya kwanza tu)..." >&2
    (
        cd "$SWA"
        MBEGU="$SWA/msingi/mbegu.bin"
        cat msingi/maktaba/kumbukumbu.swa msingi/maktaba/mfuatano.swa \
            msingi/maktaba/faili.swa gharama/msuluhishi.swa \
            > "$AKIBA/msuluhishi-chanzo.swa"
        "$MBEGU" --exe "$AKIBA/msuluhishi-chanzo.swa" > "$AKIBA/msuluhishi"
        chmod +x "$AKIBA/msuluhishi"
        "$AKIBA/msuluhishi" msingi/mkusanyaji/stage1.swa > "$AKIBA/zima.swa"
        "$MBEGU" --exe "$AKIBA/zima.swa" > "$AKIBA/stage1"
        chmod +x "$AKIBA/stage1"
        # Kizazi cha pili (stage1 ikijikusanya) -- hiki ndicho kinachotumika.
        "$AKIBA/stage1" --exe "$AKIBA/zima.swa" > "$STAGE2"
        chmod +x "$STAGE2"
    )
fi

[ $# -eq 2 ] || { echo "matumizi: $0 faili.swa towe" >&2; exit 2; }
CHANZO="$1"
TOWE="$2"
[ -f "$CHANZO" ] || { echo "hitilafu: faili halipo: $CHANZO" >&2; exit 1; }

# 2. Unganisha json.swa + faili la mtumiaji, kisha kusanya kutoka SWA.
KUU="$(mktemp "$AKIBA/kuu-XXXXXX.swa")"
trap 'rm -f "$KUU"' EXIT
cat "$KIONGOZI/json.swa" "$CHANZO" > "$KUU"
TOWE_KAMILI="$(cd "$(dirname "$TOWE")" && pwd)/$(basename "$TOWE")"
(cd "$SWA" && "$STAGE2" --exe "$KUU" > "$TOWE_KAMILI")
chmod +x "$TOWE_KAMILI"
