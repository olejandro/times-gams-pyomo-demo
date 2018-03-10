# ============================================================================
from pyomo.environ import *
from math import exp

model = AbstractModel()

# ======= System sets
model.YEAR = Set(initialize=[0]) | RangeSet(1900,2200)
model.INOUT	= Set()
model.IMPEXP = Set()
model.LIM = Set()
model.TSLVL = Set()
model.COM_TYPE = Set()
model.PRC_GRP = Set()
model.UPT = Set()
model.UC_GRPTYPE = Set()
model.UC_NAME = Set()
model.UC_COST = Set(within=model.UC_NAME)
model.COSTAGG = Set()

# ======= User input sets
model.MILEYR = Set(within=model.YEAR)
model.MODLYR = Set(within=model.YEAR)
model.TSLICE = Set()
model.REGION = Set()
model.PROCESS = Set()
model.COMMTY = Set()
model.COMGRP = Set()
model.CURENCY = Set()

# ======= Internal sets (all simple sets for now)
model.OBV = Set()
model.TS_MAP = Set(within=model.REGION * model.TSLICE * model.TSLICE)
model.RS_TREE = Set(within=model.REGION * model.TSLICE * model.TSLICE)
model.RS_PRETS = Set(within=model.REGION * model.TSLICE * model.TSLICE)
model.RC = Set(within=model.REGION * model.COMMTY)
model.DEM = Set(within=model.REGION * model.COMMTY)
model.RP = Set(within=model.REGION * model.PROCESS)
model.RP_FLO = Set(within=model.REGION * model.PROCESS)
model.RP_STD = Set(within=model.REGION * model.PROCESS)
model.RP_IRE = Set(within=model.REGION * model.PROCESS)
model.RP_STG = Param(model.REGION, model.PROCESS, within=Binary, default=0)
model.RP_PGACT = Param(model.REGION, model.PROCESS, within=Binary, default=0)
model.RP_PGFLO = Param(model.REGION, model.PROCESS, within=Binary, default=0)
model.PRC_ACT = Param(model.RP, within=Binary, default=0)
model.RDCUR = Set(within=model.REGION * model.CURENCY)
model.COM_GMAP = Set(within=model.REGION * model.COMGRP * model.COMMTY)
model.COM_ISMEM = Param(model.REGION, model.COMGRP, model.COMMTY, within=Binary, default=0)
model.TOP = Set(within=model.REGION * model.PROCESS * model.COMMTY * model.INOUT)
model.PRC_VINT=Param(model.RP, within=Binary, default=0)
model.PRC_TS = Set(within=model.REGION * model.PROCESS * model.TSLICE)
model.RPS_S1 = Set(within=model.REGION * model.PROCESS * model.TSLICE)
model.RPS_STG = Set(within=model.REGION * model.PROCESS * model.TSLICE)
model.RPC = Set(within=model.REGION * model.PROCESS * model.COMMTY)
model.RPC_PG = Set(within=model.REGION * model.PROCESS * model.COMMTY)
model.RPC_IRE = Set(within=model.REGION * model.PROCESS * model.COMMTY * model.IMPEXP)
model.RPC_STG = Param(model.RPC, within=Binary, default=0)
model.PRC_STGTSS = Set(within=model.REGION * model.PROCESS * model.COMMTY)
model.RPG_ACE = Set(within=model.REGION * model.PROCESS * model.COMGRP * model.INOUT)
model.RPC_ACE = Set(within=model.REGION * model.PROCESS * model.COMMTY)
model.RPCS_VAR = Set(within=model.REGION * model.PROCESS * model.COMMTY * model.TSLICE)
model.RPCC_FFUNC = Set(within=model.REGION * model.PROCESS * model.COMGRP * model.COMGRP)
model.RCS_COMBAL = Set(within=model.REGION * model.MILEYR * model.COMMTY * model.TSLICE * model.LIM)
model.RCS_COMPRD = Set(within=model.REGION * model.MILEYR * model.COMMTY * model.TSLICE * model.LIM)
model.RTDEM = Set(within=model.REGION * model.MODLYR * model.COMMTY)
model.RTCS = Set(within=model.REGION * model.MODLYR * model.COMMTY * model.TSLICE)
model.RHS_COMPRD = Param(model.RTCS, within=Binary, default=0)
model.RHS_COMBAL = Param(model.RTCS, within=Binary, default=0)
model.RTP = Set(within=model.REGION * model.MODLYR * model.PROCESS)
model.RTP_VARA = Param(model.RP, model.MILEYR, within=Binary, default=0)
model.RTP_VARP = Param(model.RTP, within=Binary, default=0)
model.RTP_VINTYR = Set(within=model.REGION * model.MODLYR * model.MILEYR * model.PROCESS)
model.RTP_CPTYR = Set(within=model.REGION * model.MODLYR * model.MILEYR * model.PROCESS)
model.AFS = Set(within=model.REGION * model.MILEYR * model.PROCESS * model.TSLICE * model.LIM)
model.IS_LINT = Set(within=model.REGION * model.MODLYR * model.MODLYR * model.CURENCY)
model.IS_CAPBND = Set(within=model.REGION * model.YEAR * model.PROCESS * model.LIM)
model.IS_NCAPBD = Set(within=model.REGION * model.YEAR * model.PROCESS * model.LIM)
model.RP_PTRAN = Set(within=model.REGION * model.PROCESS * model.COMGRP * model.COMGRP * model.TSLICE)
model.IS_SHAR = Set(within=model.REGION * model.YEAR * model.PROCESS * model.COMMTY * model.COMGRP * model.TSLICE * model.LIM)
model.IS_ACOST = Set(within=model.REGION * model.MODLYR * model.PROCESS * model.CURENCY)

# ============================================================================

# ======= Parameters
model.G_YRFR = Param(model.REGION, model.TSLICE)
model.RS_STGPRD = Param(model.REGION, model.TSLICE)
model.RS_STGAV = Param(model.REGION, model.TSLICE)
model.RS_FR = Param(model.REGION, model.TSLICE, model.TSLICE, default=0)
model.RTCS_FR = Param(model.REGION, model.MILEYR, model.COMMTY, model.TSLICE, model.TSLICE, default=0)
model.COM_PROJ = Param(model.REGION, model.YEAR, model.COMMTY, default=0)
model.COM_IE = Param(model.REGION, model.YEAR, model.COMMTY, model.TSLICE)
model.COM_FR = Param(model.REGION, model.YEAR, model.COMMTY, model.TSLICE)
model.PRC_CAPACT = Param(model.REGION, model.PROCESS)
model.PRC_SC = Param(model.REGION, model.PROCESS, default=0)
model.PRC_ACTFLO = Param(model.REGION, model.YEAR, model.PROCESS, model.COMGRP, default=0)
model.CAP_BND = Param(model.REGION, model.YEAR, model.PROCESS, model.LIM, default=0)
model.NCAP_BND = Param(model.REGION, model.YEAR, model.PROCESS, model.LIM)
model.NCAP_PASTI = Param(model.REGION, model.MODLYR, model.PROCESS, default=0)
model.COEF_CPT = Param(model.REGION, model.MODLYR, model.MILEYR, model.PROCESS, default=0)
model.COEF_AF = Param(model.REGION, model.MODLYR, model.MILEYR, model.PROCESS, model.TSLICE, model.LIM, default=0)
model.COEF_PTRAN = Param(model.REGION, model.MODLYR, model.PROCESS, model.COMGRP, model.COMMTY, model.COMGRP, model.TSLICE, default=0)
model.FLO_SHAR = Param(model.REGION, model.YEAR, model.PROCESS, model.COMMTY, model.COMGRP, model.TSLICE, model.LIM)
model.STG_EFF = Param(model.REGION, model.YEAR, model.PROCESS)
model.STG_LOSS = Param(model.REGION, model.YEAR, model.PROCESS, model.TSLICE, default=0)
model.STG_CHRG = Param(model.REGION, model.YEAR, model.PROCESS, model.TSLICE, default=0)
model.ACT_EFF = Param(model.REGION, model.YEAR, model.PROCESS, model.COMGRP, model.TSLICE, default=0)

# ======= Cost parameters
model.OBJ_PVT = Param(model.REGION, model.MILEYR, model.CURENCY)
model.OBJ_LINT = Param(model.REGION, model.MILEYR, model.MODLYR, model.CURENCY, default=0)
model.OBJ_ACOST = Param(model.REGION, model.MODLYR, model.PROCESS, model.CURENCY, default=0)
model.OBJ_IPRIC = Param(model.REGION, model.YEAR, model.PROCESS, model.COMMTY, model.TSLICE, model.IMPEXP, model.CURENCY, default=0)
model.COEF_OBINV = Param(model.REGION, model.MODLYR, model.PROCESS, model.CURENCY, default=0)
model.COEF_OBFIX = Param(model.REGION, model.MODLYR, model.PROCESS, model.CURENCY, default=0)

def MILE(model,y):
    if y in model.MILEYR:
        return 1
model.MILE = Param(model.MODLYR, within=Binary, default=0, initialize=MILE)

model.RP_AIRE = Param(model.RP_IRE, model.IMPEXP, within=Binary, default=0)

def ISRP(model,r,p):
    if (r,p) in model.RP:
        return 1
model.ISRP = Param(model.REGION, model.PROCESS, within=Binary, default=0, initialize=ISRP)

model.RP_ISIRE = Param(model.REGION, model.PROCESS, within=Binary, default=0)
model.RTP_IPRI = Param(model.REGION, model.PROCESS, model.MILEYR, model.CURENCY, within=Binary, default=0)

def LINTY(model,r,t,cur):
    return (y for y in model.MODLYR if (r,t,y,cur) in model.IS_LINT)
model.LINTY = Set(model.REGION, model.MILEYR, model.CURENCY, initialize=LINTY)

def RTP_VNT(model,r,t,p):
    return (y for y in model.MODLYR if (r,y,t,p) in model.RTP_VINTYR)
model.RTP_VNT = Set(model.RTP, initialize=RTP_VNT)

def RTP_CPT(model,r,t,p):
    return (y for y in model.MODLYR if (r,y,t,p) in model.RTP_CPTYR)
model.RTP_CPT = Set(model.RTP, initialize=RTP_CPT)

def RTP_AFS(model,r,t,p,l):
    return (s for s in model.TSLICE if (r,t,p,s,l) in model.AFS)
model.RTP_AFS = Set(model.RTP, model.LIM, initialize=RTP_AFS)

def RP_TS(model,r,p):
    return (s for s in model.TSLICE if (r,p,s) in model.PRC_TS)
model.RP_TS = Set(model.RP, initialize=RP_TS)

def RP_S1(model,r,p):
    return (s for s in model.TSLICE if (r,p,s) in model.RPS_S1)
model.RP_S1 = Set(model.RP, initialize=RP_S1)

def RP_PGC(model,r,p):
    return (c for c in model.COMMTY if (r,p,c) in model.RPC_PG)
model.RP_PGC = Set(model.RP, initialize=RP_PGC)

def RP_CIE(model,r,p):
    return ((c,ie) for (c,ie) in model.COMMTY*model.IMPEXP if (r,p,c,ie) in model.RPC_IRE)
model.RP_CIE = Set(model.RP_IRE, dimen=2, initialize=RP_CIE)

def RPC_TS(model,r,p,c):
    return (s for s in model.TSLICE if (r,p,c,s) in model.RPCS_VAR)
model.RPC_TS = Set(model.RPC, initialize=RPC_TS)

def RPIO_C(model,r,p,io):
    return (c for c in model.COMMTY if (r,p,c,io) in model.TOP)
model.RPIO_C = Set(model.RP, model.INOUT, initialize=RPIO_C)

def RCIO_P(model,r,c,io):
    return (p for p in model.PROCESS if (r,p,c,io) in model.TOP)
model.RCIO_P = Set(model.RC, model.INOUT, initialize=RCIO_P)

def RCIE_P(model,r,c,ie):
    return (p for p in model.PROCESS if (r,p,c,ie) in model.RPC_IRE)
model.RCIE_P = Set(model.RC, model.IMPEXP, initialize=RCIE_P)

def RP_ACE(model,r,p):
    return (c for c in model.COMMTY if (r,p,c) in model.RPC_ACE)
model.RP_ACE = Set(model.RP, initialize=RP_ACE)

# ============================================================================

# ======= Variables
model.RegObj  = Var(model.OBV, model.REGION, model.CURENCY, within=NonNegativeReals, dense=False)
model.ComPrd  = Var(model.REGION, model.MILEYR, model.COMMTY, model.TSLICE, within=NonNegativeReals, dense=False)
model.ComNet  = Var(model.REGION, model.MILEYR, model.COMMTY, model.TSLICE, within=NonNegativeReals, dense=False)

def PrcCap_bounds(model,r,y,p):
    if (r,y,p,'LO') in model.IS_CAPBND:
        lb=value(model.CAP_BND[r,y,p,'LO'])
    else:
        lb=0
    if (r,y,p,'UP') in model.IS_CAPBND: 
        ub=value(model.CAP_BND[r,y,p,'UP'])
    else: 
        ub=float('inf')
    return (lb, ub)
model.PrcCap  = Var(model.REGION, model.MODLYR, model.PROCESS, bounds=PrcCap_bounds, dense=False)

def PrcNcap_bounds(model,r,y,p):
    if (r,y,p,'LO') in model.IS_NCAPBD:
        lb=value(model.NCAP_BND[r,y,p,'LO'])
    else:
        lb=0
    if (r,y,p,'UP') in model.IS_NCAPBD: 
        ub=value(model.NCAP_BND[r,y,p,'UP'])
    else: 
        ub=float('inf')
    return (lb, ub)
model.PrcNcap = Var(model.REGION, model.MODLYR, model.PROCESS, bounds=PrcNcap_bounds, dense=False)

model.PrcAct  = Var(model.REGION, model.YEAR, model.MILEYR, model.PROCESS, model.TSLICE, within=NonNegativeReals, dense=False)
model.PrcFlo  = Var(model.REGION, model.YEAR, model.MILEYR, model.PROCESS, model.COMMTY, model.TSLICE, within=NonNegativeReals, dense=False)
model.IreFlo  = Var(model.REGION, model.YEAR, model.MILEYR, model.PROCESS, model.COMMTY, model.TSLICE, model.IMPEXP, within=NonNegativeReals, dense=False)
model.StgFlo  = Var(model.REGION, model.YEAR, model.MILEYR, model.PROCESS, model.COMMTY, model.TSLICE, model.INOUT, within=NonNegativeReals, dense=False)

# ============================================================================
#

def obj_rule(model):
	return sum(model.RegObj[o,r,cur] for o in model.OBV for (r,cur) in model.RDCUR)
model.obj = Objective(rule=obj_rule, sense=minimize)

def EQ_OBJINV(model,r,cur):
    return (sum(model.OBJ_PVT[r,t,cur] * model.COEF_CPT[r,v,t,p] * model.COEF_OBINV[r,v,p,cur] *
                ((model.PrcNcap[r,v,p] if v in model.MILEYR else 0) + model.NCAP_PASTI[r,v,p]) for (r,v,t,p)
                in model.RTP_CPTYR if model.COEF_OBINV[r,v,p,cur]) == model.RegObj['OBJINV',r,cur])
model.EQ_OBJINV = Constraint(model.RDCUR, rule=EQ_OBJINV)

def EQ_OBJFIX(model,r,cur):
    return (sum(model.OBJ_PVT[r,t,cur] * model.COEF_CPT[r,v,t,p] * model.COEF_OBFIX[r,v,p,cur] *
                ((model.PrcNcap[r,v,p] if v in model.MILEYR else 0) + model.NCAP_PASTI[r,v,p]) for (r,v,t,p) 
                in model.RTP_CPTYR if model.COEF_OBFIX[r,v,p,cur]) == model.RegObj['OBJFIX',r,cur])
model.EQ_OBJFIX = Constraint(model.RDCUR, rule=EQ_OBJFIX)

def EQ_OBJVAR(model,r,cur):
    return (sum(sum(((sum(model.OBJ_LINT[r,t,y,cur] * model.OBJ_ACOST[r,y,p,cur] for y in model.LINTY[r,t,cur]) *
                      sum(model.PrcAct[r,v,t,p,s] * (model.RS_STGAV[r,s] if model.RP_STG[r,p] else 1) 
                      for v in model.RTP_VNT[r,t,p] for s in model.RP_TS[r,p])) if model.OBJ_ACOST[r,t,p,cur] else 0) +
                      ((sum(sum(model.OBJ_LINT[r,t,y,cur] * model.OBJ_IPRIC[r,y,p,c,s,ie,cur] for y in model.LINTY[r,t,cur]) * 
                            sum(model.IreFlo[r,v,t,p,c,s,ie] for v in model.RTP_VNT[r,t,p]) 
                            for s in model.RP_TS[r,p] for (c,ie) in model.RP_CIE[r,p])) if model.RTP_IPRI[r,p,t,cur] else 0)
                      for t in model.MILEYR if model.RTP_VARA[r,p,t]) for p in model.PROCESS if model.ISRP[r,p]) == model.RegObj['OBJVAR',r,cur])
model.EQ_OBJVAR = Constraint(model.RDCUR, rule=EQ_OBJVAR)
#
# ------- Activity to Primary Group -------
#
def EQ_ACTFLO(model,r,v,t,p,s):
    if model.PRC_ACT[r,p] and s in model.RP_TS[r,p]:
        return (model.RTP_VARA[r,p,t] * model.PrcAct[r,v,t,p,s] == sum((sum(model.IreFlo[r,v,t,p,c,s,ie] 
                             for ie in model.IMPEXP if model.RP_AIRE[r,p,ie]) if model.RP_ISIRE[r,p] else model.PrcFlo[r,v,t,p,c,s]) for c in model.RP_PGC[r,p]))
    else:
        return Constraint.Skip
model.EQ_ACTFLO = Constraint(model.RTP_VINTYR, model.TSLICE, rule=EQ_ACTFLO)
#
# ------- Activity to Capacity -------
#
def EQL_CAPACT(model,r,v,y,p,s):
    if s in model.RTP_AFS[r,y,p,'UP']:
        return ((sum(model.PrcAct[r,v,y,p,ts] * model.RS_FR[r,ts,s] * exp(model.PRC_SC[r,p])/model.RS_STGPRD[r,s] for ts in model.RP_TS[r,p] if model.RS_FR[r,s,ts]) if model.RP_STG[r,p] else 
                sum(model.PrcAct[r,v,y,p,ts] for ts in model.RP_TS[r,p] if model.RS_FR[r,s,ts])) <= ((1 if model.RP_STG[r,p] else model.G_YRFR[r,s]) * model.PRC_CAPACT[r,p] * 
                   (model.COEF_AF[r,v,y,p,s,'UP'] * model.COEF_CPT[r,v,y,p] * ((model.PrcNcap[r,v,p] if model.MILE[v] else 0) + model.NCAP_PASTI[r,v,p]) if model.PRC_VINT[r,p] else 
                    sum(model.COEF_AF[r,m,y,p,s,'UP'] * model.COEF_CPT[r,m,y,p]*((model.PrcNcap[r,m,p] if model.MILE[m] else 0)+model.NCAP_PASTI[r,m,p]) for m in model.RTP_CPT[r,y,p]))))
    else:
        return Constraint.Skip
model.EQL_CAPACT = Constraint(model.RTP_VINTYR, model.TSLICE, rule=EQL_CAPACT)

def EQE_CAPACT(model,r,v,y,p,s):
    if s in model.RTP_AFS[r,y,p,'FX']:
        return ((sum(model.PrcAct[r,v,y,p,ts] * model.RS_FR[r,ts,s] * exp(model.PRC_SC[r,p])/model.RS_STGPRD[r,s] for ts in model.RP_TS[r,p] if model.RS_FR[r,s,ts]) if model.RP_STG[r,p] else 
                sum(model.PrcAct[r,v,y,p,ts] for ts in model.RP_TS[r,p] if model.RS_FR[r,s,ts])) == ((1 if model.RP_STG[r,p] else model.G_YRFR[r,s]) * model.PRC_CAPACT[r,p] * 
                   (model.COEF_AF[r,v,y,p,s,'FX'] * model.COEF_CPT[r,v,y,p] * ((model.PrcNcap[r,v,p] if model.MILE[v] else 0) + model.NCAP_PASTI[r,v,p]) if model.PRC_VINT[r,p] else 
                    sum(model.COEF_AF[r,m,y,p,s,'FX'] * model.COEF_CPT[r,m,y,p]*((model.PrcNcap[r,m,p] if model.MILE[m] else 0)+model.NCAP_PASTI[r,m,p]) for m in model.RTP_CPT[r,y,p]))))
    else:
        return Constraint.Skip
model.EQE_CAPACT = Constraint(model.RTP_VINTYR, model.TSLICE, rule=EQE_CAPACT)
#
# ------- Capacity Transfer -------
#
def EQE_CPT(model,r,y,p):
    if model.RTP_VARP[r,y,p] or model.CAP_BND[r,y,p,'FX']:
        return ((model.PrcCap[r,y,p] if model.RTP_VARP[r,y,p] else model.CAP_BND[r,y,p,'FX']) == sum(model.COEF_CPT[r,v,y,p] *
               ((model.MILE[v] * model.PrcNcap[r,v,p]) + model.NCAP_PASTI[r,v,p]) for v in model.RTP_CPT[r,y,p]))
    else:
        return Constraint.Skip
model.EQE_CPT = Constraint(model.RTP, rule=EQE_CPT)

def EQL_CPT(model,r,y,p):
    if not model.RTP_VARP[r,y,p] and model.CAP_BND[r,y,p,'LO']:
        return ((model.PrcCap[r,y,p] if model.RTP_VARP[r,y,p] else model.CAP_BND[r,y,p,'LO']) <= sum(model.COEF_CPT[r,v,y,p] *
               ((model.MILE[v] * model.PrcNcap[r,v,p]) + model.NCAP_PASTI[r,v,p]) for v in model.RTP_CPT[r,y,p]))
    else:
        return Constraint.Skip
model.EQL_CPT = Constraint(model.RTP, rule=EQL_CPT)

def EQG_CPT(model,r,y,p):
    if not model.RTP_VARP[r,y,p] and model.CAP_BND[r,y,p,'UP']:
        return ((model.PrcCap[r,y,p] if model.RTP_VARP[r,y,p] else model.CAP_BND[r,y,p,'UP']) >= sum(model.COEF_CPT[r,v,y,p] *
               ((model.MILE[v] * model.PrcNcap[r,v,p]) + model.NCAP_PASTI[r,v,p]) for v in model.RTP_CPT[r,y,p]))
    else:
        return Constraint.Skip
model.EQG_CPT = Constraint(model.RTP, rule=EQG_CPT)
#
# ------- Process Flow Shares -------
#
def EQL_FLOSHR(model,r,v,p,c,cg,s,l,t):
    if model.RTP_VARA[r,p,t] and v in model.RTP_VNT[r,t,p] and s in model.RPC_TS[r,p,c] and l=='LO':
        return (sum(model.FLO_SHAR[r,v,p,c,cg,s,l] * sum(model.PrcFlo[r,v,t,p,com,ts] * model.RS_FR[r,s,ts] for com in model.RPIO_C[r,p,io] for ts in model.RPC_TS[r,p,com] 
                        if model.COM_ISMEM[r,cg,com] and model.RS_FR[r,s,ts]) for io in model.INOUT if c in model.RPIO_C[r,p,io]) <=  model.PrcFlo[r,v,t,p,c,s])
    else:
        return Constraint.Skip
model.EQL_FLOSHR = Constraint(model.IS_SHAR,model.MILEYR, rule=EQL_FLOSHR)

def EQG_FLOSHR(model,r,v,p,c,cg,s,l,t):
    if model.RTP_VARA[r,p,t] and v in model.RTP_VNT[r,t,p] and s in model.RPC_TS[r,p,c] and l=='UP':
        return (sum(model.FLO_SHAR[r,v,p,c,cg,s,l] * sum(model.PrcFlo[r,v,t,p,com,ts] * model.RS_FR[r,s,ts] for com in model.RPIO_C[r,p,io] for ts in model.RPC_TS[r,p,com] 
                        if model.COM_ISMEM[r,cg,com] and model.RS_FR[r,s,ts]) for io in model.INOUT if c in model.RPIO_C[r,p,io]) >=  model.PrcFlo[r,v,t,p,c,s])
    else:
        return Constraint.Skip
model.EQG_FLOSHR = Constraint(model.IS_SHAR,model.MILEYR, rule=EQG_FLOSHR)

def EQE_FLOSHR(model,r,v,p,c,cg,s,l,t):
    if model.RTP_VARA[r,p,t] and v in model.RTP_VNT[r,t,p] and s in model.RPC_TS[r,p,c] and l=='FX':
        return (sum(model.FLO_SHAR[r,v,p,c,cg,s,l] * sum(model.PrcFlo[r,v,t,p,com,ts] * model.RS_FR[r,s,ts] for com in model.RPIO_C[r,p,io] for ts in model.RPC_TS[r,p,com] 
                        if model.COM_ISMEM[r,cg,com] and model.RS_FR[r,s,ts]) for io in model.INOUT if c in model.RPIO_C[r,p,io]) ==  model.PrcFlo[r,v,t,p,c,s])
    else:
        return Constraint.Skip
model.EQE_FLOSHR = Constraint(model.IS_SHAR,model.MILEYR, rule=EQE_FLOSHR)
#
# ------- Activity efficiency -------
#
def EQE_ACTEFF(model,r,p,cg,io,t,v,s):
#    if not model.RTP_VARA[r,p,t]:
#        v = Set()
#    if s in model.RP_S1[r,p] and (v in model.RTP_VNT[r,t,p] or v==()):
    if s in model.RP_S1[r,p] and model.RTP_VARA[r,p,t] and v in model.RTP_VNT[r,t,p]:
        return (sum(sum(model.PrcFlo[r,v,t,p,c,ts] * (model.ACT_EFF[r,v,p,c,ts] if model.ACT_EFF[r,v,p,c,ts] else 1) * model.RS_FR[r,s,ts] * 
                        (1 + model.RTCS_FR[r,t,c,s,ts]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts]) for c in model.RP_ACE[r,p] if model.COM_ISMEM[r,cg,c]) == 
                sum(model.RS_FR[r,s,ts] * (sum((model.PrcAct[r,v,t,p,ts] if model.RP_PGACT[r,p] else model.PrcFlo[r,v,t,p,c,ts] / model.PRC_ACTFLO[r,v,p,c]) / 
                    (model.ACT_EFF[r,v,p,c,ts] if model.ACT_EFF[r,v,p,c,ts] else 1) * (1+model.RTCS_FR[r,t,c,s,ts]) for c in model.RP_PGC[r,p]) if model.RP_PGFLO[r,p] else model.PrcAct[r,v,t,p,ts]) / max(1e-6,model.ACT_EFF[r,v,p,cg,ts]) for ts in model.RP_TS[r,p] if model.RS_FR[r,s,ts]))
    else:
        return Constraint.Skip
model.EQE_ACTEFF = Constraint(model.RPG_ACE,model.MILEYR, model.MODLYR, model.TSLICE, rule=EQE_ACTEFF)
#
# ------- Process Transformation -------
#
def EQ_PTRANS(model,r,p,cg1,cg2,s1,t,v,s):
#    if not model.RTP_VARA[r,p,t]:
#        v = Set()
#    if model.RS_FR[r,s1,s] and s in model.RP_S1[r,p] and (v in model.RTP_VNT[r,t,p] or v==()):
    if model.RS_FR[r,s1,s] and s in model.RP_S1[r,p] and model.RTP_VARA[r,p,t] and v in model.RTP_VNT[r,t,p]:
        return (sum(sum(model.PrcFlo[r,v,t,p,c,ts] * model.RS_FR[r,s,ts] * (1 + model.RTCS_FR[r,t,c,s,ts]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts]) for io in model.INOUT for c in model.RPIO_C[r,p,io] if model.COM_ISMEM[r,cg2,c]) == 
                sum(model.COEF_PTRAN[r,v,p,cg1,c,cg2,ts] * model.RS_FR[r,s,ts] * (1 + model.RTCS_FR[r,t,c,s,ts]) * model.PrcFlo[r,v,t,p,c,ts] for io in model.INOUT for c in model.RPIO_C[r,p,io] for ts in model.RPC_TS[r,p,c] if (model.COEF_PTRAN[r,v,p,cg1,c,cg2,ts] if model.RS_FR[r,s,ts] else 0)))
    else:
        return Constraint.Skip
model.EQ_PTRANS = Constraint(model.RP_PTRAN, model.MILEYR, model.MODLYR, model.TSLICE, rule=EQ_PTRANS)
#
# ------- Commodity Balance = -------
#
def EQG_COMBAL(model,r,t,c,s):
    if (r,t,c,s,'LO') in model.RCS_COMBAL:
        return ((model.ComPrd[r,t,c,s] if model.RHS_COMPRD[r,t,c,s] else (
                sum((sum(sum(model.StgFlo[r,v,t,p,c,ts,'OUT'] * model.RS_FR[r,s,ts] * (1 + model.RTCS_FR[r,t,c,s,ts]) * model.STG_EFF[r,v,p] for v in model.RTP_VNT[r,t,p]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts]) 
                if model.RPC_STG[r,p,c] else (sum(sum(model.PrcFlo[r,v,t,p,c,ts] * model.RS_FR[r,s,ts] * (1 + model.RTCS_FR[r,t,c,s,ts]) for v in model.RTP_VNT[r,t,p]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts]))) for p in model.RCIO_P[r,c,'OUT'] if model.RTP_VARA[r,p,t]) + 
                sum(sum(sum(model.IreFlo[r,v,t,p,c,ts,'IMP'] * model.RS_FR[r,s,ts] * (1 + model.RTCS_FR[r,t,c,s,ts]) for v in model.RTP_VNT[r,t,p]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts]) for p in model.RCIE_P[r,c,'IMP'] if model.RTP_VARA[r,p,t])) * model.COM_IE[r,t,c,s]) 
                >=
                sum((sum(sum(model.StgFlo[r,v,t,p,c,ts,'IN'] * model.RS_FR[r,s,ts] * (1 + model.RTCS_FR[r,t,c,s,ts]) for v in model.RTP_VNT[r,t,p]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts]) 
                if model.RPC_STG[r,p,c] else (sum(sum(model.PrcFlo[r,v,t,p,c,ts] * model.RS_FR[r,s,ts] * (1 + model.RTCS_FR[r,t,c,s,ts]) for v in model.RTP_VNT[r,t,p]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts]))) for p in model.RCIO_P[r,c,'IN'] if model.RTP_VARA[r,p,t]) + 
                sum(sum(sum(model.IreFlo[r,v,t,p,c,ts,'EXP'] * model.RS_FR[r,s,ts] * (1 + model.RTCS_FR[r,t,c,s,ts]) for v in model.RTP_VNT[r,t,p]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts]) for p in model.RCIE_P[r,c,'EXP'] if model.RTP_VARA[r,p,t]) + 
                (model.COM_PROJ[r,t,c] * model.COM_FR[r,t,c,s] if model.COM_PROJ[r,t,c] else 0)) 
    else:
        return Constraint.Skip
model.EQG_COMBAL = Constraint(model.REGION, model.MILEYR, model.COMMTY, model.TSLICE, rule=EQG_COMBAL)
#
# ------- Commodity Balance = -------
#
def EQE_COMBAL(model,r,t,c,s):
    if (r,t,c,s,'FX') in model.RCS_COMBAL:
        return ((model.ComPrd[r,t,c,s] if model.RHS_COMPRD[r,t,c,s] else (
                sum((sum(sum(model.StgFlo[r,v,t,p,c,ts,'OUT'] * model.RS_FR[r,s,ts] * (1 + model.RTCS_FR[r,t,c,s,ts]) * model.STG_EFF[r,v,p] for v in model.RTP_VNT[r,t,p]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts]) 
                if model.RPC_STG[r,p,c] else (sum(sum(model.PrcFlo[r,v,t,p,c,ts] * model.RS_FR[r,s,ts] * (1 + model.RTCS_FR[r,t,c,s,ts]) for v in model.RTP_VNT[r,t,p]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts]))) for p in model.RCIO_P[r,c,'OUT'] if model.RTP_VARA[r,p,t]) + 
                sum(sum(sum(model.IreFlo[r,v,t,p,c,ts,'IMP'] * model.RS_FR[r,s,ts] * (1 + model.RTCS_FR[r,t,c,s,ts]) for v in model.RTP_VNT[r,t,p]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts]) for p in model.RCIE_P[r,c,'IMP'] if model.RTP_VARA[r,p,t])) * model.COM_IE[r,t,c,s]) 
                ==
                sum((sum(sum(model.StgFlo[r,v,t,p,c,ts,'IN'] * model.RS_FR[r,s,ts] * (1 + model.RTCS_FR[r,t,c,s,ts]) for v in model.RTP_VNT[r,t,p]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts]) 
                if model.RPC_STG[r,p,c] else (sum(sum(model.PrcFlo[r,v,t,p,c,ts] * model.RS_FR[r,s,ts] * (1 + model.RTCS_FR[r,t,c,s,ts]) for v in model.RTP_VNT[r,t,p]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts]))) for p in model.RCIO_P[r,c,'IN'] if model.RTP_VARA[r,p,t]) + 
                sum(sum(sum(model.IreFlo[r,v,t,p,c,ts,'EXP'] * model.RS_FR[r,s,ts] * (1 + model.RTCS_FR[r,t,c,s,ts]) for v in model.RTP_VNT[r,t,p]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts]) for p in model.RCIE_P[r,c,'EXP'] if model.RTP_VARA[r,p,t]) + 
                model.RHS_COMBAL[r,t,c,s] * model.ComNet[r,t,c,s] + (model.COM_PROJ[r,t,c] * model.COM_FR[r,t,c,s] if model.COM_PROJ[r,t,c] else 0)) 
    else:
        return Constraint.Skip
model.EQE_COMBAL = Constraint(model.REGION, model.MILEYR, model.COMMTY, model.TSLICE, rule=EQE_COMBAL)
#
# ------- Commodity Production -------
#
def EQE_COMPRD(model,r,t,c,s):
    if (r,t,c,s,'FX') in model.RCS_COMPRD: 
        return (sum((sum(sum(model.StgFlo[r,v,t,p,c,ts,'OUT'] * model.RS_FR[r,s,ts] * (1+model.RTCS_FR[r,t,c,s,ts]) * model.STG_EFF[r,v,p] for v in model.RTP_VNT[r,t,p]) 
                        for ts in model.RPC_TS[r,p,c] if model.RS_RF[r,s,ts]) if model.RPC_STG[r,p,c] else sum(sum(model.PrcFlo[r,v,t,p,c,ts] * model.RS_FR[r,s,ts] * (1+model.RTCS_FR[r,t,c,s,ts]) 
                        for v in model.RTP_VNT[r,t,p]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts])) + sum(sum(sum(model.IreFlo[r,v,t,p,c,ts,'IMP'] * model.RS_FR[r,s,ts] * (1+model.RTCS_FR[r,t,c,s,ts]) 
                        for v in model.RTP_VNT[r,t,p]) for ts in model.RPC_TS[r,p,c] if model.RS_FR[r,s,ts]) for p in model.RCIE_P[r,c,'IMP'] 
                    if model.RTP_VARA[r,p,t]) for p in model.RCIO_P[r,c,'OUT'] if model.RTP_VARA[r,p,t]) * model.COM_IE[r,t,c,s] == model.ComPrd[r,t,c,s])
    else: 
        return Constraint.Skip
model.EQE_COMPRD = Constraint(model.REGION, model.MILEYR, model.COMMTY, model.TSLICE, rule=EQE_COMPRD)
#
# ------- Timeslice Storage Transformation -------
#
def EQ_STGTSS(model,r,v,y,p,s):
    if (r,p,s) in model.RPS_STG:
        return (model.PrcAct[r,v,y,p,s] == sum((model.PrcAct[r,v,y,p,all_s] + model.STG_CHRG[r,y,p,all_s] + sum(model.StgFlo[r,v,y,p,c,all_s,io] / 
                model.PRC_ACTFLO[r,v,p,c] * (1 if io=='IN' else -1) for (r,p,c,io) in model.TOP if (r,p,c) in model.PRC_STGTSS) + 
                    (model.PrcAct[r,v,y,p,s] + model.PrcAct[r,v,y,p,all_s]) / 2 * ((1-exp(min(0, model.STG_LOSS[r,v,p,all_s]) * model.G_YRFR[r,all_s] / 
                     model.RS_STGPRD[r,s])) + max(0, model.STG_LOSS[r,v,p,all_s]) * model.G_YRFR[r,all_s] / model.RS_STGPRD[r,s])) for all_s in model.TSLICE if (r,s,all_s) in model.RS_PRETS))
    else:
        return Constraint.Skip
model.EQ_STGTSS = Constraint(model.RTP_VINTYR, model.TSLICE, rule=EQ_STGTSS)
#
# ------- Output -------
#
model.dual = Suffix(direction=Suffix.IMPORT)
model.rc = Suffix(direction=Suffix.IMPORT)

def pyomo_save_results(options, instance, results):
    import os, sys
    wdir = os.getcwd()
    sys.path.append(wdir)
    
    from tiresults import df2csv, get_duals, get_rc, clean_df, mi_df    
    
    RegObj_cn=['OBV','REGION','CURENCY']
    RegObj_ocn=['REGION','OBV','CURENCY']
    
    PrcNcap_cn=['REGION','YEAR','PROCESS']
    PrcCap_cn=['REGION','YEAR','PROCESS']
    PrcAct_cn=['REGION','YEAR','T','PROCESS','TSLICE']
    PrcFlo_cn=['REGION','YEAR','T','PROCESS','COMMTY','TSLICE']
    IreFlo_cn=['REGION','YEAR','T','PROCESS','COMMTY','TSLICE','IE']
    
    EQE_COMPRD_cn=['REGION','YEAR','COMMTY','TSLICE']
    EQG_COMBAL_cn=['REGION','YEAR','COMMTY','TSLICE']
    
    # variables
    RegObj=df2csv(mi_df(instance.RegObj.get_values(),get_rc(instance,instance.RegObj),
                        RegObj_cn),RegObj_ocn,'OBJ')
    PrcCap=df2csv(mi_df(instance.PrcCap.get_values(),get_rc(instance,instance.PrcCap),
                        PrcCap_cn),PrcCap_cn,'CAP')
    PrcAct=df2csv(mi_df(instance.PrcAct.get_values(),get_rc(instance,instance.PrcAct),
                        PrcAct_cn),PrcAct_cn,'ACT')
    PrcFlo=df2csv(mi_df(instance.PrcFlo.get_values(),get_rc(instance,instance.PrcFlo),
                        PrcFlo_cn),PrcFlo_cn,'FLOW')
    IreFlo=df2csv(mi_df(instance.IreFlo.get_values(),get_rc(instance,instance.IreFlo),
                        IreFlo_cn),IreFlo_cn,'IRE')
    
    PrcNcap_duals={}
    PrcNcap_level=instance.PrcNcap.get_values()
    PrcNcap_rc=get_rc(instance,instance.PrcNcap)
    
    for (r,v,p) in instance.RTP:
        if (r,v,p) in PrcNcap_rc.keys():
            PrcNcap_duals[(r,v,p)] = PrcNcap_rc[(r,v,p)]
        elif instance.RTP_VARP[r,v,p]:
            PrcNcap_duals[(r,v,p)] = abs(instance.dual[instance.EQE_CPT[r,v,p]])
    
    PrcNcap_df = mi_df(PrcNcap_level,PrcNcap_duals,PrcNcap_cn)
    PrcNcap=df2csv(PrcNcap_df, PrcNcap_cn,'NCAP')     
    
    # equations
    COMPRD_duals={}
    COMPRD_level={}
    
    for (r,t,c,s,l) in instance.RCS_COMPRD:
            if l=='FX':
                COMPRD_level[(r,t,c,s)] = instance.ComPrd[r,t,c,s].value
                COMPRD_duals[(r,t,c,s)] = abs(instance.dual[instance.EQE_COMPRD[r,t,c,s]])
    
    COMPRD_df = mi_df(COMPRD_level,COMPRD_duals, EQE_COMPRD_cn)
    #COMPRD=df2csv(COMPRD_df,EQE_COMPRD_cn,'COMPRD')
    COMPRD_df.to_csv('COMPRD.csv', encoding='utf8', index=True)       
    
    COMBAL_duals={}
    COMBAL_level={}
    
    for (r,t,c,s) in instance.RTCS:
        if (r,t,c,s,'LO') in instance.RCS_COMBAL:
            COMBAL_level[(r,t,c,s)] = (float(instance.ComNet[r,t,c,s].value or 0) + 
                         instance.EQG_COMBAL[r,t,c,s].body())
            COMBAL_duals[(r,t,c,s)] = abs(instance.dual[instance.EQG_COMBAL[r,t,c,s]])
        elif (r,t,c,s,'FX') in instance.RCS_COMBAL:
            COMBAL_level[(r,t,c,s)] = instance.ComNet[r,t,c,s].value
            COMBAL_duals[(r,t,c,s)] = abs(instance.dual[instance.EQE_COMBAL[r,t,c,s]])
        else:
            COMBAL_level[(r,t,c,s)] = instance.ComNet[r,t,c,s].value
            
    COMBAL_df = mi_df(COMBAL_level,COMBAL_duals, EQG_COMBAL_cn)
    COMBAL=df2csv(COMBAL_df, EQG_COMBAL_cn, 'COMBAL')      

#def pyomo_print_results(options, instance, results):
#    from pyomo.core import Param
#    import pandas as pd
#
#    for p in instance.component_objects(Param):
#        print ("Parameter "+str(p))
#        parmobject = getattr(instance, str(p))
#        for index in parmobject:
#            print ("   ",index, value(parmobject[index]))
    
#    list_of_vars =[value(v[i]) for v in instance.component_objects(ctype=Var, active=True, descend_into=True) for i in ]
#    var_names =[v.name for v in instance.component_objects(ctype=Var, active=True, descend_into=True)]

#    print(list_of_vars)
#    print(var_names)

#    result_series = pd.Series(list_of_vars,index=var_names)
#    result_series.to_csv('my_results.csv')

# ============================================================================

