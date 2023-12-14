DEV_PYTHON_VER ?= 3.11
PY_VERS ?= 3.7 3.8 3.9 3.10 3.11
PANDOC_FLAGS ?= --toc --standalone

USE_MICROMAMBA ?= true
USE_ROSETTA ?= false

CHANNEL ?= conda-forge

ENVS ?= envs
BIN ?= build/bin

# Set to true if you want to use poetry shell etc.

USE_POETRY ?= false

# ------- Computed variables ------
ifeq ($(USE_MICROMAMBA), true)
  CONDA ?= $(CONDA_PRE) micromamba
	CONDA_ENV = $(CONDA)
  CONDA_ACTIVATE ?= eval "$$(micromamba shell hook --shell=bash)" && micromamba activate
else
  CONDA ?= $(CONDA_PRE) conda
	CONDA_ENV = $(CONDA) env
  CONDA_ACTIVATE ?= source $$($(CONDA) info --base)/etc/profile.d/conda.sh && $(CONDA) activate
endif

# We need special effects for 
ifeq ($(USE_ROSETTA), true)
  ifeq ($(shell uname -p),arm)
    PLATFORM = arm64
    CONDA_PRE += CONDA_SUBDIR=osx-64
  endif
endif

DEV_ENV ?= $(ENVS)/py$(DEV_PYTHON_VER)
CONDA_ACTIVATE_DEV = $(CONDA_ACTIVATE) $(DEV_ENV)
ALL_ENVS = $(foreach py,$(PY_VERS),$(ENVS)/py$(py))

# ------- Top-level targets  -------
# Default prints a help message
help:
	@make usage

usage:
	@echo "$$HELP_MESSAGE"

shell: dev
ifeq ($(USE_POETRY), true)
	poetry shell
else
	$(CONDA_ACTIVATE_DEV) && bash --init-file .init-file.bash
endif

test: dev
	$(CONDA_ACTIVATE_DEV) && pytest

README.rst: doc/README.ipynb
	jupyter nbconvert --to=rst --output=README.rst doc/README.ipynb


%.html: %.rst
	rst2html5.py $< > $@

# Running make <name>.html will use fswatch to look for modifications in the corresponding
# <name>.md file and will use pandoc to generate the html file, then calling $(OPEN_BROWSER)
# to show this. We then run fswatch to look over this looking for changes.  Once the user
# exits with a keyboard interrupt, the intermediate html file is removed.  We use Safari
# as the default browser on Mac OS X because Chrome-based browsers steal focus.
BROWSER ?= "Safari"
BROWSER ?= "Brave Browser"
OPEN_BROWSER ?= open -g -a $(BROWSER) $@
PANDOC_FLAGS ?= -s
PANDOC ?= pandoc $(PANDOC_FLAGS) --metadata title=\"$*\" $< -o $@
FSWATCH ?= fswatch -e ".*" -i "$<" -o . 
%.html: %.md
	$(PANDOC) && $(OPEN_BROWSER)
	$(FSWATCH) | while read num; do $(PANDOC) && $(OPEN_BROWSER); done

clean:
	-coverage erase
	$(RM) -r fil-result
	find . -type d -name "htmlcov"  -exec $(RM) -r {} +
	find . -type d -name "__pycache__" -exec $(RM) -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	$(RM) -r src/mmfutils.egg-info
	$(RM) -r doc/README_files/
	$(RM) *.html

realclean: clean
	$(RM) -r .nox .conda $(ENVS) $(BIN)
	$(RM) -r build

dev: $(DEV_ENV)
ifeq ($(USE_POETRY), true)
	poetry env use $(DEV_ENV)/bin/python$(DEV_PYTHON_VER)
	poetry install -E test -E doc
else
	$(CONDA_ACTIVATE_DEV) && python3 -m pip install -e .[test,doc]
endif

$(ENVS): $(ALL_ENVS)

$(ENVS)/py3.11: environment.yaml pyproject.toml
	$(CONDA_ENV) create -y -c $(CHANNEL) -p $@ -f $< $(GPU_PACKAGES) "conda-forge::python=3.11"
ifneq ($(USE_MICROMAMBA), true)
  ifeq ($(shell uname -p),arm)
	  $(CONDA_ACTIVATE) $@ && $(CONDA) config --env --set subdir osx-64
  endif
endif
	mkdir -p $(BIN)
	ln -fs $(abspath $@/bin/python3.11) $(BIN)/

$(ENVS)/py%: environment.yaml pyproject.toml
	$(CONDA_ENV) create -y -c $(CHANNEL) -p $@ -f $< $(GPU_PACKAGES) "python=$*"
ifneq ($(USE_MICROMAMBA), true)
  ifeq ($(shell uname -p),arm)
	  $(CONDA_ACTIVATE) $@ && $(CONDA) config --env --set subdir osx-64
  endif
endif
	mkdir -p $(BIN)
	ln -fs $(abspath $@/bin/python$*) $(BIN)/

.PHONY: help usage dev test clean realclean



# ----- Usage -----
define HELP_MESSAGE

This Makefile provides several tools for creating a development environment for testing, etc.
The main objective is to provide support for different architectures, specifically
on platforms like Mac OS X with an ARM processor.  At the time of writing, the tests fail
because pyFFTW does not build (see https://github.com/pyFFTW/pyFFTW/issues/144).  To get
arround this, we use various stratgies for installing python appropriately using Rosetta
for example.

Variables:
   DEV_PYTHON_VER: (= "$(DEV_PYTHON_VER)")
                     Version of python for development.
   PY_VERS: (= "$(PY_VERS)")
                     Versions of python to install in ENVS_DIR
   ENVS: (= "$(ENVS)")
                     Location of environments.
   DEV_ENV: (= "$(DEV_ENV)")
                     Python development environment.
   PANDOC_FLAGS: (= "$(PANDOC_FLAGS)")
                     Flags to pass to pandoc for generating HTML files from markdown files.
   CONDA_PRE: (= "$(CONDA_PRE)")
                     Comes before the conda command.  Use for CONDA_SUB= for example.
   CONDA: (= "$(CONDA)")
                     Command to run conda (includes/overrrides CONDA_PRE).
   CONDA_ACTIVATE: (= "$(CONDA_ACTIVATE)")
                     Command to run conda activate.  This can be tricky in a Makefile, so
                     we allow this to be customized.  See:
                     https://stackoverflow.com/questions/53382383
	                   https://stackoverflow.com/questions/60115420
   BIN: (= "$(BIN)")
                     Binary directory to symlink locally install versions of python.
                     Add this to the path so that nox will find them.

Computed variables (cannot be overwritten on command line)
	 CONDA_ACTIVATE_DEV:(= "$(CONDA_ACTIVATE_DEV)")
                     Command to activate the development environment.
	 ALL_ENVS: (= "$(ALL_ENVS)")
                     All environments that will be made.

Initialization:
   make dev          Initialize the development environment and setup poetry.
   make $(ENVS)      Initialize all environments.

Testing:
   make test         Runs the general tests in the dev environment.

Maintenance:
   make clean        Clean repo.
   make realclean    Remove all envs, etc.

Documentation:
   make README.rst   Generate the README.rst file from doc/README.ipynb

endef
export HELP_MESSAGE
