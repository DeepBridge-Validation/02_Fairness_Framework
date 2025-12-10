#!/bin/bash
# Teste rápido de todos os componentes
# Executa versões simplificadas dos experimentos para validar setup

set -e

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║           DeepBridge Fairness - Teste Rápido                      ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Ativar ambiente
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXPERIMENTS_DIR="$(dirname "$SCRIPT_DIR")"
BASE_DIR="$(dirname "$EXPERIMENTS_DIR")"
VENV_DIR="$BASE_DIR/venv_fairness"

cd "$SCRIPT_DIR"

if [ ! -d "$VENV_DIR" ]; then
    echo -e "${RED}✗ Ambiente virtual não encontrado${NC}"
    echo "Execute primeiro: ./00_setup_environment.sh"
    exit 1
fi

source "$VENV_DIR/bin/activate"
echo -e "${GREEN}✓ Ambiente ativado${NC}"
echo ""

# Teste 1: Coleta de dados (10 datasets)
echo "═══════════════════════════════════════════════════════════"
echo "  TESTE 1: Coleta de Datasets (10 sintéticos)"
echo "═══════════════════════════════════════════════════════════"
echo ""

python 01_collect_datasets.py --target 10 --output ../data/datasets_test

if [ $? -eq 0 ]; then
    n_files=$(ls -1 ../data/datasets_test/*.csv 2>/dev/null | wc -l)
    echo -e "${GREEN}✓ Teste 1 OK: $n_files datasets criados${NC}"
else
    echo -e "${RED}✗ Teste 1 FALHOU${NC}"
    exit 1
fi
echo ""

# Teste 2: Experimento 1 (modo quick)
echo "═══════════════════════════════════════════════════════════"
echo "  TESTE 2: Auto-Detecção (modo quick)"
echo "═══════════════════════════════════════════════════════════"
echo ""

python exp1_auto_detection.py --quick

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Teste 2 OK: Exp1 executado${NC}"
else
    echo -e "${RED}✗ Teste 2 FALHOU${NC}"
    exit 1
fi
echo ""

# Teste 3: Experimento 5 (modo quick)
echo "═══════════════════════════════════════════════════════════"
echo "  TESTE 3: Performance Benchmark (modo quick)"
echo "═══════════════════════════════════════════════════════════"
echo ""

python exp5_performance.py --mode quick --n-repeats 3

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Teste 3 OK: Exp5 executado${NC}"
else
    echo -e "${RED}✗ Teste 3 FALHOU${NC}"
    exit 1
fi
echo ""

# Teste 4: Template de análise estatística
echo "═══════════════════════════════════════════════════════════"
echo "  TESTE 4: Template de Análise Estatística"
echo "═══════════════════════════════════════════════════════════"
echo ""

python ../templates/statistical_analysis_template.py > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Teste 4 OK: Templates funcionando${NC}"
else
    echo -e "${RED}✗ Teste 4 FALHOU${NC}"
    exit 1
fi
echo ""

# Resumo
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║                  ${GREEN}✓ TODOS OS TESTES PASSARAM!${NC}                        ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Próximos passos:"
echo "  1. Coletar 500 datasets: python 01_collect_datasets.py --target 500"
echo "  2. Anotar ground truth (2 anotadores)"
echo "  3. Executar todos experimentos: ./run_all_experiments.sh"
echo ""
echo "Ou consulte: ../../QUICK_START.md"
echo ""
