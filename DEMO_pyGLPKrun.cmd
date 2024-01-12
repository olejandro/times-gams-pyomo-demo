SET CASE=UTOPIA
IF NOT %1.==. SET CASE=%1
IF %1.==0. SET CASE=UTOPIA
CALL GAMS %CASE%.RUN IDIR=source PS=0 GDX=%CASE% GDXCOMPRESS=1 --EXTSOL=YES
IF %1.==0. PAUSE
GAMS\gdx2sqlite -i %CASE%.gdx -o PROTO.db3 -small -fast
IF %1.==0. PAUSE
pyomo solve --solver=glpk --solver-executable=GLPK/glpsol --symbolic-solver-labels --stream-solver --report-timing --tempdir=%cd% tipyomo.py loadall.dat
PAUSE
CALL GAMS %CASE%.RUN IDIR=source PS=0 GDX=%CASE% GDXCOMPRESS=1 --EXTSOL=yes
GAMS\GDX2VEDA %CASE% source\times2veda.vdd %CASE%-PYOMO
PAUSE
