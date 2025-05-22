
# Rearm validator 

The purpose of this notebook is to check the data files in the ReArm clinical trial, and to run basic corrections. 

The `Rearm` directory contains the experimental files, organized by patient (e.g., `ReArm_C1P02`), then by visit (e.g., `ReArm_C1P02_20210306_V1`), then by type of information (e.g., `Accelerometry`):


# Usage

1. Run the notebook named `main`in the `notebooks` directory.
2. Check the output at the end of this notebook. 
3. Optional: manually copy the output and save it to a file for further reference.

# Requirements
- The ReArm dataset is not public: 
  - You have to symlink Rearm as `dat/ReArm.lnk` (i.e., in the `dat` directory).
    - On a windows system:  `mklink /D dat\ReArm.lnk C:\path\to\ReArm\dataset`.
    - On a linux-OSX system: `ln -s /path/to/ReArm/dataset dat/ReArm.lnk`.

- Python 3.9 or later
- Required packages: 
  - basic tools: `numpy`, `matplotlib`, ...   
  - vscode jupyter tools: `ipykernel`, `ipython`, `qt`, ...
  - `pyxdf` from conda-forge (https://anaconda.org/conda-forge/pyxdf)
  - `openmovement` using pip (https://github.com/digitalinteraction/openmovement-python)


You can install them by running the conda commands below:

```bash
conda create -n Rearm               # Create a new environment
conda activate Rearm                # Activate the environment
conda env create -f rearm.yml       # Create the environment from the yml file    
```




# Outputs

The output of the notebooks consists in `.log` and `.csv` or `.tsv` files stored next to the data files. 

The most important files are:

- Kinect timestamp correction: 
  - `*_time_correction.csv`: the value to add to the kinect timestamps in the corresponding `*.xdf` file. 
- Computation of the panu score:
  - In each visit: `panu.log`: the log of the panu process, with warnings.
  - In each patient: `*_panu_png.pdf`: the visualization of the data used to compute the panu score.
  - In ReArm: `panu.csv`: the database of the panu for all ReArm.

# Bug, issue and enhancements

Please report any bug, issue or enhancement request using the GitHub [issue tracker](https://github.com/DenisMot/Rearm-Validator/issues) for this repository.