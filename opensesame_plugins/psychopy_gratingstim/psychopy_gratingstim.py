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

from libopensesame.py3compat import *
from libopensesame.exceptions import osexception
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin

try:
    from psychopy_basestim import psychopy_basestim
except ImportError:
    # If basestim cannot be loaded, then that's probably because it's located
    # with the textstim.
    import sys
    import os
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
        'psychopy_textstim')
    if path not in sys.path:
        sys.path.append(path)
    from psychopy_basestim import psychopy_basestim


class psychopy_gratingstim(psychopy_basestim):

    description = u'A dynamic PsychoPy GratingStim for use with coroutines'

    def reset(self):

        psychopy_basestim.reset(self)
        self.var.tex = u'sin'
        self.var.mask = u'gauss'
        self.var.xsize = 100
        self.var.ysize = 100
        self.var.sf = 0.05
        self.var.phase = 0
        self.var.objectname = u'gratingstim'

    @property
    def _stimclass(self):

        from psychopy.visual import GratingStim
        return GratingStim

    def _prepare_bytecode(self, c):

        bytecode = psychopy_basestim._prepare_bytecode(self, c)
        bytecode.update({
            u'xsize'	: c(u'xsize'),
            u'ysize'	: c(u'ysize'),
            u'sf'		: c(u'sf'),
            u'tex'		: c(u'tex'),
            u'mask'		: c(u'mask'),
            u'phase'	: c(u'phase')
        })
        return bytecode

    def _update_attributes(self, f):

        psychopy_basestim._update_attributes(self, f)
        self._stim.sf = f(u'sf')
        self._stim.tex = f(u'tex')
        self._stim.mask = f(u'mask')
        self._stim.phase = f(u'phase')
        self._stim.size = f(u'xsize'), f(u'ysize')


class qtpsychopy_gratingstim(psychopy_gratingstim, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        psychopy_gratingstim.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
