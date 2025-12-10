# PLANO DE ANOTAÇÃO MANUAL REAL - Execução Imediata

## 🎯 OBJETIVO
Criar ground truth **100% real** sem mock, aceitável para paper TIER 1.

---

## 📊 OPÇÕES DE EXECUÇÃO

### **OPÇÃO A: Início Rápido (HOJE - 2-3 horas)**

Anotar manualmente **25 datasets estratificados** AGORA:

```bash
cd /home/guhaase/projetos/DeepBridge/papers/02_Fairness_Framework/experimentos/scripts
source ../../venv_fairness/bin/activate

# 1. Criar subset estratificado de 25 datasets
python -c "
import pandas as pd
import numpy as np
from pathlib import Path
import json

# Ler metadata
meta = pd.read_csv('../data/datasets_metadata.csv')

# Amostrar 25 datasets aleatórios (estratificados se possível)
np.random.seed(42)
sample = meta.sample(n=25, random_state=42)

# Salvar lista
subset = {
    'n_datasets': 25,
    'purpose': 'Initial real annotation for TIER 1 paper',
    'files': sample['file'].tolist(),
    'created': '2025-12-08'
}

Path('../data').mkdir(exist_ok=True)
with open('../data/annotation_subset_25.json', 'w') as f:
    json.dump(subset, f, indent=2)

print('✅ Subset de 25 datasets criado')
print('Arquivos:', sample['file'].tolist()[:5], '...')
"

# 2. VOCÊ anota os 25 datasets (1-1.5 horas)
# Leia cada dataset e identifique MANUALMENTE os atributos sensíveis
python 02_annotate_ground_truth.py --annotator 1 --n-datasets 25

# 3. RECRUTAR outra pessoa para anotar os mesmos 25 (1-1.5 horas)
#    Pode ser um colega, outro pesquisador, etc.
#    IMPORTANTE: Não mostrar suas anotações!
python 02_annotate_ground_truth.py --annotator 2 --n-datasets 25

# 4. Calcular Cohen's Kappa REAL
python 02_annotate_ground_truth.py --calculate-agreement

# 5. Usar como ground truth real
cp ../data/annotations_annotator_1.json ../data/ground_truth_real_25.json
```

**Resultado esperado**:
- ✅ 25 datasets com anotação **100% manual**
- ✅ Inter-rater agreement **real** (Kappa)
- ✅ Dados verificáveis e auditáveis
- ✅ Suficiente para validação inicial

**Para o paper**:
> "We manually annotated 25 stratified datasets by two independent raters (Cohen's κ = X.XX, 95% CI [X.XX, X.XX])..."

---

### **OPÇÃO B: Subset Robusto (Esta semana - 10 horas)**

Anotar **100 datasets** ao longo de 1 semana:

**DIA 1-2**: Você anota 50 datasets (5 horas)
```bash
python 02_annotate_ground_truth.py --annotator 1 --n-datasets 50 --start-from 0
```

**DIA 3-4**: Você anota mais 50 datasets (5 horas)
```bash
python 02_annotate_ground_truth.py --annotator 1 --n-datasets 50 --start-from 50
```

**DIA 5-7**: Recrutar colega para anotar os mesmos 100 (10 horas dele)
```bash
python 02_annotate_ground_truth.py --annotator 2 --n-datasets 100
```

**Resultado**: 100 datasets reais, estatisticamente robusto (N=100, power > 0.90)

---

### **OPÇÃO C: Completo (3 meses - 80 horas total)**

500 datasets × 2 anotadores = planejamento de longo prazo

Ver: `ANNOTATION_SCHEDULE.md` (criado pelo script 04)

---

## 🚀 RECOMENDAÇÃO: COMECE COM OPÇÃO A (HOJE)

**AGORA MESMO** (próximas 3 horas):

```bash
# 1. Preparar subset
cd /home/guhaase/projetos/DeepBridge/papers/02_Fairness_Framework/experimentos/scripts
source ../../venv_fairness/bin/activate

# 2. Limpar anotações anteriores (mock)
rm -f ../data/annotations_annotator_*.json
rm -f ../data/ground_truth_final.json

# 3. Anotar 25 datasets VOCÊ
python 02_annotate_ground_truth.py --annotator 1 --n-datasets 25

# Durante a anotação:
# - Leia CADA dataset
# - Identifique MANUALMENTE colunas sensíveis
# - Use as categorias EEOC/ECOA (1-9)
# - Seja consistente e cuidadoso

# 4. Pedir para colega anotar OS MESMOS 25
#    (sem ver suas anotações!)

# 5. Calcular agreement REAL
python 02_annotate_ground_truth.py --calculate-agreement

# 6. Se Kappa > 0.75: SUCESSO! ✅
# 7. Se Kappa < 0.75: Revisar discordâncias e anotar mais alguns
```

**DEPOIS (amanhã)**:
- Executar experimentos nos 25 datasets reais
- Escrever no paper: "validated on 25 manually annotated datasets"
- Expandir gradualmente para 50, 100, 500 conforme tempo disponível

---

## 📋 CHECKLIST DE QUALIDADE PARA ANOTAÇÃO REAL

### ✅ Antes de começar:
- [ ] Ambiente ativado
- [ ] Entendi as 9 categorias EEOC/ECOA
- [ ] Tenho 1-2 horas disponíveis sem interrupções
- [ ] Encontrei um colega para ser anotador 2

### ✅ Durante a anotação:
- [ ] Leio os VALORES das colunas, não apenas os nomes
- [ ] Considero contexto (ex: "feature_0" pode ser sensível se valores são "Male/Female")
- [ ] Em caso de dúvida, marco como sensível (conservador)
- [ ] Faço pausas a cada 10 datasets

### ✅ Após anotação:
- [ ] Kappa > 0.75 (substancial)
- [ ] Discordâncias foram discutidas
- [ ] Ground truth final consolidado
- [ ] Backup dos arquivos de anotação

---

## 🎯 CRITÉRIO DE ACEITAÇÃO PARA TIER 1

**Mínimo aceitável**:
- N ≥ 25 datasets manualmente anotados
- 2 anotadores independentes
- Kappa > 0.60 (moderado)
- Discordâncias documentadas

**Ideal**:
- N ≥ 100 datasets
- 2 anotadores experientes
- Kappa > 0.75 (substancial)
- Protocolo de anotação documentado

**Perfeito** (para journals top):
- N = 500 datasets
- Kappa > 0.80
- Terceiro anotador para resolver discordâncias
- Análise de casos difíceis

---

## 💰 CUSTO vs. BENEFÍCIO

| Opção | Datasets | Tempo | Custo | Qualidade Paper | Viabilidade |
|-------|----------|-------|-------|-----------------|-------------|
| A: 25 | 25 | 3h | $0 | Aceitável | ⭐⭐⭐⭐⭐ Agora |
| B: 100 | 100 | 20h | $400* | Bom | ⭐⭐⭐⭐ Esta semana |
| C: 500 | 500 | 80h | $1600* | Excelente | ⭐⭐ 3 meses |

*Custo se contratar anotadores ($20/hora)

---

## 🚦 AÇÃO IMEDIATA

**Cole e execute AGORA**:

```bash
cd /home/guhaase/projetos/DeepBridge/papers/02_Fairness_Framework/experimentos/scripts && \
source ../../venv_fairness/bin/activate && \
rm -f ../data/annotations_annotator_*.json ../data/ground_truth_final.json && \
echo "🎯 Pronto para começar anotação REAL!" && \
echo "Execute: python 02_annotate_ground_truth.py --annotator 1 --n-datasets 25"
```

Depois execute o comando que aparece e **anote manualmente os 25 datasets**.

---

**Quer começar AGORA ou prefere esperar para fazer com mais calma?**
