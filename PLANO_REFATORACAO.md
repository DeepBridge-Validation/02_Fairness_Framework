# 📋 Plano de Refatoração para Publicação Acadêmica

**Repositório**: Fairness Framework for Machine Learning
**Data**: 2025-12-10
**Objetivo**: Preparar repositório para publicação junto com paper acadêmico

---

## 🎯 Objetivos Principais

1. **Reprodutibilidade Total**: Qualquer pesquisador deve conseguir reproduzir todos os resultados
2. **Clareza e Organização**: Estrutura intuitiva e bem documentada
3. **Padrões Acadêmicos**: Seguir best practices de repositórios científicos
4. **Facilidade de Uso**: Onboarding rápido (<30 min para começar)
5. **Profissionalismo**: README, LICENSE, CITATION, badges, etc.

---

## 📊 Situação Atual vs. Desejada

### Situação Atual ✅
- Paper completo (3 versões: ENG, ENG_FACCT, POR)
- Framework experimental funcional
- Documentação extensa (8 arquivos markdown)
- 13 scripts Python organizados
- 500+ datasets sintéticos
- Scripts de setup e execução

### Pontos a Melhorar ⚠️
- Sem README principal no root
- Estrutura pode ser mais intuitiva
- Falta LICENSE, CITATION.cff, CONTRIBUTING
- Sem badges (status, DOI, paper link)
- Dados não versionados (5GB)
- Sem Dockerfile/container
- Falta guia de troubleshooting
- Sem exemplos mínimos de uso

---

## 🏗️ Nova Estrutura Proposta

```
02_Fairness_Framework/
│
├── README.md                          # ⭐ NOVO - Entrada principal
├── LICENSE                            # ⭐ NOVO - MIT ou Apache 2.0
├── CITATION.cff                       # ⭐ NOVO - Citação estruturada
├── CONTRIBUTING.md                    # ⭐ NOVO - Como contribuir
├── .gitignore                         # ✏️ MELHORAR - Adicionar mais padrões
├── .zenodo.json                       # ⭐ NOVO - Metadados Zenodo
├── environment.yml                    # ⭐ NOVO - Ambiente conda
├── requirements.txt                   # ✅ EXISTE - Mover para root
│
├── paper/                             # 📝 RENOMEAR DE ENG/ENG_FACCT/POR
│   ├── README.md                      # ⭐ NOVO - Guia de compilação
│   ├── main/                          # Principal (inglês)
│   │   ├── main.tex
│   │   ├── main.pdf
│   │   └── sections/
│   ├── facct2026/                     # Versão FAccT
│   │   ├── main.tex
│   │   └── main.pdf
│   └── portuguese/                    # Versão português
│       ├── main.tex
│       └── main.pdf
│
├── src/                               # 🔧 NOVO - Código principal do framework
│   ├── __init__.py
│   ├── fairness_detector.py           # Core do framework
│   ├── metrics.py                     # Métricas de fairness
│   ├── visualization.py               # Plots e gráficos
│   └── utils.py                       # Utilitários
│
├── experiments/                       # 🔬 RENOMEAR DE experimentos/
│   ├── README.md                      # ✏️ MELHORAR - Simplificar START_HERE
│   ├── QUICKSTART.md                  # ⭐ NOVO - 5 min para rodar
│   ├── config/                        # ⭐ NOVO - Configs centralizadas
│   │   ├── exp1_detection.yaml
│   │   ├── exp2_usability.yaml
│   │   └── exp3_compliance.yaml
│   ├── scripts/                       # ✅ MANTER - Scripts de execução
│   │   ├── setup.sh
│   │   ├── run_all.sh
│   │   ├── exp1_*.py
│   │   ├── exp2_*.py
│   │   └── exp3_*.py
│   ├── notebooks/                     # ⭐ NOVO - Jupyter notebooks
│   │   ├── 01_quick_demo.ipynb       # Demo 5 min
│   │   ├── 02_experiment_1.ipynb     # Exp 1 detalhado
│   │   └── 03_visualization.ipynb    # Visualizações
│   └── results/                       # ⭐ NOVO - Resultados dos experimentos
│       ├── .gitkeep
│       └── README.md                  # Como interpretar
│
├── data/                              # 📦 REORGANIZAR
│   ├── README.md                      # ⭐ NOVO - Estrutura dos dados
│   ├── raw/                           # ⭐ NOVO - Dados originais
│   │   └── .gitkeep
│   ├── processed/                     # ⭐ NOVO - Dados processados
│   │   └── .gitkeep
│   ├── synthetic/                     # MOVER DE data/synthetic_datasets/
│   │   ├── README.md                  # Como gerar
│   │   └── batch_*/                   # 500+ datasets
│   ├── case_studies/                  # MOVER DE data/datasets_reais/
│   │   ├── compas/
│   │   ├── adult/
│   │   ├── bank/
│   │   └── german_credit/
│   └── ground_truth/                  # MOVER DE data/ground_truth/
│       └── anotacoes_*.csv
│
├── docs/                              # 📚 NOVA - Documentação organizada
│   ├── README.md                      # Índice da documentação
│   ├── installation.md                # Guia instalação detalhado
│   ├── quickstart.md                  # Tutorial 15 min
│   ├── experiments/                   # MOVER docs dos experimentos
│   │   ├── overview.md                # RESUMO_EXECUTIVO atual
│   │   ├── experiment_1.md            # Detalhes Exp 1
│   │   ├── experiment_2.md            # Detalhes Exp 2
│   │   ├── experiment_3.md            # Detalhes Exp 3
│   │   └── timeline.md                # PLANO_EXPERIMENTOS
│   ├── api/                           # ⭐ NOVO - API reference
│   │   └── index.md
│   ├── troubleshooting.md             # ⭐ NOVO - Problemas comuns
│   └── faq.md                         # ⭐ NOVO - Perguntas frequentes
│
├── tests/                             # ⭐ NOVO - Testes unitários
│   ├── __init__.py
│   ├── test_fairness_detector.py
│   ├── test_metrics.py
│   └── test_utils.py
│
├── docker/                            # ⭐ NOVO - Containerização
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
│
└── scripts/                           # ⭐ NOVO - Scripts auxiliares
    ├── download_data.sh               # Download datasets
    ├── generate_synthetic_data.py     # Gerar dados sintéticos
    └── verify_installation.py         # Verificar instalação
```

---

## 📝 Arquivos Novos a Criar

### 1. README.md Principal (Root) ⭐⭐⭐

```markdown
# Fairness Framework for Machine Learning

[![Paper](https://img.shields.io/badge/Paper-PDF-red)](link)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXX)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **Automated fairness detection and bias mitigation framework with regulatory compliance (EEOC/ECOA)**

## 🎯 Overview
Brief description (2-3 paragraphs)

## ✨ Key Features
- Automated bias detection (F1-Score: 0.90)
- EEOC/ECOA compliance (100% precision)
- 2.9x faster than baseline
- User-friendly interface (SUS: 85.2)

## 🚀 Quick Start (5 minutes)
```bash
# Install
pip install -r requirements.txt

# Run demo
python src/demo.py
```

## 📊 Results
Summary of key results with figures

## 📖 Citation
```bibtex
@article{...}
```

## 📄 License
MIT License

## 🤝 Contributing
See CONTRIBUTING.md
```

### 2. LICENSE ⭐⭐⭐

Escolher entre:
- **MIT**: Mais permissiva, recomendada para pesquisa
- **Apache 2.0**: Protege contra patentes
- **GPL-3.0**: Copyleft forte

**Recomendação**: MIT (padrão acadêmico)

### 3. CITATION.cff ⭐⭐⭐

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite our paper."
type: software
title: "Fairness Framework for Machine Learning"
version: 1.0.0
date-released: 2025-01-15
authors:
  - family-names: "Haase"
    given-names: "Gustavo"
    orcid: "https://orcid.org/XXXX-XXXX-XXXX-XXXX"
repository-code: "https://github.com/username/repo"
url: "https://github.com/username/repo"
license: MIT
keywords:
  - fairness
  - machine-learning
  - bias-detection
  - regulatory-compliance
preferred-citation:
  type: article
  title: "Automated Fairness Detection Framework..."
  authors:
    - family-names: "Haase"
      given-names: "Gustavo"
  journal: "Conference/Journal Name"
  year: 2025
```

### 4. CONTRIBUTING.md ⭐⭐

```markdown
# Contributing to Fairness Framework

## How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Code Style
- Follow PEP 8
- Add docstrings
- Write tests

## Reporting Issues
Use GitHub Issues with:
- Clear description
- Reproducible example
- Environment details
```

### 5. .zenodo.json ⭐⭐

```json
{
  "title": "Fairness Framework for Machine Learning",
  "description": "Automated fairness detection...",
  "license": "MIT",
  "upload_type": "software",
  "creators": [
    {
      "name": "Haase, Gustavo",
      "affiliation": "Institution",
      "orcid": "XXXX-XXXX-XXXX-XXXX"
    }
  ],
  "keywords": [
    "fairness",
    "machine-learning",
    "bias-detection"
  ],
  "related_identifiers": [
    {
      "relation": "isSupplementTo",
      "identifier": "DOI_OF_PAPER"
    }
  ]
}
```

### 6. environment.yml ⭐⭐

```yaml
name: fairness-framework
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.8
  - numpy>=1.19.0
  - pandas>=1.1.0
  - scikit-learn>=0.23.0
  - matplotlib>=3.3.0
  - seaborn>=0.11.0
  - jupyter>=1.0.0
  - pip
  - pip:
    - fairlearn>=0.7.0
    - aif360>=0.4.0
```

### 7. Dockerfile ⭐⭐

```dockerfile
FROM python:3.8-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run tests on build
RUN python -m pytest tests/ || true

CMD ["python", "src/demo.py"]
```

### 8. Jupyter Notebooks ⭐⭐⭐

**notebooks/01_quick_demo.ipynb**:
- Demo interativo de 5 minutos
- Exemplo simples de detecção de bias
- Visualizações básicas

**notebooks/02_experiment_1.ipynb**:
- Reprodução completa do Experimento 1
- Análise passo a passo
- Gráficos e tabelas

**notebooks/03_visualization.ipynb**:
- Todas as visualizações do paper
- Gráficos interativos
- Exportação para PDF/PNG

### 9. docs/quickstart.md ⭐⭐⭐

```markdown
# Quick Start Guide (15 minutes)

## Installation

### Option 1: pip
```bash
pip install -r requirements.txt
```

### Option 2: conda
```bash
conda env create -f environment.yml
conda activate fairness-framework
```

### Option 3: Docker
```bash
docker build -t fairness-framework .
docker run -it fairness-framework
```

## First Example

```python
from src.fairness_detector import FairnessDetector

# Load data
detector = FairnessDetector()
detector.load_data("data/case_studies/adult/adult.csv")

# Detect bias
results = detector.detect_bias()
print(results)
```

## Next Steps
- See experiments/README.md for full experiments
- Check docs/experiments/ for detailed methodology
- Run notebooks for interactive demos
```

### 10. docs/troubleshooting.md ⭐⭐

```markdown
# Troubleshooting

## Common Issues

### Installation fails
**Problem**: `pip install` fails
**Solution**:
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Out of memory
**Problem**: Experiments fail with OOM
**Solution**: Reduce batch size in config files

### Data not found
**Problem**: FileNotFoundError
**Solution**: Run `scripts/download_data.sh`

## Getting Help
- Check FAQ: docs/faq.md
- Open issue: GitHub Issues
- Email: author@email.com
```

---

## 🔄 Migrações e Reorganizações

### Fase 1: Criar Nova Estrutura (1-2 horas)

```bash
# Criar diretórios
mkdir -p src tests docker scripts docs/{experiments,api}
mkdir -p paper/{main,facct2026,portuguese}
mkdir -p experiments/{config,notebooks,results}
mkdir -p data/{raw,processed,synthetic,case_studies,ground_truth}

# Criar arquivos vazios
touch README.md LICENSE CITATION.cff CONTRIBUTING.md
touch environment.yml docker/Dockerfile
touch src/__init__.py tests/__init__.py
```

### Fase 2: Migrar Arquivos Existentes (2-3 horas)

```bash
# Papers
mv ENG/* paper/main/
mv ENG_FACCT/* paper/facct2026/
mv POR/* paper/portuguese/
rm -rf ENG ENG_FACCT POR

# Experimentos
mv experimentos/* experiments/
mv experiments/START_HERE.md experiments/README.md
mv experiments/RESUMO_EXECUTIVO.md docs/experiments/overview.md
mv experiments/PLANO_EXPERIMENTOS.md docs/experiments/timeline.md

# Dados
mv experimentos/data/synthetic_datasets/* data/synthetic/
mv experimentos/data/datasets_reais/* data/case_studies/
mv experimentos/data/ground_truth/* data/ground_truth/

# Scripts
mv experiments/scripts/*.sh scripts/
```

### Fase 3: Criar Código Modular (3-4 horas)

Extrair código dos scripts para módulos em `src/`:

- `src/fairness_detector.py`: Classe principal
- `src/metrics.py`: Métricas de fairness
- `src/visualization.py`: Funções de plot
- `src/utils.py`: Utilitários gerais

### Fase 4: Criar Notebooks (2-3 horas)

- Converter scripts em notebooks interativos
- Adicionar markdown explicativo
- Incluir visualizações

### Fase 5: Documentação (4-5 horas)

- Escrever README.md principal
- Criar guias em docs/
- Adicionar docstrings no código
- Escrever CONTRIBUTING.md

### Fase 6: Containerização (1-2 horas)

- Criar Dockerfile
- Testar build
- Criar docker-compose.yml

### Fase 7: Testes (2-3 horas)

- Criar testes unitários básicos
- Adicionar CI/CD (.github/workflows)
- Testar instalação limpa

### Fase 8: Metadados e Publicação (1-2 horas)

- Finalizar CITATION.cff
- Criar .zenodo.json
- Preparar release no GitHub
- Gerar DOI no Zenodo

---

## ✅ Checklist de Tarefas

### Essencial (Must Have) ⭐⭐⭐

- [ ] README.md principal com badges, quick start, citation
- [ ] LICENSE (MIT recomendado)
- [ ] CITATION.cff estruturado
- [ ] Reorganizar estrutura de diretórios
- [ ] Migrar papers para pasta `paper/`
- [ ] Migrar experimentos para `experiments/`
- [ ] Criar módulo `src/` com código principal
- [ ] Criar notebook de demo rápido (5 min)
- [ ] docs/quickstart.md (15 min tutorial)
- [ ] requirements.txt no root
- [ ] .gitignore completo
- [ ] Verificar que tudo funciona após migração

### Importante (Should Have) ⭐⭐

- [ ] CONTRIBUTING.md
- [ ] environment.yml (conda)
- [ ] Dockerfile e docker-compose.yml
- [ ] Notebooks para cada experimento
- [ ] docs/troubleshooting.md
- [ ] docs/faq.md
- [ ] Reorganizar dados em data/ com subpastas
- [ ] Criar testes unitários básicos
- [ ] CI/CD básico (.github/workflows)
- [ ] scripts/verify_installation.py

### Desejável (Nice to Have) ⭐

- [ ] .zenodo.json para DOI automático
- [ ] GitHub Actions para testes
- [ ] ReadTheDocs ou GitHub Pages
- [ ] Binder link para notebooks
- [ ] Colab links
- [ ] Demo online (Streamlit/Gradio)
- [ ] Video tutorial
- [ ] Badges adicionais (coverage, build status)
- [ ] Jupyter Book para documentação
- [ ] API reference completa

---

## 📏 Padrões e Best Practices

### Nomenclatura
- **Arquivos**: snake_case.py
- **Classes**: PascalCase
- **Funções**: snake_case()
- **Constantes**: UPPER_CASE

### Documentação
- Docstrings em todas funções/classes
- README em cada diretório importante
- Comentários explicativos (não óbvios)
- Type hints em Python

### Código
- PEP 8 compliance
- Máximo 80-100 caracteres por linha
- Imports organizados (stdlib, third-party, local)
- Evitar magic numbers

### Git
- Commits atômicos e descritivos
- Branches para features grandes
- Tags para versões (v1.0.0, v1.1.0)
- .gitignore robusto

### Dados
- Nunca commitar dados grandes (>10MB)
- Usar Git LFS se necessário
- Incluir scripts para download
- Documentar formato e schema

---

## 🚀 Timeline Proposta

### Semana 1: Estrutura Base (12-15 horas)
- Dia 1-2: Criar nova estrutura de diretórios
- Dia 3-4: Migrar arquivos existentes
- Dia 5: Criar README.md, LICENSE, CITATION.cff

### Semana 2: Código e Notebooks (12-15 horas)
- Dia 1-2: Refatorar código para src/
- Dia 3-4: Criar notebooks interativos
- Dia 5: Testar tudo funciona

### Semana 3: Documentação (10-12 horas)
- Dia 1-2: Escrever docs/quickstart.md
- Dia 3-4: Organizar docs/experiments/
- Dia 5: CONTRIBUTING, troubleshooting, FAQ

### Semana 4: Containerização e Publicação (8-10 horas)
- Dia 1-2: Dockerfile e testes
- Dia 3: CI/CD básico
- Dia 4: Preparar release
- Dia 5: Gerar DOI e finalizar

**Total**: 4 semanas (~40-50 horas)

---

## 🎓 Exemplos de Repos Acadêmicos Excelentes

Para inspiração:
1. [fairlearn/fairlearn](https://github.com/fairlearn/fairlearn)
2. [Trusted-AI/AIF360](https://github.com/Trusted-AI/AIF360)
3. [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn)
4. [huggingface/transformers](https://github.com/huggingface/transformers)

---

## 📞 Próximos Passos

1. **Revisar este plano** e ajustar prioridades
2. **Escolher licença** (MIT recomendado)
3. **Começar pela Fase 1**: Criar nova estrutura
4. **Trabalhar iterativamente**: Testar após cada fase
5. **Pedir feedback**: Mostrar para colegas

---

## 📊 Métricas de Sucesso

Um repositório está pronto para publicação quando:

✅ Novo usuário consegue rodar em <30 minutos
✅ Todos experimentos são reproduzíveis
✅ Documentação é clara e completa
✅ Código segue padrões (PEP 8, docstrings)
✅ README tem badges, quick start, citation
✅ Possui LICENSE e CITATION.cff
✅ Docker/container funciona
✅ Testes básicos passam

---

**Status**: 🟡 PLANO CRIADO - Aguardando aprovação e execução

**Última atualização**: 2025-12-10
