# json-swa

[![CI](https://github.com/Sakajara/json-swa/actions/workflows/ci.yml/badge.svg)](https://github.com/Sakajara/json-swa/actions/workflows/ci.yml)
[![Leseni: MIT](https://img.shields.io/badge/leseni-MIT-blue.svg)](LICENSE)

Maktaba ya **JSON** (kuchanganua na kuandika) iliyoandikwa kwa **Swa safi** --
lugha ya mfumo ya Kiswahili inayojikusanya yenyewe, isiyotegemea libc kabisa.
Kichanganuzi cha RFC 8259 chenye ripoti sahihi ya makosa (mstari, safu, nafasi),
kiandikaji cha compact na pretty, na uwakilishi wa thamani unaojengeka kwa
programu.

- **Faili moja**: `json.swa` ndiyo maktaba yote (~1,200 mistari).
- **Utegemezi**: `kumbukumbu.swa` na `mfuatano.swa` za maktaba ya msingi ya
  Swa tu. Hakuna libc, hakuna lugha nyingine yoyote -- msimbo, majaribio na
  mfano vyote ni Swa (script za `bash` ni gundi ya kujenga tu, kama ilivyo
  kwenye hazina ya `lugha-swa/swa` yenyewe).
- **Imethibitishwa** dhidi ya kesi 107 za RFC 8259, mamia ya maelfu ya kesi za
  fuzz zenye mbegu inayojirudia, na kuvunja msimbo kwa makusudi (angalia
  [Uthibitisho](#uthibitisho)).

## Yaliyomo

1. [Kuanza haraka](#kuanza-haraka)
2. [Mwongozo](#mwongozo)
3. [Marejeo ya API](#marejeo-ya-api)
4. [Uwakilishi wa thamani na usanifu](#uwakilishi-wa-thamani-na-usanifu)
5. [Mipaka inayojulikana](#mipaka-inayojulikana)
6. [Uthibitisho](#uthibitisho)
7. [Kujenga na kujaribu](#kujenga-na-kujaribu)
8. [Muundo wa hazina](#muundo-wa-hazina)
9. [Uoanifu](#uoanifu)
10. [Kuchangia](#kuchangia) | [Historia ya mabadiliko](CHANGELOG.md) | [Leseni](#leseni)

## Kuanza haraka

Unahitaji hazina ya [lugha-swa/swa](https://github.com/lugha-swa/swa)
(chaguo-msingi `~/Projects/compilers/swa`, au weka `SWA=/njia`):

```sh
git clone https://github.com/Sakajara/json-swa.git && cd json-swa
./jenga.sh mfano/matumizi.swa .jenga/matumizi && .jenga/matumizi
```

`jenga.sh` hujenga mkusanyaji wa Swa mara ya kwanza tu, kisha huunganisha
`json.swa` mbele ya faili lako na kulikusanya. Faili lako **halihitaji**
kuhusisha `json.swa` mwenyewe.

Matokeo ya `mfano/matumizi.swa`:

```
jina  = Amina
umri  = 27
lugha = 2 (kwanza: Kiswahili)
{
  "jina": "Amina",
  "umri": 27,
  "lugha": [
    "Kiswahili",
    "Swa"
  ],
  "mwanafunzi": true
}
```

## Mwongozo

### Kuchanganua na kusoma

```swa
JsonKosa kosa;
Json* v = json_changanua("{\"jina\": \"Amina\", \"umri\": 27, \"lugha\": [\"Kiswahili\", \"Swa\"]}", &kosa);
kama (v == 0) {
    N8 ujumbe[512];
    json_ujumbe_wa_kosa(&kosa, ujumbe, 512);
    andika_stderr("%s\n", ujumbe, 0, 0, 0, 0, 0);
    rudisha 1;
}

N8*  jina  = json_thamani_mfuatano(json_pata(v, "jina"));      // "Amina"
D64  umri  = json_thamani_nambari(json_pata(v, "umri"));       // 27.0
Json* lugha = json_pata(v, "lugha");
N32  idadi = json_urefu(lugha);                                // 2
N8*  kwanza = json_thamani_mfuatano(json_kipengele(lugha, 0)); // "Kiswahili"
```

Kila kifikiaji ni **salama kwa aina isiyo sahihi**: `json_pata` kwenye thamani
isiyo kitu, au ufunguo usiopo, hurudisha `0`; `json_thamani_nambari` kwenye
mfuatano hurudisha `0.0`. Hakuna kuanguka -- lakini kumbuka kukagua `0`
kabla ya kupitisha matokeo ya `json_pata` kwa kifikiaji kingine.

### Kujenga na kuandika

```swa
Json* kitu = json_kitu();
json_kitu_weka(kitu, "jina", json_mfuatano("Amina"));
json_kitu_weka(kitu, "umri", json_nambari(27.0));
Json* orodha = json_orodha();
json_orodha_ongeza(orodha, json_bool(1));
json_orodha_ongeza(orodha, json_null());
json_kitu_weka(kitu, "vitu", orodha);

andika("%s\n", json_hadi_mfuatano(kitu), 0, 0, 0, 0, 0);
// {"jina":"Amina","umri":27,"vitu":[true,null]}

andika("%s\n", json_hadi_mfuatano_mzuri(kitu, 2), 0, 0, 0, 0, 0);   // nafasi 2 kwa ngazi
```

Kuweka ufunguo uliopo (`json_kitu_weka`) **hubadilisha** thamani yake, na
mpangilio wa kuingizwa unahifadhiwa.

### Makosa

`json_changanua` na `json_changanua_n` hurudisha `0` kwa ingizo batili na
kujaza `JsonKosa`:

| uwanja | maana |
|---|---|
| `msimbo` | `0` = hakuna kosa, `1` = kuna kosa |
| `nafasi` | nafasi ya baiti (kuanzia 0) |
| `mstari` | mstari (kuanzia 1) |
| `safu` | safu kwa baiti (kuanzia 1) |
| `ujumbe` | maelezo ya kosa |

`json_ujumbe_wa_kosa(&kosa, bafa, uwezo)` huandika ujumbe kamili kwenye bafa
yako, mfano:

```
kosa la JSON: herufi isiyotarajiwa (thamani ya JSON inatarajiwa) (mstari 1, safu 10, nafasi 9)
kosa la JSON: mwisho wa maandishi usiotarajiwa: thamani inatarajiwa (mstari 1, safu 7, nafasi 6)
```

### Kumbukumbu

Kila kitu kinatengwa kwa `tenga()` ya arena ya `kumbukumbu.swa`, ambayo
**haifungui vipande vya kibinafsi**: kumbukumbu inarudishwa programu
inapoisha. Hii inafaa zana za mstari-wa-amri, majaribio na kazi za muda
mfupi; kwa programu inayochanganua JSON bila mwisho (seva), kumbukumbu
itakua. Kushindwa kutenga hurudisha `0` (na `json_kosa` "kumbukumbu imeisha"
wakati wa kuchanganua) -- halianguki.

Thamani zilizojengwa **hunakiliwa**: `json_mfuatano(s)` na `json_kitu_weka`
(kwa ufunguo) hunakili maandishi yao, kwa hiyo unaweza kubadilisha `s`
baadaye.

## Marejeo ya API

Majina yote yanaanza na `json_`/`Json`/`JSON_` kwa sababu Swa haina nafasi za
majina. "0" kwenye jedwali la kurudisha kwa vielekezi inamaanisha kielekezi
tupu.

### Aina

| jina | maelezo |
|---|---|
| `Json` | thamani ya JSON (muundo mmoja wenye uwanja wa `aina`) |
| `JsonKosa` | matokeo ya kosa la kuchanganua (`msimbo`, `nafasi`, `mstari`, `safu`, `ujumbe`) |
| `JSON_NULL` `JSON_BOOL` `JSON_NAMBARI` `JSON_MFUATANO` `JSON_ORODHA` `JSON_KITU` | thamani za `aina` (0..5) |
| `JSON_KINA_JUU` | kina cha juu cha nesting kinachokubaliwa na kichanganuzi (512) |

### Kuchanganua

| kazi | inarudisha |
|---|---|
| `Json* json_changanua(N8* maandishi, JsonKosa* kosa)` | mzizi, au `0` + `kosa` limejazwa. `maandishi` unaishia kwa NUL |
| `Json* json_changanua_n(N8* data, N32 urefu, JsonKosa* kosa)` | sawa, lakini kwa data ya urefu unaojulikana (baiti `0` ndani ya data ni batili kwa JSON) |
| `N64 json_ujumbe_wa_kosa(JsonKosa* kosa, N8* bafa, N64 uwezo)` | idadi ya baiti zilizoandikwa (bila NUL); hukatwa salama kwa `uwezo` |

### Kujenga

| kazi | inarudisha |
|---|---|
| `Json* json_null()` | thamani ya null |
| `Json* json_bool(N32 kweli)` | bool (`kweli != 0` -> true) |
| `Json* json_nambari(D64 x)` | nambari (haina maandishi asili) |
| `Json* json_mfuatano(N8* s)` | mfuatano (unanakiliwa; UTF-8, unaishia kwa NUL) |
| `Json* json_orodha()` / `Json* json_kitu()` | orodha / kitu tupu |
| `N32 json_orodha_ongeza(Json* orodha, Json* kipengele)` | `1` kwa mafanikio, `0` kama kumbukumbu imeisha au `orodha` si orodha |
| `N32 json_kitu_weka(Json* kitu, N8* ufunguo, Json* kipengele)` | `1` kwa mafanikio (huchukua nafasi ya ufunguo uliopo); `0` kwa kushindwa |

Kila kijenzi hurudisha `0` kama kumbukumbu imeisha.

### Kusoma

| kazi | inarudisha |
|---|---|
| `N32 json_aina(Json* v)` | `JSON_*` |
| `N32 json_urefu(Json* v)` | idadi ya vipengele (orodha/kitu) au urefu wa baiti (mfuatano); `0` kwa aina nyingine |
| `Json* json_kipengele(Json* orodha, N32 i)` | kipengele; `0` kama nje ya mipaka au si orodha |
| `Json* json_pata(Json* kitu, N8* ufunguo)` | thamani; `0` kama haipo au si kitu |
| `N8* json_ufunguo_wa(Json* kitu, N32 i)` | ufunguo wa nafasi `i` (mpangilio wa kuingizwa); `0` kama nje ya mipaka |
| `N32 json_thamani_bool(Json* v)` | `0`/`1`; `0` kwa aina isiyo bool |
| `D64 json_thamani_nambari(Json* v)` | thamani; `0.0` kwa aina isiyo nambari |
| `N8* json_thamani_mfuatano(Json* v)` | maandishi (si nakala -- usiyabadilishe); `0` kwa aina isiyo mfuatano |

### Kuandika na kulinganisha

| kazi | inarudisha |
|---|---|
| `N8* json_hadi_mfuatano(Json* v)` | JSON ya mstari mmoja; `0` kama kumbukumbu imeisha au kina > 4096 |
| `N8* json_hadi_mfuatano_mzuri(Json* v, N32 ndani)` | JSON yenye upangaji (`ndani` nafasi kwa ngazi) |
| `N32 json_sawa(Json* a, Json* b)` | `1` kama zinawakilisha JSON ile ile: vitu bila kujali mpangilio wa funguo, nambari kwa thamani ya D64 |
| `W0 json_sahau_maandishi_asili(Json* v)` | hufanya nambari zote ziandikwe kutoka thamani ya D64 (angalia [Nambari](#nambari)) |

### Nambari

Nambari zilizosomwa huhifadhi **maandishi asili** pamoja na thamani ya D64, kwa
hiyo kuandika tena hakupotezi taarifa: `[12345678901234567890, 1.50]` inaandikwa
kama ilivyoingizwa. Nambari zilizojengwa kwa `json_nambari` huandikwa kwa
tarakimu 15 za maana (kama `%.15g`): nukuu ya kawaida kwa vipeo -5..14,
vinginevyo ya kisayansi (`1.5e+20`); isiyo na mwisho na NaN huandikwa `null`
(kama `JSON.stringify` ya JavaScript). `json_sahau_maandishi_asili` hulazimisha
njia hiyo hiyo kwa nambari zilizosomwa: `[12345678901234567890,1.50]` ->
`[1.23456789012346e+19,1.5]`.

## Uwakilishi wa thamani na usanifu

Swa haina `union` wala `enum`, kwa hiyo aina zote sita za JSON zinawakilishwa
na muundo **mmoja**, `Json`, wenye uwanja wa `aina` (tag) unaoamua nyanja zipi
zinatumika:

| aina | nyanja zinazotumika |
|---|---|
| `JSON_NULL` | -- |
| `JSON_BOOL` | `kweli` |
| `JSON_NAMBARI` | `nambari` (D64), `maandishi` (maandishi asili, au `0`) |
| `JSON_MFUATANO` | `maandishi` (UTF-8) |
| `JSON_ORODHA` | `vipengele`, `idadi`, `uwezo` |
| `JSON_KITU` | `funguo` na `vipengele` (jozi sambamba, mpangilio wa kuingizwa), `idadi`, `uwezo` |

Maamuzi ya usanifu:

- **Muundo mmoja, si miundo sita**: kielekezi kimoja (`Json*`) kinatosha kuwakilisha
  thamani yoyote, na orodha/vitu vinaweza kuchanganya aina bila kazi ya ziada.
- **Vitu kama jozi sambamba za safu, si jedwali la heshi**: utafutaji ni
  wa mstari (`O(n)`), lakini mpangilio wa kuingizwa unahifadhiwa kwa asili na
  vitu vya JSON kwa kawaida ni vidogo. Kwa vitu vikubwa sana (maelfu ya funguo)
  hili litakuwa polepole.
- **Kichanganuzi cha recursive-descent chenye kikomo cha kina (512)**: kinalinda
  rafu ya wito kutokana na `[[[[...` ya kubuni; kuzidi kunatoa kosa la wazi,
  si kuanguka.
- **Maandishi asili ya nambari yanahifadhiwa**: D64 ina tarakimu ~15.9 tu; bila
  hili nambari kama `12345678901234567890` zingebadilika kimya kimya
  zikipita kwenye maktaba.
- **Makosa ni thamani, si kuanguka**: kila njia ya kushindwa (ingizo batili,
  kumbukumbu, kina) hurudisha `0` au msimbo, na kichanganuzi hujaza mstari/safu.

## Mipaka inayojulikana

Zimeandikwa kwa uwazi -- hakuna zinazofichwa:

- **UTF-8 haithibitishwi**: baiti `>= 0x80` kwenye mifuatano hupita kama
  zilivyo (RFC 8259 inataka UTF-8 sahihi; vichanganuzi vikali hukataa
  isiyo sahihi). Mifuatano inayotoka `\uXXXX` inatoa UTF-8 sahihi.
- **`\u0000` na *surrogate* isiyo na jozi** (`\ud800` peke yake) zinakataliwa,
  ingawa RFC 8259 inaziruhusu kisintaksia (mifuatano ya Swa inaishia kwa NUL;
  surrogate pekee haina herufi halali).
- **Kina cha juu cha nesting ni 512** wakati wa kuchanganua na **4096** wakati
  wa kuandika (thamani iliyojengwa kwa programu yenye kina zaidi hufanya
  `json_hadi_mfuatano` irudishe `0`).
- **Nambari ni D64**: `json_thamani_nambari` inapoteza usahihi kupita ~2^53
  (maandishi asili yanahifadhiwa, kwa hiyo kuandika tena ni sahihi).
- **Kumbukumbu haifunguliwi** kipande kwa kipande (arena) -- angalia
  [Kumbukumbu](#kumbukumbu).
- **Vitu ni `O(n)` kwa utafutaji** -- angalia [usanifu](#uwakilishi-wa-thamani-na-usanifu).
- Funguo zinazorudiwa kwenye kitu: thamani ya **mwisho** inashinda.
- Hakuna mkondo (*streaming*) wala uandishi wa sehemu kwa sehemu: ingizo
  lote linasomwa kwenye kumbukumbu kwanza.

## Uthibitisho

Majaribio yote ni Swa safi na yanaendeshwa na `./jaribu.sh` (yenye kikomo cha
muda kwa kila jaribio, ili kuning'inia kuhesabiwe kama kushindwa):

| jaribio | linathibitisha nini |
|---|---|
| `jaribio_thamani` | vijenzi, vifikiaji, ukuaji wa orodha/kitu, aina isiyo sahihi |
| `jaribio_changanua` | kichanganuzi: thamani sahihi za kila aina (mifuatano na escape, nambari, orodha, vitu) |
| `jaribio_makosa` | JSON batili hukataliwa; mstari/safu/nafasi sahihi; kikomo cha kina |
| `jaribio_andika` | kiandikaji: compact/pretty, escape, nambari za D64 (hadi karibu `DBL_MAX`), mfuatano mrefu |
| `jaribio_corpus` | **kesi 107 za RFC 8259** (`jaribio/corpus/`, 43 lazima zikubaliwe, 64 zikataliwe) + kuandika upya kila kesi sahihi (compact na pretty, fixpoint) |
| `jaribio_fuzz` | **majaribio ya mali** (angalia chini) |

**Kuhusu corpus**: matarajio ya kila kesi yanatoka kwenye RFC 8259, si kutoka
kwa tabia ya kichanganuzi hiki; mtindo ni wa JSONTestSuite (`y_` = lazima
ikubaliwe, `n_` = lazima ikataliwe). Kesi zilizo na majibu yanayotegemea
utekelezaji (`\u0000`, surrogate pekee, UTF-8 batili) hazimo -- ni
[mipaka](#mipaka-inayojulikana) iliyoandikwa.

**Kuhusu fuzz**: kwa mbegu inayojulikana (linajirudia kabisa), kila kesi
huzalisha thamani nasibu (kina hadi 4, mifuatano yenye nukuu, backslash, herufi
za kudhibiti na UTF-8 ya baiti 2/3/4) kisha huthibitisha: compact na pretty
zinasomeka tena kwa thamani ile ile, na kuandika ni **fixpoint**; na mamia ya
maelfu ya ingizo **zilizoharibiwa** (baiti zilizobadilishwa/kufutwa/kuingizwa/
kukatwa) hazipaswi kuanguka wala kuning'inia, hutoa ujumbe wa kosa
zikikataliwa, na zikikubaliwa huandikwa upya kwa fixpoint.

```sh
.jenga/jaribio_fuzz [mbegu] [idadi]      # mfano: .jenga/jaribio_fuzz 7 50000
```

**Uaminifu kuhusu mipaka ya kila jaribio**: fuzz ni kipimo cha *uthabiti wa
ndani* (kuandika/kusoma kunakubaliana, hakuna kuanguka), si cha *usahihi wa
sarufi* -- kichanganuzi kilichokubali `[1,]` kwa makosa kingepita fuzz lakini
kinakamatwa na corpus. Ndiyo maana vyote viwili vipo, na vinakamilishana.

**Kuvunja msimbo kwa makusudi** (mutation testing, kwa mkono): tulivunja
`json.swa` kwa njia nne -- kiandikaji kisifanye escape ya backslash, kiandikaji
kiandike `\n` kama `\r`, kichanganuzi kikubali koma ya mwisho kwenye orodha, na
kichanganuzi kikubali sifuri ya mwanzo (`01`). Mianya yote minne ilikamatwa
(mbili za kwanza na corpus na fuzz zote mbili; mbili za pili na corpus).

## Kujenga na kujaribu

```sh
./jaribu.sh                                   # majaribio yote
./jaribu.sh jaribio/jaribio_corpus.swa        # jaribio moja
JARIBIO_MUDA=60 ./jaribu.sh                   # kikomo cha muda (sekunde) kwa kila jaribio; chaguo-msingi 300
SWA=/njia/ya/swa ./jaribu.sh                  # hazina ya mkusanyaji isiyo ya chaguo-msingi
```

Zana ya mstari-wa-amri `mfano/jsonzuri.swa` husoma JSON kutoka stdin na
kuiandika tena:

```sh
./jenga.sh mfano/jsonzuri.swa .jenga/jsonzuri
echo '{"a":[1,2,{"b":null}]}' | .jenga/jsonzuri        # compact
echo '{"a":[1,2,{"b":null}]}' | .jenga/jsonzuri -m     # pretty
echo '[1.50, 12345678901234567890]' | .jenga/jsonzuri -h   # nambari kutoka D64
```

Msimbo wa kutoka: `0` = sawa, `1` = JSON batili (ujumbe kwenye stderr).

## Muundo wa hazina

```
json.swa              maktaba yote
jenga.sh              kusanya programu ya Swa inayotumia json.swa
jaribu.sh             endesha majaribio yote (yenye kikomo cha muda)
jaribio/              majaribio (Swa) + msaada.swa
jaribio/corpus/       kesi 107 za RFC 8259 (ORODHA.txt + *.json)
mfano/matumizi.swa    mfano mdogo
mfano/jsonzuri.swa    zana ya mstari-wa-amri
.github/workflows/    CI
```

## Uoanifu

Imejaribiwa dhidi ya `lugha-swa/swa` @ `aa1b87f` (2026-09-18), na CI hujaribu
dhidi ya `main` ya sasa kila push na kila Jumatatu, ili mkusanyaji
ukivunja kitu ugunduliwe mapema. Inahitaji Linux x86-64 (mkusanyaji wa Swa
unatoa ELF ya x86-64 moja kwa moja).

## Kuchangia

Karibu -- angalia [CONTRIBUTING.md](CONTRIBUTING.md). Kwa ufupi: kila badiliko
lina jaribio; `./jaribu.sh` lazima ipite; msimbo unabaki Swa safi.

## Leseni

MIT -- angalia [LICENSE](LICENSE).
