from backrooms import loader
from backrooms.btime import BTime

f = """
# hello this is a commit
~ M
/ lol
~ GATE
/asd;lfjkasdfkl;ask;jldf
/asfsfjasjasdqwerwqerqwe
/asdfsadfdgdsfgdsfgqwerq
+ other
/asfasdfsdfgdsfgqwerqwer
/...... ...... . .. . . 
%bob
"""

bob = """
~bob
/lol
"""

l = loader.StrLoader("f", f)
l2 = loader.StrLoader("bob", bob)

i = loader.Iterator("f", [[l, l2]])
d = loader.build(i)
BTime(d, [])
