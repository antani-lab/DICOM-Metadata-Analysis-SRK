# Extraction of DICOM Metadata 

This repository contains a Python script designed to extract essential metadata from a collection of DICOM images. The script reads key DICOM tags—**ImageType**, **Pixel Data**, and **VOILUTFunction**—and creates an Excel file summarizing this information. Non-DICOM files (e.g., JPEG images) are also listed, though their metadata fields remain blank.

---

## Rationale

Accurate image preprocessing is crucial in clinical diagnosis. Radiologists rely on specific DICOM tags to interpret images and adjust contrast appropriately.  
- **ImageType** ensures that the data represents original/raw images.  
- **VOILUTFunction** provides information about contrast adjustments that mimic radiologists’ windowing techniques.  
- Summarizing pixel data (dimensions, datatype, mean intensity) offers a quick quality check, ensuring that downstream AI diagnostic models receive clinically relevant inputs.  

---

## Method

1. **Directory Traversal:**  
   The script scans the target directory for DICOM files (files ending with `.dcm`). JPEG files are listed but skipped for metadata extraction.

2. **Metadata Extraction:**  
   - **ImageType (0008,0008):** Retrieves information about the image origin (e.g., "ORIGINAL", "PRIMARY").
   - **Pixel Data (7fe0,0010):** Instead of storing the full pixel array (which is memory intensive), a concise summary (dimensions, datatype, mean intensity) is generated.
   - **VOILUTFunction (0028,1056):** Captures how contrast adjustments were applied.

3. **Data Aggregation:**  
   The metadata from each file is compiled into a structured DataFrame and saved as an Excel file (`metadata_dicom.xlsx`).

---

## Requirements

The script was developed and tested with the following packages:

- **pydicom** (v2.3.0): For reading DICOM files.  
- **pandas** (v1.3.5): For data handling and Excel output.  
- **numpy** (v1.21.2): For numerical computations.  
- **openpyxl** (v3.0.9): For writing Excel files.

To install the required packages, run:

```bash
pip install pydicom==2.3.0 pandas==1.3.5 numpy==1.21.2 openpyxl==3.0.9
