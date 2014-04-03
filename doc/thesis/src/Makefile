latex=latex
bibtex=bibtex
dvips=dvips
pdflatex=pdflatex

documents=these ex_chp

.PHONY: all
all: ps pdf

.PHONY: ps pdf
ps: $(documents:%=%.ps)
pdf: $(documents:%=%.pdf)

$(documents:%=%.pdf): %.pdf: %.tex
	$(pdflatex) $*
	$(bibtex) $*||true
	$(pdflatex) $*

$(documents:%=%.ps): %.ps: %.tex
	$(latex) $*
	$(bibtex) $*||true
	$(latex) $* &&\
	$(dvips) $*.dvi -o $@
