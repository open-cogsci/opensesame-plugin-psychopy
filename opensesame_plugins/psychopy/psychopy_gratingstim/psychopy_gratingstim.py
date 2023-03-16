"""This file is part of psychopy_gratingstim.

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
from opensesame_plugins.psychopy.psychopy_textstim.psychopy_basestim import \
    PsychopyBasestim


class PsychopyGratingstim(PsychopyBasestim):

    def reset(self):
        super().reset()
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
            u'xsize': c(u'xsize'),
            u'ysize': c(u'ysize'),
            u'sf': c(u'sf'),
            u'tex': c(u'tex'),
            u'mask': c(u'mask'),
            u'phase': c(u'phase')
        })
        return bytecode

    def _update_attributes(self, f):
        super()._update_attributes(f)
        self._stim.sf = f(u'sf')
        self._stim.tex = f(u'tex')
        self._stim.mask = f(u'mask')
        self._stim.phase = f(u'phase')
        self._stim.size = f(u'xsize'), f(u'ysize')
