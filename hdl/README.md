# AFRL HDL RF Projects
### Contains HDL for Analog Devices based RF FPGA systems.

---
author: Jay Convertino

date: 2024.04.16

details: Contains all HDL code for Analog Devices RF systems using the fusesoc system to build all FPGA code.

license: MIT
---

![logo_img](img/logo.png)

## Quick Info
  - ip, individual ip cores that are used for various builds.
  - projects, project cores that bring together various ip cores.
  - sim, simulation cores for base stimulation of test benches.
  - util, utility cores that provide base functionality and generators

## Targets
  - FMCOMMS2
    - zedboard
    - zc702
    - zc706
    - zcu102
    - a10soc
    - hanpilot
  - FMCOMMS5
    - zc702
    - zc706
    - zcu102
    - a10soc

## Release Versions
### Current
  - none

### Past
  - none

## Requirements
### OS
  - Tested on Ubuntu 22.04

### HDL
  - Vivado (Tested with 2022.2.2)
  - Quartus (Tested with 22.4)
  - fusesoc (2.4 or greater)
  - gtkwave
  - Icarus

## Usage
### Fusesoc
Fusesoc is a python based build system for generating FPGA projects from HDL. This folder contains everything needed to generate the projects listed below. This folder can be built using the fusesoc directly.

#### Projects, and targets.
  - AFRL:project:fmcomms2-3:1.0.0
    - zed
    - zed_bootgen
    - zc706
    - zc706_bootgen
    - zc702
    - zc702_bootgen
    - zcu102
    - zcu102_bootgen
    - hanpilot
    - hanpilot_bootgen
    - a10soc
    - a10soc_bootgen
  - AFRL:project:fmcomms5:1.0.0
    - zc706
    - zc706_bootgen
    - zc702
    - zc702_bootgen
    - zcu102
    - zcu102_bootgen
    - a10soc
    - a10soc_bootgen

#### Execution
example run command:
```
fusesoc run --build --target zc706_bootgen AFRL:project:fmcomms2-3:1.0.0
```
