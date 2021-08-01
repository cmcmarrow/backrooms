##################
backrooms - v1.0.0
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

***********
Hello World
***********
``hello_world.brs``

.. code-block:: text

   ~GATE
   /rs"Hello World!"e~ha

************
Installation
************
.. code-block:: bash

   pip install backrooms

*****************
Console Interface
*****************
.. code-block:: bash

   backrooms hello_world.brs

.. code-block:: text

   backrooms

   positional arguments:
     file                  path to main file

   optional arguments:
     -h, --help            show this help message and exit
     -a, --author          get author of backrooms
     -b, --builtins        don't include built-in libraries
     -c, --core_dump       enables CoreDump rule "?"
     -e, --error-on-space  errors if portal lands on a space
     -p, --profile         profiles backrooms
     -s, --system-out      don't write to stdio
     -v, --version         get version of backrooms
     --lost-count LOST_COUNT
                           set lost count
     --lost-rule-count LOST_RULE_COUNT
                           set lost rule count
     --profile_range PROFILE_RANGE
     --whisper WHISPER     set the log level [notset, debug, info, warning, error, critical]

*************
Documentation
*************
* `Documentation <https://esolangs.org/wiki/Backrooms>`_
* `Raw Documentation <https://github.com/cmcmarrow/backrooms/blob/master/DOCUMENTATION.txt>`_

*******
Bottles
*******
``bottles.brs``

.. code-block:: text

   ~GATE
   /ri10ibri99>ers" bottles of beer on the wall, "epers" bottles of beer."epzezri-1iaV
   /Vzeezpe".llaw eht no reeb fo selttob "srepe" ,dnuora ti ssap dna nwod eno ekaT"sr<
   /.>e~ha    1 >rs"1 bottle of beer on the wall, 1 bottle of beer."epers"Take one"epV
   /.p        p pVe".llaw eht no reeb fo selttob erom on ,dnuora ti ssap dna nwod "sr<
   /.e        . p>peers"No more bottles of beer on the wall, no more bottles of beer"V
   />.dri-1iaN^.^                                                                    e
   / ^".llaw eht no reeb fo selttob 99 ,erom emos yub dna erots eht ot oG"srepe"."srp<

******
Turing
******
``turing.brs``

.. code-block:: text

   ~GATE
   /cicOvZVpri1V
   /    p >.e>NV~ha
   /    >ri1e^e<

*********
Fibonacci
*********
``fibonacci.brs``

.. code-block:: text

   ~GATE
   /ri0>dri16isZVpri1zdV
   /   .     ah~<      >....V
   /   ^aipe" "srpech"BIF"sr<
   ~FIB
   />ZVdri3isLVpdri1isrs"FIB"hczri2isrs"FIB"hciahr
   /rh<rh1irpp<

***********
Tic Tac Toe
***********
``tic_tac_toe.brs``

.. code-block:: text

   ~GATE
   />ri0>.ri1iadri10isNVpprs"x"k0pri10ibrs"Tic Tac Toe!"epepri0V
   /.   ^..hujbz"k"srdp<           a                    >pri1ia>dri9isNVpprs"E_BOARD"hcrs"Cats!"ep...V
   /.                              h   >..rs"C_BOARD"hcZ^rs"E_BOARD"hceprs" won!"epri10ibeppVpebi01ir<
   /.                              ~   ^................huch"DRAOB_U"sr<                    .
   /^.............................p^Zeb"a"srcpe+ >>+srpebi01irpe+!niaga yalp ot "a" retnE+sr<
   # Echo board
   ~E_BOARD
   />ri10ibrs"#"s1epes2epes3epzezeeeeezezs4epes5epes6epzezeeeeezezs7epes8epes9eppephr
   # Update board
   ~U_BOARD
   />rs"rs+"s0bjrs"+k"bjV                      >pbjrs"prs+"bjs0rs"x"beZVprs"o">bjrs"+k0p">bjhr
   /  Vpe0sch"DRAOB_E"sr<.pebi01irpe"RORRE"srpp^Nib"123456789"sr<      >prs"x"^
   /  >rs": "epcdri10ibeprs"1~2~3~4~5~6~7~8~9"biZVpdrs"s"zbjuh..^
   /                    ^....ebi01irpe"RORRE"srpp<
   # Check for winner
   ~C_BOARD
   /V                         >ppzphr
   />s5ds1beNVpd.....V    >beN^ppp..V                  >ppzphr
   /         >pds9beZVphr ^oupp<    3            V..ppp^Neb<
   /                 >pds3beNVpd.....V           .    >ppuo^
   /                         >pds7beZVphr  Vai1ir<pppp^Nebou..hujbz"s"srai3ir<
   /                           2     >ppri0>dri3isNVpprs""hr                 z
   /   >zri1iars"s"zbjuh..uobeN^pppp>dri1iadrs"s"z1pbjuh..zri3iadrs"s"zbjuh..^
   /   ^..hujbz"s"srdai1irz..hujbz"s"srdai1irmi3ird<

****************
Build Executable
****************
.. code-block:: bash

   git clone https://github.com/cmcmarrow/backrooms.git
   pip install -e .[dev]
   python build.py

***
API
***
``backrooms_api.py``

.. code-block:: python

   from backrooms.backrooms import backrooms_api, StringHandler


   main_brs = """
   ~GATE
   /rs"Hello World"e~ha
   """

   main_handler = StringHandler("main", main_brs)
   backrooms_api(main_handler)()

.. code-block:: text

   info: An API to backrooms.
   :param code: Union[str, Handler, Handlers]
       str: Will treat str as main file and load its dir.
       Handler: Will load just the single Handler.
       Handlers: Will load the Handlers.
   :param inputs: Optional[Tuple[str, ...]]
   :param sys_output: bool
   :param catch_output: bool
   :param lost_count: int
   :param lost_rule_count: int
   :param error_on_space: bool
   :param br_builtins: bool
       Only adds builtins if code is str or Handler.
   :param core_dump: bool
   :param rules: Optional[Tuple[Type[Rule]]]
   :param whisper_level: str
   :return: Portal
