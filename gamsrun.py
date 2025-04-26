import subprocess
from pathlib import Path
from gamspy_base import directory

case = "UTOPIA"

# Paths to resources
gams_path = Path(directory) / "gams.exe"
gdx2veda_path = Path("libs") / "GDX2VEDA.exe"
times2veda_path = Path("source") / "times2veda.vdd"

commands = {
    "GAMS": [
        gams_path,
        f"{case}.RUN",
        "IDIR=source",
        "PS=0",
        f"GDX={case}-GAMS",
        "GDXCOMPRESS=1",
        f"O={case}-GAMS.LST",
        ],
    "gdx2veda": [
        gdx2veda_path,
        f"{case}-GAMS",
        times2veda_path,
        f"{case}-GAMS",
        ]
}

# Execute subprocesses
for name, command in commands.items():
    print(f"Executing {name}...")
    subprocess.run(command)

