######################################################################
# BioSimSpace: Making biomolecular simulation a breeze!
#
# Copyright 2017-2018
#
# Authors: Lester Hedges

# BioSimSpace is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# BioSimSpace is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BioSimSpace. If not, see <http://www.gnu.org/licenses/>.
#####################################################################

"""
Functionality for configuring and driving molecular dynamics simulations.
Author: Lester Hedges
"""

from Sire.Base import findExe

import Sire.System

from ..Process import *
from ..Protocol import *
from ..Protocol._protocol import Protocol

from os import environ, path

__all__ = ["MD"]

# A dictionary mapping MD packages to their executable names and GPU support.
#                PACKAGE        EXE           GPU
_md_packages = { "AMBER"   : { "pmemd.cuda" : True, "pmemd" : False, "sander" : False },
                 "GROMACS" : { "gmx" : True },
                 "NAMD"    : { "namd2" : False }
               }

# A dictionary reverse mapping MD packages to their Sire file extensions.
#                    EXTENSION     EXTENSION
_file_extensions = { "PRM7,RST7"    : "AMBER",
                     "PRM7,RST"     : "AMBER",
                     "GroTop,Gro87" : "GROMACS",
                     "PSF,PDB"      : "NAMD" }

def _find_md_package(system, protocol, use_gpu=True):
    """Find a molecular dynamics package on the system and return
       a handle to it as a MDPackage object.

       Positional arguments:

       system   -- The molecular system.
       protocol -- The simulation protocol.

       Keyword arguments:

       use_gpu  -- Whether to use GPU support.
    """

    # Check that the use_gpu flag is valid.
    if type(use_gpu) is not bool:
        raise TypeError("'use_gpu' keyword must be of type 'bool'")

    # Get the file format of the molecular system.
    fileformat = system.property("fileformat").toString()

    # Make sure that this format is supported.
    if not fileformat in _file_extensions:
        raise ValueError("Cannot find an MD package that supports format: %s" % fileformat)
    else:
        package = _file_extensions[fileformat]

    # Loop over each executable in turn and see whether it exists on the system.
    for exe, gpu in _md_packages[package].items():
        if package == "AMBER":
            # Search AMBERHOME, if set.
            if "AMBERHOME" in environ:
                amber_home = environ.get("AMBERHOME")
                exe = "%s/bin/%s" % (amber_home, exe)
                if path.isfile(exe):
                    return (package, exe)

            # Search PATH.
            else:
                try:
                    exe = findExe(exe).absoluteFilePath()
                    return (package, exe)
                except:
                    pass
        else:
            try:
                exe = findExe(exe).absoluteFilePath()
                return (package, exe)
            except:
                pass

    # If we get this far, then no executable was found.
    raise ValueError("No executable found for package: '%s'" % package)

class MD():
    """A simple class for driving molecular dynamics simulations."""

    @staticmethod
    def run(system, protocol, autostart=True, name="md", work_dir=None, seed=None):
        """Constructor.

           Positional arguments:

           system    -- The molecular system.
           protocol  -- The protocol for the simulation.

           Keyword arguments:

           autostart -- Whether to start the process automatically.
           name      -- The name of the process.
           work_dir  -- The working directory for the process.
           seed      -- A random number seed.
        """

        # Check that the system is valid.
        if system.__class__ is not Sire.System.System:
            raise TypeError("'system' must be of type 'Sire.System._System.System'")

        # Check that the protocol is valid.
        if not isinstance(protocol, Protocol):
            if type(protocol) is str:
                protocol = Custom(protocol)
            else:
                raise TypeError("'protocol' must be of type 'BioSimSpace.Protocol' "
                    "or the path to a custom configuration file.")

        # Find a molecular dynamics package and executable.
        package, exe = _find_md_package(system, protocol)

        # Create the process object.

        # AMBER.
        if package == "AMBER":
            process = Amber(system, protocol, name=name, work_dir=work_dir, seed=seed)

        # GROMACS.
        elif package == "GROMACS":
            process = Gromacs(system, protocol, name=name, work_dir=work_dir, seed=seed)

        # NAMD.
        elif package == "NAMD":
            process = Namd(system, protocol, name=name, work_dir=work_dir, seed=seed)

        # Start the process.
        if autostart:
            return process.start()
        else:
            return process