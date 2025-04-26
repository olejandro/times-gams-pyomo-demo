# -*- coding: utf-8 -*-
from pyomo.opt import SolverFactory
from tipyomo import pyomo_times_model, pyomo_save_results

instance = pyomo_times_model().create_instance(filename="loadall.dat")
solver = SolverFactory("highs")
results = solver.solve(instance, tee=True)

pyomo_save_results(None, instance, results)
