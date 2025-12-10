#!/bin/bash
# Setup automatizado do ambiente de experimentos
# DeepBridge Fairness Framework

set -e  # Exit on error

echo "=================================================="
echo "  DeepBridge Fairness - Setup de Ambiente"
echo "=================================================="
echo ""

# Diretório base
BASE_DIR="/home/guhaase/projetos/DeepBridge/papers/02_Fairness_Framework"
cd "$BASE_DIR" || exit 1

# 1. Criar ambiente virtual
echo "[1/6] Criando ambiente virtual..."
if [ -d "venv_fairness" ]; then
    echo "  ⚠️  Ambiente já existe. Removendo..."
    rm -rf venv_fairness
fi
python3 -m venv venv_fairness
source venv_fairness/bin/activate
echo "  ✅ Ambiente criado"

# 2. Atualizar pip
echo "[2/6] Atualizando pip..."
pip install --upgrade pip -q
echo "  ✅ pip atualizado"

# 3. Instalar dependências core
echo "[3/6] Instalando dependências core..."
pip install -q pandas numpy scipy scikit-learn
pip install -q matplotlib seaborn plotly kaleido
pip install -q jupyter notebook ipykernel
pip install -q pytest pytest-cov black flake8 mypy
pip install -q tqdm argparse pyyaml
echo "  ✅ Core instalado"

# 4. Instalar dependências de análise estatística
echo "[4/6] Instalando ferramentas estatísticas..."
pip install -q statsmodels pingouin
pip install -q openpyxl xlrd
echo "  ✅ Stats instalado"

# 5. Instalar ferramentas de fairness
echo "[5/6] Instalando bibliotecas de fairness..."
pip install -q aif360 fairlearn
# Aequitas pode ter problemas, tentar com fallback
pip install -q aequitas-lib || echo "  ⚠️  aequitas não instalado (não crítico)"
echo "  ✅ Fairness libs instaladas"

# 6. Configurar Jupyter kernel
echo "[6/6] Configurando Jupyter kernel..."
python -m ipykernel install --user --name=fairness_experiments --display-name="Fairness Experiments" &>/dev/null
echo "  ✅ Kernel configurado"

# Salvar requirements
pip freeze > requirements.txt
echo ""
echo "✅ Setup completo!"
echo ""
echo "Requirements salvos em: requirements.txt"
echo ""
echo "Para ativar o ambiente:"
echo "  source venv_fairness/bin/activate"
echo ""
echo "Para testar instalação:"
echo "  python -c 'import pandas, numpy, scipy, sklearn, aif360, fairlearn; print(\"✅ Imports OK\")'"
echo ""

# Teste rápido
echo "Testando imports..."
python -c "import pandas, numpy, scipy, sklearn; print('  ✅ Core libs OK')"
python -c "import matplotlib, seaborn, plotly; print('  ✅ Viz libs OK')"
python -c "import statsmodels, pingouin; print('  ✅ Stats libs OK')"
python -c "import aif360, fairlearn; print('  ✅ Fairness libs OK')"

echo ""
echo "=================================================="
echo "  Ambiente pronto para uso!"
echo "=================================================="
