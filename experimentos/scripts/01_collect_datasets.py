#!/usr/bin/env python3
"""
Coleta de 500 datasets para validação de auto-detecção.
Fontes: UCI, Kaggle, OpenML, Synthetic

Uso:
    python 01_collect_datasets.py --target 500 --output ../data/datasets
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
from tqdm import tqdm
import argparse
import requests
import time


class DatasetCollector:
    def __init__(self, output_dir: str = "../data/datasets"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metadata = []

        # Categorias de atributos sensíveis
        self.sensitive_attrs = {
            'gender': ['Male', 'Female', 'Non-binary', 'M', 'F', 'Other'],
            'race': ['White', 'Black', 'Asian', 'Hispanic', 'Other', 'African American'],
            'age': list(range(18, 100)),  # Will be discretized
            'age_group': ['18-25', '26-35', '36-50', '51-65', '65+'],
            'religion': ['Christian', 'Muslim', 'Jewish', 'Hindu', 'Buddhist', 'None', 'Other'],
            'disability': ['None', 'Physical', 'Mental', 'Both', 'Yes', 'No'],
            'nationality': ['US', 'UK', 'India', 'China', 'Brazil', 'Mexico', 'Germany', 'Other'],
            'marital_status': ['Single', 'Married', 'Divorced', 'Widowed'],
            'veteran': ['Yes', 'No', 'Veteran', 'Non-Veteran'],
            'sexual_orientation': ['Heterosexual', 'Homosexual', 'Bisexual', 'Other'],
        }

    def generate_synthetic_dataset(self, idx: int) -> pd.DataFrame:
        """Gera um dataset sintético com atributos sensíveis."""
        n_samples = np.random.randint(500, 10000)

        data = {}

        # Selecionar 1-4 atributos sensíveis aleatoriamente
        n_sensitive = np.random.randint(1, 5)
        selected_attrs = np.random.choice(
            list(self.sensitive_attrs.keys()),
            n_sensitive,
            replace=False
        )

        sensitive_names = []
        for attr in selected_attrs:
            # Variar os nomes (original, variations, typos)
            variations = {
                'gender': ['gender', 'sex', 'Gender', 'SEX', 'genero'],
                'race': ['race', 'ethnicity', 'Race', 'RACE', 'ethnic_group'],
                'age': ['age', 'Age', 'AGE', 'birth_year', 'anos'],
                'age_group': ['age_group', 'age_range', 'AgeGroup'],
                'religion': ['religion', 'Religion', 'faith', 'religious_affiliation'],
                'disability': ['disability', 'Disability', 'disabled', 'handicap'],
                'nationality': ['nationality', 'country', 'Nationality', 'nation'],
                'marital_status': ['marital_status', 'married', 'civil_status'],
                'veteran': ['veteran', 'military', 'Veteran'],
                'sexual_orientation': ['sexual_orientation', 'orientation', 'sexuality'],
            }

            col_name = np.random.choice(variations.get(attr, [attr]))
            sensitive_names.append(col_name)

            # Gerar valores
            if attr == 'age' and np.random.random() > 0.5:
                data[col_name] = np.random.randint(18, 80, n_samples)
            else:
                data[col_name] = np.random.choice(
                    self.sensitive_attrs[attr],
                    n_samples
                )

        # Adicionar features normais (não sensíveis)
        n_features = np.random.randint(5, 20)
        for j in range(n_features):
            feature_type = np.random.choice(['numeric', 'categorical'])
            if feature_type == 'numeric':
                data[f'feature_{j}'] = np.random.randn(n_samples) * 100
            else:
                data[f'feature_{j}'] = np.random.choice(
                    ['A', 'B', 'C', 'D', 'E'],
                    n_samples
                )

        # Target
        data['target'] = np.random.randint(0, 2, n_samples)

        return pd.DataFrame(data), sensitive_names

    def collect_synthetic(self, n: int = 400) -> int:
        """Gera datasets sintéticos."""
        print(f"\nGerando {n} datasets sintéticos...")
        count = 0

        for i in tqdm(range(n), desc="Synthetic"):
            try:
                df, sensitive_cols = self.generate_synthetic_dataset(i)

                filename = f"synthetic_{i:04d}.csv"
                output_file = self.output_dir / filename
                df.to_csv(output_file, index=False)

                self.metadata.append({
                    'dataset_id': f'synthetic_{i:04d}',
                    'source': 'synthetic',
                    'n_samples': len(df),
                    'n_features': len(df.columns),
                    'target': 'target',
                    'sensitive_attributes': ','.join(sensitive_cols),
                    'n_sensitive': len(sensitive_cols),
                    'file': filename
                })
                count += 1

            except Exception as e:
                print(f"Erro ao gerar synthetic_{i:04d}: {e}")

        return count

    def collect_uci_adult(self) -> int:
        """Coleta Adult dataset do UCI."""
        try:
            url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
            columns = ['age', 'workclass', 'fnlwgt', 'education', 'education_num',
                      'marital_status', 'occupation', 'relationship', 'race', 'sex',
                      'capital_gain', 'capital_loss', 'hours_per_week', 'native_country',
                      'income']

            df = pd.read_csv(url, names=columns, skipinitialspace=True)

            output_file = self.output_dir / "uci_adult.csv"
            df.to_csv(output_file, index=False)

            self.metadata.append({
                'dataset_id': 'uci_adult',
                'source': 'uci',
                'n_samples': len(df),
                'n_features': len(df.columns),
                'target': 'income',
                'sensitive_attributes': 'age,race,sex,marital_status,native_country',
                'n_sensitive': 5,
                'file': 'uci_adult.csv'
            })

            print("  ✅ Adult dataset coletado")
            return 1

        except Exception as e:
            print(f"  ❌ Erro ao coletar Adult: {e}")
            return 0

    def collect_uci_german(self) -> int:
        """Coleta German Credit dataset."""
        try:
            url = "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data"

            # Colunas do German Credit
            columns = [f'attr_{i}' for i in range(20)] + ['credit']
            df = pd.read_csv(url, sep=' ', names=columns, header=None)

            # Renomear algumas colunas conhecidas
            df.rename(columns={
                'attr_8': 'age',
                'attr_9': 'sex_marital',
                'attr_12': 'residence_since',
                'attr_19': 'foreign_worker'
            }, inplace=True)

            output_file = self.output_dir / "uci_german_credit.csv"
            df.to_csv(output_file, index=False)

            self.metadata.append({
                'dataset_id': 'uci_german_credit',
                'source': 'uci',
                'n_samples': len(df),
                'n_features': len(df.columns),
                'target': 'credit',
                'sensitive_attributes': 'age,sex_marital,foreign_worker',
                'n_sensitive': 3,
                'file': 'uci_german_credit.csv'
            })

            print("  ✅ German Credit coletado")
            return 1

        except Exception as e:
            print(f"  ❌ Erro ao coletar German: {e}")
            return 0

    def save_metadata(self):
        """Salva metadata consolidado."""
        df = pd.DataFrame(self.metadata)
        metadata_file = self.output_dir.parent / 'datasets_metadata.csv'
        df.to_csv(metadata_file, index=False)

        print(f"\n✅ Metadata salvo: {metadata_file}")
        print(f"   Total de datasets: {len(df)}")
        print(f"   Sintéticos: {len(df[df['source'] == 'synthetic'])}")
        print(f"   UCI: {len(df[df['source'] == 'uci'])}")


def main():
    parser = argparse.ArgumentParser(description='Coletar datasets para experimentos')
    parser.add_argument('--target', type=int, default=500, help='Número alvo de datasets')
    parser.add_argument('--output', type=str, default='../data/datasets', help='Diretório de saída')
    parser.add_argument('--uci-only', action='store_true', help='Coletar apenas UCI datasets')
    args = parser.parse_args()

    collector = DatasetCollector(args.output)

    print("=" * 60)
    print("  DeepBridge Fairness - Coleta de Datasets")
    print("=" * 60)

    total = 0

    # Coletar UCI datasets
    print("\n[1/2] Coletando datasets UCI...")
    total += collector.collect_uci_adult()
    total += collector.collect_uci_german()

    if not args.uci_only:
        # Gerar sintéticos
        n_synthetic = args.target - total
        print(f"\n[2/2] Gerando {n_synthetic} datasets sintéticos...")
        total += collector.collect_synthetic(n_synthetic)

    # Salvar metadata
    collector.save_metadata()

    print("\n" + "=" * 60)
    print(f"  ✅ Coleta concluída: {total} datasets")
    print("=" * 60)


if __name__ == '__main__':
    main()
