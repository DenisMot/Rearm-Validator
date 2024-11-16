
# Rearm validator 

The purpose of this notebook is to verify the presence of the expected data files for the ReArm clinical trial. 

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
- Required packages: `numpy`, `matplotlib`, `pyxdf`, `openmovement`. You can install them by running the conda commands below:  

```bash
conda create -n Rearm               # Create a new environment
conda activate Rearm                # Activate the environment
conda install numpy matplotlib      # Install numpy and matplotlib
conda install conda-forge::pyxdf    # Install pyxdf from conda-forge (https://anaconda.org/conda-forge/pyxdf)
pip install openmovement            # Install openmovement using pip (https://github.com/digitalinteraction/openmovement-python)
```




# Outputs

The output of this notebook consists in `.log` and `.tsv` files stored in the directory of each checked visit.  
The files are:

- `checkFilesInRearmVisit.log`:  summary of the checks performed in the visit. 
- `goodfiles.log`:  list of expected files that were found in the visit. 
- `kinect_to_mouse_delay.tsv`: the delay between the kinect and the mouse in the .xdf files.

# Bug, issue and enhancements

Please report any bug, issue or enhancement request using the GitHub [issue tracker](https://github.com/DenisMot/Rearm-Validator/issues) for this repository.