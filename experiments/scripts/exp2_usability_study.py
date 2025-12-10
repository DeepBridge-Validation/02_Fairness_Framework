#!/usr/bin/env python3
"""
Experimento 2: Estudo de Usabilidade (SUS + NASA-TLX)

Avalia a usabilidade do DeepBridge com usuários reais.

Métricas:
- SUS (System Usability Scale): Meta ≥ 75 (paper claim: 85.2)
- NASA-TLX (Task Load Index): Meta < 40 (baixa carga cognitiva)
- Taxa de sucesso: Meta ≥ 95%
- Tempo de conclusão de tarefas

Protocolo:
1. Briefing (5 min)
2. 5 tarefas padronizadas (30 min)
3. Questionários SUS + NASA-TLX (10 min)
4. Entrevista semi-estruturada (15 min)

Uso:
    # Executar sessão individual
    python exp2_usability_study.py --participant-id P01 --mode interactive

    # Analisar resultados agregados
    python exp2_usability_study.py --analyze --input ../results/exp2_usability

    # Gerar relatório final
    python exp2_usability_study.py --report --input ../results/exp2_usability
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
import json
import argparse
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


class SUSQuestionnaire:
    """System Usability Scale (SUS) - 10 questões."""

    QUESTIONS = [
        "Eu acho que gostaria de usar esse sistema frequentemente",
        "Eu achei o sistema desnecessariamente complexo",
        "Eu achei o sistema fácil de usar",
        "Eu acho que precisaria de ajuda de uma pessoa com conhecimentos técnicos para usar esse sistema",
        "Eu achei que as várias funções do sistema estavam bem integradas",
        "Eu achei que o sistema apresenta muita inconsistência",
        "Eu imagino que as pessoas aprenderão como usar esse sistema rapidamente",
        "Eu achei o sistema atrapalhado de usar",
        "Eu me senti confiante ao usar o sistema",
        "Eu precisei aprender várias coisas novas antes de conseguir usar o sistema"
    ]

    # Questões ímpares: contribuição positiva (1-5)
    # Questões pares: contribuição negativa (5-1)

    def __init__(self):
        self.responses = {}

    def ask_questions(self, participant_id: str) -> Dict:
        """Aplica questionário SUS."""
        print(f"\n{'='*80}")
        print("QUESTIONÁRIO SUS (System Usability Scale)")
        print(f"{'='*80}\n")
        print("Para cada afirmação, indique seu nível de concordância:")
        print("1 = Discordo totalmente")
        print("2 = Discordo")
        print("3 = Neutro")
        print("4 = Concordo")
        print("5 = Concordo totalmente\n")

        responses = []

        for i, question in enumerate(self.QUESTIONS, 1):
            while True:
                try:
                    print(f"Q{i}. {question}")
                    answer = int(input("    Resposta (1-5): "))
                    if 1 <= answer <= 5:
                        responses.append(answer)
                        break
                    else:
                        print("    ⚠️  Por favor, insira um número entre 1 e 5")
                except ValueError:
                    print("    ⚠️  Por favor, insira um número válido")

        # Calcular SUS score
        sus_score = self.calculate_sus_score(responses)

        return {
            'participant_id': participant_id,
            'responses': responses,
            'sus_score': sus_score,
            'timestamp': datetime.now().isoformat()
        }

    def calculate_sus_score(self, responses: List[int]) -> float:
        """
        Calcula SUS score (0-100).

        Fórmula:
        - Para questões ímpares (1,3,5,7,9): contribuição = resposta - 1
        - Para questões pares (2,4,6,8,10): contribuição = 5 - resposta
        - Score = soma das contribuições × 2.5
        """
        score = 0
        for i, response in enumerate(responses, 1):
            if i % 2 == 1:  # Ímpar
                score += (response - 1)
            else:  # Par
                score += (5 - response)

        return score * 2.5


class NASATLXQuestionnaire:
    """NASA Task Load Index (NASA-TLX) - 6 dimensões."""

    DIMENSIONS = [
        ("Mental Demand", "Quanto esforço mental foi necessário?"),
        ("Physical Demand", "Quanto esforço físico foi necessário?"),
        ("Temporal Demand", "Quão apressado foi o ritmo da tarefa?"),
        ("Performance", "Quão bem-sucedido você foi?"),
        ("Effort", "Quanto você teve que trabalhar?"),
        ("Frustration", "Quão frustrado você se sentiu?")
    ]

    def ask_questions(self, participant_id: str) -> Dict:
        """Aplica questionário NASA-TLX."""
        print(f"\n{'='*80}")
        print("QUESTIONÁRIO NASA-TLX (Task Load Index)")
        print(f"{'='*80}\n")
        print("Para cada dimensão, avalie de 0 a 100:\n")

        responses = {}

        for dimension, description in self.DIMENSIONS:
            while True:
                try:
                    print(f"{dimension}: {description}")
                    answer = int(input("    Avaliação (0-100): "))
                    if 0 <= answer <= 100:
                        responses[dimension.lower().replace(' ', '_')] = answer
                        break
                    else:
                        print("    ⚠️  Por favor, insira um número entre 0 e 100")
                except ValueError:
                    print("    ⚠️  Por favor, insira um número válido")

        # Calcular score agregado (média)
        tlx_score = np.mean(list(responses.values()))

        return {
            'participant_id': participant_id,
            'responses': responses,
            'tlx_score': tlx_score,
            'timestamp': datetime.now().isoformat()
        }


class UsabilityTask:
    """Tarefa padronizada do estudo de usabilidade."""

    def __init__(self, task_id: int, description: str, expected_duration: int):
        self.task_id = task_id
        self.description = description
        self.expected_duration = expected_duration  # segundos

    def execute(self, participant_id: str) -> Dict:
        """Executa tarefa e coleta métricas."""
        print(f"\n{'='*80}")
        print(f"TAREFA {self.task_id}")
        print(f"{'='*80}")
        print(f"\n{self.description}\n")
        print(f"Tempo esperado: ~{self.expected_duration}s")
        print("\nPressione ENTER quando o participante começar a tarefa...")
        input()

        start_time = datetime.now()
        print("⏱️  Cronômetro iniciado!")

        print("\nPressione ENTER quando o participante completar a tarefa...")
        input()

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print(f"✅ Tarefa concluída em {duration:.1f}s")

        # Perguntar sucesso
        while True:
            success = input("O participante completou a tarefa com sucesso? (s/n): ").lower()
            if success in ['s', 'n']:
                success = (success == 's')
                break

        # Dificuldade percebida
        while True:
            try:
                difficulty = int(input("Dificuldade percebida pelo participante (1=muito fácil, 5=muito difícil): "))
                if 1 <= difficulty <= 5:
                    break
            except ValueError:
                pass

        # Notas do observador
        notes = input("Notas do observador (opcional): ")

        return {
            'task_id': self.task_id,
            'participant_id': participant_id,
            'duration_seconds': duration,
            'expected_duration': self.expected_duration,
            'success': success,
            'difficulty': difficulty,
            'notes': notes,
            'timestamp': start_time.isoformat()
        }


class UsabilityStudy:
    """Estudo de usabilidade completo."""

    TASKS = [
        UsabilityTask(1, "Carregar um dataset CSV e identificar atributos sensíveis automaticamente", 60),
        UsabilityTask(2, "Executar análise de fairness com 3 métricas diferentes", 90),
        UsabilityTask(3, "Verificar conformidade EEOC/ECOA e interpretar resultados", 120),
        UsabilityTask(4, "Ajustar threshold de decisão e observar impacto nas métricas", 90),
        UsabilityTask(5, "Exportar relatório completo de fairness", 60)
    ]

    def __init__(self, output_dir: str = "../results/exp2_usability"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_session(self, participant_id: str):
        """Executa sessão completa de usabilidade."""
        print(f"\n{'='*80}")
        print(f"SESSÃO DE USABILIDADE - Participante {participant_id}")
        print(f"{'='*80}\n")

        session_dir = self.output_dir / participant_id
        session_dir.mkdir(parents=True, exist_ok=True)

        # 1. Coleta de informações demográficas
        demographics = self.collect_demographics(participant_id)

        # 2. Briefing
        print("\n📋 BRIEFING")
        print("Explique ao participante:")
        print("  - Objetivo do DeepBridge")
        print("  - Protocolo da sessão (sem interrupções)")
        print("  - Think-aloud (verbalizar pensamentos)")
        input("\nPressione ENTER quando concluir o briefing...")

        # 3. Executar tarefas
        task_results = []
        for task in self.TASKS:
            result = task.execute(participant_id)
            task_results.append(result)

            # Salvar resultado da tarefa
            task_file = session_dir / f"task_{task.task_id}.json"
            with open(task_file, 'w') as f:
                json.dump(result, f, indent=2)

        # 4. Questionários
        print("\n" + "="*80)
        print("QUESTIONÁRIOS")
        print("="*80)

        sus = SUSQuestionnaire()
        sus_result = sus.ask_questions(participant_id)

        tlx = NASATLXQuestionnaire()
        tlx_result = tlx.ask_questions(participant_id)

        # 5. Entrevista semi-estruturada
        interview = self.conduct_interview(participant_id)

        # 6. Consolidar resultados
        session_data = {
            'participant_id': participant_id,
            'demographics': demographics,
            'tasks': task_results,
            'sus': sus_result,
            'nasa_tlx': tlx_result,
            'interview': interview,
            'session_date': datetime.now().isoformat()
        }

        # Salvar sessão completa
        session_file = session_dir / "session_complete.json"
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)

        print(f"\n✅ Sessão salva em: {session_file}")

        # Mostrar resumo
        self.print_session_summary(session_data)

    def collect_demographics(self, participant_id: str) -> Dict:
        """Coleta informações demográficas."""
        print("\n📋 INFORMAÇÕES DEMOGRÁFICAS\n")

        demographics = {'participant_id': participant_id}

        demographics['age'] = input("Idade: ")
        demographics['gender'] = input("Gênero: ")
        demographics['education'] = input("Nível de educação: ")
        demographics['occupation'] = input("Ocupação: ")
        demographics['experience_ml'] = input("Anos de experiência com ML: ")
        demographics['experience_fairness'] = input("Experiência prévia com fairness em ML (sim/não): ")
        demographics['tools_used'] = input("Ferramentas de fairness já utilizadas (separadas por vírgula): ")

        return demographics

    def conduct_interview(self, participant_id: str) -> Dict:
        """Conduz entrevista semi-estruturada."""
        print(f"\n{'='*80}")
        print("ENTREVISTA SEMI-ESTRUTURADA")
        print(f"{'='*80}\n")

        questions = [
            "O que você achou da experiência geral de usar o DeepBridge?",
            "Quais foram os aspectos mais positivos?",
            "Quais foram as maiores dificuldades?",
            "Você usaria o DeepBridge em seu trabalho? Por quê?",
            "Como o DeepBridge se compara com outras ferramentas que você já usou?",
            "Que melhorias você sugeriria?"
        ]

        responses = {}
        print("(Gravar áudio ou tomar notas detalhadas)\n")

        for i, question in enumerate(questions, 1):
            print(f"Q{i}. {question}")
            response = input("Resumo da resposta: ")
            responses[f"q{i}"] = response

        return {
            'participant_id': participant_id,
            'questions': questions,
            'responses': responses,
            'timestamp': datetime.now().isoformat()
        }

    def print_session_summary(self, session_data: Dict):
        """Imprime resumo da sessão."""
        print(f"\n{'='*80}")
        print("RESUMO DA SESSÃO")
        print(f"{'='*80}\n")

        print(f"Participante: {session_data['participant_id']}")
        print(f"Data: {session_data['session_date']}\n")

        # Tarefas
        print("📊 TAREFAS:")
        success_count = sum(1 for t in session_data['tasks'] if t['success'])
        total_tasks = len(session_data['tasks'])
        print(f"  Taxa de sucesso: {success_count}/{total_tasks} ({100*success_count/total_tasks:.1f}%)")

        total_time = sum(t['duration_seconds'] for t in session_data['tasks'])
        print(f"  Tempo total: {total_time:.1f}s ({total_time/60:.1f} min)\n")

        # SUS
        sus_score = session_data['sus']['sus_score']
        print(f"📈 SUS SCORE: {sus_score:.1f}/100")
        if sus_score >= 85:
            interpretation = "EXCELENTE"
        elif sus_score >= 75:
            interpretation = "BOM"
        elif sus_score >= 60:
            interpretation = "ACEITÁVEL"
        else:
            interpretation = "BAIXO"
        print(f"  Interpretação: {interpretation}\n")

        # NASA-TLX
        tlx_score = session_data['nasa_tlx']['tlx_score']
        print(f"🧠 NASA-TLX: {tlx_score:.1f}/100")
        if tlx_score < 40:
            interpretation = "BAIXA CARGA (excelente)"
        elif tlx_score < 60:
            interpretation = "CARGA MODERADA"
        else:
            interpretation = "ALTA CARGA (preocupante)"
        print(f"  Interpretação: {interpretation}\n")


class UsabilityAnalyzer:
    """Análise agregada de múltiplas sessões."""

    def __init__(self, results_dir: str):
        self.results_dir = Path(results_dir)
        self.sessions = []

    def load_sessions(self):
        """Carrega todas as sessões."""
        for session_dir in self.results_dir.glob("P*"):
            session_file = session_dir / "session_complete.json"
            if session_file.exists():
                with open(session_file, 'r') as f:
                    self.sessions.append(json.load(f))

        print(f"✅ Carregadas {len(self.sessions)} sessões")

    def analyze(self):
        """Análise estatística agregada."""
        if len(self.sessions) == 0:
            print("❌ Nenhuma sessão encontrada")
            return

        print(f"\n{'='*80}")
        print(f"ANÁLISE AGREGADA (N={len(self.sessions)})")
        print(f"{'='*80}\n")

        # SUS Scores
        sus_scores = [s['sus']['sus_score'] for s in self.sessions]
        sus_mean = np.mean(sus_scores)
        sus_std = np.std(sus_scores, ddof=1)
        sus_ci = stats.t.interval(0.95, len(sus_scores)-1,
                                   loc=sus_mean,
                                   scale=stats.sem(sus_scores))

        print("📊 SUS SCORES:")
        print(f"  Mean: {sus_mean:.2f} ± {sus_std:.2f}")
        print(f"  95% CI: [{sus_ci[0]:.2f}, {sus_ci[1]:.2f}]")
        print(f"  Range: [{min(sus_scores):.1f}, {max(sus_scores):.1f}]")

        # Teste t (vs baseline 68)
        t_stat, p_value = stats.ttest_1samp(sus_scores, 68)
        print(f"  t-test vs 68 (average): t={t_stat:.3f}, p={p_value:.4f}")

        # Validar claim do paper (85.2)
        claim_sus = 85.2
        if sus_mean >= claim_sus - 5:
            print(f"  ✅ VALIDADO: SUS ≥ {claim_sus-5:.1f} (claim: {claim_sus})")
        else:
            print(f"  ❌ ABAIXO DO CLAIM: {sus_mean:.1f} < {claim_sus}")

        # NASA-TLX
        tlx_scores = [s['nasa_tlx']['tlx_score'] for s in self.sessions]
        tlx_mean = np.mean(tlx_scores)
        tlx_std = np.std(tlx_scores, ddof=1)

        print(f"\n🧠 NASA-TLX:")
        print(f"  Mean: {tlx_mean:.2f} ± {tlx_std:.2f}")
        if tlx_mean < 40:
            print(f"  ✅ VALIDADO: Baixa carga cognitiva (< 40)")
        else:
            print(f"  ⚠️  Carga cognitiva acima do ideal: {tlx_mean:.1f}")

        # Taxa de sucesso
        all_tasks = []
        for session in self.sessions:
            all_tasks.extend(session['tasks'])

        success_rate = sum(1 for t in all_tasks if t['success']) / len(all_tasks)
        print(f"\n✅ TAXA DE SUCESSO: {100*success_rate:.1f}%")

        claim_success = 0.95
        if success_rate >= claim_success:
            print(f"  ✅ VALIDADO: Taxa ≥ {100*claim_success:.0f}% (claim: {100*claim_success:.0f}%)")
        else:
            print(f"  ❌ ABAIXO DO CLAIM: {100*success_rate:.1f}% < {100*claim_success:.0f}%")

        # Salvar análise
        analysis = {
            'n_participants': len(self.sessions),
            'sus': {
                'mean': float(sus_mean),
                'std': float(sus_std),
                'ci_95': [float(sus_ci[0]), float(sus_ci[1])],
                'min': float(min(sus_scores)),
                'max': float(max(sus_scores)),
                't_statistic': float(t_stat),
                'p_value': float(p_value)
            },
            'nasa_tlx': {
                'mean': float(tlx_mean),
                'std': float(tlx_std)
            },
            'success_rate': float(success_rate),
            'validation': {
                'sus_validated': sus_mean >= claim_sus - 5,
                'tlx_validated': tlx_mean < 40,
                'success_validated': success_rate >= claim_success
            }
        }

        output_file = self.results_dir / "aggregate_analysis.json"
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)

        print(f"\n💾 Análise salva em: {output_file}")

        # Gerar figuras
        self.generate_figures(sus_scores, tlx_scores)

    def generate_figures(self, sus_scores: List[float], tlx_scores: List[float]):
        """Gera figuras."""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # SUS distribution
        axes[0].hist(sus_scores, bins=10, alpha=0.7, edgecolor='black')
        axes[0].axvline(np.mean(sus_scores), color='red', linestyle='--',
                       label=f'Mean: {np.mean(sus_scores):.1f}')
        axes[0].axvline(85.2, color='green', linestyle='--',
                       label='Claim: 85.2')
        axes[0].set_xlabel('SUS Score')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title('SUS Score Distribution')
        axes[0].legend()
        axes[0].grid(alpha=0.3)

        # TLX distribution
        axes[1].hist(tlx_scores, bins=10, alpha=0.7, edgecolor='black', color='orange')
        axes[1].axvline(np.mean(tlx_scores), color='red', linestyle='--',
                       label=f'Mean: {np.mean(tlx_scores):.1f}')
        axes[1].axvline(40, color='green', linestyle='--',
                       label='Target: 40')
        axes[1].set_xlabel('NASA-TLX Score')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title('NASA-TLX Distribution')
        axes[1].legend()
        axes[1].grid(alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.results_dir / 'usability_scores.png', dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✅ Figuras salvas em: {self.results_dir}")


def main():
    parser = argparse.ArgumentParser(description='Exp2: Usability Study')
    parser.add_argument('--participant-id', type=str,
                       help='ID do participante (ex: P01, P02, ...)')
    parser.add_argument('--mode', type=str, choices=['interactive', 'batch'],
                       default='interactive',
                       help='Modo de execução')
    parser.add_argument('--analyze', action='store_true',
                       help='Analisar resultados agregados')
    parser.add_argument('--input', type=str, default='../results/exp2_usability',
                       help='Diretório com resultados')

    args = parser.parse_args()

    if args.analyze:
        analyzer = UsabilityAnalyzer(args.input)
        analyzer.load_sessions()
        analyzer.analyze()
    else:
        if not args.participant_id:
            print("❌ Especifique --participant-id (ex: P01)")
            return

        study = UsabilityStudy(output_dir=args.input)
        study.run_session(args.participant_id)


if __name__ == '__main__':
    main()
