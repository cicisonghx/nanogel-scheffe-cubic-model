"""
lack-of-fit.py

Lack-of-fit F-test for a fitted scheffe mixture model.

Usage:
    from lack_of_fit import Lack_of_fit_test
    anova, df_with_resid = Lack_of_fit_test(df, model, X, y)
"""

import numpy as np
import pandas as pd
from scipy import stats

def Lack_of_fit_test(df, model, X, y):
    df2 = df.copy()
    df2['group'] = df2.groupby(['AETC','AM','BAC']).ngroup()
    df2['y'] = y.values
    df2['resid'] = model.resid.values

    pe_ss, pe_df = 0.0, 0
    for _, sub in df2.groupby('group'):
        if len(sub) > 1:
            pe_ss += np.sum((sub['y'] - sub['y'].mean())**2)
            pe_df += len(sub)-1

    if pe_df == 0:
        print("No replicate points found, cannot run lack-of-fit test.")
        return None, df2

    resid_ss = np.sum(model.resid ** 2)
    lof_ss = resid_ss - pe_ss
    n, p = X.shape
    lof_df = (n - p) - pe_df

    F_lof = (lof_ss / lof_df) / (pe_ss / pe_df)
    p_lof = 1 - stats.f.cdf(F_lof, lof_df, pe_df)

    ss_tot = np.sum((y - y.mean()) ** 2)
    anova = pd.DataFrame({
        "source": ["Regression", "Residual", "Lack-of-fit", "Pure error", "Total"],
        "SS": [ss_tot - resid_ss, resid_ss, lof_ss, pe_ss, ss_tot],
        "df": [p, n - p, lof_df, pe_df, n - 1],
    })
    anova["MS"] = anova["SS"] / anova["df"]
    anova.loc[anova["source"] == "Lack-of-fit", "F"] = F_lof
    anova.loc[anova["source"] == "Lack-of-fit", "p_value"] = p_lof

    print(f"Lack-of-fit F({lof_df},{pe_df}) = {F_lof:.3f}, p = {p_lof:.4f}")
    if p_lof < 0.05:
        print("--> Significant lack-of-fit: model form is NOT adequate")
    else:
        print("--> No significant lack-of-fit: model form is adequate")

    return anova, df2


if __name__ == "__main__":
    from fit_models import Build_terms, Fit_final_model

    test_df = pd.DataFrame({
        "AETC": [48, 48, 42.7, 42.7, 60, 60, 10, 10, 25, 22, 40, 32.9],
        "AM": [42, 42, 10, 10, 10, 10, 50, 50, 10, 50, 50, 28.5],
        "BAC": [10, 10, 47.3, 47.3, 30, 30, 40, 40, 65, 28, 10, 38.6],
        "dH": [146, 176, 52, 53, 38, 36, 94, 105, 302, 91, 24, 1144],
    })

    model, X, y = Fit_final_model(test_df, ["AETC", "AM", "BAC", "AETC_AM", "AM_BAC"])
    print()
    anova, df_with_resid = Lack_of_fit_test(test_df, model, X, y)
    print()
    print(anova)
