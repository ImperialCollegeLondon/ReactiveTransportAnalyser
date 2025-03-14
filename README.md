# ReactiveTransportAnalyser
# Reactive Transport Analyzer for CO₂ Reactions

# Overview

This tutorial provides a structured workflow for conducting single-phase flow simulations, aligning flow field images, analyzing voxel distributions, and evaluating mineral transport within a porous medium. It includes step-by-step instructions on input files, expected outputs, and usage of key scripts for data processing.

**Note:** The example shown is Sample A at 33 min (488 PV).

# Procedure

# 1. Single-Phase Flow Simulation

The single-phase flow simulator can be found here **[Porefoam1f](https://github.com/ImperialCollegeLondon/poreFoam-singlePhase)**.

# Input Files:

- Segmented Image: The image should be segmented into two phases: pore space and rock.

  - Label 0: Pore

  - Label 1: Rock

**Note:** If Avizo is used, the 'Exterior' material is alway Label 0 and is everything that isn't segmented into another material. So everything needs to be segmented except the pore space so that it would be the only thing in the 'Exterior' material and have the  Label 0. Also, the outer layer has to be segmented as rock so that flow is only simulated through the pore space.  

**(See Screenshot 1)**

**Screenshot 1: Image Segmentation for Single-Phase Flow Simulation (Avizo 3D 2023)**

**Segmenting Pore**
![screenshot_1a](https://github.com/user-attachments/assets/58b38132-fd44-4356-89fd-a43c23aa82e4)

**Segmenting Rock (rock + outer layer) - (Incorrect Labeling)**
![screenshot_1b](https://github.com/user-attachments/assets/ef7dab19-ea63-47a4-ac9d-f367f338d1e1)
![screenshot_1d](https://github.com/user-attachments/assets/abc5b16c-1e30-4652-b35e-dcad2906f67d)

**Correct Labeling**
![screenshot_1c](https://github.com/user-attachments/assets/463cf521-94ba-4770-9e6b-51bd1d96b652)
![screenshot_1e](https://github.com/user-attachments/assets/0df49207-2ad8-47b5-982c-335751c414a0)


- .MHD File **(See Screenshot 2)**
  
**Screenshot 2: Contents of .MHD file (Notepad)**
![screenshot_2](https://github.com/user-attachments/assets/93bc9505-7d97-4c73-9a4d-c578f5e0dfe1)

**Single-phase Flow Simulation Input Files**

![screenshot_1f](https://github.com/user-attachments/assets/1a39f5fd-9f03-4aa7-92f8-d7aca7e57176)

**Screenshot 3: Contents of Simulation Output Folder**

![screenshot_3](https://github.com/user-attachments/assets/7f900e04-f3e2-4a7e-b305-a0c62408cffd)


# Required Output Files:

- Velocity Files: Velocities at the cell face (Ufx, Ufy, Ufz) **(See Screenshot 3)**

  - Used as an input for the image alignment code.

- Summary File **(See Screenshot 3 & Screenshot 4)**
  
**Screenshot 4: Contents of Summary File**

![screenshot_4](https://github.com/user-attachments/assets/44069493-c5b5-4b1b-be08-02639f27c0de)


  - Contains permeability, connected porosity, and velocity distribution (probability density functions, PDFs).

- OpenMelnParaview.foam **(See Screenshot 3)**

  - Used for visualizing the velocity field in Paraview.


# 2. Image Alignment Code

This code corrects the misalignment between the flow field image and the segmented image used in the single-phase simulation. The misalignment occurs because the simulator outputs velocities at the cell face (Ufx, Ufy, Ufz) instead of at the cell center (Ux, Uy, Uz). The code adjusts for this discrepancy and calculates the velocity magnitude.

# Input Files:

- Velocities at the cell face (Ufx, Ufy, Ufz) (See Screenshot 3)

# Output File:

- Flow Field Image (See Screenshot 5)

**Screenshot 5: Output Folder from Image Alignment Code**

![screenshot_5](https://github.com/user-attachments/assets/3022c1fa-72fa-48c5-a739-092716b8bf2a)


# 3. Voxel Count & Pore Exposure Analysis (VoxelNumber_and_FacesToPore)

The VoxelNumber_and_FacesToPore script calculates:

- The number of voxels for each label in the segmented image:

  - Label 1: Outer layer

  - Label 2: Pore

  - Label 3: Microporous phase

  - Label 4: Dolomite

  - Label 5: Calcite

  - Label 6: Anhydrite
 
    **Note: Label 0 is ignored**
  
**(See Screenshot 6)**

- The number of faces of all other labels that are exposed to the pore label.

**Note:** This script requires two segmented images: one at T1 = x and another at T2 = x+1 or T2 = x+y, where y is an integer.

# Input Files:

- Two segmented images with labels **(See Screenshot 6)**.

**Screenshot 6: Segmented Image (Label 1 to 5)**

![screenshot_6a](https://github.com/user-attachments/assets/d455bebb-2b4f-40cf-8d63-dbcc5eb4c72b)


# Output File:

- Excel Spreadsheet containing (See Screenshot 7):

- Number of voxels for each label in both images.

- Difference in voxel count between T1 and T2.

- Number of faces to pore label in both images.

**Screenshot 7: Contents of VoxelNumber_and_FacesToPore Code Output Excel Spreadsheet**

![screenshot_7a](https://github.com/user-attachments/assets/86895a6c-8a77-4be1-a022-85445a76f05f)
![screenshot_7b](https://github.com/user-attachments/assets/302026a5-b466-4b66-aa50-88b0115f8d04)


# 4. Mineral Distribution Analysis

The Mineral Distribution Code calculates the number of voxels for each label at the face of a flow region and those moving away from the face.

The flow regions are defined as fast channels and slow regions **(See Screenshot 8)**.


Distance maps of the fast flow and slow regions (fastflowdistmap.tif and slowregionsdistmap.tif) are used in combination with the segmented image.

The script outputs the voxel count for all labels at the face and away from the face in both fast and slow regions **(See Screenshot 8)**.


# Input Files:

- Distance maps (fastflowdistmap.tif, slowregionsdistmap.tif)..........

- Segmented image (with labels 1 to 6) **(See Screenshot 6)**

# Output File:

- Excel Spreadsheet containing **(See Screenshot 9)**.

- Number of voxels at the face and away from the face for all labels in fast and slow regions.

**Screenshot 9: Contents of Mineral Distribution Code Output Excel Spreadsheet**

![screenshot_9a](https://github.com/user-attachments/assets/d69fdafc-508e-4db2-9257-fb5536ea4f59)
![screenshot_9b](https://github.com/user-attachments/assets/1f67eac9-f0bb-4efe-b268-830faf198930)
![screenshot_9c](https://github.com/user-attachments/assets/23f602ad-e645-4237-afde-1e2a1b33548d)



## Step-by-Step Guide to Defining Fast Channels and Slow Regions, Obtaining Distance Maps and Fast Channel Dissolved Minerals 





**Screenshots: Overview: Defining Fast Channels and Slow Regions**

![Screenshot 8a (fast channel defination)](https://github.com/user-attachments/assets/fdda27e1-fe51-4406-bc23-ab4fbb2e7406)
![screenshot_8b](https://github.com/user-attachments/assets/af820397-9172-427d-9bc1-8373647bb304)

**Screenshots: Procedure: Defining Fast Channels and Slow Regions**

![ff1](https://github.com/user-attachments/assets/6ba357a0-441e-4626-adfb-874f96625856)


![ff2](https://github.com/user-attachments/assets/ca6e56fe-8b10-468c-8537-f821d92d839f)


![ff3](https://github.com/user-attachments/assets/32d39276-8748-40ab-bf7e-bb2e0156b6b0)


![ff4](https://github.com/user-attachments/assets/c1bb28fd-bc40-4f45-9350-37439411a82e)


![ff5](https://github.com/user-attachments/assets/1ad2ba35-e3b0-48c0-bdb3-36a574ea54ef)


![ff6](https://github.com/user-attachments/assets/7c53f310-5bf0-4cb1-ac6f-ffc5634ba848)


![ff7](https://github.com/user-attachments/assets/1869f0a6-8cf0-4efb-b868-fea51beaa0ef)


![ff8](https://github.com/user-attachments/assets/b35ec764-36c0-4dd2-8517-b5f6a048f354)


![ff9](https://github.com/user-attachments/assets/9a8e8134-8a51-4ac6-93f5-04168251b8ca)


![ff10](https://github.com/user-attachments/assets/759375c3-d3f3-437d-a07b-a3a97b80aebb)


![ff11](https://github.com/user-attachments/assets/2d41e9df-9c90-418c-ae18-762a7aabbd27)


![ff12](https://github.com/user-attachments/assets/a7addad0-49d5-465d-b457-909da9fbaea2)


![ff13](https://github.com/user-attachments/assets/ed7c2632-acd0-4f4c-98ce-a52d3d3367c8)


![ff14](https://github.com/user-attachments/assets/2945df2e-2a3b-4cf4-ad0e-0b2aefbb1d09)










## References
...

## Contact
For any inquiries, please contact **Sajjad Foroughi** at [s.foroughi@imperial.ac.uk] or **Olatunbosun Adedipe** at [o.adedipe23@imperial.ac.uk]
