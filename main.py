from backrooms import loader
from backrooms.btime import BTime
from backrooms.rules import get_built_in_rules

main = """
~GATE
/ts"Hello World"nneennha*
"""


main_loader = loader.StrLoader("main", main)

loader_iterator = loader.LoaderIterator("main", [[main_loader]])
backrooms_d = loader.build(loader_iterator)
b = BTime(backrooms_d, get_built_in_rules())
b.run()
print("DONE!")
