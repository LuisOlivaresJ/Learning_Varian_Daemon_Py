# Learning Varian DICOM DB Daemon with Python

This repository is dedicated to learn and explore the **Varian DICOM Daemon Service**. It contains Python scripts and resources for understanding how to interact with and utilize the Varian Daemon functionality.

## Overview

The Varian Daemon is a component of the Varian ecosystem that allow us to request RT information that is stored in the Aria database. The purpose is to help to extract data according to the DICOM standar, for example, RT Images, RT Dose, CT Image Series, etc. This repository will use open-source Python libraries as **pydicom** and **pynetdicom** in order to: 

- Understand how to set up a Client Application Entity (client).
- Experiment with various services operations to request data.
- Provide example code and documentation.

## Repository Structure

### Scripts folder
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

### 1.1 Client-side Configuration
To make requests to the Daemon, we can use any computer that is on the network. In this repository we will use a PC running Ubuntu 24.04 LTS. To install and manage Python packages, we will use the [uv](https://docs.astral.sh/uv/) package.

To connect two computers according to the DICOM protocol, the application that will make the queries (the client) must have the following:

- *Application Entity Title* (AET). We will use **FM_SCU**
- *IP Address*, which is the address of our PC on the network. We will use the address **192.168.1.1**

### 1.2 Provider-side Configuration
We access the server that contains the database remotely.