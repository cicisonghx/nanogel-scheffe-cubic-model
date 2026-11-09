"""
fit_models.py

Fit Scheffe mixture polynomials (linear to full cubic models) to log10dH,
compare all term combinations by AICc, and fits the final selected model.

Usage:
    from fit_models import Compare_models_by_aicc, Fit_final_model
    aicc_table = Compare_models_by_aicc(df)
    best_terms = aicc_table.iloc[0]['terms']
    model,X,y = Fit_final_model(df, best_terms)
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from itertools import combinations

def Build_terms(df):
    """
    Build the 7 scheffe terms, 3 linear, 3 two-way and 1 three-way
    """
    x1, x2, x3 = df['AETC']/100, df['AM']/100, df['BAC']/100
    return {
        'AETC':x1, 'AM': x2, 'BAC':x3,
        'AETC_AM': x1*x2, 'AETC_BAC':x1*x3, 'AM_BAC':x2*x3,
        'AETC_AM_BAC':x1*x2*x3
    }

def Aicc(model,n,k):
    """
    Corrected AIC(AICc)
    penalised small-sample overfitting more than plain AIC
    :param model:
    :param n:
    :param k:
    :return:
    """
    return model.aic + (2 * k * (k+1))/(n - k -1)

def Compare_models_by_aicc(df):
    """
    Exhaustively fit every combinations of interaction terms. Main terms are always kept.
    Rank all models via AICc
    :param df:
    :return:
    """
    terms = Build_terms(df)
    y = np.log10(df['dH'])
    base = ['AETC','AM','BAC']
    higher = ['AETC_AM', 'AETC_BAC','AM_BAC','AETC_AM_BAC']
    n = len(y)

    rows = []

    for r in range(len(higher)+1):
        for combo in combinations(higher, r):
            cols = base + list(combo)
            X = pd.DataFrame({c:terms[c] for c in cols})
            m = sm.OLS(y,X).fit()
            k = len(cols)
            ss_res = np.sum(m.resid ** 2)
            ss_tot = np.sum((y - y.mean()) ** 2)
            r2 = 1 - ss_res/ ss_tot
            rows.append({'terms':cols, "k":k, 'AIC':m.aic,
                         'AICc':Aicc(m,n,k), 'R2':r2})

    table = pd.DataFrame(rows).sort_values("AICc").reset_index(drop=True)
    return table


def Fit_final_model(df, terms_to_use):
    """
    Fits OLS (no intercept, per Scheffe mixture convention) using the given
    term list, e.g. ['AETC','AM','BAC','AETC_AM','AM_BAC'].

    Returns (model, X, y) -- all needed downstream for lack-of-fit testing.
    """
    terms = Build_terms(df)
    y = np.log10(df["dH"])
    X = pd.DataFrame({c: terms[c] for c in terms_to_use})
    model = sm.OLS(y, X).fit()

    ss_res = np.sum(model.resid ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    n, p = X.shape
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

    print(f"Final model terms: {terms_to_use}")
    print(model.params.round(4))
    print(f"R2 = {r2:.3f}, adj R2 = {adj_r2:.3f}, AIC = {model.aic:.2f}")

    return model, X, y


if __name__ == "__main__":
    test_df = pd.DataFrame({
        "AETC": [48, 48, 42.7, 42.7, 60, 60, 10, 10, 25, 25, 22, 22],
        "AM": [42, 42, 10, 10, 10, 10, 50, 50, 10, 10, 50, 50],
        "BAC": [10, 10, 47.3, 47.3, 30, 30, 40, 40, 65, 65, 28, 28],
        "dH": [146, 176, 52, 53, 38, 36, 94, 105, 302, 193, 91, 81],
    })

    aicc_table = Compare_models_by_aicc(test_df)
    print("Top 5 models by AICc:")
    print(aicc_table.head())

    best_terms = aicc_table.iloc[0]["terms"]
    print()
    Fit_final_model(test_df, best_terms)