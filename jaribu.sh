#!/bin/bash
# jaribu.sh -- endesha majaribio yote ya Swa (jaribio/jaribio_*.swa)
#
# Matumizi: SWA=/njia/ya/swa ./jaribu.sh [jaribio_jina.swa ...]
# Bila hoja, inaendesha majaribio yote. Kila jaribio linaunganishwa na
# jaribio/msaada.swa, linakusanywa kwa jenga.sh, na kuendeshwa; msimbo
# wa kutoka 0 = limefaulu.
KIONGOZI="$(cd "$(dirname "$0")" && pwd)"
cd "$KIONGOZI" || exit 1
mkdir -p .jenga
if [ $# -gt 0 ]; then MAJARIBIO=("$@"); else MAJARIBIO=(jaribio/jaribio_*.swa); fi
FAULU=0; SHINDWA=0
for j in "${MAJARIBIO[@]}"; do
    jina="$(basename "$j" .swa)"
    cat jaribio/msaada.swa "$j" > ".jenga/$jina.kamili.swa"
    if ! ./jenga.sh ".jenga/$jina.kamili.swa" ".jenga/$jina" 2> ".jenga/$jina.jenga.log"; then
        echo "SHINDWA (kukusanya): $jina"; cat ".jenga/$jina.jenga.log"; SHINDWA=$((SHINDWA+1)); continue
    fi
    if ".jenga/$jina" > ".jenga/$jina.towe" 2>&1; then
        echo "imefaulu: $jina  ($(tail -1 ".jenga/$jina.towe"))"; FAULU=$((FAULU+1))
    else
        echo "SHINDWA: $jina"; cat ".jenga/$jina.towe"; SHINDWA=$((SHINDWA+1))
    fi
done
echo "=== majaribio: $FAULU yamefaulu, $SHINDWA yameshindwa ==="
[ "$SHINDWA" -eq 0 ]
