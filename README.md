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
This script (**[Flowfield_Image_Alignment_Code](Flowfield_Image_Alignment_Code.py)**.) corrects misalignment between the flow field image and the segmented image from the single-phase simulation.

### **Input Files**
- Velocities at the cell face (Ufx, Ufy, Ufz)

### **Output Files**
- Flow Field Image *(See Screenshot Below)*
  ![Output Folder](https://github.com/user-attachments/assets/3022c1fa-72fa-48c5-a739-092716b8bf2a)

## **Voxel Count & Pore Exposure Analysis (VoxelNumber_and_FacesToPore_Code)**
This script (**[VoxelNumber_and_FacesToPore_Code](VoxelNumber_and_FacesToPore_Code.py)**) calculates voxel distributions and the number of faces exposed to the pore label.

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
![voxel count differences and pore exposure calculations ](https://github.com/user-attachments/assets/8c7bc3aa-792a-4eb0-b1fa-151ff2700048)


## **Mineral Distribution Analysis (Proximity_VoxelNumber_Code)**
This code (**[Proximity_VoxelNumber_Code](Proximity_VoxelNumber_Code.py)**) analyzes voxel distribution around fast and slow flow regions.

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

**Screenshots: Defining Fast Channels and Slow Regions**

Open in Avizo:
- Grayscale image
- Flow field image

Make sure the properties highlighted in red are identical for both images. This is required to ensure the images are aligned perfectly.

![ff1](https://github.com/user-attachments/assets/6ba357a0-441e-4626-adfb-874f96625856)


Atach a histogram module to the flow field image. Generate a histogram from with :
- Range = 0 to 1E-6
- 128 bins

Save histogram as .csv file. 

![ff2](https://github.com/user-attachments/assets/ca6e56fe-8b10-468c-8537-f821d92d839f)


Copy the Darcy velocities (first column)

![ff3](https://github.com/user-attachments/assets/32d39276-8748-40ab-bf7e-bb2e0156b6b0)


Plot PDF.

![ff4](https://github.com/user-attachments/assets/83493d7b-df65-4878-a72c-6a1ef424bc68)



Calculate CDF and CDF (%). Plot CDF (%).

![ff5](https://github.com/user-attachments/assets/1ad2ba35-e3b0-48c0-bdb3-36a574ea54ef)


Paste the Darcy velocities next to PDF. CDF and CDF (%). Then go to 75% CDF and obtain the following:
- Darcy velocity for thresholding fast channels (red). (Darcy velocity 7.32E-07) 
- The corresponding x-axis (blue) and y-axis (yellow) values used in identifying fast channel velocities on the velocity distribution (PDF) plot.
  
![ff6](https://github.com/user-attachments/assets/7c53f310-5bf0-4cb1-ac6f-ffc5634ba848)

![ff7](https://github.com/user-attachments/assets/1869f0a6-8cf0-4efb-b868-fea51beaa0ef)


In Avizo, threshold, segment snd save the whole flow field to a new ‘Label field’ :
- Threshold from 1E-22 to end of data. 

![ff8](https://github.com/user-attachments/assets/b35ec764-36c0-4dd2-8517-b5f6a048f354)


Threshold, segment snd save the fast flow seed to a new ‘Label field’ :
- Threshold from 7.32E-07 to end of data. 

![ff9](https://github.com/user-attachments/assets/9a8e8134-8a51-4ac6-93f5-04168251b8ca)


View the grayscale image with the fast flow seed (blue). Attach the ‘Dilation’ module to the fast flow seed and dilate by the minimum number of pixels required to reach the nearest pore wall. It was 3 pixels (3px ) in this case.  The dilated region is shown in red.

![ff10](https://github.com/user-attachments/assets/759375c3-d3f3-437d-a07b-a3a97b80aebb)


Where the dilated region overlaps rock, the rock image is subtracted. Using expression:
- A-B


The result is a fast flow channel where blue depicts the faster velocities at the middle of the fast channel and the green depicts slower velocities  closer to the pore walls.


![ff11](https://github.com/user-attachments/assets/2d41e9df-9c90-418c-ae18-762a7aabbd27)



To get the slow regions, we subtract the fast channels from the whole flow field using expression:
- A-B


![ff12](https://github.com/user-attachments/assets/a7addad0-49d5-465d-b457-909da9fbaea2)


### **Obtaining Distance Maps**
- Use **Chamfer Distance Map** module in Avizo for both fast channels and slow regions.
- Export results as .TIFF files.
  
![ff13](https://github.com/user-attachments/assets/ed7c2632-acd0-4f4c-98ce-a52d3d3367c8)


# **Outputs: Fast Channel ans Slow Region Images, Distance Maps**

We now have images of fast channels and slow regions, along with their corresponding distance maps. Each of these files should be exported and saved as individual .TIFF files for use in later calculations and visualizations.

![ff14](https://github.com/user-attachments/assets/2945df2e-2a3b-4cf4-ad0e-0b2aefbb1d09)


## **Fast Channel Dissolved Minerals**
Mineral dissolution in fast channels is determined by multiplying mineral change images with the fast flow channel. The following images represent minerals dissolved between scan 2 (33 min) and scan 3 (66 min), calculated as scan 2 minus scan 3:
- 2-3-mpd.am
- 2-3-dol.am
- 2-3-cal.am
- 2-3-anhy.am

- Additionally, 33fastflow.channel.am is the fast channel image at scan 3 (66 min).

**Note:** These files serve as input to determine the fast channel dissolved minerals.

**Processing Steps**

Using the Arithmetic module, multiply 2-3-mpd.am by 33fastflow.channel.am using the expression:
- A * B

Repeat this operation for each dissolved mineral image.

### **Input Files**
- Dissolved mineral image (‘2-3-mpd.am’, ‘2-3-dol.am’, etc.)
- Fast channel image (‘33fastflow.channel.am’)

### **Output Files**
   - Fast channel dissolved mineral images:
      - 2-3-mpd_fast_dissolved.am
      - 2-3-dol_fast_dissolved.am
      - 2-3-cal_fast_dissolved.am
      - 2-3-anhy_fast_dissolved.am

**Note:** Export and save all output files individually as .TIFF files for visualization in ParaView.
  ![Dissolved Minerals](https://github.com/user-attachments/assets/90ec2954-1c1b-4816-8ae4-19cb24bd9353)

## **Proximity Function Profiles**
The **proximity function** quantifies mineral exposure relative to fast channels, providing insights into exposure-dependent dissolution.

![Proximity Function](https://github.com/user-attachments/assets/2858d719-218a-4331-90cd-bd279eaaab1f)

### **Input Files**
- Mineral distribution voxel count (from Proximity_VoxelNumber_Code)
- Exposed surface area (from VoxelNumber_and_FacesToPore_Code)

### **Output File**
- Excel spreadsheet containing **proximity function (voxel/m²)**

Calculate proximity function. 

![proximity_1a](https://github.com/user-attachments/assets/3cc0e95f-69d2-4307-a887-1689352cdedd)

![proximity_1b](https://github.com/user-attachments/assets/a8fa86a9-966f-4c1c-9f19-8814c525beda)


Calculate difference in proximity function. 

![proximity_1c](https://github.com/user-attachments/assets/527dd576-8b8e-4d38-bb1c-7845d4740a64)


![proximity_1d](https://github.com/user-attachments/assets/893a6970-cf91-41b3-af27-107e48e35f0c)


Plot proxmity function profiles.

![proximity_1e](https://github.com/user-attachments/assets/07be59c7-c975-44b6-a46b-3cef8fd3d2cf)




## References
...

## Contact
For any inquiries, please contact **Sajjad Foroughi** at [s.foroughi@imperial.ac.uk] or **Olatunbosun Adedipe** at [o.adedipe23@imperial.ac.uk]




