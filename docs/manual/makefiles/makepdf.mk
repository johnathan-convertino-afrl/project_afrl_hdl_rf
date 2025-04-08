SRCDIR=src

LAT_COM_SRC=$(SRCDIR)/common.tex
LAT_COM_AUX=$(LAT_COM_SRC:.tex=.aux)

LAT_PDF_SRC=$(SRCDIR)/pdf.tex
LAT_PDF_PDF=$(PROJECT_NAME).pdf

AUX=$(LAT_PDF_PDF:.pdf=.aux)
LOG=$(LAT_PDF_PDF:.pdf=.log)
TOC=$(LAT_PDF_PDF:.pdf=.toc)
OUT=$(LAT_PDF_PDF:.pdf=.out)

.PHONY: clean

all: $(LAT_PDF_PDF)

$(LAT_PDF_PDF): $(LAT_PDF_SRC) $(LAT_COM_SRC)
	pdflatex -jobname $(basename $@) -shell-escape -interaction=batchmode $<
	pdflatex -jobname $(basename $@) -shell-escape -interaction=batchmode $<
	rm $(AUX) $(LOG) $(TOC) $(OUT) $(LAT_COM_AUX)

clean:
	rm -rf *.pdf $(AUX) $(LOG) $(TOC) $(OUT) $(LAT_COM_AUX)
