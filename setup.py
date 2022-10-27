#!/usr/bin/env python
# coding=utf-8

"""
This file is part of psychopy_gratingstim.

psychopy_gratingstim is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

psychopy_gratingstim is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with psychopy_gratingstim.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
from setuptools import setup


def get_readme():

    if os.path.exists('readme.md'):
        with open('readme.md') as fd:
            return fd.read()
    return 'No readme information'


setup(
    name='opensesame-plugin-psychopy',
    version='0.6.2',
    description='PsychoPy plugins for OpenSesame',
    long_description=get_readme(),
    author='Sebastiaan Mathot',
    author_email='s.mathot@cogsci.nl',
    url='https://github.com/smathot/opensesame-plugin-psychopy',
    # Classifiers used by PyPi if you upload the plugin there
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
    packages=[],
    data_files=[
        ('share/opensesame_plugins/psychopy_gratingstim',
        [
            'opensesame_plugins/psychopy_gratingstim/psychopy_gratingstim.png',
            'opensesame_plugins/psychopy_gratingstim/psychopy_gratingstim_large.png',
            'opensesame_plugins/psychopy_gratingstim/psychopy_gratingstim.py',
            'opensesame_plugins/psychopy_gratingstim/info.yaml',
            ]
        ),
        ('share/opensesame_plugins/psychopy_textstim',
        [
            'opensesame_plugins/psychopy_textstim/psychopy_textstim.png',
            'opensesame_plugins/psychopy_textstim/psychopy_textstim_large.png',
            'opensesame_plugins/psychopy_textstim/psychopy_basestim.py',
            'opensesame_plugins/psychopy_textstim/psychopy_textstim.py',
            'opensesame_plugins/psychopy_textstim/info.yaml',
            ]
        )]
    )
