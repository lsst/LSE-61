#
#

LSE-61.pdf:  LSE-61.tex metadata.tex
	latexmk -bibtex -xelatex -f LSE-61.tex
