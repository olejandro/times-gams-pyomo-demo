import subprocess
from importlib import resources

case = "UTOPIA"

# Path to gams.exe
gams_path = resources.files("gamspy_base") / "gams.exe"

# Command to execute gams.exe
command = [
    gams_path,
    f"{case}.RUN",
    "IDIR=source",
    "PS=0",
    f"GDX={case}-GAMS",
    "GDXCOMPRESS=1",
    f"O={case}-GAMS.LST",
]

# Execute gams.exe
subprocess.run(command)
