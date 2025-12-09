# DeepBridge Fairness - FAccT 2026 Submission

> **Conference:** ACM Conference on Fairness, Accountability, and Transparency (FAccT 2026)
> **Location:** Montreal, Canada
> **Dates:** June 2026
> **Submission Deadline:** January 13, 2026
> **Abstract Deadline:** January 8, 2026

---

## 📋 Status da Submissão

### ✅ Concluído

- [x] Template configurado com `\documentclass[manuscript, review, anonymous]{acmart}`
- [x] Modo anônimo ativado (nomes e afiliações removidos)
- [x] Números de linha adicionados (modo `review`)
- [x] Bibliografia configurada com `ACM-Reference-Format`
- [x] CCS Concepts incluídos
- [x] Keywords definidas
- [x] Links externos anonimizados
- [x] Todas as 7 seções traduzidas para inglês
- [x] Figuras e bibliografia copiadas
- [x] Compilação bem-sucedida (34 páginas)

### ⚠️ Pendente

- [ ] **CRÍTICO: Condensar de 34 para ~14 páginas de conteúdo**
  - Limite FAccT: 14 páginas (excluindo referências)
  - Atual: ~34 páginas total (precisa verificar onde começam as referências)
  - Ação: Condensar seções, remover detalhes redundantes

- [ ] Verificar e corrigir warnings da bibliografia (32 warnings)
- [ ] Adicionar declarações obrigatórias (se aceito):
  - Author Contributions
  - Positionality Statement
  - Competing Interests
  - Acknowledgements (apenas na versão camera-ready)

- [ ] Verificar anonimização completa:
  - Citações de trabalhos próprios em terceira pessoa
  - Remover metadados do PDF
  - Verificar que não há informações identificadoras

---

## 📁 Estrutura de Arquivos

```
ENG_FACCT/
├── main.tex                    # Documento principal (configurado para FAccT)
├── sections/
│   ├── 01_introduction.tex
│   ├── 02_related_work.tex
│   ├── 03_architecture.tex
│   ├── 04_case_studies.tex
│   ├── 05_evaluation.tex
│   ├── 06_discussion.tex
│   └── 07_conclusion.tex
├── bibliography/
│   └── references.bib
├── figures/
│   ├── architecture_simple.tex
│   ├── architecture_simple.pdf
│   ├── figure1_detection_performance.pdf
│   └── figure2_performance_comparison.pdf
└── README.md                   # Este arquivo
```

---

## 🔧 Como Compilar

```bash
cd /home/guhaase/projetos/DeepBridge/papers/02_Fairness_Framework/ENG_FACCT

# Compilação completa
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Verificar número de páginas
pdfinfo main.pdf | grep Pages
```

---

## 📏 Limites e Regras FAccT 2026

### Limites de Páginas

| Item | Limite |
|------|--------|
| **Conteúdo principal** | **14 páginas** (obrigatório) |
| **Referências** | Ilimitado |
| **Apêndice** | Ilimitado (revisores não são obrigados a ler) |

### Formato Obrigatório

- **Classe:** `acmart` com opções `[manuscript, review, anonymous]`
- **Bibliografia:** `ACM-Reference-Format.bst`
- **Anonimização:** Completa (double-blind review)
- **Números de linha:** Sim (modo `review`)
- **Coluna única:** Sim (modo `manuscript`)

### O que REMOVER na Submissão

- ❌ Nomes e afiliações dos autores
- ❌ Acknowledgements
- ❌ Funding information
- ❌ Author Contributions
- ❌ Positionality Statement
- ❌ Links identificadores (GitHub pessoal, etc.)

### O que INCLUIR

- ✅ Abstract
- ✅ CCS Concepts
- ✅ Keywords
- ✅ Citações próprias em terceira pessoa
- ✅ Links anonimizados (anonymous.4open.science ou placeholder)

---

## 📝 Checklist Pré-Submissão

### Formatação

- [x] Template correto: `\documentclass[manuscript, review, anonymous]{acmart}`
- [x] Bibliografia ACM: `\bibliographystyle{ACM-Reference-Format}`
- [x] CCS Concepts incluídos
- [x] Keywords definidas
- [ ] Limite de 14 páginas respeitado (CRÍTICO)

### Anonimização

- [x] Modo `anonymous` ativado
- [x] Nomes removidos
- [x] Links externos anonimizados
- [ ] Verificar citações próprias (terceira pessoa)
- [ ] Remover metadados do PDF:
  ```bash
  exiftool -all= main.pdf
  ```

### Conteúdo

- [ ] Abstract revisado (≤300 palavras recomendado)
- [ ] Figuras legíveis
- [ ] Tabelas formatadas com `booktabs`
- [ ] Código formatado com `listings`
- [ ] Citações completas e corretas

### Qualidade

- [ ] Spell check
- [ ] Grammar check
- [ ] Verificar warnings LaTeX
- [ ] Verificar warnings BibTeX (32 warnings atualmente)
- [ ] Compilação sem erros

---

## 🎯 Próximos Passos (Prioridade)

### 1. **URGENTE: Condensar para 14 páginas**

O paper atual tem ~34 páginas no formato manuscript (coluna única). Precisa ser reduzido para 14 páginas de conteúdo (excluindo referências).

**Estratégias:**

- Condensar seção de Related Work (combinar subseções)
- Mover detalhes técnicos para apêndice
- Reduzir tamanho de tabelas e figuras
- Remover exemplos redundantes
- Consolidar resultados experimentais

### 2. Corrigir Warnings da Bibliografia

32 warnings BibTeX precisam ser corrigidos:
- Adicionar campos faltantes (volume, number, pages)
- Completar informações de publisher/address
- Verificar entradas duplicadas

### 3. Revisão de Anonimização

- Fazer busca por nomes próprios no PDF
- Verificar metadados: `pdfinfo main.pdf`
- Remover se necessário: `exiftool -all= main.pdf`

### 4. Revisão Final

- Leitura completa para clareza e coerência
- Verificar que claims são suportados por evidências
- Revisar abstract (máximo impacto, ~300 palavras)

---

## 📚 Recursos e Referências

| Recurso | Link |
|---------|------|
| **FAccT 2026 CFP** | https://facctconference.org/2026/cfp.html |
| **Author Guide** | https://facctconference.org/2026/authorguide.html |
| **ACM Template** | https://www.acm.org/publications/proceedings-template |
| **CCS Generator** | https://dl.acm.org/ccs/ccs.cfm |
| **LaTeX Whitelist** | https://www.acm.org/publications/taps/whitelist-of-latex-packages |
| **Guia Completo** | `../facct_2026_latex_guide.md` |

---

## 🚀 Timeline Sugerida

```
Dezembro 2025
├── Semana 3-4
│   ├── [x] Configurar template LaTeX
│   ├── [x] Traduzir para inglês
│   ├── [ ] Condensar para 14 páginas
│   └── [ ] Corrigir bibliografia

Janeiro 2026
├── Semana 1 (até 8 Jan)
│   ├── [ ] Revisão completa
│   ├── [ ] Verificar anonimização
│   ├── [ ] Submeter Abstract
│   └── [ ] Preparar supplementary materials
│
└── Semana 2 (até 13 Jan)
    ├── [ ] Revisão final
    ├── [ ] Remover metadados PDF
    └── [ ] SUBMETER PAPER
```

---

## ⚙️ Comandos Úteis

```bash
# Verificar número de páginas
pdfinfo main.pdf | grep Pages

# Contar palavras (aproximado)
texcount main.tex

# Verificar metadados
pdfinfo main.pdf

# Remover metadados
exiftool -all= main.pdf

# Compilação rápida (sem bibliografia)
pdflatex -interaction=nonstopmode main.tex

# Compilação completa
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

---

## 📧 Contato para Suporte

- **Template LaTeX:** acmtexsupport@aptaracorp.com
- **FAccT Program Chairs:** program-chairs@facctconference.org

---

**Última atualização:** Dezembro 8, 2025
**Status:** Em preparação - **AÇÃO CRÍTICA: Reduzir para 14 páginas**
