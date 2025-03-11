# ReactiveTransportAnalyser
# Reactive Transport Analyzer for CO₂ Reactions

# Overview

This tutorial provides a structured workflow for conducting single-phase flow simulations, aligning flow field images, analyzing voxel distributions, and evaluating mineral transport within a porous medium. It includes step-by-step instructions on input files, expected outputs, and usage of key scripts for data processing.

# Procedure

# 1. Single-Phase Flow Simulation

The single-phase flow simulator can be found here **[Porefoam1f](https://github.com/ImperialCollegeLondon/poreFoam-singlePhase)**.

# Input Files:

- Segmented Image: The image should be segmented into two phases: pore space and rock.

  - Label 0: Pore

  - Label 1: Rock

**(See screenshot_1)**

- MHD File **(See screenshot_2)**

# Required Output Files:

- Velocity Files: Velocities at the cell face (Ufx, Ufy, Ufz) **(See screenshot_3)**

  - Used as an input for the image alignment code.

- Summary File **(See screenshot_3)**

  - Contains permeability, connected porosity, and velocity distribution (probability density functions, PDFs).

- OpenMelnParaview.foam **(See screenshot_3)**

  - Used for visualizing the velocity field in Paraview.

**Note:** The output folder from the single-phase simulation contains many files (See screenshot_3).

# 2. Image Alignment Code

This code corrects the misalignment between the flow field image and the segmented image used in the single-phase simulation. The misalignment occurs because the simulator outputs velocities at the cell face (Ufx, Ufy, Ufz) instead of at the cell center (Ux, Uy, Uz). The code adjusts for this discrepancy and calculates the velocity magnitude.

# Input Files:

- Velocities at the cell face (Ufx, Ufy, Ufz) (See screenshot_3)

# Output File:

- Flow Field Image (See screenshot_4)

# 3. Voxel Count & Pore Exposure Analysis (VoxelNumber_and_FacesToPore)

The VoxelNumber_and_FacesToPore script calculates:

- The number of voxels for each label in the segmented image:

  - Label 0: Outer layer

  - Label 1: Pore

  - Label 2: Microporous phase

  - Label 3: Dolomite

  - Label 4: Calcite

  - Label 5: Anhydrite
  
**(See screenshot_5)**

- The number of faces of all other labels that are exposed to the pore label.

**Note:** This script requires two segmented images: one at T1 = x and another at T2 = x+1 or T2 = x+y, where y is an integer.

# Input Files:

- Two segmented images with labels **(See screenshot_5)**.

# Output File:

- Excel Spreadsheet containing (See screenshot_6):

- Number of voxels for each label in both images.

- Difference in voxel count between T1 and T2.

- Number of faces to pore label in both images.

# 4. Mineral Distribution Analysis

The Mineral Distribution Code calculates the number of voxels for each label at the face of a flow region and those moving away from the face.

The flow regions are defined as fast channels and slow regions.
![Fast channel defination](https://github.com/user-attachments/assets/679eae56-5d64-47c6-abf9-b7b0c64fe35a)

Distance maps (fastflowdistmap.tif and slowregionsdistmap.tif) are used in combination with the segmented image.

The script outputs the voxel count for all labels at the face and away from the face in both fast and slow regions **(See screenshot_7)**.

# Input Files:

- Distance maps (fastflowdistmap.tif, slowregionsdistmap.tif)

- Segmented image with labels (See screenshot_7)

# Output File:

- Excel Spreadsheet containing (See screenshot_8):

- Number of voxels at the face and away from the face for all labels in fast and slow regions.




## References
...

## Contact
For any inquiries, please contact **Sajjad Foroughi** at [s.foroughi@imperial.ac.uk] or **Olatunbosun Adedipe** at [o.adedipe23@imperial.ac.uk]
