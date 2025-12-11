#!/bin/bash
# Script de compilação LaTeX com BibTeX
# Uso: ./compile.sh

set -e

echo "🔨 Compilando documento LaTeX com referências bibliográficas..."

# Primeira compilação - gera arquivos auxiliares
echo "  [1/4] Primeira compilação (pdflatex)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1

# Processa bibliografia
echo "  [2/4] Processando referências (bibtex)..."
bibtex main > /dev/null 2>&1

# Segunda compilação - resolve citações
echo "  [3/4] Segunda compilação (resolver citações)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1

# Terceira compilação - resolve referências cruzadas
echo "  [4/4] Terceira compilação (referências cruzadas)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1

# Verifica se o PDF foi gerado
if [ -f main.pdf ]; then
    PAGES=$(pdfinfo main.pdf | grep Pages | awk '{print $2}')
    REFS=$(grep -c "bibitem" main.bbl 2>/dev/null || echo "0")
    SIZE=$(du -h main.pdf | cut -f1)

    echo ""
    echo "✅ Compilação concluída com sucesso!"
    echo "   📄 Páginas: $PAGES"
    echo "   📚 Referências: $REFS"
    echo "   💾 Tamanho: $SIZE"
    echo "   📦 Arquivo: main.pdf"
else
    echo ""
    echo "❌ Erro: PDF não foi gerado"
    exit 1
fi
