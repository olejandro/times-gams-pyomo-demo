from pyomo.environ import *
from math import exp

mdl = AbstractModel()

# %% System sets
mdl.YEAR = Set(initialize=[0]) | RangeSet(1900, 2200)
mdl.INOUT = Set()
mdl.IMPEXP = Set()
mdl.LIM = Set()
mdl.TSLVL = Set()
mdl.COM_TYPE = Set()
mdl.PRC_GRP = Set()
mdl.UPT = Set()
mdl.UC_GRPTYPE = Set()
mdl.UC_NAME = Set()
mdl.UC_COST = Set(within=mdl.UC_NAME)
mdl.COSTAGG = Set()

# %% User input sets
mdl.MILEYR = Set(within=mdl.YEAR)
mdl.MODLYR = Set(within=mdl.YEAR)
mdl.TSLICE = Set()
mdl.REGION = Set()
mdl.PROCESS = Set()
mdl.COMMTY = Set()
mdl.COMGRP = Set()
mdl.CURENCY = Set()

# %% Internal sets (all simple sets for now)
mdl.OBV = Set()
mdl.TS_MAP = Set(within=mdl.REGION * mdl.TSLICE * mdl.TSLICE)
mdl.RS_TREE = Set(within=mdl.REGION * mdl.TSLICE * mdl.TSLICE)
mdl.RS_PRETS = Set(within=mdl.REGION * mdl.TSLICE * mdl.TSLICE)
mdl.RC = Set(within=mdl.REGION * mdl.COMMTY)
mdl.DEM = Set(within=mdl.REGION * mdl.COMMTY)
mdl.RP = Set(within=mdl.REGION * mdl.PROCESS)
mdl.RP_FLO = Set(within=mdl.REGION * mdl.PROCESS)
mdl.RP_STD = Set(within=mdl.REGION * mdl.PROCESS)
mdl.RP_IRE = Set(within=mdl.REGION * mdl.PROCESS)
mdl.RP_STG = Param(mdl.REGION, mdl.PROCESS, within=Binary, default=0)
mdl.RP_PGACT = Param(mdl.REGION, mdl.PROCESS, within=Binary, default=0)
mdl.RP_PGFLO = Param(mdl.REGION, mdl.PROCESS, within=Binary, default=0)
mdl.PRC_ACT = Param(mdl.RP, within=Binary, default=0)
mdl.RDCUR = Set(within=mdl.REGION * mdl.CURENCY)
mdl.COM_GMAP = Set(within=mdl.REGION * mdl.COMGRP * mdl.COMMTY)
mdl.COM_ISMEM = Param(mdl.REGION, mdl.COMGRP, mdl.COMMTY, within=Binary, default=0)
mdl.TOP = Set(within=mdl.REGION * mdl.PROCESS * mdl.COMMTY * mdl.INOUT)
mdl.PRC_VINT = Param(mdl.RP, within=Binary, default=0)
mdl.PRC_TS = Set(within=mdl.REGION * mdl.PROCESS * mdl.TSLICE)
mdl.RPS_S1 = Set(within=mdl.REGION * mdl.PROCESS * mdl.TSLICE)
mdl.RPS_STG = Set(within=mdl.REGION * mdl.PROCESS * mdl.TSLICE)
mdl.RPC = Set(within=mdl.REGION * mdl.PROCESS * mdl.COMMTY)
mdl.RPC_PG = Set(within=mdl.REGION * mdl.PROCESS * mdl.COMMTY)
mdl.RPC_IRE = Set(within=mdl.REGION * mdl.PROCESS * mdl.COMMTY * mdl.IMPEXP)
mdl.RPC_STG = Param(mdl.RPC, within=Binary, default=0)
mdl.PRC_STGTSS = Set(within=mdl.REGION * mdl.PROCESS * mdl.COMMTY)
mdl.RPG_ACE = Set(within=mdl.REGION * mdl.PROCESS * mdl.COMGRP * mdl.INOUT)
mdl.RPC_ACE = Set(within=mdl.REGION * mdl.PROCESS * mdl.COMMTY)
mdl.RPCS_VAR = Set(within=mdl.REGION * mdl.PROCESS * mdl.COMMTY * mdl.TSLICE)
mdl.RPCC_FFUNC = Set(within=mdl.REGION * mdl.PROCESS * mdl.COMGRP * mdl.COMGRP)
mdl.RCS_COMBAL = Set(within=mdl.REGION * mdl.MILEYR * mdl.COMMTY * mdl.TSLICE * mdl.LIM)
mdl.RCS_COMPRD = Set(within=mdl.REGION * mdl.MILEYR * mdl.COMMTY * mdl.TSLICE * mdl.LIM)
mdl.RTDEM = Set(within=mdl.REGION * mdl.MODLYR * mdl.COMMTY)
mdl.RTCS = Set(within=mdl.REGION * mdl.MODLYR * mdl.COMMTY * mdl.TSLICE)
mdl.RHS_COMPRD = Param(mdl.RTCS, within=Binary, default=0)
mdl.RHS_COMBAL = Param(mdl.RTCS, within=Binary, default=0)
mdl.RTP = Set(within=mdl.REGION * mdl.MODLYR * mdl.PROCESS)
mdl.RTP_VARA = Param(mdl.RP, mdl.MILEYR, within=Binary, default=0)
mdl.RTP_VARP = Param(mdl.RTP, within=Binary, default=0)
mdl.RTP_VINTYR = Set(within=mdl.REGION * mdl.MODLYR * mdl.MILEYR * mdl.PROCESS)
mdl.RTP_CPTYR = Set(within=mdl.REGION * mdl.MODLYR * mdl.MILEYR * mdl.PROCESS)
mdl.AFS = Set(within=mdl.REGION * mdl.MILEYR * mdl.PROCESS * mdl.TSLICE * mdl.LIM)
mdl.IS_LINT = Set(within=mdl.REGION * mdl.MODLYR * mdl.MODLYR * mdl.CURENCY)
mdl.IS_CAPBND = Set(within=mdl.REGION * mdl.YEAR * mdl.PROCESS * mdl.LIM)
mdl.IS_NCAPBD = Set(within=mdl.REGION * mdl.YEAR * mdl.PROCESS * mdl.LIM)
mdl.RP_PTRAN = Set(
    within=mdl.REGION * mdl.PROCESS * mdl.COMGRP * mdl.COMGRP * mdl.TSLICE
)
mdl.IS_SHAR = Set(
    within=mdl.REGION
    * mdl.YEAR
    * mdl.PROCESS
    * mdl.COMMTY
    * mdl.COMGRP
    * mdl.TSLICE
    * mdl.LIM
)
mdl.IS_ACOST = Set(within=mdl.REGION * mdl.MODLYR * mdl.PROCESS * mdl.CURENCY)

# %% Parameters
mdl.G_YRFR = Param(mdl.REGION, mdl.TSLICE)
mdl.RS_STGPRD = Param(mdl.REGION, mdl.TSLICE)
mdl.RS_STGAV = Param(mdl.REGION, mdl.TSLICE)
mdl.RS_FR = Param(mdl.REGION, mdl.TSLICE, mdl.TSLICE, default=0)
mdl.RTCS_FR = Param(
    mdl.REGION, mdl.MILEYR, mdl.COMMTY, mdl.TSLICE, mdl.TSLICE, default=0
)
mdl.COM_PROJ = Param(mdl.REGION, mdl.YEAR, mdl.COMMTY, default=0)
mdl.COM_IE = Param(mdl.REGION, mdl.YEAR, mdl.COMMTY, mdl.TSLICE)
mdl.COM_FR = Param(mdl.REGION, mdl.YEAR, mdl.COMMTY, mdl.TSLICE)
mdl.PRC_CAPACT = Param(mdl.REGION, mdl.PROCESS)
mdl.PRC_SC = Param(mdl.REGION, mdl.PROCESS, default=0)
mdl.PRC_ACTFLO = Param(mdl.REGION, mdl.YEAR, mdl.PROCESS, mdl.COMGRP, default=0)
mdl.CAP_BND = Param(mdl.REGION, mdl.YEAR, mdl.PROCESS, mdl.LIM, default=0)
mdl.NCAP_BND = Param(mdl.REGION, mdl.YEAR, mdl.PROCESS, mdl.LIM)
mdl.NCAP_PASTI = Param(mdl.REGION, mdl.MODLYR, mdl.PROCESS, default=0)
mdl.COEF_CPT = Param(mdl.REGION, mdl.MODLYR, mdl.MILEYR, mdl.PROCESS, default=0)
mdl.COEF_AF = Param(
    mdl.REGION, mdl.MODLYR, mdl.MILEYR, mdl.PROCESS, mdl.TSLICE, mdl.LIM, default=0
)
mdl.COEF_PTRAN = Param(
    mdl.REGION,
    mdl.MODLYR,
    mdl.PROCESS,
    mdl.COMGRP,
    mdl.COMMTY,
    mdl.COMGRP,
    mdl.TSLICE,
    default=0,
)
mdl.FLO_SHAR = Param(
    mdl.REGION, mdl.YEAR, mdl.PROCESS, mdl.COMMTY, mdl.COMGRP, mdl.TSLICE, mdl.LIM
)
mdl.STG_EFF = Param(mdl.REGION, mdl.YEAR, mdl.PROCESS)
mdl.STG_LOSS = Param(mdl.REGION, mdl.YEAR, mdl.PROCESS, mdl.TSLICE, default=0)
mdl.STG_CHRG = Param(mdl.REGION, mdl.YEAR, mdl.PROCESS, mdl.TSLICE, default=0)
mdl.ACT_EFF = Param(
    mdl.REGION, mdl.YEAR, mdl.PROCESS, mdl.COMGRP, mdl.TSLICE, default=0
)

# %% Cost parameters
mdl.OBJ_PVT = Param(mdl.REGION, mdl.MILEYR, mdl.CURENCY)
mdl.OBJ_LINT = Param(mdl.REGION, mdl.MILEYR, mdl.MODLYR, mdl.CURENCY, default=0)
mdl.OBJ_ACOST = Param(mdl.REGION, mdl.MODLYR, mdl.PROCESS, mdl.CURENCY, default=0)
mdl.OBJ_IPRIC = Param(
    mdl.REGION,
    mdl.YEAR,
    mdl.PROCESS,
    mdl.COMMTY,
    mdl.TSLICE,
    mdl.IMPEXP,
    mdl.CURENCY,
    default=0,
)
mdl.COEF_OBINV = Param(mdl.REGION, mdl.MODLYR, mdl.PROCESS, mdl.CURENCY, default=0)
mdl.COEF_OBFIX = Param(mdl.REGION, mdl.MODLYR, mdl.PROCESS, mdl.CURENCY, default=0)


def MILE(mdl, y):
    if y in mdl.MILEYR:
        return 1
    else:
        return 0


mdl.MILE = Param(mdl.MODLYR, initialize=MILE, default=0, within=Binary)

mdl.RP_AIRE = Param(mdl.RP_IRE, mdl.IMPEXP, default=0, within=Binary)


def ISRP(mdl, r, p):
    if (r, p) in mdl.RP:
        return 1
    else:
        return 0


mdl.ISRP = Param(mdl.REGION, mdl.PROCESS, initialize=ISRP, default=0, within=Binary)

mdl.RP_ISIRE = Param(mdl.REGION, mdl.PROCESS, default=0, within=Binary)
mdl.RTP_IPRI = Param(
    mdl.REGION, mdl.PROCESS, mdl.MILEYR, mdl.CURENCY, default=0, within=Binary
)


def LINTY(mdl, r, t, cur):
    return (y for y in mdl.MODLYR if (r, t, y, cur) in mdl.IS_LINT)


mdl.LINTY = Set(mdl.REGION, mdl.MILEYR, mdl.CURENCY, initialize=LINTY)


def RTP_VNT(mdl, r, t, p):
    return (y for y in mdl.MODLYR if (r, y, t, p) in mdl.RTP_VINTYR)


mdl.RTP_VNT = Set(mdl.RTP, initialize=RTP_VNT)


def RTP_CPT(mdl, r, t, p):
    return (y for y in mdl.MODLYR if (r, y, t, p) in mdl.RTP_CPTYR)


mdl.RTP_CPT = Set(mdl.RTP, initialize=RTP_CPT)


def RTP_AFS(mdl, r, t, p, l):
    return (s for s in mdl.TSLICE if (r, t, p, s, l) in mdl.AFS)


mdl.RTP_AFS = Set(mdl.RTP, mdl.LIM, initialize=RTP_AFS)


def RP_TS(mdl, r, p):
    return (s for s in mdl.TSLICE if (r, p, s) in mdl.PRC_TS)


mdl.RP_TS = Set(mdl.RP, initialize=RP_TS)


def RP_S1(mdl, r, p):
    return (s for s in mdl.TSLICE if (r, p, s) in mdl.RPS_S1)


mdl.RP_S1 = Set(mdl.RP, initialize=RP_S1)


def RP_PGC(mdl, r, p):
    return (c for c in mdl.COMMTY if (r, p, c) in mdl.RPC_PG)


mdl.RP_PGC = Set(mdl.RP, initialize=RP_PGC)


def RP_CIE(mdl, r, p):
    return (
        (c, ie) for (c, ie) in mdl.COMMTY * mdl.IMPEXP if (r, p, c, ie) in mdl.RPC_IRE
    )


mdl.RP_CIE = Set(mdl.RP_IRE, dimen=2, initialize=RP_CIE)


def RPC_TS(mdl, r, p, c):
    return (s for s in mdl.TSLICE if (r, p, c, s) in mdl.RPCS_VAR)


mdl.RPC_TS = Set(mdl.RPC, initialize=RPC_TS)


def RPIO_C(mdl, r, p, io):
    return (c for c in mdl.COMMTY if (r, p, c, io) in mdl.TOP)


mdl.RPIO_C = Set(mdl.RP, mdl.INOUT, initialize=RPIO_C)


def RCIO_P(mdl, r, c, io):
    return (p for p in mdl.PROCESS if (r, p, c, io) in mdl.TOP)


mdl.RCIO_P = Set(mdl.RC, mdl.INOUT, initialize=RCIO_P)


def RCIE_P(mdl, r, c, ie):
    return (p for p in mdl.PROCESS if (r, p, c, ie) in mdl.RPC_IRE)


mdl.RCIE_P = Set(mdl.RC, mdl.IMPEXP, initialize=RCIE_P)


def RP_ACE(mdl, r, p):
    return (c for c in mdl.COMMTY if (r, p, c) in mdl.RPC_ACE)


mdl.RP_ACE = Set(mdl.RP, initialize=RP_ACE)

# %% Variables
mdl.RegObj = Var(mdl.OBV, mdl.REGION, mdl.CURENCY, within=NonNegativeReals, dense=False)
mdl.ComPrd = Var(
    mdl.REGION, mdl.MILEYR, mdl.COMMTY, mdl.TSLICE, within=NonNegativeReals, dense=False
)
mdl.ComNet = Var(
    mdl.REGION, mdl.MILEYR, mdl.COMMTY, mdl.TSLICE, within=NonNegativeReals, dense=False
)


def PrcCap_bounds(mdl, r, y, p):
    if (r, y, p, "LO") in mdl.IS_CAPBND:
        lb = value(mdl.CAP_BND[r, y, p, "LO"])
    else:
        lb = 0
    if (r, y, p, "UP") in mdl.IS_CAPBND:
        ub = value(mdl.CAP_BND[r, y, p, "UP"])
    else:
        ub = float("inf")
    return (lb, ub)


mdl.PrcCap = Var(mdl.REGION, mdl.MODLYR, mdl.PROCESS, bounds=PrcCap_bounds, dense=False)


def PrcNcap_bounds(mdl, r, y, p):
    if (r, y, p, "LO") in mdl.IS_NCAPBD:
        lb = value(mdl.NCAP_BND[r, y, p, "LO"])
    else:
        lb = 0
    if (r, y, p, "UP") in mdl.IS_NCAPBD:
        ub = value(mdl.NCAP_BND[r, y, p, "UP"])
    else:
        ub = float("inf")
    return (lb, ub)


mdl.PrcNcap = Var(
    mdl.REGION, mdl.MODLYR, mdl.PROCESS, bounds=PrcNcap_bounds, dense=False
)
mdl.PrcAct = Var(
    mdl.REGION,
    mdl.YEAR,
    mdl.MILEYR,
    mdl.PROCESS,
    mdl.TSLICE,
    within=NonNegativeReals,
    dense=False,
)
mdl.PrcFlo = Var(
    mdl.REGION,
    mdl.YEAR,
    mdl.MILEYR,
    mdl.PROCESS,
    mdl.COMMTY,
    mdl.TSLICE,
    within=NonNegativeReals,
    dense=False,
)
mdl.IreFlo = Var(
    mdl.REGION,
    mdl.YEAR,
    mdl.MILEYR,
    mdl.PROCESS,
    mdl.COMMTY,
    mdl.TSLICE,
    mdl.IMPEXP,
    within=NonNegativeReals,
    dense=False,
)
mdl.StgFlo = Var(
    mdl.REGION,
    mdl.YEAR,
    mdl.MILEYR,
    mdl.PROCESS,
    mdl.COMMTY,
    mdl.TSLICE,
    mdl.INOUT,
    within=NonNegativeReals,
    dense=False,
)


# %% Objective Function


def obj_rule(mdl):
    return sum(mdl.RegObj[o, r, cur] for o in mdl.OBV for (r, cur) in mdl.RDCUR)


mdl.obj = Objective(rule=obj_rule, sense=minimize)


def EQ_OBJINV(mdl, r, cur):
    return (
        sum(
            mdl.OBJ_PVT[r, t, cur]
            * mdl.COEF_CPT[r, v, t, p]
            * mdl.COEF_OBINV[r, v, p, cur]
            * (
                (mdl.PrcNcap[r, v, p] if v in mdl.MILEYR else 0)
                + mdl.NCAP_PASTI[r, v, p]
            )
            for (r, v, t, p) in mdl.RTP_CPTYR
            if mdl.COEF_OBINV[r, v, p, cur]
        )
        == mdl.RegObj["OBJINV", r, cur]
    )


mdl.EQ_OBJINV = Constraint(mdl.RDCUR, rule=EQ_OBJINV)


def EQ_OBJFIX(mdl, r, cur):
    return (
        sum(
            mdl.OBJ_PVT[r, t, cur]
            * mdl.COEF_CPT[r, v, t, p]
            * mdl.COEF_OBFIX[r, v, p, cur]
            * (
                (mdl.PrcNcap[r, v, p] if v in mdl.MILEYR else 0)
                + mdl.NCAP_PASTI[r, v, p]
            )
            for (r, v, t, p) in mdl.RTP_CPTYR
            if mdl.COEF_OBFIX[r, v, p, cur]
        )
        == mdl.RegObj["OBJFIX", r, cur]
    )


mdl.EQ_OBJFIX = Constraint(mdl.RDCUR, rule=EQ_OBJFIX)


def EQ_OBJVAR(mdl, r, cur):
    return (
        sum(
            sum(
                (
                    (
                        sum(
                            mdl.OBJ_LINT[r, t, y, cur] * mdl.OBJ_ACOST[r, y, p, cur]
                            for y in mdl.LINTY[r, t, cur]
                        )
                        * sum(
                            mdl.PrcAct[r, v, t, p, s]
                            * (mdl.RS_STGAV[r, s] if mdl.RP_STG[r, p] else 1)
                            for v in mdl.RTP_VNT[r, t, p]
                            for s in mdl.RP_TS[r, p]
                        )
                    )
                    if mdl.OBJ_ACOST[r, t, p, cur]
                    else 0
                )
                + (
                    (
                        sum(
                            sum(
                                mdl.OBJ_LINT[r, t, y, cur]
                                * mdl.OBJ_IPRIC[r, y, p, c, s, ie, cur]
                                for y in mdl.LINTY[r, t, cur]
                            )
                            * sum(
                                mdl.IreFlo[r, v, t, p, c, s, ie]
                                for v in mdl.RTP_VNT[r, t, p]
                            )
                            for s in mdl.RP_TS[r, p]
                            for (c, ie) in mdl.RP_CIE[r, p]
                        )
                    )
                    if mdl.RTP_IPRI[r, p, t, cur]
                    else 0
                )
                for t in mdl.MILEYR
                if mdl.RTP_VARA[r, p, t]
            )
            for p in mdl.PROCESS
            if mdl.ISRP[r, p]
        )
        == mdl.RegObj["OBJVAR", r, cur]
    )


mdl.EQ_OBJVAR = Constraint(mdl.RDCUR, rule=EQ_OBJVAR)


# %% Activity to Primary Group


def EQ_ACTFLO(mdl, r, v, t, p, s):
    if mdl.PRC_ACT[r, p] and s in mdl.RP_TS[r, p]:
        return mdl.RTP_VARA[r, p, t] * mdl.PrcAct[r, v, t, p, s] == sum(
            (
                sum(
                    mdl.IreFlo[r, v, t, p, c, s, ie]
                    for ie in mdl.IMPEXP
                    if mdl.RP_AIRE[r, p, ie]
                )
                if mdl.RP_ISIRE[r, p]
                else mdl.PrcFlo[r, v, t, p, c, s]
            )
            for c in mdl.RP_PGC[r, p]
        )
    else:
        return Constraint.Skip


mdl.EQ_ACTFLO = Constraint(mdl.RTP_VINTYR, mdl.TSLICE, rule=EQ_ACTFLO)


# %% Activity to Capacity


def EQL_CAPACT(mdl, r, v, y, p, s):
    if s in mdl.RTP_AFS[r, y, p, "UP"]:
        return (
            sum(
                mdl.PrcAct[r, v, y, p, ts]
                * mdl.RS_FR[r, ts, s]
                * exp(mdl.PRC_SC[r, p])
                / mdl.RS_STGPRD[r, s]
                for ts in mdl.RP_TS[r, p]
                if mdl.RS_FR[r, s, ts]
            )
            if mdl.RP_STG[r, p]
            else sum(
                mdl.PrcAct[r, v, y, p, ts]
                for ts in mdl.RP_TS[r, p]
                if mdl.RS_FR[r, s, ts]
            )
        ) <= (
            (1 if mdl.RP_STG[r, p] else mdl.G_YRFR[r, s])
            * mdl.PRC_CAPACT[r, p]
            * (
                mdl.COEF_AF[r, v, y, p, s, "UP"]
                * mdl.COEF_CPT[r, v, y, p]
                * (
                    (mdl.PrcNcap[r, v, p] if mdl.MILE[v] else 0)
                    + mdl.NCAP_PASTI[r, v, p]
                )
                if mdl.PRC_VINT[r, p]
                else sum(
                    mdl.COEF_AF[r, m, y, p, s, "UP"]
                    * mdl.COEF_CPT[r, m, y, p]
                    * (
                        (mdl.PrcNcap[r, m, p] if mdl.MILE[m] else 0)
                        + mdl.NCAP_PASTI[r, m, p]
                    )
                    for m in mdl.RTP_CPT[r, y, p]
                )
            )
        )
    else:
        return Constraint.Skip


mdl.EQL_CAPACT = Constraint(mdl.RTP_VINTYR, mdl.TSLICE, rule=EQL_CAPACT)


def EQE_CAPACT(mdl, r, v, y, p, s):
    if s in mdl.RTP_AFS[r, y, p, "FX"]:
        return (
            sum(
                mdl.PrcAct[r, v, y, p, ts]
                * mdl.RS_FR[r, ts, s]
                * exp(mdl.PRC_SC[r, p])
                / mdl.RS_STGPRD[r, s]
                for ts in mdl.RP_TS[r, p]
                if mdl.RS_FR[r, s, ts]
            )
            if mdl.RP_STG[r, p]
            else sum(
                mdl.PrcAct[r, v, y, p, ts]
                for ts in mdl.RP_TS[r, p]
                if mdl.RS_FR[r, s, ts]
            )
        ) == (
            (1 if mdl.RP_STG[r, p] else mdl.G_YRFR[r, s])
            * mdl.PRC_CAPACT[r, p]
            * (
                mdl.COEF_AF[r, v, y, p, s, "FX"]
                * mdl.COEF_CPT[r, v, y, p]
                * (
                    (mdl.PrcNcap[r, v, p] if mdl.MILE[v] else 0)
                    + mdl.NCAP_PASTI[r, v, p]
                )
                if mdl.PRC_VINT[r, p]
                else sum(
                    mdl.COEF_AF[r, m, y, p, s, "FX"]
                    * mdl.COEF_CPT[r, m, y, p]
                    * (
                        (mdl.PrcNcap[r, m, p] if mdl.MILE[m] else 0)
                        + mdl.NCAP_PASTI[r, m, p]
                    )
                    for m in mdl.RTP_CPT[r, y, p]
                )
            )
        )
    else:
        return Constraint.Skip


mdl.EQE_CAPACT = Constraint(mdl.RTP_VINTYR, mdl.TSLICE, rule=EQE_CAPACT)


# %% Capacity Transfer


def EQE_CPT(mdl, r, y, p):
    if mdl.RTP_VARP[r, y, p] or mdl.CAP_BND[r, y, p, "FX"]:
        return (
            mdl.PrcCap[r, y, p] if mdl.RTP_VARP[r, y, p] else mdl.CAP_BND[r, y, p, "FX"]
        ) == sum(
            mdl.COEF_CPT[r, v, y, p]
            * ((mdl.MILE[v] * mdl.PrcNcap[r, v, p]) + mdl.NCAP_PASTI[r, v, p])
            for v in mdl.RTP_CPT[r, y, p]
        )
    else:
        return Constraint.Skip


mdl.EQE_CPT = Constraint(mdl.RTP, rule=EQE_CPT)


def EQL_CPT(mdl, r, y, p):
    if not mdl.RTP_VARP[r, y, p] and mdl.CAP_BND[r, y, p, "LO"]:
        return (
            mdl.PrcCap[r, y, p] if mdl.RTP_VARP[r, y, p] else mdl.CAP_BND[r, y, p, "LO"]
        ) <= sum(
            mdl.COEF_CPT[r, v, y, p]
            * ((mdl.MILE[v] * mdl.PrcNcap[r, v, p]) + mdl.NCAP_PASTI[r, v, p])
            for v in mdl.RTP_CPT[r, y, p]
        )
    else:
        return Constraint.Skip


mdl.EQL_CPT = Constraint(mdl.RTP, rule=EQL_CPT)


def EQG_CPT(mdl, r, y, p):
    if not mdl.RTP_VARP[r, y, p] and mdl.CAP_BND[r, y, p, "UP"]:
        return (
            mdl.PrcCap[r, y, p] if mdl.RTP_VARP[r, y, p] else mdl.CAP_BND[r, y, p, "UP"]
        ) >= sum(
            mdl.COEF_CPT[r, v, y, p]
            * ((mdl.MILE[v] * mdl.PrcNcap[r, v, p]) + mdl.NCAP_PASTI[r, v, p])
            for v in mdl.RTP_CPT[r, y, p]
        )
    else:
        return Constraint.Skip


mdl.EQG_CPT = Constraint(mdl.RTP, rule=EQG_CPT)


# %% Process Flow Shares


def EQL_FLOSHR(mdl, r, v, p, c, cg, s, l, t):
    if (
        mdl.RTP_VARA[r, p, t]
        and v in mdl.RTP_VNT[r, t, p]
        and s in mdl.RPC_TS[r, p, c]
        and l == "LO"
    ):
        return (
            sum(
                mdl.FLO_SHAR[r, v, p, c, cg, s, l]
                * sum(
                    mdl.PrcFlo[r, v, t, p, com, ts] * mdl.RS_FR[r, s, ts]
                    for com in mdl.RPIO_C[r, p, io]
                    for ts in mdl.RPC_TS[r, p, com]
                    if mdl.COM_ISMEM[r, cg, com] and mdl.RS_FR[r, s, ts]
                )
                for io in mdl.INOUT
                if c in mdl.RPIO_C[r, p, io]
            )
            <= mdl.PrcFlo[r, v, t, p, c, s]
        )
    else:
        return Constraint.Skip


mdl.EQL_FLOSHR = Constraint(mdl.IS_SHAR, mdl.MILEYR, rule=EQL_FLOSHR)


def EQG_FLOSHR(mdl, r, v, p, c, cg, s, l, t):
    if (
        mdl.RTP_VARA[r, p, t]
        and v in mdl.RTP_VNT[r, t, p]
        and s in mdl.RPC_TS[r, p, c]
        and l == "UP"
    ):
        return (
            sum(
                mdl.FLO_SHAR[r, v, p, c, cg, s, l]
                * sum(
                    mdl.PrcFlo[r, v, t, p, com, ts] * mdl.RS_FR[r, s, ts]
                    for com in mdl.RPIO_C[r, p, io]
                    for ts in mdl.RPC_TS[r, p, com]
                    if mdl.COM_ISMEM[r, cg, com] and mdl.RS_FR[r, s, ts]
                )
                for io in mdl.INOUT
                if c in mdl.RPIO_C[r, p, io]
            )
            >= mdl.PrcFlo[r, v, t, p, c, s]
        )
    else:
        return Constraint.Skip


mdl.EQG_FLOSHR = Constraint(mdl.IS_SHAR, mdl.MILEYR, rule=EQG_FLOSHR)


def EQE_FLOSHR(mdl, r, v, p, c, cg, s, l, t):
    if (
        mdl.RTP_VARA[r, p, t]
        and v in mdl.RTP_VNT[r, t, p]
        and s in mdl.RPC_TS[r, p, c]
        and l == "FX"
    ):
        return (
            sum(
                mdl.FLO_SHAR[r, v, p, c, cg, s, l]
                * sum(
                    mdl.PrcFlo[r, v, t, p, com, ts] * mdl.RS_FR[r, s, ts]
                    for com in mdl.RPIO_C[r, p, io]
                    for ts in mdl.RPC_TS[r, p, com]
                    if mdl.COM_ISMEM[r, cg, com] and mdl.RS_FR[r, s, ts]
                )
                for io in mdl.INOUT
                if c in mdl.RPIO_C[r, p, io]
            )
            == mdl.PrcFlo[r, v, t, p, c, s]
        )
    else:
        return Constraint.Skip


mdl.EQE_FLOSHR = Constraint(mdl.IS_SHAR, mdl.MILEYR, rule=EQE_FLOSHR)


# %% Activity efficiency


def EQE_ACTEFF(mdl, r, p, cg, io, t, v, s):
    #    if not mdl.RTP_VARA[r,p,t]:
    #        v = Set()
    #    if s in mdl.RP_S1[r,p] and (v in mdl.RTP_VNT[r,t,p] or v==()):
    if s in mdl.RP_S1[r, p] and mdl.RTP_VARA[r, p, t] and v in mdl.RTP_VNT[r, t, p]:
        return sum(
            sum(
                mdl.PrcFlo[r, v, t, p, c, ts]
                * (mdl.ACT_EFF[r, v, p, c, ts] if mdl.ACT_EFF[r, v, p, c, ts] else 1)
                * mdl.RS_FR[r, s, ts]
                * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                for ts in mdl.RPC_TS[r, p, c]
                if mdl.RS_FR[r, s, ts]
            )
            for c in mdl.RP_ACE[r, p]
            if mdl.COM_ISMEM[r, cg, c]
        ) == sum(
            mdl.RS_FR[r, s, ts]
            * (
                sum(
                    (
                        mdl.PrcAct[r, v, t, p, ts]
                        if mdl.RP_PGACT[r, p]
                        else mdl.PrcFlo[r, v, t, p, c, ts] / mdl.PRC_ACTFLO[r, v, p, c]
                    )
                    / (
                        mdl.ACT_EFF[r, v, p, c, ts]
                        if mdl.ACT_EFF[r, v, p, c, ts]
                        else 1
                    )
                    * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                    for c in mdl.RP_PGC[r, p]
                )
                if mdl.RP_PGFLO[r, p]
                else mdl.PrcAct[r, v, t, p, ts]
            )
            / max(1e-6, mdl.ACT_EFF[r, v, p, cg, ts])
            for ts in mdl.RP_TS[r, p]
            if mdl.RS_FR[r, s, ts]
        )
    else:
        return Constraint.Skip


mdl.EQE_ACTEFF = Constraint(
    mdl.RPG_ACE, mdl.MILEYR, mdl.MODLYR, mdl.TSLICE, rule=EQE_ACTEFF
)


# %% Process Transformation


def EQ_PTRANS(mdl, r, p, cg1, cg2, s1, t, v, s):
    #    if not mdl.RTP_VARA[r,p,t]:
    #        v = Set()
    #    if mdl.RS_FR[r,s1,s] and s in mdl.RP_S1[r,p] and (v in mdl.RTP_VNT[r,t,p] or v==()):
    if (
        mdl.RS_FR[r, s1, s]
        and s in mdl.RP_S1[r, p]
        and mdl.RTP_VARA[r, p, t]
        and v in mdl.RTP_VNT[r, t, p]
    ):
        return sum(
            sum(
                mdl.PrcFlo[r, v, t, p, c, ts]
                * mdl.RS_FR[r, s, ts]
                * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                for ts in mdl.RPC_TS[r, p, c]
                if mdl.RS_FR[r, s, ts]
            )
            for io in mdl.INOUT
            for c in mdl.RPIO_C[r, p, io]
            if mdl.COM_ISMEM[r, cg2, c]
        ) == sum(
            mdl.COEF_PTRAN[r, v, p, cg1, c, cg2, ts]
            * mdl.RS_FR[r, s, ts]
            * (1 + mdl.RTCS_FR[r, t, c, s, ts])
            * mdl.PrcFlo[r, v, t, p, c, ts]
            for io in mdl.INOUT
            for c in mdl.RPIO_C[r, p, io]
            for ts in mdl.RPC_TS[r, p, c]
            if (mdl.COEF_PTRAN[r, v, p, cg1, c, cg2, ts] if mdl.RS_FR[r, s, ts] else 0)
        )
    else:
        return Constraint.Skip


mdl.EQ_PTRANS = Constraint(
    mdl.RP_PTRAN, mdl.MILEYR, mdl.MODLYR, mdl.TSLICE, rule=EQ_PTRANS
)


# %% Commodity Balance - Greater


def EQG_COMBAL(mdl, r, t, c, s):
    if (r, t, c, s, "LO") in mdl.RCS_COMBAL:
        return (
            mdl.ComPrd[r, t, c, s]
            if mdl.RHS_COMPRD[r, t, c, s]
            else (
                sum(
                    (
                        sum(
                            sum(
                                mdl.StgFlo[r, v, t, p, c, ts, "OUT"]
                                * mdl.RS_FR[r, s, ts]
                                * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                                * mdl.STG_EFF[r, v, p]
                                for v in mdl.RTP_VNT[r, t, p]
                            )
                            for ts in mdl.RPC_TS[r, p, c]
                            if mdl.RS_FR[r, s, ts]
                        )
                        if mdl.RPC_STG[r, p, c]
                        else (
                            sum(
                                sum(
                                    mdl.PrcFlo[r, v, t, p, c, ts]
                                    * mdl.RS_FR[r, s, ts]
                                    * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                                    for v in mdl.RTP_VNT[r, t, p]
                                )
                                for ts in mdl.RPC_TS[r, p, c]
                                if mdl.RS_FR[r, s, ts]
                            )
                        )
                    )
                    for p in mdl.RCIO_P[r, c, "OUT"]
                    if mdl.RTP_VARA[r, p, t]
                )
                + sum(
                    sum(
                        sum(
                            mdl.IreFlo[r, v, t, p, c, ts, "IMP"]
                            * mdl.RS_FR[r, s, ts]
                            * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                            for v in mdl.RTP_VNT[r, t, p]
                        )
                        for ts in mdl.RPC_TS[r, p, c]
                        if mdl.RS_FR[r, s, ts]
                    )
                    for p in mdl.RCIE_P[r, c, "IMP"]
                    if mdl.RTP_VARA[r, p, t]
                )
            )
            * mdl.COM_IE[r, t, c, s]
        ) >= sum(
            (
                sum(
                    sum(
                        mdl.StgFlo[r, v, t, p, c, ts, "IN"]
                        * mdl.RS_FR[r, s, ts]
                        * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                        for v in mdl.RTP_VNT[r, t, p]
                    )
                    for ts in mdl.RPC_TS[r, p, c]
                    if mdl.RS_FR[r, s, ts]
                )
                if mdl.RPC_STG[r, p, c]
                else (
                    sum(
                        sum(
                            mdl.PrcFlo[r, v, t, p, c, ts]
                            * mdl.RS_FR[r, s, ts]
                            * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                            for v in mdl.RTP_VNT[r, t, p]
                        )
                        for ts in mdl.RPC_TS[r, p, c]
                        if mdl.RS_FR[r, s, ts]
                    )
                )
            )
            for p in mdl.RCIO_P[r, c, "IN"]
            if mdl.RTP_VARA[r, p, t]
        ) + sum(
            sum(
                sum(
                    mdl.IreFlo[r, v, t, p, c, ts, "EXP"]
                    * mdl.RS_FR[r, s, ts]
                    * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                    for v in mdl.RTP_VNT[r, t, p]
                )
                for ts in mdl.RPC_TS[r, p, c]
                if mdl.RS_FR[r, s, ts]
            )
            for p in mdl.RCIE_P[r, c, "EXP"]
            if mdl.RTP_VARA[r, p, t]
        ) + (
            mdl.COM_PROJ[r, t, c] * mdl.COM_FR[r, t, c, s]
            if mdl.COM_PROJ[r, t, c]
            else 0
        )
    else:
        return Constraint.Skip


mdl.EQG_COMBAL = Constraint(
    mdl.REGION, mdl.MILEYR, mdl.COMMTY, mdl.TSLICE, rule=EQG_COMBAL
)


# %% Commodity Balance - Equal


def EQE_COMBAL(mdl, r, t, c, s):
    if (r, t, c, s, "FX") in mdl.RCS_COMBAL:
        return (
            mdl.ComPrd[r, t, c, s]
            if mdl.RHS_COMPRD[r, t, c, s]
            else (
                sum(
                    (
                        sum(
                            sum(
                                mdl.StgFlo[r, v, t, p, c, ts, "OUT"]
                                * mdl.RS_FR[r, s, ts]
                                * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                                * mdl.STG_EFF[r, v, p]
                                for v in mdl.RTP_VNT[r, t, p]
                            )
                            for ts in mdl.RPC_TS[r, p, c]
                            if mdl.RS_FR[r, s, ts]
                        )
                        if mdl.RPC_STG[r, p, c]
                        else (
                            sum(
                                sum(
                                    mdl.PrcFlo[r, v, t, p, c, ts]
                                    * mdl.RS_FR[r, s, ts]
                                    * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                                    for v in mdl.RTP_VNT[r, t, p]
                                )
                                for ts in mdl.RPC_TS[r, p, c]
                                if mdl.RS_FR[r, s, ts]
                            )
                        )
                    )
                    for p in mdl.RCIO_P[r, c, "OUT"]
                    if mdl.RTP_VARA[r, p, t]
                )
                + sum(
                    sum(
                        sum(
                            mdl.IreFlo[r, v, t, p, c, ts, "IMP"]
                            * mdl.RS_FR[r, s, ts]
                            * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                            for v in mdl.RTP_VNT[r, t, p]
                        )
                        for ts in mdl.RPC_TS[r, p, c]
                        if mdl.RS_FR[r, s, ts]
                    )
                    for p in mdl.RCIE_P[r, c, "IMP"]
                    if mdl.RTP_VARA[r, p, t]
                )
            )
            * mdl.COM_IE[r, t, c, s]
        ) == sum(
            (
                sum(
                    sum(
                        mdl.StgFlo[r, v, t, p, c, ts, "IN"]
                        * mdl.RS_FR[r, s, ts]
                        * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                        for v in mdl.RTP_VNT[r, t, p]
                    )
                    for ts in mdl.RPC_TS[r, p, c]
                    if mdl.RS_FR[r, s, ts]
                )
                if mdl.RPC_STG[r, p, c]
                else (
                    sum(
                        sum(
                            mdl.PrcFlo[r, v, t, p, c, ts]
                            * mdl.RS_FR[r, s, ts]
                            * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                            for v in mdl.RTP_VNT[r, t, p]
                        )
                        for ts in mdl.RPC_TS[r, p, c]
                        if mdl.RS_FR[r, s, ts]
                    )
                )
            )
            for p in mdl.RCIO_P[r, c, "IN"]
            if mdl.RTP_VARA[r, p, t]
        ) + sum(
            sum(
                sum(
                    mdl.IreFlo[r, v, t, p, c, ts, "EXP"]
                    * mdl.RS_FR[r, s, ts]
                    * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                    for v in mdl.RTP_VNT[r, t, p]
                )
                for ts in mdl.RPC_TS[r, p, c]
                if mdl.RS_FR[r, s, ts]
            )
            for p in mdl.RCIE_P[r, c, "EXP"]
            if mdl.RTP_VARA[r, p, t]
        ) + mdl.RHS_COMBAL[
            r, t, c, s
        ] * mdl.ComNet[
            r, t, c, s
        ] + (
            mdl.COM_PROJ[r, t, c] * mdl.COM_FR[r, t, c, s]
            if mdl.COM_PROJ[r, t, c]
            else 0
        )
    else:
        return Constraint.Skip


mdl.EQE_COMBAL = Constraint(
    mdl.REGION, mdl.MILEYR, mdl.COMMTY, mdl.TSLICE, rule=EQE_COMBAL
)


# %% Commodity Production


def EQE_COMPRD(mdl, r, t, c, s):
    if (r, t, c, s, "FX") in mdl.RCS_COMPRD:
        return (
            sum(
                (
                    sum(
                        sum(
                            mdl.StgFlo[r, v, t, p, c, ts, "OUT"]
                            * mdl.RS_FR[r, s, ts]
                            * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                            * mdl.STG_EFF[r, v, p]
                            for v in mdl.RTP_VNT[r, t, p]
                        )
                        for ts in mdl.RPC_TS[r, p, c]
                        if mdl.RS_RF[r, s, ts]
                    )
                    if mdl.RPC_STG[r, p, c]
                    else sum(
                        sum(
                            mdl.PrcFlo[r, v, t, p, c, ts]
                            * mdl.RS_FR[r, s, ts]
                            * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                            for v in mdl.RTP_VNT[r, t, p]
                        )
                        for ts in mdl.RPC_TS[r, p, c]
                        if mdl.RS_FR[r, s, ts]
                    )
                )
                + sum(
                    sum(
                        sum(
                            mdl.IreFlo[r, v, t, p, c, ts, "IMP"]
                            * mdl.RS_FR[r, s, ts]
                            * (1 + mdl.RTCS_FR[r, t, c, s, ts])
                            for v in mdl.RTP_VNT[r, t, p]
                        )
                        for ts in mdl.RPC_TS[r, p, c]
                        if mdl.RS_FR[r, s, ts]
                    )
                    for p in mdl.RCIE_P[r, c, "IMP"]
                    if mdl.RTP_VARA[r, p, t]
                )
                for p in mdl.RCIO_P[r, c, "OUT"]
                if mdl.RTP_VARA[r, p, t]
            )
            * mdl.COM_IE[r, t, c, s]
            == mdl.ComPrd[r, t, c, s]
        )
    else:
        return Constraint.Skip


mdl.EQE_COMPRD = Constraint(
    mdl.REGION, mdl.MILEYR, mdl.COMMTY, mdl.TSLICE, rule=EQE_COMPRD
)


# %% Timeslice Storage Transformation


def EQ_STGTSS(mdl, r, v, y, p, s):
    if (r, p, s) in mdl.RPS_STG:
        return mdl.PrcAct[r, v, y, p, s] == sum(
            (
                mdl.PrcAct[r, v, y, p, all_s]
                + mdl.STG_CHRG[r, y, p, all_s]
                + sum(
                    mdl.StgFlo[r, v, y, p, c, all_s, io]
                    / mdl.PRC_ACTFLO[r, v, p, c]
                    * (1 if io == "IN" else -1)
                    for (r, p, c, io) in mdl.TOP
                    if (r, p, c) in mdl.PRC_STGTSS
                )
                + (mdl.PrcAct[r, v, y, p, s] + mdl.PrcAct[r, v, y, p, all_s])
                / 2
                * (
                    (
                        1
                        - exp(
                            min(0, mdl.STG_LOSS[r, v, p, all_s])
                            * mdl.G_YRFR[r, all_s]
                            / mdl.RS_STGPRD[r, s]
                        )
                    )
                    + max(0, mdl.STG_LOSS[r, v, p, all_s])
                    * mdl.G_YRFR[r, all_s]
                    / mdl.RS_STGPRD[r, s]
                )
            )
            for all_s in mdl.TSLICE
            if (r, s, all_s) in mdl.RS_PRETS
        )
    else:
        return Constraint.Skip


mdl.EQ_STGTSS = Constraint(mdl.RTP_VINTYR, mdl.TSLICE, rule=EQ_STGTSS)

# %% Output

mdl.dual = Suffix(direction=Suffix.IMPORT)
mdl.rc = Suffix(direction=Suffix.IMPORT)


def pyomo_save_results(options, instance, results):
    import os, sys

    wdir = os.getcwd()
    sys.path.append(wdir)

    from tiresults import df2csv, get_duals, get_rc, clean_df, mi_df

    RegObj_cn = ["OBV", "REGION", "CURENCY"]
    RegObj_ocn = ["REGION", "OBV", "CURENCY"]

    PrcNcap_cn = ["REGION", "YEAR", "PROCESS"]
    PrcCap_cn = ["REGION", "YEAR", "PROCESS"]
    PrcAct_cn = ["REGION", "YEAR", "T", "PROCESS", "TSLICE"]
    PrcFlo_cn = ["REGION", "YEAR", "T", "PROCESS", "COMMTY", "TSLICE"]
    IreFlo_cn = ["REGION", "YEAR", "T", "PROCESS", "COMMTY", "TSLICE", "IE"]

    EQE_COMPRD_cn = ["REGION", "YEAR", "COMMTY", "TSLICE"]
    EQG_COMBAL_cn = ["REGION", "YEAR", "COMMTY", "TSLICE"]

    # variables
    RegObj = df2csv(
        mi_df(
            instance.RegObj.get_values(), get_rc(instance, instance.RegObj), RegObj_cn
        ),
        RegObj_ocn,
        "OBJ",
    )
    PrcCap = df2csv(
        mi_df(
            instance.PrcCap.get_values(), get_rc(instance, instance.PrcCap), PrcCap_cn
        ),
        PrcCap_cn,
        "CAP",
    )
    PrcAct = df2csv(
        mi_df(
            instance.PrcAct.get_values(), get_rc(instance, instance.PrcAct), PrcAct_cn
        ),
        PrcAct_cn,
        "ACT",
    )
    PrcFlo = df2csv(
        mi_df(
            instance.PrcFlo.get_values(), get_rc(instance, instance.PrcFlo), PrcFlo_cn
        ),
        PrcFlo_cn,
        "FLOW",
    )
    IreFlo = df2csv(
        mi_df(
            instance.IreFlo.get_values(), get_rc(instance, instance.IreFlo), IreFlo_cn
        ),
        IreFlo_cn,
        "IRE",
    )

    PrcNcap_duals = {}
    PrcNcap_level = instance.PrcNcap.get_values()
    PrcNcap_rc = get_rc(instance, instance.PrcNcap)

    for r, v, p in instance.RTP:
        if (r, v, p) in PrcNcap_rc.keys():
            PrcNcap_duals[(r, v, p)] = PrcNcap_rc[(r, v, p)]
        elif instance.RTP_VARP[r, v, p]:
            PrcNcap_duals[(r, v, p)] = abs(instance.dual[instance.EQE_CPT[r, v, p]])

    PrcNcap_df = mi_df(PrcNcap_level, PrcNcap_duals, PrcNcap_cn)
    PrcNcap = df2csv(PrcNcap_df, PrcNcap_cn, "NCAP")

    # equations
    COMPRD_duals = {}
    COMPRD_level = {}

    for r, t, c, s, l in instance.RCS_COMPRD:
        if l == "FX":
            COMPRD_level[(r, t, c, s)] = instance.ComPrd[r, t, c, s].value
            COMPRD_duals[(r, t, c, s)] = abs(
                instance.dual[instance.EQE_COMPRD[r, t, c, s]]
            )

    COMPRD_df = mi_df(COMPRD_level, COMPRD_duals, EQE_COMPRD_cn)
    # COMPRD=df2csv(COMPRD_df,EQE_COMPRD_cn,'COMPRD')
    COMPRD_df.to_csv("COMPRD.csv", encoding="utf8", index=True)

    COMBAL_duals = {}
    COMBAL_level = {}

    for r, t, c, s in instance.RTCS:
        if (r, t, c, s, "LO") in instance.RCS_COMBAL:
            COMBAL_level[(r, t, c, s)] = (
                float(instance.ComNet[r, t, c, s].value or 0)
                + instance.EQG_COMBAL[r, t, c, s].body()
            )
            COMBAL_duals[(r, t, c, s)] = abs(
                instance.dual[instance.EQG_COMBAL[r, t, c, s]]
            )
        elif (r, t, c, s, "FX") in instance.RCS_COMBAL:
            COMBAL_level[(r, t, c, s)] = instance.ComNet[r, t, c, s].value
            COMBAL_duals[(r, t, c, s)] = abs(
                instance.dual[instance.EQE_COMBAL[r, t, c, s]]
            )
        else:
            COMBAL_level[(r, t, c, s)] = instance.ComNet[r, t, c, s].value

    COMBAL_df = mi_df(COMBAL_level, COMBAL_duals, EQG_COMBAL_cn)
    COMBAL = df2csv(COMBAL_df, EQG_COMBAL_cn, "COMBAL")


# def pyomo_print_results(options, instance, results):
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
