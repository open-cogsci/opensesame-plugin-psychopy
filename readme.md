# PsychoPy plugins for OpenSesame

Copyright (2016) Sebastiaan Mathôt


## Installation

In a terminal:

~~~
pip install psychopy-plugin-opensesame
~~~

In the OpenSesame debug window:

~~~
import pip
pip.main(['install', 'psychopy-plugin-opensesame'])
~~~

See also:

- http://osdoc.cogsci.nl/3.1/manual/environment/


## About

For the moment, there's only one plugin: `psychopy_gratingstim`.

### GratingStim plugin (`psychopy_gratingstim`)

The [GratingStim](http://www.psychopy.org/api/visual/gratingstim.html) is a visual stimulus from PsychoPy, a Python library for psychology.

With this plugin, you can use the GratingStim easily within OpenSesame, a graphical experiment builder for the social sciences. You can use the plugin in OpenSesame [coroutines](http://osdoc.cogsci.nl/3.1/manual/structure/coroutines/), and adjust its properties periodically; this allows you, for example, to implement a drifting gabor patch.


## License

This software is distributed under the terms of the GNU General Public License 3. The full license should be included in the file `COPYING`, or can be obtained from:

- <http://www.gnu.org/licenses/gpl.txt>
