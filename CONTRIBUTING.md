# Kuchangia kwenye json-swa

Karibu! Mradi huu ni maktaba ya JSON iliyoandikwa kwa **Swa safi**. Kanuni
tatu zinaongoza kila badiliko:

1. **Swa safi.** Msimbo wa maktaba, majaribio na mifano ni Swa -- hakuna
   Python, hakuna C, hakuna utegemezi wa libc. Script za `bash` (`jenga.sh`,
   `jaribu.sh`) ni gundi ya kujenga tu; usiongeze mantiki ya majaribio ndani
   yake. Kama unahitaji kipimo, kiandike kama jaribio la Swa.
2. **Kila badiliko lina jaribio.** Marekebisho ya mdudu huanza na jaribio
   linalofeli, kisha suluhisho. Kipengele kipya kinakuja na majaribio yake.
3. **Uaminifu kuhusu mipaka.** Kama badiliko linaongeza au linaondoa kikomo,
   sasisha sehemu ya "Mipaka inayojulikana" kwenye README na
   [CHANGELOG.md](CHANGELOG.md) kwenye PR ile ile.

## Mazingira

- Linux x86-64, `bash`, na hazina ya
  [lugha-swa/swa](https://github.com/lugha-swa/swa) (chaguo-msingi
  `~/Projects/compilers/swa`, au `SWA=/njia`).

```sh
./jaribu.sh                              # majaribio yote -- lazima yapite
./jaribu.sh jaribio/jaribio_corpus.swa   # jaribio moja
.jenga/jaribio_fuzz 7 50000              # fuzz ndefu kwa mbegu nyingine
```

## Kabla ya kutuma PR

- [ ] `./jaribu.sh` inapita (6 kati ya 6 kwa sasa).
- [ ] Kama umegusa kichanganuzi: kesi mpya kwenye `jaribio/corpus/` (na
      `ORODHA.txt`) yenye matarajio kutoka **RFC 8259**, si kutoka tabia ya
      msimbo wako. Kesi za `y_` lazima zikubaliwe, `n_` zikataliwe.
- [ ] Kama umegusa kiandikaji: kesi kwenye `jaribio_andika.swa`.
- [ ] `fuzz` bado inapita kwa mbegu chache tofauti (angalau
      `.jenga/jaribio_fuzz 424242 20000`).
- [ ] Ujumbe wa commit kwa Kiswahili, wenye aina: `ongeza:`, `rekebisha:`,
      `jaribio:`, `panga upya:` (angalia `git log`).
- [ ] Hakuna faili la lugha nyingine; hakuna alama za AI kwenye commit/PR.

## Kuripoti mdudu

Fungua issue yenye: ingizo dogo kabisa linaloonyesha tatizo, matokeo
uliyotarajia (na kifungu cha RFC 8259 kama ni suala la sarufi), na matokeo
uliyopata. Ingizo la JSON ni kesi bora ya `corpus/` tayari.

## Mtindo

- Majina ya kazi/aina/vigezo vya ulimwengu yanaanza na `json_`/`Json`/`JSON_`
  (Swa haina nafasi za majina); msaada wa ndani hutumia `json_` pia lakini
  haujaorodheshwa kwenye README.
- Maoni kwa Kiswahili; eleza *kwa nini*, si *nini*.
- Kila njia ya kushindwa hurudisha `0`/msimbo -- usiache kuanguka kwa ingizo
  lolote la mtumiaji.
