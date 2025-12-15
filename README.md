# Learning Varian DICOM DB Daemon with Python

This repository is dedicated to learn and explore the **Varian DICOM Daemon Service**. It contains Python scripts and resources for understanding how to interact with and utilize the Varian Daemon functionality.

## Overview

The Varian Daemon is a component of the Varian ecosystem that allow us to request RT information that is stored in the Aria database. The purpose is to help to extract data according to the DICOM standar, for example, RT Images, RT Dose, CT Image Series, etc. This repository will use open-source Python libraries as **pydicom** and **pynetdicom** in order to: 

- Understand how to set up a Client Application Entity (client).
- Experiment with various services operations to request data.
- Provide example code and documentation.

## Repository Structure

### Scripts folder

- `00_setup.md` Provides step-by-step instructions to configure the Varian Daemon Service.
- `01_echo.py` Implements a C-ECHO request to verify connectivity with the Varian Daemon.
- `02_find.py` Demonstrates how to perform a C-FIND request to search for studies.
- `03_get.py` (TODO) Shows how to execute a C-GET request to retrieve images 

## Learning Resources

- [VarianAPIBook](https://varianapis.github.io/VarianApiBook.pdf)
- [Varian Conformance Statements](https://www.varian.com/es/why-varian/interoperability/dicom-statements)
- [Pynetdicom](https://pydicom.github.io/pynetdicom/stable/) documentation
- [Pydicom](https://pydicom.github.io/pydicom/stable/) documentation
- Pianykh, O. S. (2012). Digital imaging and communications in medicine (DICOM) a practical introduction and survival guide. Berlin, Heidelberg: Springer Berlin Heidelberg.

---
