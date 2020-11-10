import sympy as sp
from src.equations.symbols import *

nomoto_first_order = sp.Eq(K*delta,
                           r + T_1*r_1d + T_2*r_2d)