# Learning Varian DICOM DB Daemon with Python

This repository is dedicated to learn and explore the **Varian DICOM Daemon Service**. It contains Python scripts and resources for understanding how to interact with the Varian Daemon functionality.

## Overview

The Varian Daemon is a component of the Varian ecosystem that allow us to request RT information that is stored in the Aria database. The purpose of this repository is to help to extract data according to the DICOM standar, for example, RT Images, RT Dose, CT Image Series, etc. 

We use open-source Python libraries as **pydicom** and **pynetdicom** in order to: 

- Understand how to set up a Client Application Entity (client and provider).
- Experiment with services (C-FIND and C-MOVE) to request dicom files.
- Provide example code.

## Repository Structure

### 🗂️ Scripts

- `00_setup.md` Provides step-by-step instructions to configure the Varian Daemon Service.
- `01_echo.py` Implements a C-ECHO request to verify connectivity with the Varian Daemon.
- `02_find.py` Demonstrates how to perform a C-FIND request to search for studies for a given patient.
- `03_storage_scp.py` Shows how to set up a Storage Service Class Provider to store images.
- `04_get_image.py` Implements C-FIND and C-MOVE requests.

## 📚 Learning Resources

- [VarianAPIBook](https://varianapis.github.io/VarianApiBook.pdf)
- [Varian Conformance Statements](https://www.varian.com/es/why-varian/interoperability/dicom-statements)
- [Pynetdicom](https://pydicom.github.io/pynetdicom/stable/) documentation
- [Pydicom](https://pydicom.github.io/pydicom/stable/) documentation
- Pianykh, O. S. (2012). Digital imaging and communications in medicine (DICOM) a practical introduction and survival guide. Berlin, Heidelberg: Springer Berlin Heidelberg.

---

## ⚠️ Disclaimer

For Research and Educational Use Only. This tool is not a medical device and has not been cleared for clinical use by any regulatory authority. The author assumes no liability for clinical errors or misuse of these scripts.

---

## ✉️ Contact & Collaboration
I am a Medical Physicist interested about the intersection of oncology and software development. I am open to feedback, collaborations, and professional opportunities.

LinkedIn: Luis Alfonso Olivares Jiménez [LinkedIn](www.linkedin.com/in/luis-alfonso-olivares-jimenez-682736122)

Email: alfonso.cucei.udg@gmail.com
