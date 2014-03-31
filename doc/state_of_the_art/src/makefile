
all: touch dvi bib dvi dvi pdf clean 

touch:
	for file in $$(ls *pdf | cut -d \. -f 1) ; do touch $$file.tex ; done

dvi:
	for file in $$(ls *tex | cut -d \. -f 1) ; do make $$file.dvi ; done

pdf:
	for file in $$(ls *dvi | cut -d \. -f 1) ; do make $$file.pdf ; done

bib:
	for file in $$(ls *aux | cut -d \. -f 1) ; do make $$file.aux ; done

%.aux: %
	bibtex $<

%.dvi: %.tex
	latex $<

%.pdf: %.dvi
	dvipdf $<

clean:
	rm -f *.toc *.aux *.log *.out

cleanall:
	rm -f *.toc *.pdf *.aux *.log *.out

.PHONY: all pdf clean cleanall
.SILENT: pdf

# vim: set tabstop=4 shiftwidth=4 noexpandtab:
