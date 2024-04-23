# AFRL HDL RF Projects
### Contains all Analog Devices RF projects converted to fusesoc

---
author: Jay Convertino

date: 2024.04.16

details: Contains HDL and Linux items to build RF example systems targeting SDCARDs.

license: MIT
---

![logo_img](img/logo.png)

## RELEASE VERSIONS
### Current
  - none

### Past
  - none

## Requirements
### HDL
  - Vivado (Tested with 2022.2.2)
  - fusesoc (2.4 or greater)
  - gtkwave
  - Icarus
### Software (SW)
  - build-essentials
  - ??

## Quick Start
0. Clone this repo, and run 'git submodule update --init --recursive' in the root to pull all sub repos.
1. Install Vivado
2. Install build essentials package for Ubuntu.

## USAGE
### General Usage

  copy:
    last: true
    tool: cp
    from: sw/linux/buildroot-afrl/output/images
    to:   output/
  image:
    last: true
    tool: genimage
    path: cfg/
    config: zed_sdcard_linux.img
