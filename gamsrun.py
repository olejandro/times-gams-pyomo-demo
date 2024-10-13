import subprocess
from importlib import resources

case = "UTOPIA"

# Paths to resources
gams_path = resources.files("gamspy_base") / "gams.exe"
gdx2veda_path = resources.files("gamsrun") / "GAMS" / "GDX2VEDA.exe"
times2veda_path = resources.files("gamsrun") / "source" / "times2veda.vdd"

# Command to execute gams.exe
gams_command = [
    gams_path,
    f"{case}.RUN",
    "IDIR=source",
    "PS=0",
    f"GDX={case}-GAMS",
    "GDXCOMPRESS=1",
    f"O={case}-GAMS.LST",
]

# Command to execute gdx2veda.exe
gdx2veda_command = [
    gdx2veda_path,
    f"{case}-GAMS",
    times2veda_path,
    f"{case}-GAMS",
]

# Execute subprocesses
subprocess.run(gams_command)
subprocess.run(gdx2veda_command)