# -*- coding: utf-8 -*-
"""
GenPark Growth Agent FastMCP Server
"""

import json
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP
from client import GenParkGrowthAgent

mcp = FastMCP("genpark-growth-agent")
growth = GenParkGrowthAgent()

@mcp.tool()
def simulate_viral_k_factor_branching(
    initial_users: int = 1000,
    invites_per_user: float = 3.5,
    invite_conversion_rate: float = 0.35,
    generations: int = 6
) -> str:
    """
    Simulates geometric branching process for viral loop expansion.
    """
    res = growth.simulate_viral_k_factor_branching(initial_users, invites_per_user, invite_conversion_rate, generations)
    return json.dumps(res, indent=2)

@mcp.tool()
def model_ltv_cac_cohort_decay(
    blended_cac_usd: float,
    arpu_monthly_usd: float,
    gross_margin_pct: float,
    monthly_churn_rate: float,
    months_projection: int = 24
) -> str:
    """
    Models cohort retention decay and customer lifetime value (LTV) against CAC.
    """
    res = growth.model_ltv_cac_cohort_decay(blended_cac_usd, arpu_monthly_usd, gross_margin_pct, monthly_churn_rate, months_projection)
    return json.dumps(res, indent=2)

@mcp.tool()
def evaluate_sprt_ab_test_early_stopping(
    variant_a_conversions: int,
    variant_a_visitors: int,
    variant_b_conversions: int,
    variant_b_visitors: int,
    alpha: float = 0.05,
    beta: float = 0.20,
    minimum_detectable_effect: float = 0.10
) -> str:
    """
    Conducts Wald's Sequential Probability Ratio Test (SPRT) for continuous A/B test early stopping.
    """
    res = growth.evaluate_sprt_ab_test_early_stopping(variant_a_conversions, variant_a_visitors, variant_b_conversions, variant_b_visitors, alpha, beta, minimum_detectable_effect)
    return json.dumps(res, indent=2)

def main():
    print("Testing Growth Agent:")
    print(simulate_viral_k_factor_branching(1000, 3.0, 0.4))

if __name__ == "__main__":
    main()
