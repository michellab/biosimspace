######################################################################
# BioSimSpace: Making biomolecular simulation a breeze!
#
# Copyright: 2017-2018
#
# Authors: Lester Hedges <lester.hedges@gmail.com>
#
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
An energy type.
Author: Lester Hedges <lester.hedges@gmail.com>
"""

import Sire.Units as _Units

from ._type import Type as _Type

__all__ = ["Time"]

class Time(_Type):
    # Dictionary of allowed units.
    _supported_units = { "DAY"         : _Units.day,
                         "HOUR"        : _Units.hour,
                         "MINUTE"      : _Units.minute,
                         "SECOND"      : _Units.second,
                         "MILLISECOND" : _Units.millisecond,
                         "NANOSECOND"  : _Units.nanosecond,
                         "PICOSECOND"  : _Units.picosecond,
                         "FEMTOSECOND" : _Units.femtosecond }

    # Map unit abbreviations to the full name.
    _abbreviations = { "HR"  : "HOUR",
                       "MIN" : "MINUTE",
                       "SEC" : "SECOND",
                       "MS"  : "MILLISECOND",
                       "NS"  : "NANOSECOND",
                       "PS"  : "PICOSECOND",
                       "FS"  : "FEMTOSECOND" }

    # Print formatting.
    _print_format = { "DAY"         : "day",
                      "HOUR"        : "hour",
                      "MINUTE"      : "min",
                      "SECOND"      : "sec",
                      "MILLISECOND" : "ms",
                      "NANOSECOND"  : "ns",
                      "PICOSECOND"  : "ps",
                      "FEMTOSECOND" : "fs" }

    def __init__(self, *args):
        """Constructor.

           Positional arguments:

           magnitude -- The magnitude.
           unit      -- The unit.

           or

           string    -- A string representation of the time.
        """

        # Call the base class constructor.
        super().__init__(*args)

        # Don't support negative times.
        if self._magnitude < 0:
            raise ValueError("The time cannot be negative!")

    def __str__(self):
        """Return a human readable string representation of the object."""

        abbrev = self._print_format[self._unit]
        if self._magnitude > 1:
            if abbrev[-1] != "s":
                abbrev = abbrev + "s"
        if abs(self._magnitude) > 1e4 or abs(self._magnitude) < 1e-4:
            return "%.4e %s" % (self._magnitude, abbrev)
        else:
            return "%5.4f %s" % (self._magnitude, abbrev)

    def weeks(self):
        """Return the time in weeks."""
        return Time((self._magnitude * self._supported_units[self._unit]).to(_Units.week), "WEEK")

    def days(self):
        """Return the time in days."""
        return Time((self._magnitude * self._supported_units[self._unit]).to(_Units.day), "DAY")

    def hours(self):
        """Return the time in hours."""
        return Time((self._magnitude * self._supported_units[self._unit]).to(_Units.hour), "HOUR")

    def minutes(self):
        """Return the time in minutes."""
        return Time((self._magnitude * self._supported_units[self._unit]).to(_Units.minute), "MINUTE")

    def seconds(self):
        """Return the time in seconds."""
        return Time((self._magnitude * self._supported_units[self._unit]).to(_Units.second), "SECOND")

    def milliseconds(self):
        """Return the time in milliseconds."""
        return Time((self._magnitude * self._supported_units[self._unit]).to(_Units.millisecond), "MILLISECOND")

    def nanoseconds(self):
        """Return the time in nanoseconds."""
        return Time((self._magnitude * self._supported_units[self._unit]).to(_Units.nanosecond), "NANOSECOND")

    def picoseconds(self):
        """Return the time in picoseconds."""
        return Time((self._magnitude * self._supported_units[self._unit]).to(_Units.picosecond), "PICOSECOND")

    def femtoseconds(self):
        """Return the time in femtoseconds."""
        return Time((self._magnitude * self._supported_units[self._unit]).to(_Units.femtosecond), "FEMTOSECOND")

    def _default_unit(self, mag=None):
        """Internal method to return an object of the same type in the default unit.

           Positional argument:

           mag -- The magnitude (optional).
        """
        if mag is None:
            return self.picoseconds()
        else:
            return Time(mag, "PICOSECOND")

    def _convert_to(self, unit):
        """Return the time in a different unit.

           Positional arguments:

           unit -- The unit to convert to.
        """
        if unit == "WEEK":
            return self.weeks()
        elif unit == "DAY":
            return self.days()
        elif unit == "HOUR":
            return self.hours()
        elif unit == "MINUTE":
            return self.minutes()
        elif unit == "SECOND":
            return self.seconds()
        elif unit == "MILLISECOND":
            return self.milliseconds()
        elif unit == "NANOSECOND":
            return self.nanoseconds()
        elif unit == "PICOSECOND":
            return self.picoseconds()
        elif unit == "FEMTOSECOND":
            return self.femtoseconds()
        else:
            raise ValueError("Supported units are: '%s'" % list(self._supported_units.keys()))

    def _validate_unit(self, unit):
        """Validate that the unit are supported."""

        # Strip whitespace and convert to upper case.
        unit = unit.replace(" ", "").upper()

        # Check that the unit is supported.
        if unit in self._supported_units:
            return unit
        elif unit[:-1] in self._supported_units:
            return unit[:-1]
        elif unit in self._abbreviations:
            return self._abbreviations[unit]
        elif unit[:-1] in self._abbreviations:
            return self._abbreviations[unit[:-1]]
        else:
            raise ValueError("Supported units are: '%s'" % list(self._supported_units.keys()))