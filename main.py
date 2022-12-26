import random
from simulation_model import DiscreteVarSimulation

sim_time = 200
events = [0, 1, 2, 3, 4, 5]
event_probs = [0.1, 0.15, 0.3, 0.2, 0.13, 0.12]

model = DiscreteVarSimulation(events, event_probs, sim_time, True)

model.feed_random_events(50)
print(f'Dist series: {model.get_sim_dist_series()}')
model.feed_random_events(70)
print(f'Dist series: {model.get_sim_dist_series()}')
model.feed_random_events(30)
print(f'Dist series: {model.get_sim_dist_series()}')
model.feed_random_events(50)
print(f'Dist series: {model.get_sim_dist_series()}')
