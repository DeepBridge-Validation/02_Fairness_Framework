#!/bin/bash
# Master script para executar todos os experimentos
# DeepBridge Fairness Framework - Paper TIER 1

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║      DeepBridge Fairness - Execução Completa de Experimentos      ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Diretórios
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXPERIMENTS_DIR="$(dirname "$SCRIPT_DIR")"
BASE_DIR="$(dirname "$EXPERIMENTS_DIR")"
RESULTS_DIR="$EXPERIMENTS_DIR/results"
DATA_DIR="$EXPERIMENTS_DIR/data"
VENV_DIR="$BASE_DIR/venv_fairness"

cd "$SCRIPT_DIR" || exit 1

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções auxiliares
print_step() {
    echo ""
    echo "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo "${BLUE}  $1${NC}"
    echo "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
}

print_success() {
    echo "${GREEN}✓ $1${NC}"
}

print_error() {
    echo "${RED}✗ $1${NC}"
}

print_warning() {
    echo "${YELLOW}⚠ $1${NC}"
}

# Verificar ambiente
print_step "ETAPA 0: Verificação de Ambiente"

if [ -z "$VIRTUAL_ENV" ]; then
    print_warning "Ambiente virtual não ativado"
    echo "Tentando ativar venv_fairness..."

    if [ -d "$VENV_DIR" ]; then
        source "$VENV_DIR/bin/activate"
        print_success "Ambiente ativado: $VENV_DIR"
    else
        print_error "Ambiente não encontrado em: $VENV_DIR"
        print_error "Execute: cd $BASE_DIR && ./experimentos/scripts/00_setup_environment.sh"
        exit 1
    fi
else
    print_success "Ambiente virtual ativo: $VIRTUAL_ENV"
fi

# Testar imports
python -c "import pandas, numpy, scipy, sklearn" 2>/dev/null
if [ $? -eq 0 ]; then
    print_success "Dependências instaladas"
else
    print_error "Dependências faltando. Execute: ./00_setup_environment.sh"
    exit 1
fi

# Verificar dados
if [ ! -f "$DATA_DIR/ground_truth_final.json" ]; then
    print_warning "Ground truth não encontrado"
    print_warning "Você precisa executar primeiro:"
    echo "  1. python 01_collect_datasets.py --target 500"
    echo "  2. python 02_annotate_ground_truth.py --annotator 1"
    echo "  3. python 02_annotate_ground_truth.py --annotator 2"
    echo "  4. python 02_annotate_ground_truth.py --calculate-agreement"
    echo ""
    read -p "Continuar mesmo assim com dados mock? (s/n): " answer
    if [ "$answer" != "s" ]; then
        exit 1
    fi
    USE_MOCK=1
else
    print_success "Ground truth encontrado"
    USE_MOCK=0
fi

# Criar diretório de resultados
mkdir -p "$RESULTS_DIR"

# Timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$RESULTS_DIR/experiment_run_${TIMESTAMP}.log"

echo "Resultados serão salvos em: $RESULTS_DIR"
echo "Log completo em: $LOG_FILE"
echo ""

# Perguntar quais experimentos executar
echo "Selecione experimentos para executar:"
echo "  1. Exp1: Auto-Detecção (F1 Score)"
echo "  2. Exp2: Usabilidade (SUS/NASA-TLX) [REQUER INTERAÇÃO]"
echo "  3. Exp3: Validação EEOC/ECOA"
echo "  4. Exp4: Case Studies"
echo "  5. Exp5: Performance Benchmarks"
echo "  6. TODOS (exceto Exp2)"
echo ""
read -p "Opção (1-6): " option

run_exp1=0
run_exp2=0
run_exp3=0
run_exp4=0
run_exp5=0

case $option in
    1) run_exp1=1 ;;
    2) run_exp2=1 ;;
    3) run_exp3=1 ;;
    4) run_exp4=1 ;;
    5) run_exp5=1 ;;
    6) run_exp1=1; run_exp3=1; run_exp4=1; run_exp5=1 ;;
    *) echo "Opção inválida"; exit 1 ;;
esac

# ═══════════════════════════════════════════════════════════
# EXPERIMENTO 1: AUTO-DETECÇÃO
# ═══════════════════════════════════════════════════════════

if [ $run_exp1 -eq 1 ]; then
    print_step "EXPERIMENTO 1: Auto-Detecção de Atributos Sensíveis"

    start_time=$(date +%s)

    if [ $USE_MOCK -eq 1 ]; then
        print_warning "Executando em modo QUICK (dados mock)"
        python exp1_auto_detection.py --quick 2>&1 | tee -a "$LOG_FILE"
    else
        python exp1_auto_detection.py \
            --ground-truth "$DATA_DIR/ground_truth_final.json" \
            --datasets-dir "$DATA_DIR/datasets" \
            --output "$RESULTS_DIR/exp1_auto_detection" \
            2>&1 | tee -a "$LOG_FILE"
    fi

    if [ $? -eq 0 ]; then
        end_time=$(date +%s)
        elapsed=$((end_time - start_time))
        print_success "Exp1 concluído em ${elapsed}s"

        # Verificar F1 score
        if [ -f "$RESULTS_DIR/exp1_auto_detection/summary.json" ]; then
            f1=$(python -c "import json; print(json.load(open('$RESULTS_DIR/exp1_auto_detection/summary.json'))['f1_mean'])" 2>/dev/null || echo "N/A")
            echo "  F1 Score: $f1"
        fi
    else
        print_error "Exp1 falhou"
    fi
fi

# ═══════════════════════════════════════════════════════════
# EXPERIMENTO 2: USABILIDADE
# ═══════════════════════════════════════════════════════════

if [ $run_exp2 -eq 1 ]; then
    print_step "EXPERIMENTO 2: Estudo de Usabilidade"

    print_warning "Este experimento REQUER INTERAÇÃO com participantes (N=20)"
    print_warning "Tempo estimado: 20 horas (20 × 1h por sessão)"
    echo ""
    read -p "Quantos participantes executar agora? (0-20): " n_participants

    if [ "$n_participants" -gt 0 ]; then
        for i in $(seq 1 $n_participants); do
            pid=$(printf "P%02d" $i)
            print_step "Sessão com participante $pid"

            python exp2_usability_study.py \
                --participant-id "$pid" \
                --mode interactive \
                2>&1 | tee -a "$LOG_FILE"

            if [ $? -eq 0 ]; then
                print_success "Sessão $pid concluída"
            else
                print_error "Sessão $pid falhou"
            fi
        done

        # Análise agregada
        if [ "$n_participants" -ge 3 ]; then
            print_step "Análise Agregada de Usabilidade"
            python exp2_usability_study.py \
                --analyze \
                --input "$RESULTS_DIR/exp2_usability" \
                2>&1 | tee -a "$LOG_FILE"
        fi
    else
        print_warning "Pulando Exp2"
    fi
fi

# ═══════════════════════════════════════════════════════════
# EXPERIMENTO 3: VALIDAÇÃO EEOC/ECOA
# ═══════════════════════════════════════════════════════════

if [ $run_exp3 -eq 1 ]; then
    print_step "EXPERIMENTO 3: Validação EEOC/ECOA"

    start_time=$(date +%s)

    python exp3_eeoc_validation.py \
        --datasets-dir "$DATA_DIR/datasets" \
        --output "$RESULTS_DIR/exp3_eeoc" \
        --n-datasets 100 \
        2>&1 | tee -a "$LOG_FILE"

    if [ $? -eq 0 ]; then
        end_time=$(date +%s)
        elapsed=$((end_time - start_time))
        print_success "Exp3 concluído em ${elapsed}s"
    else
        print_error "Exp3 falhou"
    fi
fi

# ═══════════════════════════════════════════════════════════
# EXPERIMENTO 4: CASE STUDIES
# ═══════════════════════════════════════════════════════════

if [ $run_exp4 -eq 1 ]; then
    print_step "EXPERIMENTO 4: Case Studies"

    start_time=$(date +%s)

    python exp4_case_studies.py \
        --datasets compas,german,adult,healthcare \
        --output "$RESULTS_DIR/exp4_case_studies" \
        2>&1 | tee -a "$LOG_FILE"

    if [ $? -eq 0 ]; then
        end_time=$(date +%s)
        elapsed=$((end_time - start_time))
        print_success "Exp4 concluído em ${elapsed}s"
    else
        print_error "Exp4 falhou"
    fi
fi

# ═══════════════════════════════════════════════════════════
# EXPERIMENTO 5: PERFORMANCE
# ═══════════════════════════════════════════════════════════

if [ $run_exp5 -eq 1 ]; then
    print_step "EXPERIMENTO 5: Performance Benchmarks"

    start_time=$(date +%s)

    read -p "Modo (quick/full)? [quick]: " mode
    mode=${mode:-quick}

    python exp5_performance.py \
        --mode "$mode" \
        --n-repeats 10 \
        --output "$RESULTS_DIR/exp5_performance" \
        2>&1 | tee -a "$LOG_FILE"

    if [ $? -eq 0 ]; then
        end_time=$(date +%s)
        elapsed=$((end_time - start_time))
        print_success "Exp5 concluído em ${elapsed}s"
    else
        print_error "Exp5 falhou"
    fi
fi

# ═══════════════════════════════════════════════════════════
# RELATÓRIO FINAL
# ═══════════════════════════════════════════════════════════

print_step "RELATÓRIO FINAL"

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    RESUMO DA EXECUÇÃO                              ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar resultados
total_claims=0
claims_validated=0

if [ $run_exp1 -eq 1 ] && [ -f "$RESULTS_DIR/exp1_auto_detection/summary.json" ]; then
    f1=$(python -c "import json; d=json.load(open('$RESULTS_DIR/exp1_auto_detection/summary.json')); print(f\"{d.get('f1_mean', 0):.3f}\")" 2>/dev/null || echo "N/A")
    total_claims=$((total_claims + 1))
    if (( $(echo "$f1 >= 0.85" | bc -l 2>/dev/null || echo 0) )); then
        print_success "Exp1: F1 = $f1 ✓ (meta: ≥0.85)"
        claims_validated=$((claims_validated + 1))
    else
        print_error "Exp1: F1 = $f1 ✗ (meta: ≥0.85)"
    fi
fi

if [ $run_exp2 -eq 1 ] && [ -f "$RESULTS_DIR/exp2_usability/aggregate_analysis.json" ]; then
    sus=$(python -c "import json; d=json.load(open('$RESULTS_DIR/exp2_usability/aggregate_analysis.json')); print(f\"{d['sus']['mean']:.1f}\")" 2>/dev/null || echo "N/A")
    total_claims=$((total_claims + 1))
    if (( $(echo "$sus >= 75" | bc -l 2>/dev/null || echo 0) )); then
        print_success "Exp2: SUS = $sus ✓ (meta: ≥75)"
        claims_validated=$((claims_validated + 1))
    else
        print_error "Exp2: SUS = $sus ✗ (meta: ≥75)"
    fi
fi

if [ $run_exp3 -eq 1 ] && [ -f "$RESULTS_DIR/exp3_eeoc/eeoc_validation_results.json" ]; then
    accuracy=$(python -c "import json; d=json.load(open('$RESULTS_DIR/exp3_eeoc/eeoc_validation_results.json')); print(f\"{d.get('accuracy', 0):.1%}\")" 2>/dev/null || echo "N/A")
    print_success "Exp3: EEOC Accuracy = $accuracy"
fi

if [ $run_exp5 -eq 1 ] && [ -f "$RESULTS_DIR/exp5_performance/performance_results.json" ]; then
    speedup=$(python -c "import json, numpy as np; d=json.load(open('$RESULTS_DIR/exp5_performance/performance_results.json')); speedups=[r['speedups']['vs_manual'] for r in d]; print(f\"{np.mean(speedups):.2f}x\")" 2>/dev/null || echo "N/A")
    total_claims=$((total_claims + 1))
    if [[ "$speedup" != "N/A" ]]; then
        speedup_val=$(echo "$speedup" | sed 's/x//')
        if (( $(echo "$speedup_val >= 2.5" | bc -l 2>/dev/null || echo 0) )); then
            print_success "Exp5: Speedup = $speedup ✓ (meta: ≥2.5x)"
            claims_validated=$((claims_validated + 1))
        else
            print_error "Exp5: Speedup = $speedup ✗ (meta: ≥2.5x)"
        fi
    fi
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
if [ $total_claims -gt 0 ]; then
    success_rate=$((100 * claims_validated / total_claims))
    echo "║  Claims validadas: $claims_validated/$total_claims ($success_rate%)                                   ║"

    if [ $success_rate -ge 80 ]; then
        echo "║  Status: ${GREEN}PRONTO PARA TIER 1${NC}                                          ║"
    elif [ $success_rate -ge 60 ]; then
        echo "║  Status: ${YELLOW}NECESSITA AJUSTES${NC}                                          ║"
    else
        echo "║  Status: ${RED}NÃO PRONTO${NC}                                                 ║"
    fi
else
    echo "║  Nenhuma claim validada (dados mock?)                             ║"
fi
echo "╚════════════════════════════════════════════════════════════════════╝"

echo ""
echo "Resultados em: $RESULTS_DIR"
echo "Log completo: $LOG_FILE"
echo ""

print_success "Execução concluída!"
