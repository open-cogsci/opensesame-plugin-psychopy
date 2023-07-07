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
        self.var.tex = "'sin'"
        self.var.mask = "'gauss'"
        self.var.xsize = 100
        self.var.ysize = 100
        self.var.sf = 0.05
        self.var.phase = 0
        self.var.objectname = 'gratingstim'

    @property
    def _stimclass(self):
        from psychopy.visual import GratingStim
        return GratingStim

    def _prepare_bytecode(self, c):
        bytecode = super()._prepare_bytecode(c)
        bytecode.update({
            'xsize': c('xsize'),
            'ysize': c('ysize'),
            'sf': c('sf'),
            'tex': c('tex'),
            'mask': c('mask'),
            'phase': c('phase')
        })
        return bytecode

    def _update_attributes(self, f):
        super()._update_attributes(f)
        self._stim.sf = f('sf')
        self._stim.tex = f('tex')
        self._stim.mask = f('mask')
        self._stim.phase = f('phase')
        self._stim.size = f('xsize'), f('ysize')
