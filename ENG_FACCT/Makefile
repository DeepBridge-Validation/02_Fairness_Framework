# Makefile for FAccT 2026 Submission
# DeepBridge Fairness Paper

.PHONY: all clean quick full check info anonymize help

# Default target
all: full

# Quick compilation (no bibliography)
quick:
	@echo "=== Quick compilation (no bibliography) ==="
	pdflatex -interaction=nonstopmode main.tex
	@echo "=== Done! Check main.pdf ==="

# Full compilation with bibliography
full:
	@echo "=== Full compilation with bibliography ==="
	pdflatex -interaction=nonstopmode main.tex
	bibtex main
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex
	@echo ""
	@echo "=== Compilation complete! ==="
	@$(MAKE) info

# Check paper info
info:
	@echo ""
	@echo "=== Paper Information ==="
	@pdfinfo main.pdf | grep -E "(Pages|File size|Page size)"
	@echo ""
	@echo "WARNING: FAccT limit is 14 pages (excluding references)"
	@echo "Check if references start after page 14!"
	@echo ""

# Check for identifying information (anonymization check)
anonymize:
	@echo "=== Checking for identifying information ==="
	@echo ""
	@echo "PDF Metadata:"
	@pdfinfo main.pdf | grep -E "(Author|Creator|Producer|Title)"
	@echo ""
	@echo "Searching for potential identifying strings in .tex files:"
	@grep -n "Gustavo\|Paulo\|Haase\|Silva\|Banco do Brasil" sections/*.tex main.tex || echo "No author names found (good!)"
	@echo ""
	@echo "Searching for GitHub links:"
	@grep -n "github.com" sections/*.tex main.tex || echo "No direct GitHub links found (good!)"
	@echo ""
	@echo "If any identifying information found, remove it before submission!"

# Remove metadata from PDF
strip-metadata:
	@echo "=== Removing PDF metadata ==="
	@if command -v exiftool > /dev/null; then \
		exiftool -all= main.pdf; \
		rm -f main.pdf_original; \
		echo "Metadata removed successfully!"; \
	else \
		echo "ERROR: exiftool not found. Install with: sudo apt-get install libimage-exiftool-perl"; \
	fi

# Word count (approximate)
wordcount:
	@echo "=== Approximate word count ==="
	@if command -v texcount > /dev/null; then \
		texcount -total -inc main.tex; \
	else \
		echo "texcount not found. Install with: tlmgr install texcount"; \
	fi

# Check LaTeX/BibTeX errors
check:
	@echo "=== Checking for errors ==="
	@echo ""
	@echo "LaTeX warnings:"
	@grep -i "warning\|error" main.log | head -20 || echo "No critical warnings"
	@echo ""
	@echo "BibTeX warnings:"
	@grep -i "warning" main.blg | head -10 || echo "No BibTeX warnings"

# Clean auxiliary files
clean:
	@echo "=== Cleaning auxiliary files ==="
	rm -f *.aux *.log *.out *.bbl *.blg *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz
	rm -f sections/*.aux
	@echo "Clean complete!"

# Clean everything including PDF
distclean: clean
	@echo "=== Removing PDF ==="
	rm -f main.pdf
	@echo "Distclean complete!"

# Archive for submission
archive:
	@echo "=== Creating submission archive ==="
	@mkdir -p ../submission
	tar czf ../submission/facct2026_submission_$(shell date +%Y%m%d).tar.gz \
		main.tex sections/ bibliography/ figures/ \
		--exclude='*.aux' --exclude='*.log' --exclude='*.pdf'
	@echo "Archive created: ../submission/facct2026_submission_$(shell date +%Y%m%d).tar.gz"

# Help
help:
	@echo "DeepBridge Fairness - FAccT 2026 Submission"
	@echo ""
	@echo "Available targets:"
	@echo "  make           - Full compilation (default)"
	@echo "  make quick     - Quick compilation (no bibliography)"
	@echo "  make full      - Full compilation with bibliography"
	@echo "  make info      - Show PDF info (pages, size)"
	@echo "  make check     - Check for LaTeX/BibTeX errors"
	@echo "  make anonymize - Check for identifying information"
	@echo "  make strip-metadata - Remove PDF metadata"
	@echo "  make wordcount - Count words (approximate)"
	@echo "  make clean     - Remove auxiliary files"
	@echo "  make distclean - Remove all generated files"
	@echo "  make archive   - Create submission archive"
	@echo "  make help      - Show this help"
	@echo ""
	@echo "FAccT 2026 Requirements:"
	@echo "  - Maximum 14 pages (excluding references)"
	@echo "  - Anonymous submission (double-blind)"
	@echo "  - ACM format with manuscript, review, anonymous options"
	@echo ""
