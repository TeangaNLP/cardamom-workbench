# Embedding models

## Data

The data come from [UD treebanks v2.12](https://universaldependencies.org/). Original tokenisation and sentence splitting are preserved for each corpus. Sentence-level punctuation is removed, word-level punctuation is untouched. The texts are lowercased.

Specialised corpora (sign language, code mixing, pronouns, ATIS) and corpora containing less than 5000 text symbols have not been used. 

Model names contain 3-letter [ISO 639-3 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-3_codes) for all the languages used in training (NB! UD use ISO 639-1 in their corpora filenames). There are a few custom 4-letter codes for language varieties not yet covered by ISO 639-3:

* islh — historical Islandic
* faoh — historical Faroese
* bulp — Pomak
* aram — Maghrebi Arabic

## Models

There are 4 types of models:

1. Trained on a single corpus for a single language (`Russian_SynTagRus_rus_ft_100_5_2`)
2. Synhronic: trained on all available corpora for a language (`Italian_UD_ita_ft_100_5_2`)
3. Diachronic: trained on different historical stages of the same language or a modern language and its ancestor (`Hebrew_UD_diachronic_heb_hbo_ft_100_5_2`)
4. Related: trained on related languages or dialects (`Kypchak_UD_related_kaz_kir_tat_ft_100_5_2`)

The structure of a model name is as follows:

|name of a language / group of languages|data source|diachronic / related|ISO codes|model type|emb_size|window|min_count|extension|
|-------------------------------------|-----------|------------------|---------|----------|--------|------|---------|---------|
|Komi|UD|related|koi_kpv|ft|100|5|2|.txt|
|Ancient-Greek|Perseus||grc|ft|100|5|2|.txt|
|Chinese|UD||cmn|ft|100|5|2|.txt|
|Ukrainian|UD|diachronic|ukr_orv|ft|100|5|2|.txt|

More information about corpora used in training synchronic, diachronic and related embedding models can be found below.

### Synchronic

Models trained on merged UD corpora for the same language.

* Akkadian = PISANDUB + RIAO
* Ancient Greek = Perseus + PROIEL + PTNK
* Arabic = PADT + PUD
* Armenian = ArmTDP + BSUT
* Chinese = CFL + GSD + GSDSimp + HK + PatentChar + PUD
* Czech = CAC + CLTT + FicTree + PDT + PUD
* Dutch = Alpino + LassySmall
* English = EWT + GUM + LinES + PatTUT + PUD + GENTLE
* Estonian = EDT + EWT
* Finnish = FTB + OOD + PUD + TDT
* French = FQB + GSD + ParisStories + ParTUT + PUD + Rhapsodie + Sequoia
* Galician = CTG + TreeGal
* German = GSD + HDT + LIT + PUD
* Greek = GDT + GUD
* Hebrew = IAHLTwiki + HTB
* Hindi = HDTB + PUD
* Icelandic = GC + Modern + PUD
* Indonesian = CSUI + GSD + PUD
* Irish = Cadhan + IDT + TwittIrish
* Italian = ISDT + MarkIT + ParlaMint + ParTUT + PoSTWITA + PUD + TWITTIRO + Valico + VIT
* Japanese = GSD + GSDLUW + Modern + PUD + PUDLUW
* Komi-Zyrian = IKDP + LAttice
* Korean = GSD + Kaist + PUD
* Latin = ITTB + LLCT + Perseus + PROIEL + UDante
* Lithuanian = ALKSNIS + HSE
* Norwegian Nynorsk = Nynorsk + NynorskLIA
* Old East Slavic = Birchbark + RNC + Ruthenian + TOROT
* Persian = PerDT + Seraji
* Polish = LFG + PDB + PUD
* Portuguese = Bosque + CINTIL + GSD + PetroGold + PUD
* Romanian = ArT + Nonstandard + RRT + SiMoNERo
* Russian = GSD + PUD + SynTagRus + Taiga
* Slovenian = SSJ + SST
* Spanish = AnCora + GSD + PUD
* Swedish = LinES + PUD + Talbanken
* Tagalog = TRG + Ugnayan
* Tamil = MWTT + TTB
* Turkish = BOUN + FrameNet + GB + IMST + Kenet + Penn + PUD + Tourism


### Related

Models trained on merged UD corpora of related languages or dialects. Every word has a language tag attached to it, but you can make queries without these tags.

* Albanian = Albanian + Gheg
* Arabic = Arabic + South Levantine Arabic
* Armenian = Armenian + West Armenian
* Bulgarian = Bulgarian + Pomak
* Czech_Slovak = Czech + Slovak
* Eastern Scandianvian = Danish + Swedish + Norwegian Bokmaal + Norwegian Nynorsk
* Eastern Slavic = Ukrainian + Belorussian + Russian
* German = German + Swiss German
* Goidelic = Irish + Scottish Gaelic + Manx
* Guarani = Guarani + Mbya-Guarani
* Iberian Romance = Spanish + Portuguese + Galician + Catalan
* Karelian = Karelian + Livvi Karelian
* Komi = Komi-Zyrian + Komi-Permyak
* Kypchak = Tatar + Kazakh + Kyrgyz
* Low_Saxon_Frisisan = Low Saxon + West Frisian
* Mordvin = Moksha + Erzya
* Northern Finnic = Finnish + Karelian + Livvi Karelian
* Sami = North Sami + Skolt Sami
* Serbo-Croatian = Serbian + Croatian
* South-West Slavic = Serbian + Croatian + Slovenian
* Western Scandinavian = Icelandic + Faroese
* Western Slavic = Polish + Czech + Slovak


### Diachronic

Models trained on merged UD corpora of differenct historical stages of the same language. Every word has a language tag attached to it, but you can make queries without these tags

* Belorussian Diachronic = Belorussian + Old East Slavic
* Chinese Diachronic = Chinese + Classical Chinese
* French Diachronic = French + Old French
* Faroese Diachronic = Faroese + Historical Faroese
* Greek Diachronic = Greek + Ancient Greek
* Hebrew Diachronic = Hebrew + Ancient Hebrew
* Icelandic Diachronic = Icelandic + Historical Icelandic
* Russian Diachronic = Russian + Old East Slavic
* Ukrainian Diachronic = Ukrainian + Old East Slavic