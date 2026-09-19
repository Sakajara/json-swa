#!/usr/bin/env python3
"""linganisha_python.py -- ulinganisho huru na moduli ya `json` ya Python.

Inajenga mfano/jsonzuri.swa (kupitia jenga.sh), kisha inalinganisha tabia
yake na json.loads/json.dumps ya Python kwa:

  1. JSON sahihi (bahati nasibu na kesi ngumu za mkono): towe la
     jsonzuri lazima liwe na THAMANI ile ile (ulinganisho mkali wa aina:
     True != 1, 1 != 1.0) -- kwa modi ya compact (-) na pretty (-m).
  2. Modi ya -h (nambari zinaandikwa upya kutoka D64): thamani lazima ziwe
     ndani ya makosa ya 1e-13 (tarakimu 15 za maana).
  3. Ingizo lililoharibiwa (mutation): jsonzuri na Python lazima wakubaliane
     kama ingizo ni sahihi au la, na yakikubaliwa, thamani ziwe sawa.

Tofauti zinazojulikana na zilizoandikwa (README): Swa inakataa \\u0000 na
surrogate isiyo na jozi (Python inakubali), na inakataa kina > 512; ingizo
lenye NaN/Infinity (ambazo si JSON sahihi) linaepukwa.

Matumizi: SWA=/njia/ya/swa python3 jaribio/linganisha_python.py [mbegu] [idadi]
"""
import json
import math
import os
import random
import re
import subprocess
import sys

KIONGOZI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZURI = os.path.join(KIONGOZI, ".jenga", "jsonzuri")

MBEGU = int(sys.argv[1]) if len(sys.argv) > 1 else 20260919
IDADI = int(sys.argv[2]) if len(sys.argv) > 2 else 1500


def jenga():
    os.makedirs(os.path.join(KIONGOZI, ".jenga"), exist_ok=True)
    r = subprocess.run(
        [os.path.join(KIONGOZI, "jenga.sh"), os.path.join(KIONGOZI, "mfano", "jsonzuri.swa"), ZURI],
        capture_output=True,
    )
    if r.returncode != 0:
        sys.stderr.write(r.stderr.decode("utf-8", "replace"))
        sys.exit("hitilafu: kujenga jsonzuri kumeshindwa")


def endesha(maandishi, *hoja):
    """Endesha jsonzuri; rudisha (msimbo, stdout(bytes), stderr(str))."""
    r = subprocess.run([ZURI, *hoja], input=maandishi.encode("utf-8"), capture_output=True)
    return r.returncode, r.stdout, r.stderr.decode("utf-8", "replace")


def sawa_kali(a, b):
    """Ulinganisho mkali: aina lazima zilingane (True != 1, 1 != 1.0)."""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(sawa_kali(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(sawa_kali(x, y) for x, y in zip(a, b))
    return a == b


def karibu(a, b):
    """Kama sawa_kali lakini nambari zinalinganishwa kwa makosa ya 1e-13."""
    ni_nambari = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
    if ni_nambari(a) and ni_nambari(b):
        if a == b:
            return True
        return math.isclose(float(a), float(b), rel_tol=1e-13, abs_tol=0.0)
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(karibu(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(karibu(x, y) for x, y in zip(a, b))
    return a == b


# ---------------------------------------------------------------- jenereta
HERUFI = ["a", "b", "z", "A", "0", "9", " ", "_", "-", '"', "\\", "/", "\n", "\t", "\r",
          "\b", "\f", "\x01", "\x1f", "\x7f", "é", "ß", "€", "中", "文", "😀", " ", "\U0001f680"]


def jina(r):
    return "".join(r.choice(HERUFI) for _ in range(r.randint(0, 12)))


def nambari(r):
    t = r.randint(0, 6)
    if t == 0:
        return r.randint(-1000, 1000)
    if t == 1:
        return r.randint(-10**18, 10**18)
    if t == 2:
        return r.randint(-10**30, 10**30)
    if t == 3:
        return r.uniform(-1000, 1000)
    if t == 4:
        return r.uniform(-1, 1) * 10.0 ** r.randint(-30, 30)
    if t == 5:
        return float(r.randint(-100, 100))
    return r.choice([0.0, -0.0, 0.5, 0.1, 1e-5, 1e15, 1e16, 123456789.125, 2.675, 1 / 3, 5e-324 * 0 + 1e-300, 1.7e300])


def thamani(r, kina):
    aina = r.randint(0, 7 if kina < 5 else 4)
    if aina == 0:
        return None
    if aina == 1:
        return r.choice([True, False])
    if aina in (2, 3):
        return nambari(r)
    if aina == 4:
        return jina(r)
    if aina in (5, 6):
        return [thamani(r, kina + 1) for _ in range(r.randint(0, 5))]
    return {jina(r): thamani(r, kina + 1) for _ in range(r.randint(0, 5))}


def andika_py(r, v):
    """Andika `v` kwa Python kwa chaguo za bahati nasibu (ensure_ascii, indent, ...)."""
    return json.dumps(
        v,
        ensure_ascii=r.choice([True, False]),
        indent=r.choice([None, None, 2, 4, "\t"]),
        separators=r.choice([None, (",", ":"), (" , ", " : ")]),
        sort_keys=r.choice([True, False]),
    )


# ------------------------------------------------------------ kesi za mkono
SAHIHI_NGUMU = [
    "0", "-0", "0.0", "-0.0", "1e0", "1E0", "1e+0", "1e-0", "0e0", "0E+0", "123e-2", "[1E+2]", "[-1.5e-10]",
    "1.7976931348623157e308", "4.9e-324", "9007199254740993", "-9223372036854775808", "12345678901234567890123",
    "0.000001", "0.0000001", "123456789012345.6", "[0.1, 0.2, 0.30000000000000004]",
    '""', '" "', '"\\u0041"', '"\\ud83d\\ude00"', '"\\uD83D\\uDE00"', '"\\u00e9\\u00E9"', '"\\/"', '"\\\\"',
    '"\\"quoted\\""', '"tab\\there"', '"nl\\nhere"', '"\\b\\f\\n\\r\\t"', '"€ 中文 😀"',
    "[]", "{}", "[[]]", "[{}]", "{\"\":1}", '{"":""}', '{"a":{"a":{"a":{}}}}', "[[[[[[[[[[1]]]]]]]]]]",
    "  [  1  ,  2  ]  ", "\n\t\r [\n1\n,\n2\n]\n", '{"a":1,"a":2}', '{"a":1,"b":2,"a":3}', '{"a\\nb":1}',
    "true", "false", "null", "[true,false,null]", '{"t":true,"f":false,"n":null}',
    "[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]",
    # Miundo halisi (kama API ya kawaida)
    '{"id":1234567,"jina":"Amina Juma","barua":"amina@example.com","umri":29,"hai":true,"mke":null,'
    '"anwani":{"mji":"Dar es Salaam","nchi":"TZ","kodi":"11101","kuratibu":[-6.7924,39.2083]},'
    '"lugha":["Kiswahili","English"],"alama":[98.5,87.25,92,100],"maelezo":"Anapenda \\"kusoma\\" na kupika.\\nAmeajiriwa 2019.",'
    '"zamani":[],"tupu":{},"mizani":-1234.5e-2}',
    '{"data":[{"x":1,"y":2.5,"tags":["a","b"]},{"x":-3,"y":0,"tags":[]},{"x":1e10,"y":-1e-10,"tags":["\\u00e9"]}],'
    '"meta":{"jumla":3,"ukurasa":1,"ijayo":null}}',
]

BATILI_NGUMU = [
    "", " ", "[", "]", "{", "}", "[1,]", "[,1]", "[1 2]", '{"a":1,}', '{a:1}', "{'a':1}", '{"a"}', '{"a":}',
    "01", "-01", "+1", ".5", "1.", "1e", "1e+", "--1", "0x1", "1_0", "nul", "tru", "True", "NULL", "undefined",
    '"', '"abc', '"a\nb"', '"a\tb"', '"\\q"', '"\\x41"', '"\\u12"', '"\\u12g4"', "'a'", "[1] 2", "{} {}", "1 2",
    "[1,2", '{"a":1', '{"a" 1}', '{"a":1 "b":2}', "[1,,2]", "[[]", "[]]", "\x00", "[\x00]", "tru e",
    '{"a":1}}', '["a" "b"]', '{"a":"b":"c"}', "-", "-a", "1e1e1", "0.e1", "[.5]", "[-.5]", "[1.e2]",
    "﻿[1]",
]

# Tofauti zilizoandikwa: Python inakubali, Swa inakataa kwa makusudi.
TOFAUTI_ZINAZOJULIKANA = re.compile(r"\\u0000|\\u[dD][89a-fA-F]")


def main():
    jenga()
    r = random.Random(MBEGU)
    kosa = []
    jumla = {"sahihi": 0, "sahihi-mzuri": 0, "sahihi-h": 0, "batili-mkono": 0, "mutation": 0, "mutation-kubaliwa": 0}

    def ripoti(kundi, ingizo, maelezo):
        kosa.append((kundi, ingizo, maelezo))

    # 1. kesi za mkono sahihi
    for s in SAHIHI_NGUMU:
        v = json.loads(s)
        for hoja, kundi in (((), "sahihi"), (("-m",), "sahihi-mzuri")):
            rc, out, err = endesha(s, *hoja)
            jumla[kundi] += 1
            if rc != 0:
                ripoti(kundi, s, "imekataliwa: " + err.strip())
                continue
            try:
                w = json.loads(out.decode("utf-8"))
            except Exception as e:  # noqa: BLE001
                ripoti(kundi, s, f"towe si JSON: {e}: {out!r}")
                continue
            if not sawa_kali(v, w):
                ripoti(kundi, s, f"thamani tofauti: {w!r}")

    # 2. kesi za mkono batili
    for s in BATILI_NGUMU:
        jumla["batili-mkono"] += 1
        try:
            json.loads(s)
            py_ok = True
        except (ValueError, RecursionError):
            py_ok = False
        rc, out, err = endesha(s)
        if py_ok:
            ripoti("batili-mkono", s, "Python inakubali (kesi si batili kweli) -- hitilafu ya jaribio")
        elif rc == 0:
            ripoti("batili-mkono", s, f"Swa imekubali ingizo batili: {out!r}")

    # 2b. Vikomo vya nambari kupitia modi ya -h (D64 -> maandishi -> Python).
    # Nambari za kawaida: makosa ya 1e-13; subnormal (< 2.3e-308): tofauti
    # ndogo ya mzunguko (hadi vipande 8 vya 5e-324) inakubalika.
    VIKOMO = ["5e-324", "1e-320", "1.5e-310", "2.2250738585072014e-308", "2.3e-308", "1e-308", "1e-300", "1e-100",
              "1e-10", "1e-7", "0.00001", "0.0001", "0.001", "0.5", "1", "9.5", "10", "99.99", "12345.6789",
              "1e14", "999999999999999", "1e15", "1e16", "123456789012345678", "1e22", "1e23", "1e100", "1e300",
              "1.79e308", "-1e-320", "-2.5", "-1e300", "1.7", "2.675", "1.005", "4.35", "0.1", "0.2", "0.3",
              "3.141592653589793", "2.718281828459045", "1.4142135623730951", "6.02214076e23", "1.602176634e-19",
              "299792458", "0.000123456789012345", "123456789.123456789", "1e-5", "9.999999999999999e22"]
    for n in VIKOMO:
        jumla["h-vikomo"] = jumla.get("h-vikomo", 0) + 1
        rc, out, err = endesha("[" + n + "]", "-h")
        if rc != 0:
            ripoti("h-vikomo", n, "imekataliwa: " + err.strip())
            continue
        try:
            w = json.loads(out.decode("utf-8"))[0]
        except Exception as e:  # noqa: BLE001
            ripoti("h-vikomo", n, f"towe si JSON: {e}: {out!r}")
            continue
        a = float(n)
        if abs(a) < 2.3e-308:
            ok = w is not None and abs(w - a) <= 8 * 5e-324
        else:
            ok = w is not None and math.isclose(w, a, rel_tol=1e-13)
        if not ok:
            ripoti("h-vikomo", n, f"karibu-sawa imeshindwa: swa={out!r} py={a!r}")

    # 3. JSON sahihi ya bahati nasibu
    hati = []
    for _ in range(IDADI):
        v = thamani(r, 0)
        s = andika_py(r, v)
        hati.append((s, v))
    for s, v in hati:
        for hoja, kundi in (((), "sahihi"), (("-m",), "sahihi-mzuri")):
            jumla[kundi] += 1
            rc, out, err = endesha(s, *hoja)
            if rc != 0:
                ripoti(kundi, s, "imekataliwa: " + err.strip())
                continue
            try:
                w = json.loads(out.decode("utf-8"))
            except Exception as e:  # noqa: BLE001
                ripoti(kundi, s, f"towe si JSON: {e}")
                continue
            if not sawa_kali(json.loads(s), w):
                ripoti(kundi, s, f"thamani tofauti: {w!r}")
        # Modi ya -h: nambari zinapangwa upya kutoka D64.
        jumla["sahihi-h"] += 1
        rc, out, err = endesha(s, "-h")
        if rc != 0:
            ripoti("sahihi-h", s, "imekataliwa: " + err.strip())
            continue
        try:
            w = json.loads(out.decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            ripoti("sahihi-h", s, f"towe si JSON: {e}: {out!r}")
            continue
        if not karibu(json.loads(s), w):
            ripoti("sahihi-h", s, f"thamani hazikaribiani: {w!r}")

    # 4. Ingizo lililoharibiwa: Swa na Python lazima wakubaliane.
    KIINGIZO = list('{}[]",:0123456789-+.eE tfnalsu\\/\n') + ["\\u", "true", "null", "1e5", "\\ud", '"a"', "[]", "{}"]
    for s, _ in hati[: IDADI]:
        for _ in range(3):
            m = list(s)
            if not m:
                continue
            for _ in range(r.randint(1, 2)):
                if not m:
                    break
                t = r.randint(0, 4)
                p = r.randrange(len(m))
                if t == 0:
                    del m[p]
                elif t == 1:
                    m.insert(p, r.choice(KIINGIZO))
                elif t == 2:
                    m = m[:p]
                elif t == 3:
                    m[p] = r.choice(KIINGIZO)
                else:
                    q = r.randrange(len(m))
                    m[p], m[q] = m[q], m[p]
            mut = "".join(m)
            if TOFAUTI_ZINAZOJULIKANA.search(mut) or "NaN" in mut or "Infinity" in mut:
                continue
            try:
                mut.encode("utf-8")
            except UnicodeEncodeError:
                continue
            try:
                pv = json.loads(mut)
                py_ok = True
            except (ValueError, RecursionError):
                py_ok = False
            jumla["mutation"] += 1
            rc, out, err = endesha(mut)
            swa_ok = rc == 0
            if py_ok != swa_ok:
                ripoti("mutation", mut, f"Python inakubali={py_ok}, Swa inakubali={swa_ok} ({err.strip()})")
                continue
            if py_ok:
                jumla["mutation-kubaliwa"] += 1
                try:
                    sv = json.loads(out.decode("utf-8"))
                except Exception as e:  # noqa: BLE001
                    ripoti("mutation", mut, f"towe si JSON: {e}")
                    continue
                if not sawa_kali(pv, sv):
                    ripoti("mutation", mut, f"thamani tofauti: {sv!r}")

    print(f"mbegu={MBEGU} idadi={IDADI}")
    for k, n in jumla.items():
        print(f"  {k:20s} {n}")
    if kosa:
        print(f"\nTOFAUTI {len(kosa)}:")
        for kundi, ingizo, maelezo in kosa[:25]:
            print(f"  [{kundi}] {ingizo[:200]!r}\n      -> {maelezo[:300]}")
        sys.exit(1)
    print("\nSAWA: hakuna tofauti dhidi ya Python json.")


if __name__ == "__main__":
    main()
