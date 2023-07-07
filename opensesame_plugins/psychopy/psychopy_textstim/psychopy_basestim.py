"""This file is part of OpenSesame.

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
from libopensesame.exceptions import MissingDependency, OSException, \
    PythonSyntaxError, PythonError
from libopensesame.item import Item


class PsychopyBasestim(Item):

    def reset(self):
        self.var.framerate = -1
        self.var.interpretation = 'python'
        self.var.xpos = 0
        self.var.ypos = 0
        self.var.ori = 0
        self.var.color = "'white'"
        self.var.contrast = 1
        self.var.opacity = 1
        self.var.script = ''
        self.var.order = 0

    def coroutine(self, coroutines=None):
        try:
            from psychopy.visual import Window
        except ImportError as e:
            raise MissingDependency('Failed to import PsychoPy')
        # Check whether the PsychoPy window is available
        if not hasattr(self.experiment, 'window') or \
                not isinstance(self.experiment.window, Window):
            raise OSException('No PsychoPy window available. Have you '
                              'selected the psychopy backend?')
        self._stim = self._stimclass(self.experiment.window)
        # Make sure that the window is flipped after every cycle
        if coroutines is not None and \
                self.winflip not in coroutines.post_cycle_functions:
            coroutines.post_cycle_functions.append(self.winflip)
            self.experiment._psychopystim_needflip = False
        # Add all gratings to the grating queue, which is drawn in order
        # before the window flip. We sort the queue to control the drawing
        # order/ depth/ z-index of the stimuli.
        if not hasattr(self.experiment, '_psychopystim_queue'):
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
        # OpenSesame-style values, which are evaluated by the syntax module
        # when the variable is retrieved.
        if self.var.interpretation == 'python':
            # A compile function that gets a statement, converts it to a str,
            # and then byte-compiles it to a code object. We cannot use
            # python_workspace._compile(), because this assumes exec
            # statements.
            def c(stm):
                script = safe_decode(self.var.get(stm, _eval=False))
                try:
                    return compile(script, '<string>', 'eval')  # __ignore_traceback__
                except SyntaxError as e:
                    raise PythonSyntaxError(
                        f'Syntax error in Python expression',
                        line_nr=e.lineno)
            # The compile function is then applied to all statements so that
            # they are precompiled. This is done in another function so that it
            # can be overridden.
            bytecode = self._prepare_bytecode(c)
            # And the evalutation function just evals the bytecode
            def f(stm):
                try:
                    return self.python_workspace._eval(bytecode[stm])
                except Exception as e:
                    raise PythonError(
                        'Error while evaluating Python expression')
        else:
            # If the statements are OpenSesame-style, all the work is done by
            # the var store
            def f(stm): return self.var.get(stm)
        # If a custom Python script is provided, it's byte-compiled
        script = self.var.get('script', _eval=False).strip()
        script = None if not script else self.python_workspace._compile(script)
        self.is_active = False
        yield  # Preparation done

        # Run, PsychoPy, run!
        self.is_active = True
        while alive:
            now = self.clock.time()
            if last_update is None or \
                    (self.var.framerate >= 0
                     and now - last_update >= self.var.framerate):
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
            'color': c('color'),
            'contrast': c('contrast'),
            'opacity': c('opacity'),
            'xpos': c('xpos'),
            'ypos': c('ypos'),
            'ori': c('ori')
        }

    def _update_attributes(self, f):
        self._stim.color = f('color')
        self._stim.contrast = f('contrast')
        self._stim.opacity = f('opacity')
        self._stim.pos = f('xpos'), f('ypos')
        self._stim.ori = f('ori')

    def winflip(self):
        if not self.experiment._psychopystim_needflip:
            return
        for item_ in self.experiment._psychopystim_queue:
            if item_.is_active:
                item_._stim.draw()
        self.experiment.window.flip()
        self.experiment._psychopystim_needflip = False

    def prepare(self):
        super().prepare()
        self._coroutine = self.coroutine()
        next(self._coroutine)

    def run(self):
        self._coroutine.send(False)
        self._stim.draw()
        self.experiment.window.flip()
