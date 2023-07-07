"""This file is part of psychopy_textstim.

psychopy_textstim is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

psychopy_textstim is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with psychopy_textstim.  If not, see <http://www.gnu.org/licenses/>.
"""
from libopensesame.py3compat import *
from opensesame_plugins.psychopy.psychopy_textstim.psychopy_basestim import \
    PsychopyBasestim


class PsychopyTextstim(PsychopyBasestim):

    def reset(self):
        super().reset()
        self.var.text = "'text'"
        self.var.font_family = "'mono'"
        self.var.font_size = 18
        self.var.objectname = 'textstim'
        
    @property
    def _stimclass(self):
        from psychopy.visual import TextStim
        return TextStim
        
    def _prepare_bytecode(self, c):
        bytecode = super()._prepare_bytecode(c)
        bytecode.update({
            'text': c('text'),
            'font_family': c('font_family'),
            'font_size': c('font_size'),
            })
        return bytecode
        
    def _update_attributes(self, f):
        super()._update_attributes(f)
        self._stim.text = f('text')
        self._stim.font = f('font_family')
        self._stim.height = f('font_size')
