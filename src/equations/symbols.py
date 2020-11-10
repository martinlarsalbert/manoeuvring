
import rolldecayestimators.special_symbol as ss
import sympy as sp
import sympy.physics.mechanics as me

t = ss.Symbol(name='t',description='time',unit='s')
delta = ss.Symbol(name='delta',description='Rudder angle',unit='rad')
r = me.dynamicsymbols('r')  # yaw rate [rad/s]
r_1d = r.diff()
r_2d = r_1d.diff()

K = ss.Symbol(name='K',description='Nomoto coefficient',unit=r'1/s')
T_1 = ss.Symbol(name='T_1',description='Nomoto time coefficient',unit='s')
T_2 = ss.Symbol(name='T_2',description='Nomoto time coefficient',unit='s')
