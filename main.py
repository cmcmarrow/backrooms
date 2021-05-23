from backrooms.backrooms import Hallway, BackRoomsCord, Backrooms, BackroomsD, BackRoomsCordD

r = Backrooms("chad", {BackRoomsCord(1, 1): "d"}, [Hallway("Main", BackRoomsCord()), Hallway("ug", BackRoomsCord(-10))])
d = BackroomsD({0: r})

print(d.in_hallway(BackRoomsCordD()))
