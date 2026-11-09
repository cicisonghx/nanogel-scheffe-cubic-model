from load_data import Load_data
from plot_contour import Plot_contour
from fit_models import Compare_models_by_aicc, Fit_final_model
from lack_of_fit import Lack_of_fit_test
from save_data import Save_table

import pandas as pd

if __name__ == '__main__':
    df = Load_data()

    Plot_contour(df)

    aicc_table = Compare_models_by_aicc(df)
    best_terms = aicc_table.iloc[0]['terms']

    print("\n--- AICc model comparison ---")
    model, X, y = Fit_final_model(df, best_terms)

    coef_table = pd.DataFrame({
        "term": model.params.index,
        "coefficient": model.params.values,
        "std_err": model.bse.values,
        "t_value": model.tvalues.values,
        "p_value": model.pvalues.values,
    })
    Save_table(coef_table, "final_model_coefficients.csv")


    print("\n--- Lack-of-fit test ---")
    anova, df_with_resid = Lack_of_fit_test(df, model, X, y)
    if anova is not None:
        print(anova)
        Save_table(anova, "lack_of_fit_anova.csv")

