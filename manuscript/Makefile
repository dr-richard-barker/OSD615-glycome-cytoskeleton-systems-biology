all: pdf docx
pdf:
	pdflatex main && bibtex main && pdflatex main && pdflatex main
docx:
	pandoc main.tex -o ../docs/manuscript/glycome_cytoskeleton_manuscript.docx --bibliography=references.bib --citeproc
clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk
