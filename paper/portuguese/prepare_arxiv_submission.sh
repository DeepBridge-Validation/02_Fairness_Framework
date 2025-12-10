#!/bin/bash
# Script para preparar submissão ao arXiv
# Uso: ./prepare_arxiv_submission.sh

set -e

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║          Preparação de Submissão para arXiv                       ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Diretório base
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Criar diretório temporário
SUBMISSION_DIR="arxiv_submission"
rm -rf "$SUBMISSION_DIR"
mkdir -p "$SUBMISSION_DIR"

echo "📁 Copiando arquivos necessários..."

# Copiar arquivos principais
cp main.tex "$SUBMISSION_DIR/"
cp acmart.cls "$SUBMISSION_DIR/"

# Copiar seções
cp -r sections "$SUBMISSION_DIR/"

# Copiar bibliografia
cp -r bibliography "$SUBMISSION_DIR/"

# Copiar figuras
mkdir -p "$SUBMISSION_DIR/figures"
cp figures/figure1_detection_performance.pdf "$SUBMISSION_DIR/figures/"
cp figures/figure2_performance_comparison.pdf "$SUBMISSION_DIR/figures/"
cp figures/architecture_simple.pdf "$SUBMISSION_DIR/figures/" 2>/dev/null || echo "  ⚠️  architecture_simple.pdf não encontrado (opcional)"

echo "✅ Arquivos copiados para $SUBMISSION_DIR/"
echo ""

# Listar arquivos
echo "📋 Conteúdo do pacote de submissão:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
find "$SUBMISSION_DIR" -type f | sort
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Contar arquivos
n_tex=$(find "$SUBMISSION_DIR" -name "*.tex" | wc -l)
n_bib=$(find "$SUBMISSION_DIR" -name "*.bib" | wc -l)
n_pdf=$(find "$SUBMISSION_DIR" -name "*.pdf" | wc -l)
n_cls=$(find "$SUBMISSION_DIR" -name "*.cls" | wc -l)

echo "📊 Estatísticas:"
echo "  • Arquivos .tex: $n_tex"
echo "  • Arquivos .bib: $n_bib"
echo "  • Figuras .pdf: $n_pdf"
echo "  • Classes .cls: $n_cls"
echo ""

# Testar compilação dentro do diretório de submissão
echo "🔨 Testando compilação no diretório de submissão..."
cd "$SUBMISSION_DIR"

pdflatex -interaction=nonstopmode main.tex > compilation_test.log 2>&1
bibtex main >> compilation_test.log 2>&1
pdflatex -interaction=nonstopmode main.tex >> compilation_test.log 2>&1
pdflatex -interaction=nonstopmode main.tex >> compilation_test.log 2>&1

if [ -f main.pdf ]; then
    pages=$(pdfinfo main.pdf | grep "Pages:" | awk '{print $2}')
    size=$(ls -lh main.pdf | awk '{print $5}')
    echo "  ✅ Compilação bem-sucedida!"
    echo "  📄 PDF gerado: $pages páginas, $size"
else
    echo "  ❌ Erro na compilação. Verifique compilation_test.log"
    cd "$SCRIPT_DIR"
    exit 1
fi

cd "$SCRIPT_DIR"
echo ""

# Criar arquivo .tar.gz
echo "📦 Criando pacote arXiv (.tar.gz)..."
TARBALL="deepbridge_fairness_arxiv_$(date +%Y%m%d).tar.gz"

cd "$SUBMISSION_DIR"
tar -czf "../$TARBALL" \
    main.tex \
    acmart.cls \
    sections/*.tex \
    bibliography/references.bib \
    figures/*.pdf

cd "$SCRIPT_DIR"

if [ -f "$TARBALL" ]; then
    size=$(ls -lh "$TARBALL" | awk '{print $5}')
    echo "  ✅ Pacote criado: $TARBALL ($size)"
else
    echo "  ❌ Erro ao criar pacote"
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    PREPARAÇÃO CONCLUÍDA                            ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📤 Próximos passos para submissão ao arXiv:"
echo ""
echo "1. Acesse: https://arxiv.org/submit"
echo ""
echo "2. Faça upload do arquivo:"
echo "   $TARBALL"
echo ""
echo "3. Preencha os metadados:"
echo "   • Título: DeepBridge Fairness: Da Pesquisa à Regulação"
echo "   • Autores: Gustavo Coelho Haase, Paulo Henrique Dourado da Silva"
echo "   • Categoria: cs.LG (Machine Learning)"
echo "   • Categorias secundárias: cs.AI, cs.CY (Computers and Society)"
echo "   • Abstract: Copie do main.tex"
echo ""
echo "4. Licença recomendada: CC BY 4.0 (permite uso comercial e modificações)"
echo ""
echo "5. Comentários (opcional):"
echo "   \"17 pages, 2 figures, 3 tables. Experimental validation with"
echo "   statistical rigor (p < 0.001, Cohen's d = 2.85)\""
echo ""
echo "✅ Arquivos prontos para submissão!"
echo ""

# Limpar arquivos temporários de compilação
cd "$SUBMISSION_DIR"
rm -f *.aux *.log *.out *.toc *.bbl *.blg
cd "$SCRIPT_DIR"

echo "📁 Arquivos disponíveis:"
echo "  • Pacote arXiv: $TARBALL"
echo "  • Diretório de revisão: $SUBMISSION_DIR/"
echo ""
