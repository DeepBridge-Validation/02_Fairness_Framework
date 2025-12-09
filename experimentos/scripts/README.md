# Scripts de Experimentos - DeepBridge Fairness

Documentação completa de todos os scripts experimentais para validação do paper.

---

## 📁 Estrutura

```
scripts/
├── 00_setup_environment.sh         # Setup automatizado
├── 01_collect_datasets.py          # Coleta de 500 datasets
├── 02_annotate_ground_truth.py     # Anotação manual (2 anotadores)
├── exp1_auto_detection.py          # Exp 1: Auto-detecção
├── exp2_usability_study.py         # Exp 2: Usabilidade (SUS/TLX)
├── exp3_eeoc_validation.py         # Exp 3: Validação EEOC/ECOA
├── exp4_case_studies.py            # Exp 4: Case studies
├── exp5_performance.py             # Exp 5: Performance benchmarks
├── run_all_experiments.sh          # Master script (executa todos)
└── utils.py                        # Funções utilitárias
```

---

## 🚀 QUICK START

### 1. Setup Inicial (1 vez)

```bash
# Configurar ambiente
./00_setup_environment.sh

# Ativar
source ../venv_fairness/bin/activate

# Verificar
python -c "import pandas, numpy, scipy; print('✅ OK')"
```

### 2. Preparação de Dados (Semana 1)

```bash
# Coletar 500 datasets
python 01_collect_datasets.py --target 500

# Anotar ground truth (2 anotadores independentes)
python 02_annotate_ground_truth.py --annotator 1 --n-datasets 500
python 02_annotate_ground_truth.py --annotator 2 --n-datasets 500

# Calcular inter-rater agreement
python 02_annotate_ground_truth.py --calculate-agreement
```

### 3. Executar Experimentos (Semanas 2-12)

```bash
# Opção 1: Executar todos de uma vez
./run_all_experiments.sh

# Opção 2: Executar individualmente
python exp1_auto_detection.py --ground-truth ../data/ground_truth_final.json
python exp2_usability_study.py --participant-id P01
python exp3_eeoc_validation.py --n-datasets 100
python exp4_case_studies.py --datasets compas,german,adult,healthcare
python exp5_performance.py --mode full --n-repeats 10
```

---

## 📋 DETALHAMENTO DOS SCRIPTS

### **00_setup_environment.sh**

**Propósito**: Configurar ambiente Python completo

**Execução**:
```bash
./00_setup_environment.sh
```

**O que faz**:
- Cria ambiente virtual `venv_fairness`
- Instala todas dependências (pandas, numpy, scipy, sklearn, aif360, fairlearn, etc.)
- Configura Jupyter kernel
- Salva `requirements.txt`
- Testa imports

**Output esperado**:
- ✅ Ambiente funcional em ~5 minutos
- Arquivo `requirements.txt` gerado

---

### **01_collect_datasets.py**

**Propósito**: Coletar 500 datasets para validação

**Execução**:
```bash
# Full (500 datasets)
python 01_collect_datasets.py --target 500 --output ../data/datasets

# Quick test (50 datasets)
python 01_collect_datasets.py --target 50
```

**Fontes**:
- UCI ML Repository (50 datasets)
- OpenML (50 datasets)
- Datasets sintéticos (400 datasets)

**Output**:
- `../data/datasets/` - 500 arquivos CSV
- `../data/datasets_metadata.csv` - Catálogo completo

**Tempo**: ~30 minutos

---

### **02_annotate_ground_truth.py**

**Propósito**: Anotação manual de atributos sensíveis

**Execução**:
```bash
# Anotador 1
python 02_annotate_ground_truth.py --annotator 1 --n-datasets 500

# Anotador 2 (independente)
python 02_annotate_ground_truth.py --annotator 2 --n-datasets 500

# Calcular Cohen's Kappa
python 02_annotate_ground_truth.py --calculate-agreement
```

**Interface**:
- CLI interativa
- Mostra colunas do dataset
- Categorias EEOC/ECOA (1-9)
- Salva progresso automaticamente

**Output**:
- `../data/annotations_annotator_1.json`
- `../data/annotations_annotator_2.json`
- `../data/inter_rater_agreement_report.json`

**Meta**: Kappa > 0.75 (agreement substancial)

**Tempo**: ~60 horas (2 anotadores × 30h)

---

### **exp1_auto_detection.py**

**Experimento 1: Auto-Detecção de Atributos Sensíveis**

**Execução**:
```bash
# Full experiment
python exp1_auto_detection.py \
    --ground-truth ../data/ground_truth_final.json \
    --datasets-dir ../data/datasets \
    --output ../results/exp1_auto_detection

# Ajustar threshold
python exp1_auto_detection.py --threshold 0.80 --ground-truth ...
```

**Algoritmo**:
1. Fuzzy matching de nomes de colunas
2. Comparação com keywords EEOC/ECOA
3. Threshold de similaridade (default: 0.75)

**Métricas**:
- Precision, Recall, F1 Score (por dataset)
- Micro e Macro averages
- Confusion matrix
- Análise de erros (FP/FN)

**Meta**:
- F1 ≥ 0.85 (paper claim: 0.90)

**Output**:
- `exp1_results.json` - Resultados completos
- `exp1_report.txt` - Relatório textual
- `metrics_distribution.png` - Histogramas
- `precision_recall_scatter.png` - Scatter plot

**Tempo**: ~2 horas (500 datasets)

---

### **exp2_usability_study.py**

**Experimento 2: Estudo de Usabilidade**

**Execução**:
```bash
# Sessão individual (N=20)
python exp2_usability_study.py --participant-id P01 --mode interactive
python exp2_usability_study.py --participant-id P02 --mode interactive
# ... (até P20)

# Análise agregada
python exp2_usability_study.py --analyze --input ../results/exp2_usability
```

**Protocolo (60 min/participante)**:
1. **Briefing** (5 min) - Explicar DeepBridge
2. **5 Tarefas** (30 min):
   - Tarefa 1: Carregar dataset e auto-detectar
   - Tarefa 2: Análise de fairness (3 métricas)
   - Tarefa 3: Verificação EEOC/ECOA
   - Tarefa 4: Ajustar threshold
   - Tarefa 5: Exportar relatório
3. **Questionários** (10 min):
   - SUS (10 questões, escala 1-5)
   - NASA-TLX (6 dimensões, escala 0-100)
4. **Entrevista** (15 min) - Semi-estruturada

**Métricas**:
- SUS Score (0-100): Meta ≥ 75 (claim: 85.2)
- NASA-TLX (0-100): Meta < 40
- Taxa de sucesso: Meta ≥ 95%
- Tempo por tarefa

**Output**:
- `P01/session_complete.json` - Dados completos
- `aggregate_analysis.json` - Análise estatística
- `usability_scores.png` - Distribuições SUS/TLX

**Tempo**: ~20 horas (20 participantes × 1h)

---

### **exp3_eeoc_validation.py**

**Experimento 3: Validação EEOC/ECOA**

**Execução**:
```bash
python exp3_eeoc_validation.py \
    --datasets-dir ../data/datasets \
    --output ../results/exp3_eeoc \
    --n-datasets 100
```

**Verificações**:
- 4/5 Rule (Disparate Impact)
- Statistical Parity (diferença < 0.2)
- Equal Opportunity (diferença < 0.1)
- Conformidade EEOC/ECOA

**Meta**:
- 100% precisão (sem margem de erro)

**Output**:
- `eeoc_validation_results.json`
- `eeoc_compliance_report.txt`
- `eeoc_violations.csv`

**Tempo**: ~1 hora (100 datasets)

---

### **exp4_case_studies.py**

**Experimento 4: Case Studies Detalhados**

**Execução**:
```bash
python exp4_case_studies.py \
    --datasets compas,german,adult,healthcare \
    --output ../results/exp4_case_studies
```

**4 Case Studies**:
1. **COMPAS** (Criminal Justice) - Recidivism prediction
2. **German Credit** (Finance) - Credit risk
3. **Adult Income** (Employment) - Income prediction
4. **Healthcare** (Medical) - Readmission prediction

**Análise por case**:
- Exploração de dados
- Detecção de bias
- Verificação EEOC
- Recomendações de mitigação
- Comparação manual vs. DeepBridge (tempo)

**Output**:
- `compas/case_study_report.md`
- `compas/fairness_metrics.json`
- `compas/bias_analysis.png`
- (idem para german, adult, healthcare)

**Tempo**: ~8 horas (2h por case)

---

### **exp5_performance.py**

**Experimento 5: Performance Benchmarks**

**Execução**:
```bash
# Quick test
python exp5_performance.py --mode quick --n-repeats 3

# Full benchmark
python exp5_performance.py --mode full --n-repeats 10
```

**Comparações**:
1. DeepBridge (automático)
2. Análise manual (estimado do exp2)
3. AIF360
4. Fairlearn

**Tamanhos de dataset**:
- 1,000 linhas
- 10,000 linhas
- 100,000 linhas

**Métricas**:
- Tempo de execução médio
- Speedup (×)
- Statistical tests (paired t-test, Cohen's d)

**Meta**:
- Speedup ≥ 2.5x vs. manual (claim: 2.9x)

**Output**:
- `performance_results.json`
- `performance_results.csv`
- `performance_comparison.png`
- `performance_comparison_bar.png`

**Tempo**: ~2 horas (full mode)

---

## 🔬 EXECUÇÃO COMPLETA (Master Script)

### **run_all_experiments.sh**

```bash
./run_all_experiments.sh
```

**O que faz**:
1. Verifica ambiente
2. Executa exp1-exp5 sequencialmente
3. Gera relatório consolidado
4. Valida todas as claims do paper

**Tempo total**: ~4 horas (assumindo dados já coletados)

---

## 📊 VALIDAÇÃO DE CLAIMS

| Claim | Experimento | Meta | Script |
|-------|-------------|------|--------|
| F1 ≥ 0.90 | Auto-detecção | F1 ≥ 0.85 | exp1 |
| SUS = 85.2 | Usabilidade | SUS ≥ 75 | exp2 |
| Success rate ≥ 95% | Usabilidade | 95% | exp2 |
| EEOC 100% accuracy | EEOC validation | 100% | exp3 |
| Speedup 2.9x | Performance | ≥ 2.5x | exp5 |

---

## 📂 OUTPUT ESPERADO

```
results/
├── exp1_auto_detection/
│   ├── exp1_results.json
│   ├── exp1_report.txt
│   └── *.png
├── exp2_usability/
│   ├── P01/ ... P20/
│   ├── aggregate_analysis.json
│   └── usability_scores.png
├── exp3_eeoc/
│   ├── eeoc_validation_results.json
│   └── eeoc_compliance_report.txt
├── exp4_case_studies/
│   ├── compas/
│   ├── german/
│   ├── adult/
│   └── healthcare/
└── exp5_performance/
    ├── performance_results.json
    ├── performance_results.csv
    └── *.png
```

---

## ⚙️ TROUBLESHOOTING

### Erro: "DeepBridge não instalado"
```bash
# Opção 1: Usar modo mock (testes)
export DEEPBRIDGE_MOCK=1
python exp1_auto_detection.py --quick

# Opção 2: Instalar DeepBridge
pip install deepbridge
```

### Erro: "Ground truth não encontrado"
```bash
# Criar ground truth primeiro
python 02_annotate_ground_truth.py --annotator 1 --n-datasets 10

# Consolidar anotações
python -c "
import json
with open('../data/annotations_annotator_1.json') as f:
    data = json.load(f)
with open('../data/ground_truth_final.json', 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Erro: "Memória insuficiente"
```bash
# Reduzir tamanho de datasets
python exp1_auto_detection.py --n-datasets 100  # em vez de 500

# Ou processar em lotes
python exp1_auto_detection.py --batch-size 50
```

---

## 📞 SUPORTE

- **Issues**: https://github.com/DeepBridge-Validation/DeepBridge/issues
- **Docs**: `/experimentos/docs/`
- **Roadmap**: `ROADMAP_TIER1.md`

---

**Última atualização**: 2025-12-08
**Versão**: 1.0
