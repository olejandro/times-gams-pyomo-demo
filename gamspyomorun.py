import subprocess
from importlib import resources
from gamspy_base import directory
from gams.connect import ConnectDatabase

case = "UTOPIA"
sqlite_file = "PROTO.db3"
project_path = resources.files("gamsrun")

# Paths to resources
gams_path = resources.files("gamspy_base") / "gams.exe"
# Raise an error if gams_path does not exist
if not gams_path.exists():
    raise FileNotFoundError("gams.exe not found in the specified resources.")
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

cdb = ConnectDatabase(system_directory=directory)

# Read the GDX file
cdb.execute({
    'GDXReader': {
        'file': f"{case}.gdx",
        'symbols': 'all'
        }})

# Check if the sqlite file already exists and delete it if it does
if (project_path/sqlite_file).exists():
    (project_path/sqlite_file).unlink()

cdb.execute({
    'SQLWriter': {
        'connection': {'database': sqlite_file},
        'ifExists': 'replace',
        'connectionType': 'sqlite',
        'symbols': 'all'
        }})


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