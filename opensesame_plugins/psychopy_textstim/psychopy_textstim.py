# coding=utf-8

"""
This file is part of psychopy_textstim.

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
from libqtopensesame.items.qtautoplugin import qtautoplugin
from psychopy_basestim import psychopy_basestim

class psychopy_textstim(psychopy_basestim):

    description = u'A dynamic PsychoPy TextStim for use with coroutines'

    def reset(self):

        psychopy_basestim.reset(self)
        self.var.text = u''
        self.var.font_family = u'mono'
        self.var.font_size = 18
        self.var.objectname = 'textstim'
        
    @property
    def _stimclass(self):
        
        from psychopy.visual import TextStim
        return TextStim
        
    def _prepare_bytecode(self, c):
        
        bytecode = psychopy_basestim._prepare_bytecode(self, c)
        bytecode.update({
            u'text'			: c(u'text'),
            u'font_family'	: c(u'font_family'),
            u'font_size'	: c(u'font_size'),
            })
        return bytecode
        
    def _update_attributes(self, f):
        
        psychopy_basestim._update_attributes(self, f)
        self._stim.text = f(u'text')
        self._stim.font = f(u'font_family')
        self._stim.height = f(u'font_size')


class qtpsychopy_textstim(psychopy_textstim, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        psychopy_textstim.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
