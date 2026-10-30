# -*- coding: utf-8 -*-
import json
from client import GenParkGrowthAgent

agent = GenParkGrowthAgent()

# 1. Viral K-Factor Branching Process Simulation
viral = agent.simulate_viral_k_factor_branching(initial_users=500, invites_per_user=4.0, invite_conversion_rate=0.32, generations=5)
print(f"Viral K-Factor: {viral['k_factor']} ({viral['growth_regime']}) | Total Reached: {viral['total_users_reached']} users")
for g in viral["generation_breakdown"][:4]:
    print(f"  Gen {g['generation']}: New={g['new_users']}, Cum={g['cumulative_users']}")

# 2. LTV / CAC Cohort Decay Modeling
ltv_cac = agent.model_ltv_cac_cohort_decay(
    blended_cac_usd=350.0,
    arpu_monthly_usd=65.0,
    gross_margin_pct=85.0,
    monthly_churn_rate=0.035,
    months_projection=24
)
print()
print(f"SaaS Unit Economics: LTV=${ltv_cac['theoretical_ltv_usd']} | CAC=${ltv_cac['blended_cac_usd']} | Ratio={ltv_cac['ltv_cac_ratio']}x ({ltv_cac['unit_economics_health']})")
print(f"  Payback Period: {ltv_cac['payback_period_months']} months")

# 3. Wald's SPRT A/B Test Early Stopping
ab_test = agent.evaluate_sprt_ab_test_early_stopping(
    variant_a_conversions=210,
    variant_a_visitors=5000,
    variant_b_conversions=285,
    variant_b_visitors=5000,
    minimum_detectable_effect=0.15
)
print()
print(f"SPRT A/B Test: CR_A={ab_test['variant_a_conversion_rate_pct']}% vs CR_B={ab_test['variant_b_conversion_rate_pct']}% (Lift: +{ab_test['relative_lift_pct']}%)")
print(f"  Decision: {ab_test['sprt_decision']} -> {ab_test['recommendation']}")
