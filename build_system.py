#!/usr/bin/env python3
################################################################################
# @file   build_system.py
# @author Jay Convertino(johnathan.convertino.1@us.af.mil)
# @date   24.04.17
# @brief  parse yaml file to execute built in tools
#
# @license MIT
# Copyright 2024 Jay Convertino
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
################################################################################

import yaml
import subprocess
import os
import pathlib
import shutil
import sys
import argparse
import logging
import time

try:
  import fusesoc
except ImportError:
  print("REQUIREMENT MISSING: fusesoc, pip install fusesoc")
  exit(0)

try:
  import git
except ImportError:
  print("REQUIREMENT MISSING: gitpython, pip install gitpython")
  exit(0)

logger = logging.getLogger(__name__)

# def main():
#   ## only want one argument
#   if len(sys.argv) != 2:
#     raise Exception("ERROR: parse_and_arg takes one argument, yaml file to open.")
#
#   stream = open(sys.argv[1], 'r')
#
#   loaded = yaml.safe_load(stream)
#
#   log = open(os.getcwd() + '/' + "generate.log", "w")
#
#   for key, value in loaded.items():
#     print("INFO: GENERATING", key)
#     print("INFO: TOOL", value['tool'])
#
#     if value['tool'] == 'git_pull':
#       git_pull(value, log)
#     elif value['tool'] == 'make':
#       make(value, log)
#     elif value['tool'] == 'copy':
#       copy(value, log)
#     elif value['tool'] == 'bash':
#       bash(value, log)
#     elif value['tool'] == 'quartus_cpf':
#       quartus_cpf(value, log)
#     elif value['tool'] == 'mkimage_for_boot_script':
#       mkimage_for_boot_script(value, log)
#     elif value['tool'] == 'vivado_xsa_gen':
#       vivado_xsa_gen(value, log)
#     elif value['tool'] == 'find_and_move':
#       find_and_move(value, log)
#     elif value['tool'] == 'xsct_tcl_run':
#       xsct_tcl_run(value, log)
#     elif value['tool'] == 'xilinx_bootgen':
#       xilinx_bootgen(value, log)
#     else:
#       print("ERROR: NO VALID TOOL")
#
#   log.close()


def main():
  args = parse_args(sys.argv[1:])

  if args.clean:
    exit(clean())

  yaml_data = open_yaml(args.yaml_file)

  if yaml_data is None:
    exit(~0)

  if args.list_all:
    exit(list_projects(yaml_data, args.yaml_file))

  logger_setup()

  submodule_init()

def submodule_init():
  repo = git.Repo(os.getcwd())

  for submodule in repo.submodules:
    if not submodule.module_exists():
      submodule.update(init=True)

def open_yaml(file_name):
  try:
    stream = open(file_name, 'r')
  except:
    logger.error(file_name + " not available.")
    return None

  try:
    yaml_data = yaml.safe_load(stream)
  except yaml.YAMLError as e:
    logger.error("yaml issue, " + e)
    return None

  return yaml_data

def list_projects(yaml, file_name):
  if not len(yaml):
    return ~0

  print('\n' + "BUILD SYSTEM TARGETS FROM " + file_name.upper() + '\n')

  for key, value in yaml.items():
    print("\tTARGET: " + key)

  print()
  return 0

def clean():
  print("*****************************")
  print("** CLEANING")

  if os.path.isdir(os.getcwd() + "/log"):
    print("*** REMOVE FOLDER: log")
    shutil.rmtree(os.getcwd() + "/log")

  if os.path.isdir(os.getcwd() + "/output"):
    print("*** REMOVE FOLDER: output")
    shutil.rmtree(os.getcwd() + "/output")

  print("** CLEANING COMPLETE")
  print("*****************************")

  return 0

def parse_args(argv):
  parser = argparse.ArgumentParser(description='Automate AFRL projects build using yaml target list.')

  group = parser.add_mutually_exclusive_group()

  group.add_argument('--hdl',    action='store_true', default=False,      dest='hdl_only',  required=False, help='Build only the HDL target.')
  group.add_argument('--sw',     action='store_true', default=False,      dest='sw_only',   required=False, help='Build only the SW target.')
  group.add_argument('--list',   action='store_true', default=False,      dest='list_all',  required=False, help='List all targets.')
  group.add_argument('--clean',  action='store_true', default=False,      dest='clean', required=False, help='remove all generated outputs, including logs.')

  parser.add_argument('--yaml',   action='store', default="config.yml",   dest='yaml_file', required=False, help='Path to configuration yaml file. config.yaml is default.')
  parser.add_argument('--target', action='store', default=None,           dest='target',    required=False, help='Target name from list. No target will build all by default.')

  return parser.parse_args()

def logger_setup():
  log_name = time.strftime("log/" + "%y%m%d", time.localtime()) + '_' +  str(int(time.mktime(time.localtime()))) + '.log'

  os.makedirs(os.getcwd() + "/log", exist_ok=True)

  logger.setLevel(logging.INFO)

  log_file = logging.FileHandler(filename = log_name, mode = 'w', delay=True)
  log_file.setLevel(logging.INFO)
  format_file = logging.Formatter(fmt = '%(asctime)-12s : %(levelname)-8s : %(message)s', datefmt='%y.%m.%d %H:%M')
  log_file.setFormatter(format_file)

  log_console = logging.StreamHandler()
  log_console.setLevel(logging.INFO)
  format_console = logging.Formatter(fmt = '%(levelname)-8s : %(message)s')
  log_console.setFormatter(format_console)

  logger.addHandler(log_file)
  logger.addHandler(log_console)

# def git_pull(value, log):
#   #get dirrrs
#   repo_url = value['repo_url']
#   tag      = value['tag']
#   repo_dir = value['repo_dir']
#
#   if os.path.exists(os.getcwd() + '/' + repo_dir):
#     print("INFO: GIT library exists in path, no pull, no checkout.")
#     return
#
#   try:
#     repo_data = git.Repo.clone_from(repo_url, os.getcwd() + '/' + repo_dir)
#   except Exception as e:
#     print("ERROR: ", e)
#     return
#
#   try:
#     if tag is not None:
#       repo_data.git.checkout(tag)
#   except Exception as e:
#     print("ERROR: ", e)
#     return
#
# def make(value, log):
#   src_dir   = value['src_dir']
#   make_args = value['make_args']
#
#   make_make_args = ["make"] + make_args
#
#   try:
#     subprocess.run(make_make_args, stdout=log, stderr=log, cwd=os.getcwd() + '/' + src_dir)
#   except subprocess.CalledProcessError as error_code:
#     print("ERROR: Make,", error_code.returncode, error_code.output)
#     return
#
# def copy(value, log):
#   src_dir = value['src_dir']
#   dest_dir = value['dest_dir']
#
#   try:
#     shutil.copyfile(os.getcwd() + '/' + src_dir, os.getcwd() + '/' + dest_dir)
#   except Exception as e:
#     print("ERROR: ", e)
#     return
#
# def bash(value, log):
#   command   = value['command']
#   arguments = value['arguments']
#
#   executioner = command + arguments
#
#   try:
#     subprocess.run(executioner, stdout=log, stderr=log, cwd=os.getcwd())
#   except subprocess.CalledProcessError as error_code:
#     print("ERROR: Bash,", error_code.returncode, error_code.output)
#     return
#
# def quartus_cpf(value, log):
#   sof_file = value['sof_file']
#   rbf_name = value['rbf_name']
#
#   files_found = sorted(pathlib.Path().glob("output_files/*.sof"))
#
#   if len(files_found) == 0:
#     print("ERROR: No sof file found, generation failed.")
#     return
#
#   try:
#     subprocess.run(["quartus_cpf", "-c", "--hps", "-o", "bitstream_compression=on", files_found[0], rbf_name], stdout=log, stderr=log, cwd=str(pathlib.Path.cwd()))
#   except subprocess.CalledProcessError as error_code:
#     print("ERROR:", error_code.returncode, error_code.output)
#     return
#
# def mkimage_for_boot_script(value, log):
#   arch       = value['arch']
#   src_file   = value['src_file']
#   dest_file  = value['dest_file']
#
#   try:
#     subprocess.run(["mkimage", "-C", "none", "-A", arch, "-T", "script", "-d", src_file, dest_file], stdout=log, stderr=log, cwd=str(pathlib.Path.cwd()))
#   except subprocess.CalledProcessError as error_code:
#     print("ERROR:", error_code.returncode, error_code.output)
#     return
#
# def vivado_xsa_gen(value, log):
#   xsa_tcl_file = value['xsa_tcl_file']
#
#   try:
#     subprocess.run(["vivado", "-mode", "tcl", "-nolog", "-nojournal", "-source", xsa_tcl_file], stdout=log, stderr=log, cwd=str(pathlib.Path.cwd()))
#   except subprocess.CalledProcessError as error_code:
#     print("ERROR:", error_code.returncode, error_code.output)
#     return
#
# def find_and_move(value, log):
#   src_file   = value['src_file']
#   dest_file  = value['dest_file']
#
#   files_found = sorted(pathlib.Path().glob(src_file))
#
#   if len(files_found) == 0:
#     print("ERROR: src_file not found.")
#     return
#
#   pathlib.Path(files_found[0]).replace(dest_file)
#
# def xsct_tcl_run(value, log):
#   tcl_file  = value['tcl_file']
#
#   try:
#     subprocess.run(["xsct", tcl_file], stdout=log, stderr=log, cwd=str(pathlib.Path.cwd()))
#   except subprocess.CalledProcessError as error_code:
#     print("ERROR:", error_code.returncode, error_code.output)
#     return
#
# def xilinx_bootgen(value, log):
#   arch       = value['arch']
#   src_file   = value['src_file']
#   dest_file  = value['dest_file']
#   exec_dir   = value['exec_dir']
#
#   try:
#     subprocess.run(["bootgen", "-image", src_file, "-arch", arch, "-o", dest_file],  stdout=log, stderr=log, cwd=str(pathlib.Path.cwd()) + "/" + exec_dir)
#   except subprocess.CalledProcessError as error_code:
#     print("ERROR:", error_code.returncode, error_code.output)
#     return

if __name__=="__main__":
  main()
