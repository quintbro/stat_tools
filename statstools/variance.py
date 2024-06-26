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
        var_estimators = self.__prepare(var_form)
        self.var_est = var_estimators
        self.n_est = var_estimators.shape[1]

    def __prepare(self, var_form):
        dm = patsy.dmatrix(var_form, self.data)
        new_df = pd.DataFrame(dm, columns = dm.design_info.column_names)

        for col in new_df.columns:
            new_df[col] = (new_df[col] - new_df[col].mean()) / new_df[col].std()

        return np.array(new_df)

    def __ExpVariance(self, theta):
        theta = np.array(theta)
        return np.exp(self.var_est @ theta.reshape(-1, 1))
    
    def __log_likelihood(self, theta):
        test_mod = smf.wls(self.formula, data=self.data, weights = 1/self.__ExpVariance(theta=theta)).fit()
        return -test_mod.llf

    def fit(self, initial_values = "rand"):
        '''
        Parameters
        ==========
        initial_values : A list of values for the optimization algorithm to start on, 
        default is to choose random numbers between -10 and 10

        Returns
        =======
        A 1D numpy array containing the weights for the variance parameter, if used 
        with statsmodels.api.WLS() then the inverse should be used.
        '''
        if initial_values == "rand":
            initial_values = np.random.uniform(-10, 10, self.n_est)
        optimized = minimize(self.__log_likelihood, 
                            x0 = initial_values)
        self.best_theta = optimized["x"]
        return self.__ExpVariance(theta=self.best_theta).flatten()