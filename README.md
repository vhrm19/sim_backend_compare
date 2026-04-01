# Reproducing the benchmark results

This repository contains the implementations and execution scripts used to benchmark GPU-oriented Python backends for 2D acoustic wave simulation.

## What this repository does

The project compares multiple simulators built on top of different Python GPU frameworks, using the same acoustic FDTD benchmark setup. The evaluation includes:

* runtime
* GPU memory usage
* GPU utilization
* reflected energy at the boundaries
* implementation effort, for the ranking stage

The aggregation script `run_and_collect_all.py` automates the execution of every simulator found in the repository, collects metrics, and generates summary files.

## Requirements

You need:

* Python 3.12 or newer
* `numpy`
* `pandas`
* NVIDIA drivers with `nvidia-smi` available in the command line
* an NVIDIA GPU, for the GPU benchmarks
* the same backend dependencies required by each simulator, for example CuPy, PyTorch, Taichi, Numba, WebGPU bindings, depending on the implementation you want to run

A practical setup is to use a virtual environment and install the Python dependencies first.

## Repository structure expected by the script

The collection script assumes the following layout:

* `sim_*.py`, simulator scripts to be benchmarked
* `setups/dot/dot_without_plots.json`, base configuration file
* `setups/dot/results/`, folder where simulator result text files are stored
* `logs/`, folder created automatically for NVIDIA SMI logs

The script skips files named `sim_cpu_*.py` when searching for simulators.

## Benchmark workflow

The script `run_and_collect_all.py` does the following:

1. finds every simulator matching `sim_*.py`
2. creates a temporary configuration from `setups/dot/dot_without_plots.json`
3. runs each simulator for five ROI sizes
4. monitors GPU usage with `nvidia-smi` every 200 ms
5. extracts runtime and reflected energy from the simulator stdout or result files
6. writes summary tables in TSV and CSV format

The ROI sizes used by default are:

* 1000 x 1000
* 2000 x 2000
* 3000 x 3000
* 4000 x 4000
* 5000 x 5000

## How to run

From the repository root, execute:

```bash
python run_and_collect_all.py
```

During the run, the script will generate a temporary configuration file at `setups/dot/dot_temp_runtime.json`, one log file per simulator and ROI inside `logs/`, and the final outputs `summary_gpu_memory_times.tsv` and `detailed_results.csv`.

## Expected simulator output

To allow the script to collect the runtime and reflected energy, each simulator should print, or save in its result file, lines compatible with these patterns:

* `Tempo medio total (inclui transferencia de dados): ... s`
* `Energia refletida (sensor): ...`

If these values are not found in stdout, the script looks inside `setups/dot/results/result_*<sim_name>*__desc.txt`.

## Main output files

### `summary_gpu_memory_times.tsv`

Contains one row per simulator and the aggregated metrics for each ROI size.

### `detailed_results.csv`

Contains one row per simulator and ROI, with the raw measurements used to build the summary.

### `logs/*.csv`

Contains the raw `nvidia-smi` samples collected during each execution.

## Notes for reproducibility

For a fair comparison, keep the following consistent across runs:

* same GPU and driver version
* same Python version and package versions
* same simulator implementations
* same base configuration file
* same ROI sizes and number of iterations

The benchmark reported in the paper used a standardized setup with fixed physical parameters and varied only the ROI size across the tested cases.

## Common issues

### `nvidia-smi` not found

Make sure the NVIDIA driver is installed correctly and that `nvidia-smi` works from a terminal.

### No simulators are detected

Check whether the simulator files follow the `sim_*.py` naming pattern and are located in the repository root.

### Missing runtime or energy values

Verify that each simulator prints the expected text or saves a compatible result file in `setups/dot/results/`.

### Missing Python dependencies

Install the backend-specific packages required by the simulator you are running. Some implementations require CUDA-enabled libraries, while others depend on framework-specific packages.
