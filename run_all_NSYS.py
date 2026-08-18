import glob
import subprocess
import os
import sys

output_dir = "nsys_data"
os.makedirs(output_dir, exist_ok=True)

env = os.environ.copy()
env["PYTHONPATH"] = os.pathsep.join(sys.path)

files = [f for f in glob.glob("sim_*.py") if not os.path.basename(f).startswith("sim_cpu_")]
print("Scripts found (GPU):", files)

nsys_path = r"C:\Program Files\NVIDIA Corporation\Nsight Systems 2025.3.2\target-windows-x64\nsys.exe"

for file in files:
    base_name = os.path.splitext(os.path.basename(file))[0]
    rep_file = os.path.join(output_dir, f"perfil_{base_name}.nsys-rep")

    print(f"\n### Profiling {file} com Nsight Systems ###")

    profile_cmd = [
        nsys_path,
        "profile",
        "--trace=cuda,wddm",
        "--gpu-metrics-devices=all",
        "--force-overwrite=true",
        "--wddm-additional-events=true",
        "--stats=true",
        f"--output={os.path.splitext(rep_file)[0]}",
        "python",
        file,
        "-c",
        os.path.join(".", "ensaios", "ponto", "ponto_sem_plots.json")
    ]

    result = subprocess.run(profile_cmd, capture_output=True, text=True, env=env)
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
