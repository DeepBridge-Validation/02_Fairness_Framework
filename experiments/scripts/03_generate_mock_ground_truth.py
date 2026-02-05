#!/usr/bin/env python3
"""
Gera ground truth mock para desenvolvimento/teste.

ATENÇÃO: Use apenas para DESENVOLVIMENTO.
Para o paper final, você PRECISA de anotação manual real!

Uso:
    python 03_generate_mock_ground_truth.py --n-datasets 500
"""

import argparse
import json
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
import pandas as pd


class MockGroundTruthGenerator:
    """Gera ground truth automático para desenvolvimento."""

    def __init__(self, datasets_dir: str, output_file: str):
        self.datasets_dir = Path(datasets_dir)
        self.output_file = Path(output_file)

        # Keywords de atributos sensíveis
        self.sensitive_keywords = {
            'race': ['race', 'ethnicity', 'ethnic', 'raca', 'etnia', 'color'],
            'gender': ['gender', 'sex', 'genero', 'sexo', 'male', 'female'],
            'age': ['age', 'birth', 'birthday', 'anos', 'idade', 'dob'],
            'religion': ['religion', 'religious', 'faith', 'religiao'],
            'disability': ['disability', 'disabled', 'handicap', 'deficiencia'],
            'nationality': ['nationality', 'national', 'country', 'nation'],
            'marital': ['marital', 'married', 'marriage', 'civil'],
            'veteran': ['veteran', 'military', 'service'],
            'orientation': ['orientation', 'sexual', 'lgbt']
        }

    def fuzzy_match(self, text1: str, text2: str) -> float:
        """Calcula similaridade entre strings."""
        text1 = text1.lower().strip().replace('_', '').replace(' ', '')
        text2 = text2.lower().strip().replace('_', '').replace(' ', '')
        return SequenceMatcher(None, text1, text2).ratio()

    def detect_sensitive_columns(self, df: pd.DataFrame, threshold: float = 0.75) -> list:
        """Detecta colunas sensíveis automaticamente."""
        detected = []

        for column in df.columns:
            col_clean = column.lower().strip()

            for category, keywords in self.sensitive_keywords.items():
                for keyword in keywords:
                    # Fuzzy matching
                    score = self.fuzzy_match(col_clean, keyword)

                    # Ou substring matching
                    if keyword in col_clean:
                        score = max(score, 0.9)

                    if score >= threshold:
                        detected.append({
                            'column': column,
                            'category': category,
                            'confidence': score
                        })
                        break  # Já encontrou, não precisa testar outros keywords
                if detected and detected[-1]['column'] == column:
                    break  # Já classificou esta coluna

        # Remover duplicatas
        seen = set()
        unique_detected = []
        for item in detected:
            if item['column'] not in seen:
                seen.add(item['column'])
                unique_detected.append(item)

        return unique_detected

    def generate_ground_truth(self, n_datasets: int = None):
        """Gera ground truth para N datasets."""
        datasets = sorted(self.datasets_dir.glob('*.csv'))

        if n_datasets:
            datasets = datasets[:n_datasets]

        print(f"\nGerando ground truth para {len(datasets)} datasets...")
        print(f"⚠️  ATENÇÃO: Isso é APENAS para desenvolvimento!")
        print(f"⚠️  Para o paper final, use anotação manual real.\n")

        ground_truth = {}

        for i, dataset_path in enumerate(datasets, 1):
            try:
                # Ler apenas header
                df = pd.read_csv(dataset_path, nrows=10)

                # Detectar atributos sensíveis
                detections = self.detect_sensitive_columns(df)

                # Salvar
                ground_truth[dataset_path.name] = {
                    'file': str(dataset_path),
                    'sensitive_columns': [d['column'] for d in detections],
                    'sensitive_categories': [d['category'] for d in detections],
                    'n_sensitive': len(detections),
                    'n_features': len(df.columns),
                    'n_samples': len(df),
                    'method': 'auto_generated_mock',
                    'warning': 'THIS IS MOCK DATA - NOT REAL ANNOTATION'
                }

                if (i % 50) == 0:
                    print(f"  Processado: {i}/{len(datasets)} datasets")

            except Exception as e:
                print(f"  ⚠️  Erro em {dataset_path.name}: {e}")

        # Salvar
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_file, 'w') as f:
            json.dump(ground_truth, f, indent=2)

        print(f"\n✅ Ground truth mock salvo em: {self.output_file}")
        print(f"   Total de datasets: {len(ground_truth)}")

        # Estatísticas
        total_sensitive = sum(gt['n_sensitive'] for gt in ground_truth.values())
        avg_sensitive = total_sensitive / len(ground_truth) if ground_truth else 0

        print(f"   Total de atributos sensíveis detectados: {total_sensitive}")
        print(f"   Média por dataset: {avg_sensitive:.2f}")

        # Simular 2 anotadores (com pequenas variações)
        self.generate_annotator_versions(ground_truth)

    def generate_annotator_versions(self, ground_truth: dict):
        """Gera versões para 2 anotadores com pequenas variações."""
        # Anotador 1: igual ao ground truth
        anno1_file = self.output_file.parent / 'annotations_annotator_1.json'
        with open(anno1_file, 'w') as f:
            json.dump(ground_truth, f, indent=2)

        print(f"\n✅ Anotações do anotador 1: {anno1_file}")

        # Anotador 2: com 5% de variação (para simular discordância)
        anno2 = {}
        np.random.seed(42)

        for dataset_name, gt in ground_truth.items():
            anno2[dataset_name] = gt.copy()

            # 5% de chance de remover um atributo sensível
            if gt['sensitive_columns'] and np.random.random() < 0.05:
                cols = gt['sensitive_columns'].copy()
                if len(cols) > 1:  # Manter pelo menos 1
                    remove_idx = np.random.randint(0, len(cols))
                    cols.pop(remove_idx)
                    anno2[dataset_name]['sensitive_columns'] = cols
                    anno2[dataset_name]['n_sensitive'] = len(cols)

            # 3% de chance de adicionar um falso positivo
            elif np.random.random() < 0.03:
                # Pegar uma coluna não-sensível aleatória
                all_cols = range(gt['n_features'])
                non_sensitive = [i for i in all_cols if i not in range(len(gt['sensitive_columns']))]
                if non_sensitive:
                    fake_col = f"feature_{np.random.choice(non_sensitive)}"
                    anno2[dataset_name]['sensitive_columns'].append(fake_col)
                    anno2[dataset_name]['n_sensitive'] += 1

        anno2_file = self.output_file.parent / 'annotations_annotator_2.json'
        with open(anno2_file, 'w') as f:
            json.dump(anno2, f, indent=2)

        print(f"✅ Anotações do anotador 2: {anno2_file}")
        print(f"\n⚠️  Variação simulada de ~5% entre anotadores")
        print(f"⚠️  Kappa esperado: ~0.85-0.90 (substancial)")


def main():
    parser = argparse.ArgumentParser(description='Gerar ground truth mock')
    parser.add_argument('--n-datasets', type=int, default=500,
                       help='Número de datasets')
    parser.add_argument('--datasets-dir', type=str, default='../data/datasets',
                       help='Diretório com datasets')
    parser.add_argument('--output', type=str, default='../data/ground_truth_final.json',
                       help='Arquivo de saída')

    args = parser.parse_args()

    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║                                                                    ║")
    print("║         GERADOR DE GROUND TRUTH MOCK (DESENVOLVIMENTO)            ║")
    print("║                                                                    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()
    print("⚠️  ATENÇÃO: Este script gera ground truth AUTOMATICAMENTE")
    print("⚠️  É adequado APENAS para desenvolvimento e testes")
    print("⚠️  Para o PAPER FINAL, você PRECISA de anotação manual real!")
    print()

    response = input("Continuar? (s/n): ")
    if response.lower() != 's':
        print("Cancelado.")
        return

    generator = MockGroundTruthGenerator(
        datasets_dir=args.datasets_dir,
        output_file=args.output
    )

    generator.generate_ground_truth(n_datasets=args.n_datasets)

    print("\n" + "="*70)
    print("✅ CONCLUÍDO")
    print("="*70)
    print()
    print("Próximos passos:")
    print("  1. Verificar agreement: python 02_annotate_ground_truth.py --calculate-agreement")
    print("  2. Executar experimentos: ./run_all_experiments.sh")
    print()
    print("LEMBRETE: Substitua por anotação manual real antes da submissão!")
    print()


if __name__ == '__main__':
    main()
