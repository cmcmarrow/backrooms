##################
Backrooms - v0.4.0
##################

********
Warning!
********
Backrooms is still in Development Status Alpha!
This means rules "intrusions" MAY still change!
But the Esolang is close to being finalized.

*****
About
*****
This python module "backrooms" is an `Esolang <https://esolangs.org/wiki/Main_Page>`_.

backrooms was inspired by:
    * backrooms Creepypasta/MEME
    * ASCIIDOTS Esolang
    * CISC Architecture

Backrooms was designed to be:
    * hackable VIA memory overflow attacks, poor error handling, ect.
    * visually pleasing.
    * enjoy able to write small/medium programs.
    * capable to rewrite all of a program at run-time.

********
Road Map
********
* v0.4.0
    * Development Status :: 4 - Beta
    * Add builtin libraries
    * Tests and bug fixes
    * Add examples
    * Update translator
    * Improve rule error handling
* v1.0.0
    * Development Status :: 5 - Production/Stable
    * Clean code
    * Write documentation
    * Tests and bug fixes
* v1.1.0
    * Development Status :: 6 - Mature
    * Make Backrooms faster
        * Rooms.set_hallway_name, Big-O(n) -> Big-O(n log(n))
        * Rooms.remove_hallway, Big-O(n) -> Big-O(n log(n))
        * Portal.new_conscious, Big-O(n) -> Big-O(n log(n))
        * etc ...
