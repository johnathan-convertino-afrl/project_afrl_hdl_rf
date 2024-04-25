#!/usr/bin/env python3
################################################################################
# @file   system_builder.py
# @author Jay Convertino(johnathan.convertino.1@us.af.mil)
# @date   2024.04.17
# @brief  Build various projects using builder object to parse and execute parts
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

logger = logging.getLogger()

# check for git
try:
  import git
except ImportError:
  print("REQUIREMENT MISSING: gitpython, pip install gitpython")
  exit(0)

sys.path.append("./py/")

sys.dont_write_bytecode = True

import builder

# main execution function
def main():
  args = parse_args(sys.argv[1:])

  if args.clean:
    exit(clean())

  yaml_data = open_yaml(args.config_file)

  if yaml_data is None:
    exit(~0)

  if args.list_cmds:
    exit(builder.bob(yaml_data, args.target).list())

  if args.list_all:
    exit(list_projects(yaml_data, args.config_file))

  logger_setup()

  submodule_init()

  exit(builder.bob(yaml_data, args.target).run())

  #image generation

# make sure submodules have been pulled. If not, pull them.
def submodule_init():
  repo = git.Repo(os.getcwd())

  logger.info("Checking for submodules...")

  for submodule in repo.submodules:
    if not submodule.module_exists():
      logger.info("Updating submodule...")
      logger.info("Submodule " + str(submodule.update(init=True)) + " pulled")

  logger.info("Checking for submodules complete.")

# open the yaml file for processing
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

# List projects from the yaml file.
def list_projects(yaml, file_name):
  if not len(yaml):
    return ~0

  print('\n' + f"SYSTEM BUILDER TARGETS FROM {file_name.upper()}" + '\n')

  for target, value in yaml.items():
    print(f"TARGET: {target}")

  return 0

# Clean up folders used for output (output and log)
def clean():
  print("********************************")
  print("** CLEANING UNTRACKED ITEMS")

  repo = git.Repo(os.getcwd())

  if len(repo.ignored(os.listdir())) == 0:
    print("** NOTHING TO REMOVE")

  for item in repo.ignored(os.listdir()):
    if os.path.isfile(item):
      print(f"** REMOVING FILE: {item}")
      os.remove(item)
    else:
      print(f"** REMOVING DIR: {item}")
      shutil.rmtree(item, ignore_errors=True)

  print("** CLEANING COMPLETE")
  print("********************************")

  return 0

# parse args for tuning build
def parse_args(argv):
  parser = argparse.ArgumentParser(description='Automate projects build using yaml target list.')

  group = parser.add_mutually_exclusive_group()

  group.add_argument('--list_targets',    action='store_true',  default=False,        dest='list_all',    required=False, help='List all targets.')
  group.add_argument('--list_commands',   action='store_true',  default=False,        dest='list_cmds',   required=False, help='List all available yaml build commands.')
  group.add_argument('--clean',           action='store_true',  default=False,        dest='clean',       required=False, help='remove all generated outputs, including logs.')

  parser.add_argument('--deps',   action='store',       default="deps.yml",   dest='deps_files',  required=False, help='Path to dependecys file, used to check if command line applications exist.')
  parser.add_argument('--build',  action='store',       default="build.yml",  dest='config_file', required=False, help='Path to build configuration yaml file. build.yaml is default.')
  parser.add_argument('--target', action='store',       default=None,         dest='target',      required=False, help='Target name from list. No target will build all by default.')

  return parser.parse_args()

# setup logger for log file and console output
def logger_setup():
  log_name = time.strftime("log/" + "%y%m%d", time.localtime()) + '_' +  str(int(time.mktime(time.localtime()))) + '.log'

  os.makedirs(os.getcwd() + "/log", exist_ok=True)

  logger.setLevel(logging.DEBUG)

  log_file = logging.FileHandler(filename = log_name, mode = 'w', delay=True)
  log_file.setLevel(logging.DEBUG)
  format_file = logging.Formatter(fmt = '%(asctime)-12s : %(levelname)-8s : %(message)s', datefmt='%y.%m.%d %H:%M')
  log_file.setFormatter(format_file)

  log_console = logging.StreamHandler()
  log_console.setLevel(logging.INFO)
  format_console = logging.Formatter(fmt = '%(levelname)-8s : %(message)s')
  log_console.setFormatter(format_console)

  logger.addHandler(log_file)
  logger.addHandler(log_console)

# name is main is main
if __name__=="__main__":
  main()
