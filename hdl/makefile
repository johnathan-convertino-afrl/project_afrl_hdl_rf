# AFRL_FUSE_PRJ	:= $(shell fusesoc list-cores 2> /dev/null | awk '/AFRL:project/ {print $1}' -)
PROJECTS 	:= $(notdir $(wildcard projects/*))
# TARGETS		= zed zc702 zc706 zcu102 hanpilot a10soc
# TARGETS_BOOTGEN = $(addsuffix _bootgen, $(TARGETS))
# SRCDIR		= $(shell pwd)
# SRC 		= $(shell find $(SRCDIR) -name '*.v')
# BITDIR  	= $(SRCDIR)/build/AFRL_project_fmcomms2-3_1.0.0/$(TARGET)-vivado/
# BIT		= AFRL_project_ace_vexriscv_murax_1.0.0.bit

.PHONY: clean $(PROJECTS)

all: $(PROJECTS)

$(PROJECTS):

# $(BITDIR)$(BIT): $(SRC)
# 	fusesoc run --target $(TARGETS) --build AFRL:project:$(PROJECTS)

clean:
	rm -rf build
