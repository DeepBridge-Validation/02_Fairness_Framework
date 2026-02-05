#!/usr/bin/env python3
"""
Cria batches para anotação manual incremental.

Divide 500 datasets em batches menores para facilitar anotação.
Permite anotar gradualmente ao longo de vários dias/semanas.

Uso:
    python 04_create_annotation_batches.py --batch-size 50 --n-batches 10
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def create_stratified_batches(datasets_dir: Path, metadata_file: Path,
                              batch_size: int, n_batches: int):
    """Cria batches estratificados para anotação."""

    # Carregar metadata
    if metadata_file.exists():
        df_meta = pd.read_csv(metadata_file)
    else:
        # Criar metadata se não existir
        datasets = sorted(datasets_dir.glob('*.csv'))
        df_meta = pd.DataFrame({
            'dataset_id': [d.stem for d in datasets],
            'file': [d.name for d in datasets],
            'source': ['synthetic'] * len(datasets)
        })

    # Estratificar por fonte (se houver múltiplas fontes)
    if 'source' in df_meta.columns:
        # Amostrar proporcionalmente de cada fonte
        batches = []
        for i in range(n_batches):
            batch = []
            for source in df_meta['source'].unique():
                source_data = df_meta[df_meta['source'] == source]
                n_sample = min(batch_size // len(df_meta['source'].unique()), len(source_data))

                # Amostrar sem reposição
                sample = source_data.sample(n=n_sample, random_state=42+i)
                batch.extend(sample['file'].tolist())

            batches.append(batch)
    else:
        # Dividir aleatoriamente
        shuffled = df_meta.sample(frac=1, random_state=42)
        batches = [
            shuffled.iloc[i*batch_size:(i+1)*batch_size]['file'].tolist()
            for i in range(n_batches)
        ]

    return batches


def create_annotation_plan(batches: list, output_dir: Path):
    """Cria plano de anotação."""

    plan = {
        'total_datasets': sum(len(b) for b in batches),
        'n_batches': len(batches),
        'batch_size': len(batches[0]) if batches else 0,
        'estimated_time_per_batch': '3-4 hours',
        'total_estimated_time': f'{len(batches) * 3.5:.0f} hours',
        'batches': []
    }

    for i, batch in enumerate(batches, 1):
        batch_info = {
            'batch_id': i,
            'n_datasets': len(batch),
            'files': batch,
            'status': 'pending',
            'annotator_1_completed': False,
            'annotator_2_completed': False
        }
        plan['batches'].append(batch_info)

        # Criar arquivo de batch
        batch_file = output_dir / f'batch_{i:02d}.json'
        with open(batch_file, 'w') as f:
            json.dump(batch_info, f, indent=2)

    # Salvar plano geral
    plan_file = output_dir / 'annotation_plan.json'
    with open(plan_file, 'w') as f:
        json.dump(plan, f, indent=2)

    return plan


def generate_annotation_schedule(plan: dict, output_file: Path):
    """Gera cronograma de anotação."""

    schedule = []
    schedule.append("# CRONOGRAMA DE ANOTAÇÃO MANUAL\n")
    schedule.append(f"Total de datasets: {plan['total_datasets']}")
    schedule.append(f"Dividido em: {plan['n_batches']} batches de ~{plan['batch_size']} datasets")
    schedule.append(f"Tempo estimado total: {plan['total_estimated_time']}\n")
    schedule.append("## PLANO DE EXECUÇÃO\n")
    schedule.append("**Semana 1-2**: Batches 1-4 (Anotador 1)")
    schedule.append("**Semana 3-4**: Batches 5-8 (Anotador 1)")
    schedule.append("**Semana 5-6**: Batches 9-10 (Anotador 1)")
    schedule.append("**Semana 7-8**: Batches 1-4 (Anotador 2)")
    schedule.append("**Semana 9-10**: Batches 5-8 (Anotador 2)")
    schedule.append("**Semana 11-12**: Batches 9-10 (Anotador 2)")
    schedule.append("**Semana 13**: Calcular agreement e resolver discordâncias\n")

    schedule.append("## COMANDOS POR BATCH\n")
    for i in range(1, plan['n_batches'] + 1):
        schedule.append(f"\n### Batch {i}")
        schedule.append(f"```bash")
        schedule.append(f"# Anotador 1")
        schedule.append(f"python 02_annotate_ground_truth.py --annotator 1 --batch {i}")
        schedule.append(f"")
        schedule.append(f"# Anotador 2 (depois)")
        schedule.append(f"python 02_annotate_ground_truth.py --annotator 2 --batch {i}")
        schedule.append(f"```")

    with open(output_file, 'w') as f:
        f.write('\n'.join(schedule))


def main():
    parser = argparse.ArgumentParser(description='Criar batches de anotação')
    parser.add_argument('--batch-size', type=int, default=50,
                       help='Tamanho de cada batch')
    parser.add_argument('--n-batches', type=int, default=10,
                       help='Número de batches')
    parser.add_argument('--datasets-dir', type=str, default='../data/datasets',
                       help='Diretório com datasets')
    parser.add_argument('--output-dir', type=str, default='../data/annotation_batches',
                       help='Diretório de saída')

    args = parser.parse_args()

    datasets_dir = Path(args.datasets_dir)
    metadata_file = datasets_dir.parent / 'datasets_metadata.csv'
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║              CRIAR BATCHES DE ANOTAÇÃO MANUAL                     ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()

    # Criar batches
    print(f"Criando {args.n_batches} batches de ~{args.batch_size} datasets...")
    batches = create_stratified_batches(
        datasets_dir, metadata_file,
        args.batch_size, args.n_batches
    )

    print(f"✅ {len(batches)} batches criados")

    # Criar plano
    print("\nCriando plano de anotação...")
    plan = create_annotation_plan(batches, output_dir)

    print(f"✅ Plano salvo em: {output_dir}/annotation_plan.json")

    # Gerar cronograma
    schedule_file = output_dir / 'ANNOTATION_SCHEDULE.md'
    generate_annotation_schedule(plan, schedule_file)

    print(f"✅ Cronograma salvo em: {schedule_file}")

    # Resumo
    print("\n" + "="*70)
    print("RESUMO DO PLANO")
    print("="*70)
    print(f"Total de datasets: {plan['total_datasets']}")
    print(f"Batches: {plan['n_batches']} × {plan['batch_size']} datasets")
    print(f"Tempo estimado: {plan['total_estimated_time']}")
    print()
    print("PRÓXIMOS PASSOS:")
    print("  1. Revisar o cronograma: cat ../data/annotation_batches/ANNOTATION_SCHEDULE.md")
    print("  2. Iniciar Batch 1: python 02_annotate_ground_truth.py --annotator 1 --batch 1")
    print("  3. Acompanhar progresso: python check_annotation_progress.py")
    print()


if __name__ == '__main__':
    main()
