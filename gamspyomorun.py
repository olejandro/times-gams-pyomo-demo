import subprocess
from pathlib import Path
from gamspy_base import directory
from gams.connect import ConnectDatabase
from tipyomo import pyomo_times_model 

case = "UTOPIA"
sqlite_file = "model_data.db3"

# Paths to resources
gams_path = Path(directory) / "gams.exe"
# Raise an error if gams_path does not exist
if not gams_path.exists():
    raise FileNotFoundError("gams.exe not found in the specified resources.")

gdx2veda_path = Path("libs") / "GDX2VEDA.exe"
times2veda_path = Path("source") / "times2veda.vdd"

# Command to create the GDX file
create_gdx = [
    gams_path,
    f"{case}.RUN",
    "IDIR=source",
    "PS=0",
    f"GDX={case}",
    "GDXCOMPRESS=1",
    "--EXTSOL=YES",
]
subprocess.run(create_gdx)
# Read the created GDX file and convert it to SQLite
cdb = ConnectDatabase(system_directory=directory)
# Read the GDX file
cdb.execute({
    'GDXReader': {
        'file': f"{case}.gdx",
        'symbols': 'all'
        }})
# Check if the sqlite file already exists and delete it if it does
if Path(sqlite_file).exists():
    print(f"Deleting existing SQLite file: {sqlite_file}")
    Path(sqlite_file).unlink()
# Create the SQLite database
cdb.execute({
    'SQLWriter': {
        'connection': {'database': sqlite_file},
        'ifExists': 'replace',
        'connectionType': 'sqlite',
        'symbols': 'all',
        'skipText': True,
        }})

# pyomo solve --solver=glpk --solver-executable=GLPK/glpsol --symbolic-solver-labels --stream-solver --report-timing --tempdir=%cd% tipyomo.py loadall.dat
execute_pyomo = [
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
subprocess.run(execute_pyomo)

# Command to execute gdx2veda.exe
gdx2veda_command = [
    gdx2veda_path,
    f"{case}",
    times2veda_path,
    f"{case}-PYOMO",
]

# Execute subprocesses

subprocess.run(gams_command)
subprocess.run(gdx2veda_command)