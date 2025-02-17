# Copyright (C) 2015: The University of Edinburgh
#            Authors: Craig Warren and Antonis Giannopoulos
#
# This file is part of gprMax.
#
# gprMax is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gprMax is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gprMax.  If not, see <http://www.gnu.org/licenses/>.

import sys
import decimal as d
from pyfiglet import Figlet


class ListStream:
    """A list can be streamed into. Required when temporarily redirecting stdio to capture output from users Python code blocks."""
    
    def __init__(self):
        self.data = []
    
    def write(self, s):
        self.data.append(s)


def logo(version):
    """Print gprMax logo, version, and licencing/copyright information.
        
    Args:
        version (str): Version number.
    """
    
    licenseinfo = """
Copyright (C) 2015: The University of Edinburgh
           Authors: Craig Warren and Antonis Giannopoulos
        
gprMax is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
                    
gprMax is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
                                    
You should have received a copy of the GNU General Public License
along with gprMax.  If not, see <http://www.gnu.org/licenses/>."""
    width = 65
    url = 'www.gprmax.com'
    print('\n{} {} {}'.format('*'*round((width - len(url))/2), url, '*'*round((width - len(url))/2)))
    gprMaxlogo = Figlet(font='standard', width=width, justify='center')
    print('{}'.format(gprMaxlogo.renderText('gprMax')))
    print('{} v{} {}'.format('*'*round((width - len(version))/2), (version), '*'*round((width - len(version))/2)))
    print(licenseinfo)
    print('\n{}\n'.format('*'*(width+3)))


def update_progress(progress):
    """Displays or updates a console progress bar.
        
    Args:
        progress (float): Number between zero and one to signify progress.
    """
    
    # Modify this to change the length of the progress bar
    barLength = 50
    block = rvalue(barLength * progress)
    text = '\r|{}| {:2.1f}%'.format( '#' * block + '-' * (barLength - block), progress * 100)
    sys.stdout.write(text)
    sys.stdout.flush()


def rvalue(value):
    """Rounds half values downward.
        
    Args:
        value (float): Number to round.
        
    Returns:
        Rounded value (float).
    """
    
    return int(d.Decimal(value).quantize(d.Decimal('1'),rounding=d.ROUND_HALF_DOWN))


def human_size(size, a_kilobyte_is_1024_bytes=True):
    """Convert a file size to human-readable form.
        
    Args:
        size (int): file size in bytes
        a_kilobyte_is_1024_bytes (boolean) - true for multiples of 1024, false for multiples of 1000
        
    Returns:
        Human-readable (string).
    """

    suffixes = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'], 1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}

    if size < 0:
        raise ValueError('Number must be non-negative.')
    
    multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
    for suffix in suffixes[multiple]:
        size /= multiple
        if size < multiple:
            return '{0:.1f} {1}'.format(size, suffix)

    raise ValueError('Number is too large.')


