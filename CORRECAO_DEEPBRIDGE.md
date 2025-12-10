# 🔧 Correção: Usar DeepBridge ao Invés de `src/`

## Problema Identificado

Durante a refatoração, foi criada uma implementação própria em `src/` quando o projeto deveria usar a biblioteca **DeepBridge** existente.

## Opções de Correção

### Opção 1: Remover `src/` e Usar Só DeepBridge ⭐⭐⭐

**Quando usar**: Se o paper é sobre validar/testar DeepBridge

**Passos**:

```bash
# 1. Backup (caso precise)
cp -r src/ src_backup/

# 2. Remover implementação própria
rm -rf src/
rm -rf tests/  # Testes eram para src/

# 3. Atualizar exemplos nos READMEs
# Substituir:
#   from src.fairness_detector import FairnessDetector
# Por:
#   from deepbridge import DBDataset

# 4. Criar exemplos corretos com DeepBridge
```

**Exemplo de código correto**:

```python
from deepbridge import DBDataset

# Carregar dados
dataset = DBDataset.from_csv(
    "data/case_studies/adult/adult.csv",
    target="income",
    sensitive_attrs=["race", "sex"]
)

# Detectar bias
results = dataset.detect_bias()

# Ver resultados
print(results.summary())
results.plot()
```

---

### Opção 2: `src/` como Wrappers do DeepBridge ⭐⭐

**Quando usar**: Se você quer adicionar funcionalidades extras

**Passos**:

```bash
# 1. Renomear src/ para extensions/
mv src/ extensions/

# 2. Modificar para usar DeepBridge internamente
```

**Exemplo**:

```python
# extensions/enhanced_detector.py
from deepbridge import DBDataset

class EnhancedFairnessDetector:
    """Wrapper que adiciona funcionalidades ao DeepBridge."""

    def __init__(self, data_path):
        self.dataset = DBDataset.from_csv(data_path)

    def detect_bias_with_eeoc(self):
        # Usa DeepBridge + adiciona EEOC
        results = self.dataset.detect_bias()
        eeoc = self.check_eeoc_compliance()
        return {**results, 'eeoc': eeoc}

    def check_eeoc_compliance(self):
        # Sua implementação extra
        ...
```

---

### Opção 3: Manter Ambos ⭐

**Quando usar**: Se você quer comparar implementações

**Exemplo**:

```python
# Comparar DeepBridge vs implementação de referência
from deepbridge import DBDataset
from src.fairness_detector import FairnessDetector

# Testar DeepBridge
db_results = DBDataset.from_csv("data.csv").detect_bias()

# Testar implementação de referência
ref_detector = FairnessDetector()
ref_results = ref_detector.detect_bias(data)

# Comparar
print(f"DeepBridge: {db_results}")
print(f"Reference: {ref_results}")
```

---

## Arquivos a Atualizar

Se escolher Opção 1 (remover `src/`):

### 1. README.md

```diff
- from src.fairness_detector import FairnessDetector
- detector = FairnessDetector()
+ from deepbridge import DBDataset
+ dataset = DBDataset.from_csv("data.csv")
```

### 2. docs/quickstart.md

```diff
- # Import the Framework
- from src.fairness_detector import FairnessDetector
+ # Import DeepBridge
+ from deepbridge import DBDataset, FairnessTestManager
```

### 3. experiments/notebooks/

Atualizar todos notebooks para usar DeepBridge:

```python
# Célula 1
import sys
sys.path.insert(0, '../..')

from deepbridge import DBDataset  # Correto
# from src.fairness_detector import FairnessDetector  # Remover
```

### 4. scripts/

Atualizar `demo_quick.py` e `verify_installation.py`:

```python
# Verificar se DeepBridge está instalado
try:
    from deepbridge import DBDataset
    print("✓ DeepBridge")
except ImportError:
    print("✗ DeepBridge - NOT INSTALLED")
```

---

## Script de Correção Automática

```bash
#!/bin/bash
# fix_deepbridge.sh

echo "🔧 Corrigindo para usar DeepBridge..."

# Backup
echo "📦 Fazendo backup..."
cp -r src/ src_backup_$(date +%Y%m%d)/ 2>/dev/null
cp -r tests/ tests_backup_$(date +%Y%m%d)/ 2>/dev/null

# Remover implementação própria
echo "🗑️  Removendo src/ e tests/..."
rm -rf src/
rm -rf tests/

# Atualizar imports nos notebooks
echo "📝 Atualizando notebooks..."
find experiments/notebooks/ -name "*.ipynb" -exec sed -i 's/from src\./from deepbridge import /g' {} \;

# Atualizar scripts
echo "🔧 Atualizando scripts..."
find scripts/ -name "*.py" -exec sed -i 's/from src\./from deepbridge import /g' {} \;

echo "✅ Correção completa!"
echo ""
echo "Próximos passos:"
echo "1. Instalar DeepBridge: pip install deepbridge"
echo "2. Testar: python -c 'from deepbridge import DBDataset; print(\"OK\")'"
echo "3. Atualizar READMEs manualmente"
```

---

## Verificação Pós-Correção

```bash
# 1. Verificar que DeepBridge está instalado
pip install deepbridge

# 2. Testar import
python -c "from deepbridge import DBDataset; print('✓ DeepBridge OK')"

# 3. Verificar que src/ não existe mais
ls src/ 2>/dev/null && echo "⚠️  src/ ainda existe" || echo "✓ src/ removido"

# 4. Grep para encontrar imports antigos
grep -r "from src\." . --include="*.py" --include="*.ipynb" || echo "✓ Nenhum import de src/ encontrado"
```

---

## Recomendação Final

Para um paper sobre **validação experimental do DeepBridge**:

1. ✅ **USE: Opção 1** (Remover `src/`, usar só DeepBridge)
2. ✅ Focar nos experimentos de validação
3. ✅ Mostrar que DeepBridge funciona como esperado

**Justificativa**:
- Paper é sobre validar DeepBridge, não criar biblioteca nova
- Ter `src/` confunde o propósito do repositório
- Revisores esperam ver uso do DeepBridge

---

## Suporte

Se tiver dúvidas sobre qual opção escolher:
- Leia o título/abstract do paper
- Se menciona "DeepBridge validation" → Opção 1
- Se menciona "novel extensions" → Opção 2
- Se menciona "comparative analysis" → Opção 3

---

**Status**: 🟡 Aguardando decisão sobre qual opção seguir
**Data**: 2025-12-10
