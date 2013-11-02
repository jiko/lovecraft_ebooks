import os, re
corpus_files = []
[corpus_files.append(files) for files in os.listdir(".") if files.endswith(".txt")]
with open('corpus.txt','a') as a:
	for f in corpus_files:
		with open(f) as o:
			text = o.read()
			text = ' '.join(text.split())
			# remove the default intro
			sin_intro = text.split("Strictly for personal use, do not use this file for commercial purposes.")
			text = sin_intro[1]
			# remove the default outro
			sin_outro = re.split("Loved this book\s?\?",text)
			text = sin_outro[0]+"\n\n"
			# need to remove chapter headings and such
			roman_numerals = "chapter\s+(?:X{0,3})?(?:IX|IV|V?I{0,3})(?:\s+\d{1,2}\s+)?"
			text = ' '.join(re.split(roman_numerals,text,flags=re.I))
			text = ' '.join(re.split("chapter\s\d+",text,flags=re.I))
			a.write(text)
