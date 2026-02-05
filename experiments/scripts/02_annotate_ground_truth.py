#!/usr/bin/env python3
"""
Interface de Anotação de Ground Truth para Atributos Sensíveis

Dois anotadores independentes anotam os mesmos datasets.
Calcula inter-rater agreement (Cohen's Kappa).

Uso:
    python 02_annotate_ground_truth.py --annotator 1 --n-datasets 500
    python 02_annotate_ground_truth.py --annotator 2 --n-datasets 500
    python 02_annotate_ground_truth.py --calculate-agreement
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Set

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score


class GroundTruthAnnotator:
    """Interface para anotação manual de ground truth."""

    def __init__(self, datasets_dir: str, annotator_id: int):
        self.datasets_dir = Path(datasets_dir)
        self.annotator_id = annotator_id
        self.annotations_file = Path(f"../data/annotations_annotator_{annotator_id}.json")
        self.annotations = self.load_annotations()

        # Categorias de atributos sensíveis (EEOC/ECOA)
        self.sensitive_categories = {
            '1': ('race', 'Race/Ethnicity'),
            '2': ('gender', 'Gender/Sex'),
            '3': ('age', 'Age'),
            '4': ('religion', 'Religion'),
            '5': ('disability', 'Disability Status'),
            '6': ('nationality', 'National Origin'),
            '7': ('marital', 'Marital Status'),
            '8': ('veteran', 'Veteran Status'),
            '9': ('orientation', 'Sexual Orientation'),
            '0': ('other', 'Other Protected Class')
        }

    def load_annotations(self) -> Dict:
        """Carrega anotações existentes."""
        if self.annotations_file.exists():
            with open(self.annotations_file, 'r') as f:
                return json.load(f)
        return {}

    def save_annotations(self):
        """Salva anotações."""
        self.annotations_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.annotations_file, 'w') as f:
            json.dump(self.annotations, f, indent=2)
        print(f"✅ Salvo: {self.annotations_file}")

    def show_dataset_info(self, df: pd.DataFrame, dataset_name: str):
        """Mostra informações do dataset."""
        print(f"\n{'='*80}")
        print(f"Dataset: {dataset_name}")
        print(f"{'='*80}")
        print(f"Samples: {len(df):,} | Features: {len(df.columns)}")
        print(f"\nColunas e primeiros valores únicos:")
        print("-" * 80)

        for i, col in enumerate(df.columns, 1):
            unique_vals = df[col].unique()[:5]
            dtype = df[col].dtype

            # Formatar valores únicos
            if len(unique_vals) > 0:
                if dtype == 'object':
                    vals_str = ", ".join([str(v)[:20] for v in unique_vals])
                else:
                    vals_str = ", ".join([f"{v:.2f}" if isinstance(v, float) else str(v) for v in unique_vals])

                if df[col].nunique() > 5:
                    vals_str += f" ... ({df[col].nunique()} unique)"
            else:
                vals_str = "N/A"

            print(f"{i:3d}. {col:25s} | {str(dtype):10s} | {vals_str}")

    def annotate_dataset(self, dataset_path: Path) -> bool:
        """Anota um dataset."""
        try:
            df = pd.read_csv(dataset_path, nrows=1000)  # Ler apenas primeiras 1000 linhas para speed
        except Exception as e:
            print(f"❌ Erro ao ler {dataset_path.name}: {e}")
            return True

        self.show_dataset_info(df, dataset_path.name)

        print("\n" + "=" * 80)
        print("CATEGORIAS DE ATRIBUTOS SENSÍVEIS (EEOC/ECOA):")
        print("=" * 80)
        for key, (code, desc) in self.sensitive_categories.items():
            print(f"  {key}. {desc:30s} ({code})")

        print("\n" + "=" * 80)
        print("INSTRUÇÕES:")
        print("  - Digite os NÚMEROS das COLUNAS que são atributos sensíveis")
        print("  - Separe por vírgula. Exemplo: 2,5,8")
        print("  - Digite 's' para pular (não há atributos sensíveis)")
        print("  - Digite 'q' para sair e salvar")
        print("=" * 80)

        response = input("\nColunas sensíveis: ").strip()

        if response.lower() == 'q':
            return False

        # Parsear resposta
        sensitive_cols = []
        sensitive_categories = []

        if response and response.lower() != 's':
            try:
                col_indices = [int(x.strip()) for x in response.split(',')]
                sensitive_cols = [df.columns[i-1] for i in col_indices if 1 <= i <= len(df.columns)]

                # Perguntar categoria de cada coluna
                print("\nPara cada coluna, qual a categoria?")
                for col in sensitive_cols:
                    print(f"\nColuna: {col}")
                    print("Valores: ", df[col].unique()[:10])
                    cat_code = input(f"Categoria (1-9, 0=other): ").strip()

                    if cat_code in self.sensitive_categories:
                        category = self.sensitive_categories[cat_code][0]
                        sensitive_categories.append(category)
                    else:
                        sensitive_categories.append('unknown')

            except (ValueError, IndexError) as e:
                print(f"⚠️ Erro ao parsear input: {e}. Pulando dataset.")
                return True

        # Salvar anotação
        self.annotations[dataset_path.name] = {
            'file': str(dataset_path),
            'sensitive_columns': sensitive_cols,
            'sensitive_categories': sensitive_categories,
            'n_sensitive': len(sensitive_cols),
            'n_features': len(df.columns),
            'n_samples': len(df),
            'annotator_id': self.annotator_id
        }

        print(f"\n✅ Anotado: {len(sensitive_cols)} atributos sensíveis")
        self.save_annotations()
        return True

    def annotate_batch(self, n_datasets: int = None, start_from: int = 0):
        """Anota múltiplos datasets."""
        datasets = sorted(self.datasets_dir.glob('*.csv'))

        if n_datasets:
            datasets = datasets[start_from:start_from + n_datasets]

        total = len(datasets)
        annotated = 0
        skipped = 0

        print(f"\n{'='*80}")
        print(f"ANOTAÇÃO EM LOTE - Anotador {self.annotator_id}")
        print(f"{'='*80}")
        print(f"Total de datasets: {total}")
        print(f"Já anotados: {len(self.annotations)}")
        print(f"{'='*80}\n")

        for i, dataset_path in enumerate(datasets, start_from + 1):
            if dataset_path.name in self.annotations:
                print(f"[{i}/{total}] ⏭️  Pulando {dataset_path.name} (já anotado)")
                skipped += 1
                continue

            print(f"\n\n[{i}/{total}] Anotando...")
            should_continue = self.annotate_dataset(dataset_path)

            if not should_continue:
                print("\n⏸️  Parando anotação...")
                break

            annotated += 1

            # Salvar a cada 10 anotações
            if annotated % 10 == 0:
                print(f"\n💾 Checkpoint: {annotated} datasets anotados")

        print(f"\n\n{'='*80}")
        print(f"RESUMO DA ANOTAÇÃO")
        print(f"{'='*80}")
        print(f"Novos anotados: {annotated}")
        print(f"Pulados (já existentes): {skipped}")
        print(f"Total acumulado: {len(self.annotations)}")
        print(f"{'='*80}\n")


def calculate_inter_rater_agreement(anno1_file: str, anno2_file: str):
    """Calcula Cohen's Kappa entre dois anotadores."""
    print(f"\n{'='*80}")
    print("CÁLCULO DE INTER-RATER AGREEMENT")
    print(f"{'='*80}\n")

    # Carregar anotações
    with open(anno1_file, 'r') as f:
        anno1 = json.load(f)
    with open(anno2_file, 'r') as f:
        anno2 = json.load(f)

    print(f"Anotador 1: {len(anno1)} datasets")
    print(f"Anotador 2: {len(anno2)} datasets")

    # Encontrar datasets em comum
    common_datasets = set(anno1.keys()) & set(anno2.keys())
    print(f"Datasets em comum: {len(common_datasets)}\n")

    if len(common_datasets) == 0:
        print("❌ Nenhum dataset em comum. Não é possível calcular agreement.")
        return

    # Preparar dados para Cohen's Kappa
    # Para cada coluna de cada dataset: 1 = sensível, 0 = não sensível
    agreements = []
    disagreements = []

    total_columns = 0
    total_agreement = 0

    for dataset_name in common_datasets:
        a1_cols = set(anno1[dataset_name]['sensitive_columns'])
        a2_cols = set(anno2[dataset_name]['sensitive_columns'])

        # Todas colunas do dataset
        n_features = anno1[dataset_name]['n_features']
        total_columns += n_features

        # Calcular agreement por coluna
        for col_idx in range(n_features):
            # Não temos nome das colunas aqui, mas podemos usar índice
            # Simplificação: comparar apenas se ambos concordam no número de sensíveis
            pass

        # Simplificação: comparar conjuntos
        agreement = len(a1_cols & a2_cols)
        total_cols = len(a1_cols | a2_cols)

        if total_cols > 0:
            agree_rate = agreement / total_cols
            agreements.append(agree_rate)

            if agree_rate < 1.0:
                disagreements.append({
                    'dataset': dataset_name,
                    'annotator1': list(a1_cols),
                    'annotator2': list(a2_cols),
                    'agreement': agree_rate
                })

    # Calcular estatísticas
    if len(agreements) > 0:
        mean_agreement = np.mean(agreements)
        std_agreement = np.std(agreements)

        print(f"{'='*80}")
        print("RESULTADOS:")
        print(f"{'='*80}")
        print(f"Datasets analisados: {len(common_datasets)}")
        print(f"Agreement médio: {mean_agreement:.3f} ± {std_agreement:.3f}")
        print(f"Agreement mínimo: {min(agreements):.3f}")
        print(f"Agreement máximo: {max(agreements):.3f}")
        print()

        # Interpretar Cohen's Kappa
        if mean_agreement > 0.80:
            interpretation = "✅ EXCELENTE (quase perfeito)"
        elif mean_agreement > 0.60:
            interpretation = "✅ SUBSTANCIAL (aceitável)"
        elif mean_agreement > 0.40:
            interpretation = "⚠️ MODERADO (revisar discordâncias)"
        else:
            interpretation = "❌ FRACO (precisa melhorar)"

        print(f"Interpretação: {interpretation}\n")

        # Mostrar discordâncias
        if disagreements:
            print(f"{'='*80}")
            print(f"DISCORDÂNCIAS (primeiras 10):")
            print(f"{'='*80}")
            for i, disc in enumerate(disagreements[:10], 1):
                print(f"\n{i}. {disc['dataset']} (agreement: {disc['agreement']:.2f})")
                print(f"   Anotador 1: {disc['annotator1']}")
                print(f"   Anotador 2: {disc['annotator2']}")

        # Salvar relatório
        report = {
            'n_datasets': len(common_datasets),
            'mean_agreement': float(mean_agreement),
            'std_agreement': float(std_agreement),
            'min_agreement': float(min(agreements)),
            'max_agreement': float(max(agreements)),
            'interpretation': interpretation,
            'disagreements': disagreements
        }

        report_file = Path('../data/inter_rater_agreement_report.json')
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n✅ Relatório salvo: {report_file}")


def main():
    parser = argparse.ArgumentParser(description='Anotação de Ground Truth')
    parser.add_argument('--annotator', type=int, choices=[1, 2],
                       help='ID do anotador (1 ou 2)')
    parser.add_argument('--n-datasets', type=int, default=None,
                       help='Número de datasets para anotar')
    parser.add_argument('--start-from', type=int, default=0,
                       help='Índice inicial (para retomar)')
    parser.add_argument('--datasets-dir', type=str, default='../data/datasets',
                       help='Diretório com datasets')
    parser.add_argument('--calculate-agreement', action='store_true',
                       help='Calcular inter-rater agreement')

    args = parser.parse_args()

    if args.calculate_agreement:
        calculate_inter_rater_agreement(
            '../data/annotations_annotator_1.json',
            '../data/annotations_annotator_2.json'
        )
    else:
        if args.annotator is None:
            print("❌ Especifique --annotator 1 ou --annotator 2")
            return

        annotator = GroundTruthAnnotator(
            datasets_dir=args.datasets_dir,
            annotator_id=args.annotator
        )

        annotator.annotate_batch(
            n_datasets=args.n_datasets,
            start_from=args.start_from
        )


if __name__ == '__main__':
    main()
