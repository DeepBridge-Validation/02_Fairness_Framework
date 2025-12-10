# Como Compilar o Paper com Referências Bibliográficas

## Problema
As referências bibliográficas aparecem como `[?]` quando compilado apenas com `pdflatex`. Isso acontece porque é necessário rodar o BibTeX para processar o arquivo `.bib`.

## Solução 1: Script Automático (Recomendado)

Execute o script de compilação:

```bash
./compile.sh
```

Este script executa automaticamente a sequência correta:
1. `pdflatex` - primeira passagem
2. `bibtex` - processa referências
3. `pdflatex` - resolve citações
4. `pdflatex` - resolve referências cruzadas

## Solução 2: VSCode LaTeX Workshop

Se você tem a extensão **LaTeX Workshop** instalada no VSCode:

1. A configuração em `.vscode/settings.json` já está configurada
2. Basta salvar o arquivo `main.tex` (Ctrl+S)
3. O VSCode compila automaticamente com BibTeX

## Solução 3: Manual

Execute os comandos manualmente:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Verificação

Após compilar, o PDF deve ter:
- **17 páginas**
- **23 referências bibliográficas** (na última página)
- Citações no formato `[1]`, `[2]`, etc. ao invés de `[?]`

## Arquivos Gerados

- `main.pdf` - documento final
- `main.bbl` - bibliografia processada (6.1 KB, 23 refs)
- `main.aux` - arquivo auxiliar
- `main.blg` - log do BibTeX

## Diferença Overleaf vs. Local

- **Overleaf**: Executa automaticamente toda a sequência (pdflatex → bibtex → pdflatex × 2)
- **VSCode/Local**: Você precisa rodar manualmente ou usar o script/configuração

## Extensão Recomendada para VSCode

**LaTeX Workshop** by James Yu
- Install: `code --install-extension James-Yu.latex-workshop`
- Recursos: compilação automática, preview, autocompletar, etc.
