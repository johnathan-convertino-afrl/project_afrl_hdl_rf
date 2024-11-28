# AFRL HDL RF Projects
### HDL and Linux SDCARD system generator for RF FPGA devices

![logo_img](docs/manual/img/AFRL.png)

---

author: Jay Convertino

date: 2024.04.16

details: Contains all of the needed parts to generate FPGA based RF devices. Targets listed below. Uses fusesoc to generate HDL code, and buildroot for Linux. Combined these generate full SDCARD image files using genimage.

license: MIT

---

### Version
#### Current
  - none

#### Previous
  - none

### TODO
  - Add rfsoc projects
  - Add jesd204 projects

### DOCUMENTATION
  For detailed usage information, please navigate to one of the following sources. They are the same, just in a different format.

  - [project_afrl_hdl_rf.pdf](docs/manual/project_afrl_hdl_rf.pdf)
  - [github page](https://johnathan-convertino-afrl.github.io/project_afrl_hdl_rf/)

#### Quick Info
  - output is a folder generated that contains all build outputs.
    - hdl for all FPGA code
    - linux for all linux code
    - genimage for its builds
    - sdcard contains sdcard image files and source files for sdcard image.
  - log is a folder generated that contains all information logged from execution.

#### Targets
  - FMCOMMS2-3
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

### HELP
#### General
Look at the build log log/DATE_TIME.log for hints on where the error happened. Add the --debug option to the run to get all output dumped to the log file.

HDL and Buildroot use various external sites to pull in remote dependencies. If there is no internet connection, then the repo will not be pulled and the build will fail.

#### HDL
For fusesoc FPGA builds look at output/hdl/TARGET_NAME/*.log . For Vivado this is vivado.log. For the parse_and_gen python script its log file is generate.log.

#### Linux (Buildroot, busybox)
For buildroot, please enable the debug option at run time to get detailed output to the main log file. Errors will always go to the log file.
