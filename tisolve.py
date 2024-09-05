# -*- coding: utf-8 -*-
from pyomo.opt import SolverFactory
from pyomo.core import Constraint, Var

instance = mdl.create_instance("loadall.dat")

solver = SolverFactory("glpk", executable="GLPK/glpsol.exe", tee=True)
results = solver.solve(instance)
instance.solutions.store_to(results)

pyomo_save_results(None, instance, results)
