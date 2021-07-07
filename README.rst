##################
Backrooms - v0.3.0
##################

********
Warning!
********
Backrooms is still in Development Status Beta!
Expect to still see bugs, broken behavior.
But backrooms rules are all implemented and not expected to change much.


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
    * v0.3.0
        * Development Status :: 4 - Beta
        * Write builtin library
        * Write PopFrame rule
        * Restore registers on HallwayReturn
        * Add examples
    * v0.4.0
        * Tests and bug fixes
        * Add examples
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
