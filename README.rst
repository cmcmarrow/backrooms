##################
Backrooms - v0.4.0
##################

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
    * enjoyable to write small/medium programs.
    * capable to rewrite all of a program at run-time.

********
Warning!
********
Backrooms is still in Development Status Beta!
This means rules "intrusions" have been finalized!
Expect to see some share edges still.

******
v0.4.0
******
* Development Status :: 4 - Beta
* Add builtin libraries
* Tests and bug fixes
* Add examples
* Update Translator only allow valid row characters
* Improve Rule error handling
* Remove Worker Rule
* Add ThreadLock Rule
* Add ThreadUnlock Rule
* Add UncommonHotPatch Rule
* Add UncommonSimpleDump Rule
* Add Forward Mirror
* Add Backward Mirror
* Add Fall Back to must Rules
* Modified Store Rule
* Modified Keep Rule
* Modified UncommonDynamicDump Rule
* Modified Thread Rule
* Modified HallwayModule
* Modified LevelModule

********
Road Map
********
* Add ClearStack Rule
* v1.0.0
    * Development Status :: 5 - Production/Stable
    * Clean code
    * Write documentation
    * Tests and bug fixes
* v1.1.0
    * Development Status :: 6 - Mature
    * Clean code
    * Make Backrooms faster
        * Rooms.set_hallway_name, Big-O(n) -> Big-O(n log(n))
        * Rooms.remove_hallway, Big-O(n) -> Big-O(n log(n))
        * Portal.new_conscious, Big-O(n) -> Big-O(n log(n))
        * etc ...
