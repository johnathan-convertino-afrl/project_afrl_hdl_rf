# AFRL HDL RF Projects
### Contains all parts needed to build complete Analog Devices based RF Linux FPGA systems.

---

author: Jay Convertino

date: 2024.04.16

details: Contains all HDL code for Analog Devices RF systems using the fusesoc system to build all FPGA code. It also contains all of the needed Linux build items using buildroot. This is tied together with a python build system called system_builder.py to execute the required builds and generate output products.

license: MIT

---


![logo_img](img/logo.png)


## Quick Info
  - output is a folder generated that contains all build outputs.
    - hdl for all FPGA code
    - linux for all linux code
    - genimage for its builds
    - sdcard contains sdcard image files and source files for sdcard image.
  - log is a folder generated that contains all information logged from execution.

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

### Software
  - build-essentials
  - genimage
  - make
  - mkimage
  - bootgen
  - gcc
  - which
  - sed
  - gcc
  - g++
  - bash
  - patch
  - gzip
  - bzip2
  - perl
  - tar
  - cpio
  - unzip
  - rsync
  - file
  - bc
  - wget
  - find
  - xargs
  - diff
  - cmp
  - diff3
  - sdiff
  - ld
  - as
  - gold

## Quick Start
  0. Clone this repo
  1. Install Requirements listed above.
  2. Make sure all requirements are accessable from the command line.
  3. execute: python system_builder.py to build all targets.

## Usage
### System Builder
System builder is a python script that will build all targets in order based on a yaml script. By default this is build.yml if it is not specified. It also checks dependencies, cleans toplevel untracked artifacts, and pulls subrepos.

#### Options
```
  --list_targets       List all targets.
  --list_commands      List all available yaml build commands.
  --list_deps          List all available dependencies.
  --clean              remove all generated outputs, including logs.
  --deps DEPS_FILE     Path to dependencies txt file, used to check if command
                       line applications exist.
  --build CONFIG_FILE  Path to build configuration yaml file. build.yml is
                       default.
  --target TARGET      Target name from list. None will build all targets by
                       default.
```

#### build.yml
build.yml (default value system builder looks for) file specifies targets with parts that contain commands for builds. These parts can be concurrent for multithreading, or sequenctial for one at a time. The order these are executed is from the top down. Meaning the top command will be executed before the one below it.

Sample build.yml

```
zed_fmcomms2-3_linux_busybox_sdcard:
  concurrent:
    fusesoc: &fusesoc_fmcomms2-3
      path: hdl
      project: AFRL:project:fmcomms2-3:1.0.0
      target: zed_bootgen
    buildroot: &buildroot_fmcomms2-3
      path: sw/linux/buildroot-afrl
      config: zynq_zed_ad_fmcomms2-3_defconfig
  sequential:
    script: &output_files_fmcomms2-3
      exec: python
      file: py/output_gen.py
      args: "--rootfs output/linux --bootfs output/hdl --dest output/sdcard"
    genimage:
      path: img_cfg
zc702_fmcomms2-3_linux_busybox_sdcard:
  concurrent:
    fusesoc:
      <<: *fusesoc_fmcomms2-3
      target: zc702_bootgen
    buildroot:
      <<: *buildroot_fmcomms2-3
      config: zynq_zc702_ad_fmcomms2-3_defconfig
  sequential:
    script:
      <<: *output_files_fmcomms2-3
    genimage:
      path: img_cfg
```

#### deps.txt
deps.txt (default value system builder looks for) file specifies any executable dependency of the project. These are list line by line in a simple text file. No version checks at the moment. If any are missing the application will print out the missing executable and quit.

Sample deps.txt

```
genimage
fusesoc
make
quartus_cpf
quartus
mkimage
vivado
xsct
bootgen
gcc
```
