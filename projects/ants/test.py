from ants_plans import *
from ants import *
beehive, layout = Hive(make_test_assault_plan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
#
# Testing TankAnt action
tank = TankAnt()
place = gamestate.places['tunnel_0_1']
place.add_insect(tank)
for _ in range(3):
    place.add_insect(Bee(1))
print('len bees before', len(place.bees))

tank.action(gamestate)
print('len bees', len(place.bees))