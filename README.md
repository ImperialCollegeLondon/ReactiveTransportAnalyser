# **Reactive Transport Analyzer for CO₂ Reactions**

## **Table of Contents**
1. [Overview](#overview)
2. [Single-Phase Flow Simulation](#single-phase-flow-simulation)
   - [Input Files](#input-files)
   - [Required Output Files](#required-output-files)
3. [Image Alignment Code](#image-alignment-code)
   - [Input Files](#input-files-1)
   - [Output Files](#output-files)
4. [Voxel Count & Pore Exposure Analysis](#voxel-count--pore-exposure-analysis)
   - [Input Files](#input-files-2)
   - [Output Files](#output-files-1)
5. [Mineral Distribution Analysis](#mineral-distribution-analysis)
   - [Input Files](#input-files-3)
   - [Output Files](#output-files-2)
6. [Defining Fast Channels & Slow Regions](#defining-fast-channels--slow-regions)
   - [Obtaining Distance Maps](#obtaining-distance-maps)
   - [Fast Channel Dissolved Minerals](#fast-channel-dissolved-minerals)
7. [Proximity Function Profiles](#proximity-function-profiles)

## **Overview**
This tutorial provides a structured workflow for conducting single-phase flow simulations, aligning flow field images, analyzing voxel distributions, and evaluating mineral transport within a porous medium. Step-by-step instructions are provided for input files, expected outputs, and key scripts used for data processing.

**Example Used:** Sample A at 33 min (488 PV).

## **Single-Phase Flow Simulation**
The single-phase flow simulator is available at **[Porefoam1f](https://github.com/ImperialCollegeLondon/poreFoam-singlePhase)**.

### **Input Files**
- **Segmented Image** (Labeling Guide):
  - **Label 0:** Pore
  - **Label 1:** Rock (including outer layer to prevent external flow)
  
**Screenshots:**
**Segmenting Pore**
![Segmenting Pore](https://github.com/user-attachments/assets/58b38132-fd44-4356-89fd-a43c23aa82e4)

**Segmenting Rock (rock + outer layer) - (Incorrect Labeling)**
![Segmenting Rock](https://github.com/user-attachments/assets/ef7dab19-ea63-47a4-ac9d-f367f338d1e1)
![Material stats](https://github.com/user-attachments/assets/abc5b16c-1e30-4652-b35e-dcad2906f67d)

**Correct Labeling**
![screenshot_1c](https://github.com/user-attachments/assets/463cf521-94ba-4770-9e6b-51bd1d96b652)
![Material stats](https://github.com/user-attachments/assets/0df49207-2ad8-47b5-982c-335751c414a0)


- **.MHD File Format** *(See Screenshot Below)*
  ![MHD File](https://github.com/user-attachments/assets/93bc9505-7d97-4c73-9a4d-c578f5e0dfe1)

### **Required Output Files**
- **Velocity Files**: Velocities at the cell face (Ufx, Ufy, Ufz)
- **Summary File**: Contains permeability, connected porosity, velocity distribution (PDFs)
- **OpenMelnParaview.foam**: Used in Paraview for velocity visualization

**Contents of Simulation Output Folder**

![Contents of Simulation Output Folder
](https://github.com/user-attachments/assets/7f900e04-f3e2-4a7e-b305-a0c62408cffd)

**Contents of Summary File**

![Contents of Summary File](https://github.com/user-attachments/assets/44069493-c5b5-4b1b-be08-02639f27c0de)


## **Image Alignment Code (Flowfield_Image_Alignment_Code)**
This script corrects misalignment between the flow field image and the segmented image from the single-phase simulation.

### **Input Files**
- Velocities at the cell face (Ufx, Ufy, Ufz)

### **Output Files**
- Flow Field Image *(See Screenshot Below)*
  ![Output Folder](https://github.com/user-attachments/assets/3022c1fa-72fa-48c5-a739-092716b8bf2a)

## **Voxel Count & Pore Exposure Analysis (VoxelNumber_and_FacesToPore_Code)**
This script calculates voxel distributions and the number of faces exposed to the pore label.

### **Input Files**
- Two segmented images at different time intervals


**Segmented Image (Label 1 to 5)**

 - Label 1: Outer layer

  - Label 2: Pore

  - Label 3: Microporous phase

  - Label 4: Dolomite

  - Label 5: Calcite

  - Label 6: Anhydrite
 
    **Note: Label 0 is ignored**

![screenshot_6a](https://github.com/user-attachments/assets/d455bebb-2b4f-40cf-8d63-dbcc5eb4c72b)

### **Output Files**
- Excel file with voxel count differences and pore exposure calculations *(See Screenshot Below)*
  ![Excel Output](https://github.com/user-attachments/assets/86895a6c-8a77-4be1-a022-85445a76f05f)

## **Mineral Distribution Analysis**
This code analyzes voxel distribution around fast and slow flow regions.

### **Input Files**
- Distance maps (fastflowdistmap.tif, slowregionsdistmap.tif)
- Segmented image with labeled minerals

### **Output Files**
- Excel file with voxel counts at the face and away from the face *(See Screenshot Below)*
  ![Mineral Analysis Output](https://github.com/user-attachments/assets/d69fdafc-508e-4db2-9257-fb5536ea4f59)

## **Defining Fast Channels & Slow Regions**
This section guides defining high and low velocity zones based on flow field analysis.

**Procedure:**
1. Load grayscale and flow field images in Avizo.
2. Generate a histogram and extract Darcy velocity threshold at **75% CDF**.
3. Threshold and segment fast flow regions.
4. Dilate by 3 pixels to reach the nearest pore wall.
5. Subtract rock areas to isolate the **fast flow channel**.
6. Subtract fast channels from the full flow field to obtain **slow regions**.

**Screenshots:**
- ![Fast Flow Segmentation](https://github.com/user-attachments/assets/759375c3-d3f3-437d-a07b-a3a97b80aebb)
- ![Slow Regions Segmentation](https://github.com/user-attachments/assets/a7addad0-49d5-465d-b457-909da9fbaea2)

### **Obtaining Distance Maps**
- Use **Chamfer Distance Map** module in Avizo for both fast channels and slow regions.
- Export results as .TIFF files.

## **Fast Channel Dissolved Minerals**
Mineral dissolution in fast channels is determined by multiplying mineral change images with the fast flow channel.

### **Input Files**
- Dissolved mineral image (‘2-3-mpd.am’, ‘2-3-dol.am’, etc.)
- Fast channel image (‘33fastflow.channel.am’)

### **Output Files**
- TIFF images showing dissolved minerals in fast channels *(See Screenshot Below)*
  ![Dissolved Minerals](https://github.com/user-attachments/assets/90ec2954-1c1b-4816-8ae4-19cb24bd9353)

## **Proximity Function Profiles**
The **proximity function** quantifies mineral exposure relative to fast channels, providing insights into exposure-dependent dissolution.

### **Input Files**
- Mineral distribution voxel count (from Proximity_VoxelNumber_Code)
- Exposed surface area (from VoxelNumber_and_FacesToPore_Code)

### **Output File**
- Excel spreadsheet containing **proximity function (voxel/m²)**

![Proximity Function](https://github.com/user-attachments/assets/2858d719-218a-4331-90cd-bd279eaaab1f)

---

This guide provides a **clear, structured, and interactive** approach to analyzing reactive transport processes in CO₂ storage environments. If you encounter any issues, refer to the screenshots or reach out for support!

