import subprocess
from importlib import resources

case = "UTOPIA"
project_path = resources.files("gamsrun")

# Paths to resources
gams_path = resources.files("gamspy_base") / "gams.exe"
gdx2sqlite_path = project_path / "GAMS" / "gdx2sqlite.exe"
gdx2veda_path = project_path / "GAMS" / "GDX2VEDA.exe"
times2veda_path = project_path / "source" / "times2veda.vdd"

# Command to execute gams.exe
gams_command = [
    gams_path,
    f"{case}.RUN",
    "IDIR=source",
    "PS=0",
    f"GDX={case}",
    "GDXCOMPRESS=1",
    "--EXTSOL=YES",
]

# Command to execute gdx2sqlite
gdx2sqlite_command = [
    gdx2sqlite_path,
    "-i",
    f"{case}.gdx",
    "-o",
    "PROTO.db3",
    "-small",
    "-fast",
]

# pyomo solve --solver=glpk --solver-executable=GLPK/glpsol --symbolic-solver-labels --stream-solver --report-timing --tempdir=%cd% tipyomo.py loadall.dat
pyomo_command = [
    "pyomo",
    "solve",
    "--solver=glpk",
    "--solver-executable=GLPK/glpsol",
    "--symbolic-solver-labels",
    "--stream-solver",
    "--report-timing",
    f"--tempdir={project_path}",
    "tipyomo.py",
    "loadall.dat",
]   

# Command to execute gdx2veda.exe
gdx2veda_command = [
    gdx2veda_path,
    f"{case}",
    times2veda_path,
    f"{case}-PYOMO",
]

# Execute subprocesses
subprocess.run(gams_command)
subprocess.run(gdx2sqlite_command)
subprocess.run(pyomo_command)
subprocess.run(gams_command)
subprocess.run(gdx2veda_command)