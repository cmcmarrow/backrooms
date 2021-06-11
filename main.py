from backrooms.translator import translator, Handlers, StringHandler
# TODO write

x = """
x = 2345
y =    435,32
"""

y = """
c = 2345,2532
"""
h = Handlers(StringHandler("x", x), ((StringHandler("y", y),),))
h.include("y")
rooms = translator(h)
