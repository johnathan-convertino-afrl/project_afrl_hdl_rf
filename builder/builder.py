#!/usr/bin/env python3
################################################################################
# @file   builder.py
# @author Jay Convertino(johnathan.convertino.1@us.af.mil)
# @date   24.04.22
# @brief  parse yaml file to execute build tools
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
import logging
import threading

logger = logging.getLogger(__name__)

class bob:
  def __init__(self, yaml_data, target):
    self._yaml_data = yaml_data
    self._target = target
    # template strings for commands
    self._command_template = {
      'fusesoc':   { 'cmd_1' : ["fusesoc", "--cores-root", "{path}", "--config", "{config}", "run", "--build", "--target", "{target}", "{project}"]},
      'buildroot': { 'cmd 1' : ["make", "-C", "{path}", "clean"], 'cmd_2' : ["make", "-C", "{path}", "{config}"], 'cmd_3' : ["make", "-C", "{path}"]}
    }
    self._projects = None
    self._threads  = []

  # run the steps to build parts of targets
  def run(self):
    self._process()
    self._execute()
    self._package()

  # create dict of lists with lists of strings to execute with subprocess
  # {project: [[["make", "def_config"], ["make"]], ['thread':["fusesoc", "run", "--build", "--target", "zed_blinky", "::blinky:1.0.0"]]]}
  def _process(self):

    #filter target into updated dictionary if it was selected
    if self._target != None:
      try:
        self._yaml_data = { self._target: self._yaml_data[self._target]}
      except KeyError:
        logger.error(f"Target: {self._target}, does not exist.")
        return ~0

    self._projects = {}

    for project, parts in self._yaml_data.items():
      project_parts = []

      for part, command in parts.items():

        try:
          command_template = self._command_template[part].values()
        except KeyError:
          logger.info(f"No build rule for part: {part}.")
          continue

        part_commands = []

        for commands in command_template:
          populate_command = []

          string_command = ' '.join(commands)

          part_commands.append(list(string_command.format_map(command).split(" ")))

        project_parts.append(part_commands)

      self._projects[project] = project_parts

      logger.info(f"Added commands for project: {project}")

    return 0

  #call subprocess as a thread and add it to a list of threads for wait to check on.
  #iterate over projects avaiable and execute commands per project
  def _execute(self):

    for project, commands in self._projects.items():
      logger.info(f"Starting build for project: {project}")

      self._threads.clear()

      for command_list in commands:
        thread = threading.Thread(target=self._subprocess, name=project, args=[command_list])

        self._threads.append(thread)

        thread.start()

      for t in self._threads:
        t.join()

  def _subprocess(self, list_of_commands):
    for command in list_of_commands:
      result = None

      try:
        logger.info(f"Executing command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, check=True, text=True, cwd=str(pathlib.Path.cwd()))
      except subprocess.CalledProcessError as error_code:
        logger.error(error_code.returncode)

        # for t in self._threads:
        #   if t.is_alive():
        #     t.raise_exception()
        return ~0

      logger.info(f"Completed command: {' '.join(command)}")

  #maybe a special method for image?
  def _package(self):
    pass
