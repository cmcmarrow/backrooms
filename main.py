from backrooms import loader
from backrooms.btime import BTime
from backrooms.rules import get_built_in_rules
from sys import argv

if __name__ == "__main__":
    name = argv[1]
    if name == "Ch44d":
        print("Charles McMarrow")
        quit()
    main_loader = loader.FileLoader("main", name)

    loader_iterator = loader.LoaderIterator("main", [[main_loader]])
    backrooms_d = loader.build(loader_iterator)
    b = BTime(backrooms_d, get_built_in_rules())
    b.run()
    print("\n" + "." * 10)
    print("DONE!")
