SRC_DIR=src

CSS_DIR=css
CSS_DEFAULT=$(CSS_DIR)/custom_font_l2h.css

HTML_DIR=html
ND_HTML=$(HTML_DIR)/index.html
ND_HTML_FILES=$(wildcard $(HTML_DIR)/files/*.html)

LAT_COM_SRC=$(SRC_DIR)/common.tex
LAT_HTML_SRC=$(SRC_DIR)/html.tex
LAT_HTML_HTML=$(LAT_HTML_SRC:.tex=.html)
LAT_HTML_CSS=$(LAT_HTML_SRC:.tex=.css)

.PHONY: clean

all: $(ND_HTML)

$(ND_HTML): $(LAT_HTML_SRC)
	mkdir -p $(HTML_DIR)
	latex2html $< -prefix $(PROJECT_NAME)_ -dir $(HTML_DIR)
	cp $(CSS_DEFAULT) $(HTML_DIR)/$(notdir $(LAT_HTML_CSS))

clean:
	rm -rf $(HTML_DIR)/*
