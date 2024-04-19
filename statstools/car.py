import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels.api as sm
import math
import matplotlib.pyplot as plt

# Define Added Variable Plots Function
def get_coords(num, ncols, nrows):
  iter = 0
  ax1 = 0
  ax2 = 0
  for i in range(nrows):
    for j in range(ncols):
      if iter == num:
        return ax1, ax2
      iter += 1
      ax2 += 1
    ax2 = 0
    ax1 += 1

def avPlots(X, y, width = 15, height = 3):
    '''
    Parameters
    ==========
    X : pd Dataframe, numpy array, matrix like
      Pandas dataframe containing the explanatory variables (Can contain categorical variables)
    y : pd Series, numpy array
      Pandas series containing the response variable
    width : int, float
      A number describing the width of the plot, to be passed to "figsize" arguement from matplot lib
    height : int, float
      A number describing the height of 1 of the plots
    '''
    X = pd.DataFrame(X)
    X = pd.get_dummies(X, drop_first=True).astype(float)
    n_cols_data = X.shape[1]
    n_rows = math.ceil(n_cols_data / 3)
    fig, ax = plt.subplots(nrows=n_rows, ncols=3, figsize = [width, height*n_rows])
    plots = []
    n_plot = 0
    for col in X.columns:
        # Get Y-Axis Residuals
        endog = np.array(y)
        exog = np.array(X.drop(col, axis = 1))
        y_lm = sm.OLS(endog, exog).fit()
        y_axis = y_lm.resid

        # Get the X-Axis Residuals
        endog = np.array(X[col])
        exog = np.array(X.drop(col, axis = 1))
        x_lm = sm.OLS(endog, exog).fit()
        x_axis = x_lm.resid

        # Make the plot
        cord1, cord2 = get_coords(n_plot, ncols=3, nrows=n_rows)
        if X.shape[1] <=3:
          sns.regplot(x = x_axis, y = y_axis, line_kws={"color" : "red"},
                      ax = ax[cord2],
                      ci = None,
                      scatter_kws= {"s" : 8})
          ax[cord2].set_title(col)
        else:
          sns.regplot(x = x_axis, y = y_axis, line_kws={"color" : "red"},
                      ax = ax[cord1, cord2],
                      ci = None,
                      scatter_kws= {"s" : 8})
          ax[cord1, cord2].set_title(col)
        n_plot += 1
    plt.show()
