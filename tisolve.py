# -*- coding: utf-8 -*-
from pyomo.opt import SolverFactory
from pyomo.core import Constraint, Var
from tipyomo import pyomo_times_model, pyomo_save_results

instance = pyomo_times_model().create_instance(filename="loadall.dat")
solver = SolverFactory("glpk", executable="GLPK/glpsol.exe", tee=True)
results = solver.solve(instance)

pyomo_save_results(None, instance, results)
