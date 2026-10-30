# -*- coding: utf-8 -*-
"""
GenPark Growth Agent Client
Zero-dependency viral K-factor branching process simulator, LTV/CAC cohort retention decay model,
and Wald's Sequential Probability Ratio Test (SPRT) A/B test early-stopping evaluator.
"""

import math
from typing import Dict, List, Any, Optional

class GenParkGrowthAgent:
    """
    Simulates viral branching cascades, models SaaS LTV/CAC cohort decay curves,
    and conducts continuous Wald SPRT hypothesis testing for fast A/B test convergence.
    """

    def simulate_viral_k_factor_branching(
        self,
        initial_users: int = 1000,
        invites_per_user: float = 3.5,
        invite_conversion_rate: float = 0.35,
        generations: int = 6
    ) -> Dict[str, Any]:
        """
        Simulates geometric branching process for viral loop expansion.
        Formula: K-factor = invites_per_user * invite_conversion_rate
        """
        if initial_users <= 0 or generations <= 0:
            raise ValueError("Initial users and generations must be positive.")

        k_factor = round(invites_per_user * invite_conversion_rate, 4)
        is_supercritical = k_factor >= 1.0

        gen_users = []
        curr_cohort = float(initial_users)
        total_cumulative = 0.0

        for g in range(generations + 1):
            if g == 0:
                gen_users.append({"generation": 0, "new_users": initial_users, "cumulative_users": initial_users})
                total_cumulative = float(initial_users)
            else:
                new_users = round(curr_cohort * k_factor, 1)
                total_cumulative += new_users
                gen_users.append({
                    "generation": g,
                    "new_users": new_users,
                    "cumulative_users": round(total_cumulative, 1)
                })
                curr_cohort = new_users

        # Theoretical viral amplifier multiplier = 1 / (1 - K) if K < 1.0
        viral_multiplier = round(1.0 / (1.0 - k_factor), 3) if k_factor < 1.0 else "Exponential (Supercritical)"

        return {
            "initial_users": initial_users,
            "invites_per_user": invites_per_user,
            "invite_conversion_rate": invite_conversion_rate,
            "k_factor": k_factor,
            "growth_regime": "SUPERCRITICAL_VIRAL" if is_supercritical else "SUBCRITICAL_DECAY",
            "viral_multiplier": viral_multiplier,
            "generations_simulated": generations,
            "generation_breakdown": gen_users,
            "total_users_reached": round(total_cumulative, 1)
        }

    def model_ltv_cac_cohort_decay(
        self,
        blended_cac_usd: float,
        arpu_monthly_usd: float,
        gross_margin_pct: float,
        monthly_churn_rate: float,
        months_projection: int = 24
    ) -> Dict[str, Any]:
        """
        Models cohort retention decay and customer lifetime value (LTV) against CAC.
        Formula: LTV = (ARPU * Gross Margin) / Monthly Churn
        """
        if blended_cac_usd <= 0 or arpu_monthly_usd <= 0 or monthly_churn_rate <= 0:
            raise ValueError("Financial parameters must be strictly positive.")

        margin_ratio = gross_margin_pct / 100.0
        monthly_gp_per_user = arpu_monthly_usd * margin_ratio

        # Theoretical LTV
        theoretical_ltv = monthly_gp_per_user / monthly_churn_rate
        ltv_cac_ratio = round(theoretical_ltv / blended_cac_usd, 2)

        # Payback period calculation
        cohort_curve = []
        cum_gp = 0.0
        payback_month = None

        retention = 1.0
        for m in range(1, months_projection + 1):
            retention *= (1.0 - monthly_churn_rate)
            gp_m = monthly_gp_per_user * retention
            cum_gp += gp_m
            
            if payback_month is None and cum_gp >= blended_cac_usd:
                payback_month = m

            if m in [1, 3, 6, 12, 18, 24]:
                cohort_curve.append({
                    "month": m,
                    "retention_rate_pct": round(retention * 100.0, 1),
                    "cumulative_gp_usd": round(cum_gp, 2)
                })

        return {
            "blended_cac_usd": blended_cac_usd,
            "arpu_monthly_usd": arpu_monthly_usd,
            "gross_margin_pct": gross_margin_pct,
            "monthly_churn_rate_pct": round(monthly_churn_rate * 100.0, 2),
            "theoretical_ltv_usd": round(theoretical_ltv, 2),
            "ltv_cac_ratio": ltv_cac_ratio,
            "payback_period_months": payback_month if payback_month is not None else ">24",
            "unit_economics_health": "OUTSTANDING" if ltv_cac_ratio >= 4.0 else ("HEALTHY" if ltv_cac_ratio >= 3.0 else "UNSUSTAINABLE"),
            "cohort_projections": cohort_curve
        }

    def evaluate_sprt_ab_test_early_stopping(
        self,
        variant_a_conversions: int,
        variant_a_visitors: int,
        variant_b_conversions: int,
        variant_b_visitors: int,
        alpha: float = 0.05,
        beta: float = 0.20,
        minimum_detectable_effect: float = 0.10
    ) -> Dict[str, Any]:
        """
        Conducts Wald's Sequential Probability Ratio Test (SPRT) for continuous A/B test early stopping.
        """
        if variant_a_visitors <= 0 or variant_b_visitors <= 0:
            raise ValueError("Visitor counts must be positive.")

        p_a = variant_a_conversions / float(variant_a_visitors)
        p_b = variant_b_conversions / float(variant_b_visitors)

        # Baseline proportion
        p0 = p_a
        p1 = p_a * (1.0 + minimum_detectable_effect)
        p1 = min(0.999, max(0.001, p1))
        p0 = min(0.999, max(0.001, p0))

        # Wald boundaries: A = (1 - beta) / alpha, B = beta / (1 - alpha)
        upper_bound = (1.0 - beta) / alpha
        lower_bound = beta / (1.0 - alpha)

        # Log-likelihood ratio for Bernoulli trials
        y = variant_b_conversions
        n = variant_b_visitors
        
        llr = y * math.log(p1 / p0) + (n - y) * math.log((1.0 - p1) / (1.0 - p0))

        log_upper = math.log(upper_bound)
        log_lower = math.log(lower_bound)

        if llr >= log_upper:
            decision = "STOP_EARLY_ACCEPT_VARIANT_B"
            explanation = "Variant B has proven statistically superior with minimal sample waste."
        elif llr <= log_lower:
            decision = "STOP_EARLY_REJECT_VARIANT_B"
            explanation = "Variant B failed to outperform baseline; safely terminate experiment."
        else:
            decision = "CONTINUE_TESTING"
            explanation = "Inconclusive evidence; continue gathering sample data."

        relative_lift_pct = round(100.0 * (p_b - p_a) / max(1e-9, p_a), 2)

        return {
            "variant_a_conversion_rate_pct": round(p_a * 100.0, 3),
            "variant_b_conversion_rate_pct": round(p_b * 100.0, 3),
            "relative_lift_pct": relative_lift_pct,
            "log_likelihood_ratio": round(llr, 4),
            "upper_boundary": round(log_upper, 4),
            "lower_boundary": round(log_lower, 4),
            "sprt_decision": decision,
            "recommendation": explanation
        }
