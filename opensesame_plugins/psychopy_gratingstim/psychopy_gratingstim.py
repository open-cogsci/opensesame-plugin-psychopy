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


class psychopy_gratingstim(item):

	description = u'A dynamic PsychoPy GratingStim for use with coroutines'

	def reset(self):

		self.var.framerate = -1
		self.var.interpretation = u'opensesame'
		self.var.tex = u'sin'
		self.var.mask = u'gauss'
		self.var.xpos = 0
		self.var.ypos = 0
		self.var.xsize = 100
		self.var.ysize = 100
		self.var.sf = 0.05
		self.var.ori = 0
		self.var.color = u'white'
		self.var.contrast = 1
		
	def coroutine(self, coroutines=None):
		
		try:
			from psychopy.visual import GratingStim, Window
		except ImportError as e:
			raise osexception(u'Failed to import PsychoPy', exception=e)
		# Check whether the PsychoPy window is available
		if not hasattr(self.experiment, u'window') or \
			not isinstance(self.experiment.window, Window):
			raise osexception(u'No PsychoPy window available. '
				u'Have you selected the psychopy backend?')
		# Make sure that the window is flipped after every cycle
		if coroutines is not None and self.experiment.window.flip not in \
			coroutines.post_cycle_functions:
			coroutines.post_cycle_functions.append(self.experiment.window.flip)
		grating = GratingStim(self.experiment.window)
		alive = True
		last_update = None
		# The function to evaluate values depends on whether they are
		# Python-style values, which are evaluated in the workspace, or
		# OpenSesame-style values, which are evaluated by the syntax module when
		# the variable is retrieved (so we can just return it in f_os).
		f_py = lambda script: self.python_workspace._eval(safe_decode(script))
		f_os = lambda script: script
		f = f_py if self.var.interpretation == u'python' else f_os
		yield # Preparation done
		while alive:
			now = self.clock.time()
			if last_update is None or \
					(self.var.framerate >= 0 and \
					now - last_update >= self.var.framerate):
				last_update = now
				grating.color = f(self.var.color)
				grating.contrast = f(self.var.contrast)					
				grating.pos = f(self.var.xpos), f(self.var.ypos)
				grating.size = f(self.var.xsize), f(self.var.ysize)
				grating.sf = f(self.var.sf)
				grating.tex = f(self.var.tex)
				grating.mask = f(self.var.mask)
				grating.ori = f(self.var.ori)
			grating.draw()
			alive = yield

	def prepare(self):

		item.prepare(self)
		self._coroutine = self.coroutine()
		self._coroutine.next()

	def run(self):

		self._coroutine.send(False)
		self.experiment.window.flip()


class qtpsychopy_gratingstim(psychopy_gratingstim, qtautoplugin):

	def __init__(self, name, experiment, script=None):

		psychopy_gratingstim.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)
