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
from libopensesame.exceptions import osexception
from libopensesame.item import item


class psychopy_basestim(item):

    def reset(self):

        self.var.framerate = -1
        self.var.interpretation = u'opensesame'
        self.var.xpos = 0
        self.var.ypos = 0
        self.var.ori = 0
        self.var.color = u'white'
        self.var.contrast = 1
        self.var.opacity = 1
        self.var.script = u''
        self.var.order = 0

    def coroutine(self, coroutines=None):

        try:
            from psychopy.visual import Window
        except ImportError as e:
            raise osexception(u'Failed to import PsychoPy', exception=e)
        # Check whether the PsychoPy window is available
        if not hasattr(self.experiment, u'window') or \
            not isinstance(self.experiment.window, Window):
            raise osexception(u'No PsychoPy window available. '
                u'Have you selected the psychopy backend?')
        self._stim = self._stimclass(self.experiment.window)
        # Make sure that the window is flipped after every cycle
        if coroutines is not None and \
            self.winflip not in coroutines.post_cycle_functions:
            coroutines.post_cycle_functions.append(self.winflip)
            self.experiment._psychopystim_needflip = False
        # Add all gratings to the grating queue, which is drawn in order
        # before the window flip. We sort the queue to control the drawing
        # order/ depth/ z-index of the stimuli.
        if not hasattr(self.experiment, u'_psychopystim_queue'):
            self.experiment._psychopystim_queue = []
        if self not in self.experiment._psychopystim_queue:
            self.experiment._psychopystim_queue.append(self)
            self.experiment._psychopystim_queue.sort(
                key=lambda item: item.var.order)
        # Register the grating in the Python workspace
        self.python_workspace[self.var.objectname] = self._stim
        alive = True
        last_update = None
        # The function to evaluate values depends on whether they are
        # Python-style values, which are evaluated in the workspace, or
        # OpenSesame-style values, which are evaluated by the syntax module when
        # the variable is retrieved.
        if self.var.interpretation == u'python':
            # A compile function that gets a statement, converts it to a str,
            # and then byte-compiles it to a code object. We cannot use
            # python_workspace._compile(), because this assumes exec statements.
            c = lambda stm: compile(
                    (u'#-*- coding:%s -*-\n' % self.experiment.encoding + \
                 	safe_decode(self.var.get(stm, _eval=False))) \
                    .encode(self.experiment.encoding),
                    u'<string>', u'eval')
            # The compile function is then applied to all statements so that
            # they are precompiled. This is done in another function so that it
            # can be overridden.
            bytecode = self._prepare_bytecode(c)
            # And the evalutation function just evals the bytecode
            f = lambda stm: self.python_workspace._eval(bytecode[stm])
        else:
            # If the statements are OpenSesame-style, all the work is done by
            # the var store
            f = lambda stm: self.var.get(stm)
        # If a custom Python script is provided, it's byte-compiled
        script = self.var.get(u'script', _eval=False).strip()
        script = None if not script else self.python_workspace._compile(script)
        self.is_active = False
        yield # Preparation done

        # Run, PsychoPy, run!
        self.is_active = True
        while alive:
            now = self.clock.time()
            if last_update is None or \
                    (self.var.framerate >= 0 and \
                    now - last_update >= self.var.framerate):
                if script is not None:
                    self.python_workspace._exec(script)
                self.experiment._psychopystim_needflip = True
                last_update = now
                self._update_attributes(f)
            alive = yield
        # Remove the grating from the queue when done
        self.experiment._psychopystim_queue.remove(self)
        self.experiment._psychopystim_needflip = True
        self.is_active = False

    @property
    def _stimclass(self):

        raise NotImplementedError()

    def _prepare_bytecode(self, c):

        return {
            u'color' 		: c(u'color'),
            u'contrast' 	: c(u'contrast'),
            u'opacity' 		: c(u'opacity'),
            u'xpos' 		: c(u'xpos'),
            u'ypos' 		: c(u'ypos'),
            u'ori' 			: c(u'ori')
            }

    def _update_attributes(self, f):

        self._stim.color 		= f(u'color')
        self._stim.contrast 	= f(u'contrast')
        self._stim.opacity 		= f(u'opacity')
        self._stim.pos 			= f(u'xpos'), f(u'ypos')
        self._stim.ori 			= f(u'ori')

    def winflip(self):

        if not self.experiment._psychopystim_needflip:
            return
        for item_ in self.experiment._psychopystim_queue:
            if item_.is_active:
                item_._stim.draw()
        self.experiment.window.flip()
        self.experiment._psychopystim_needflip = False

    def prepare(self):

        item.prepare(self)
        self._coroutine = self.coroutine()
        next(self._coroutine)

    def run(self):

        self._coroutine.send(False)
        self._stim.draw()
        self.experiment.window.flip()
