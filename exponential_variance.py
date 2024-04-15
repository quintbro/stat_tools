import statsmodels.formula.api as smf
import statsmodels.api as sm
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import patsy

class VarExp:
    '''
    Parameters
    ==========
    df : Pandas Dataframe containing the data from which you are fitting the model

    model_form : A patsy formula specifying the main model

    var_form : a formula for the exponential variance function, this does not get rid 
    of the intercept by default
    '''

    def __init__(self, df, model_form, var_form):
        self.data = df
        self.formula = model_form
        var_estimators = self.prepare(var_form)
        self.var_est = var_estimators
        self.n_est = var_estimators.shape[1]

    def prepare(self, var_form):
        dm = patsy.dmatrix(var_form, self.data)
        new_df = pd.DataFrame(dm, columns = dm.design_info.column_names)

        for col in new_df.columns:
            new_df[col] = (new_df[col] - new_df[col].mean()) / new_df[col].std()

        return np.array(new_df)

    def ExpVariance(self, theta):
        theta = np.array(theta)
        return np.exp(self.var_est @ theta.reshape(-1, 1))
    
    def new_log_likelihood(self, theta):
        test_mod = smf.wls(self.formula, data=self.data, weights = 1/self.ExpVariance(theta=theta)).fit()
        return -test_mod.llf

    def fit(self, initial_values = "rand"):
        if initial_values == "rand":
            initial_values = np.random.uniform(-10, 10, self.n_est)
        optimized = minimize(self.new_log_likelihood, 
                            x0 = initial_values)
        self.best_theta = optimized["x"]
        return self.ExpVariance(theta=self.best_theta).flatten()