"""
These is the standard setup for the notebooks.
"""

%matplotlib inline
%load_ext autoreload
%autoreload 2

from jupyterthemes import jtplot
jtplot.style(theme='onedork', context='notebook', ticks=True, grid=False)

import pandas as pd
pd.options.display.max_rows = 999
pd.options.display.max_columns = 999
pd.set_option("display.max_columns", None)
import numpy as np
import os
import matplotlib.pyplot as plt
#plt.style.use('paper')

import copy

import numpy as np
import os

from src.data import database
from mdldb import mdl_to_evaluation
from mdldb.tables import Run
import src.data
import os.path

from sklearn.pipeline import Pipeline

import sympy as sp
from sklearn.metrics import r2_score
import src.reporting.paper_writing as paper_writing

from src.equations import equations
from src.equations import symbols
from rolldecayestimators.substitute_dynamic_symbols import lambdify