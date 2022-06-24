python3 get_rankstats.py ../../data/ud-treebanks-v2.3/ UD_German UD_Gothic UD_English UD_Finnish UD_Latin UD_Turkish UD_Spanish
python3 read_lemmas_CHILDES_by_dir.py ../../data/CHILDES/English/Brown ../../data/CHILDES/German/Leo/ ../../data/CHILDES/Spanish/FernAguado/ --language English German Spanish

tail -n +2 lemmasCDS.csv >> lemmas.csv
tail -n +2 inflCDS.csv >> infls.csv
