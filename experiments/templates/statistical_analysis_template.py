#!/usr/bin/env python3
"""
Template de Análise Estatística para Experimentos DeepBridge Fairness

Inclui:
- Testes de significância (t-test, Mann-Whitney, McNemar, Binomial)
- Intervalos de confiança (bootstrap, paramétrico)
- Power analysis
- Effect sizes (Cohen's d, Cramér's V)
- Correção para múltiplas comparações (Bonferroni, Holm)
"""

from typing import Dict, Tuple

import numpy as np
import pandas as pd
import pingouin as pg
from scipy import stats
from statsmodels.stats.power import TTestIndPower, TTestPower
from statsmodels.stats.proportion import proportion_confint


class StatisticalAnalysis:
    """Análise estatística rigorosa para papers TIER 1."""

    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha

    # ==================== TESTES DE HIPÓTESE ====================

    def paired_ttest(self, group1: np.ndarray, group2: np.ndarray,
                     alternative: str = 'two-sided') -> Dict:
        """
        Paired t-test (ex: DeepBridge vs. Manual no mesmo dataset).

        H0: μ_diff = 0
        H1: μ_diff != 0 (ou > 0, < 0)
        """
        # Teste
        stat, pvalue = stats.ttest_rel(group1, group2, alternative=alternative)

        # Effect size (Cohen's d pareado)
        diff = group1 - group2
        d = np.mean(diff) / np.std(diff, ddof=1)

        # Intervalo de confiança
        ci = stats.t.interval(
            1 - self.alpha,
            df=len(diff) - 1,
            loc=np.mean(diff),
            scale=stats.sem(diff)
        )

        return {
            'test': 'Paired t-test',
            't_statistic': stat,
            'p_value': pvalue,
            'df': len(diff) - 1,
            'mean_diff': np.mean(diff),
            'std_diff': np.std(diff, ddof=1),
            'cohens_d': d,
            'ci_95': ci,
            'significant': pvalue < self.alpha,
            'interpretation': self._interpret_cohens_d(abs(d))
        }

    def independent_ttest(self, group1: np.ndarray, group2: np.ndarray,
                         equal_var: bool = True) -> Dict:
        """
        Independent t-test (ex: Grupo A vs. Grupo B diferentes).
        """
        # Teste de normalidade (Shapiro-Wilk)
        _, p_norm1 = stats.shapiro(group1)
        _, p_norm2 = stats.shapiro(group2)

        # Se não normal, avisar para usar Mann-Whitney
        if p_norm1 < 0.05 or p_norm2 < 0.05:
            warning = "⚠️ Dados não-normais. Considere Mann-Whitney U test."
        else:
            warning = None

        # Teste de Levene (homogeneidade de variâncias)
        _, p_levene = stats.levene(group1, group2)
        equal_var = p_levene > 0.05

        # t-test
        stat, pvalue = stats.ttest_ind(group1, group2, equal_var=equal_var)

        # Cohen's d
        pooled_std = np.sqrt(
            ((len(group1) - 1) * np.var(group1, ddof=1) +
             (len(group2) - 1) * np.var(group2, ddof=1)) /
            (len(group1) + len(group2) - 2)
        )
        d = (np.mean(group1) - np.mean(group2)) / pooled_std

        return {
            'test': 'Independent t-test' if equal_var else 'Welch t-test',
            't_statistic': stat,
            'p_value': pvalue,
            'df': len(group1) + len(group2) - 2,
            'mean_group1': np.mean(group1),
            'mean_group2': np.mean(group2),
            'cohens_d': abs(d),
            'significant': pvalue < self.alpha,
            'warning': warning
        }

    def mann_whitney_u(self, group1: np.ndarray, group2: np.ndarray,
                       alternative: str = 'two-sided') -> Dict:
        """
        Mann-Whitney U test (não-paramétrico).
        Usar quando dados não são normais.
        """
        stat, pvalue = stats.mannwhitneyu(
            group1, group2,
            alternative=alternative
        )

        # Rank-biserial correlation (effect size)
        r = 1 - (2 * stat) / (len(group1) * len(group2))

        return {
            'test': 'Mann-Whitney U',
            'u_statistic': stat,
            'p_value': pvalue,
            'rank_biserial_r': abs(r),
            'median_group1': np.median(group1),
            'median_group2': np.median(group2),
            'significant': pvalue < self.alpha
        }

    def mcnemar_test(self, table: np.ndarray) -> Dict:
        """
        McNemar test (para dados pareados binários).

        table: 2x2 confusion matrix
               [[a, b],
                [c, d]]

        Exemplo: Comparar DeepBridge vs. Ground Truth
        - a: ambos acertam
        - b: DeepBridge acerta, ground truth erra
        - c: DeepBridge erra, ground truth acerta
        - d: ambos erram
        """
        from statsmodels.stats.contingency_tables import mcnemar

        result = mcnemar(table, exact=False, correction=True)

        return {
            'test': 'McNemar',
            'statistic': result.statistic,
            'p_value': result.pvalue,
            'significant': result.pvalue < self.alpha
        }

    def binomial_test(self, successes: int, trials: int,
                     p_expected: float = 0.5) -> Dict:
        """
        Exact binomial test.

        Exemplo: Testar se precisão EEOC = 100%
        H0: p = p_expected
        H1: p != p_expected
        """
        pvalue = stats.binom_test(successes, trials, p_expected,
                                   alternative='two-sided')

        # Intervalo de confiança (método Wilson)
        ci_low, ci_high = proportion_confint(
            successes, trials,
            alpha=self.alpha,
            method='wilson'
        )

        return {
            'test': 'Exact Binomial',
            'successes': successes,
            'trials': trials,
            'observed_proportion': successes / trials,
            'expected_proportion': p_expected,
            'p_value': pvalue,
            'ci_95': (ci_low, ci_high),
            'significant': pvalue < self.alpha
        }

    # ==================== INTERVALOS DE CONFIANÇA ====================

    def bootstrap_ci(self, data: np.ndarray, statistic: callable,
                    n_bootstrap: int = 10000, ci: float = 0.95) -> Tuple:
        """
        Bootstrap confidence interval (não-paramétrico).

        Args:
            data: Dados originais
            statistic: Função para calcular estatística (ex: np.mean, np.median)
            n_bootstrap: Número de reamostragens
            ci: Nível de confiança

        Returns:
            (lower, upper, bootstrap_distribution)
        """
        bootstrap_stats = []
        n = len(data)

        for _ in range(n_bootstrap):
            sample = np.random.choice(data, size=n, replace=True)
            bootstrap_stats.append(statistic(sample))

        bootstrap_stats = np.array(bootstrap_stats)

        alpha = 1 - ci
        lower = np.percentile(bootstrap_stats, 100 * alpha / 2)
        upper = np.percentile(bootstrap_stats, 100 * (1 - alpha / 2))

        return lower, upper, bootstrap_stats

    def parametric_ci(self, data: np.ndarray, ci: float = 0.95) -> Tuple:
        """
        Intervalo de confiança paramétrico (assume normalidade).
        """
        mean = np.mean(data)
        sem = stats.sem(data)
        ci_range = stats.t.interval(
            ci,
            df=len(data) - 1,
            loc=mean,
            scale=sem
        )
        return ci_range

    # ==================== POWER ANALYSIS ====================

    def power_analysis_ttest(self, effect_size: float, n: int = None,
                            power: float = None, alpha: float = None) -> Dict:
        """
        Power analysis para t-test.

        Resolver para qualquer parâmetro desconhecido:
        - Se n=None: calcular tamanho de amostra necessário
        - Se power=None: calcular poder estatístico
        - Se effect_size=None: calcular effect size detectável
        """
        if alpha is None:
            alpha = self.alpha

        analysis = TTestIndPower()

        if n is None:
            # Calcular n necessário
            n_required = analysis.solve_power(
                effect_size=effect_size,
                power=power,
                alpha=alpha,
                ratio=1.0,
                alternative='two-sided'
            )
            return {
                'effect_size': effect_size,
                'power': power,
                'alpha': alpha,
                'n_required': int(np.ceil(n_required))
            }

        elif power is None:
            # Calcular poder estatístico
            power_achieved = analysis.solve_power(
                effect_size=effect_size,
                nobs1=n,
                alpha=alpha,
                ratio=1.0,
                alternative='two-sided'
            )
            return {
                'effect_size': effect_size,
                'n': n,
                'alpha': alpha,
                'power': power_achieved
            }

    # ==================== CORREÇÃO PARA MÚLTIPLAS COMPARAÇÕES ====================

    def bonferroni_correction(self, pvalues: list) -> Dict:
        """
        Correção de Bonferroni (conservadora).

        alpha_corrected = alpha / n_tests
        """
        n_tests = len(pvalues)
        alpha_corrected = self.alpha / n_tests

        significant = [p < alpha_corrected for p in pvalues]

        return {
            'method': 'Bonferroni',
            'n_tests': n_tests,
            'alpha_original': self.alpha,
            'alpha_corrected': alpha_corrected,
            'significant': significant,
            'n_significant': sum(significant)
        }

    def holm_correction(self, pvalues: list) -> Dict:
        """
        Correção de Holm (menos conservadora que Bonferroni).
        """
        from statsmodels.stats.multitest import multipletests

        rejected, pvals_corrected, _, _ = multipletests(
            pvalues,
            alpha=self.alpha,
            method='holm'
        )

        return {
            'method': 'Holm',
            'n_tests': len(pvalues),
            'alpha': self.alpha,
            'pvalues_corrected': pvals_corrected,
            'significant': rejected,
            'n_significant': sum(rejected)
        }

    # ==================== UTILIDADES ====================

    def _interpret_cohens_d(self, d: float) -> str:
        """Interpreta magnitude de Cohen's d."""
        if d < 0.2:
            return "negligible"
        elif d < 0.5:
            return "small"
        elif d < 0.8:
            return "medium"
        else:
            return "large"

    def format_result(self, result: Dict) -> str:
        """Formata resultado para paper (estilo APA)."""
        test_name = result['test']

        if 't-test' in test_name:
            return (
                f"{test_name}: t({result['df']}) = {result['t_statistic']:.3f}, "
                f"p = {result['p_value']:.4f}, "
                f"d = {result['cohens_d']:.3f} ({result['interpretation']})"
            )
        elif 'Mann-Whitney' in test_name:
            return (
                f"Mann-Whitney U = {result['u_statistic']:.0f}, "
                f"p = {result['p_value']:.4f}, "
                f"r = {result['rank_biserial_r']:.3f}"
            )
        elif 'Binomial' in test_name:
            return (
                f"Binomial test: {result['successes']}/{result['trials']} "
                f"({result['observed_proportion']:.1%}), "
                f"p = {result['p_value']:.4f}, "
                f"95% CI [{result['ci_95'][0]:.3f}, {result['ci_95'][1]:.3f}]"
            )
        else:
            return str(result)


# ==================== EXEMPLO DE USO ====================

def example_usage():
    """Exemplo de uso da classe StatisticalAnalysis."""

    stats_analyzer = StatisticalAnalysis(alpha=0.05)

    # Exemplo 1: Paired t-test (DeepBridge vs. Manual)
    print("=" * 60)
    print("EXEMPLO 1: Paired t-test")
    print("=" * 60)

    deepbridge_times = np.array([5.2, 6.1, 4.8, 5.9, 6.3, 5.1, 5.7, 6.0, 5.5, 5.8])
    manual_times = np.array([15.3, 16.2, 14.5, 15.8, 16.9, 15.2, 15.5, 16.1, 15.7, 16.0])

    result = stats_analyzer.paired_ttest(manual_times, deepbridge_times,
                                         alternative='greater')
    print(stats_analyzer.format_result(result))
    print()

    # Exemplo 2: Bootstrap CI para F1 score
    print("=" * 60)
    print("EXEMPLO 2: Bootstrap CI para F1 score")
    print("=" * 60)

    f1_scores = np.array([0.89, 0.91, 0.90, 0.88, 0.92, 0.90, 0.91, 0.89, 0.90, 0.91])
    lower, upper, _ = stats_analyzer.bootstrap_ci(f1_scores, np.mean,
                                                   n_bootstrap=10000)
    print(f"F1 Score: {np.mean(f1_scores):.3f}, 95% CI [{lower:.3f}, {upper:.3f}]")
    print()

    # Exemplo 3: Power Analysis
    print("=" * 60)
    print("EXEMPLO 3: Power Analysis")
    print("=" * 60)

    power_result = stats_analyzer.power_analysis_ttest(
        effect_size=0.8,  # Large effect
        power=0.80,       # 80% power
        alpha=0.05
    )
    print(f"Para detectar d=0.8 com 80% de poder: N = {power_result['n_required']}")
    print()

    # Exemplo 4: Binomial test (precisão EEOC)
    print("=" * 60)
    print("EXEMPLO 4: Binomial Test (EEOC accuracy)")
    print("=" * 60)

    result = stats_analyzer.binomial_test(
        successes=100,
        trials=100,
        p_expected=1.0  # Esperamos 100%
    )
    print(stats_analyzer.format_result(result))


if __name__ == '__main__':
    example_usage()
