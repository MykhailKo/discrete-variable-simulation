from simulation_model import DiscreteVarSimulation
from probability_theory_utils import *
from chart_builder import *

SEGMENT_BOTTOM = 3
SEGMENT_TOP = 5

sim_time = 120
events = [0, 1, 2, 3, 4, 5]
event_probs = [0.1, 0.15, 0.3, 0.2, 0.13, 0.12]

base_dist_series = {events[i]: event_probs[i] for i in range(len(events))}
ref_exp_val = get_discrete_expected_value(base_dist_series)
ref_dispersion = get_discrete_dispertion(base_dist_series)
ref_seg_prob = get_discrete_segment_prob(
    SEGMENT_BOTTOM, SEGMENT_TOP, gen_discrete_dist_function(base_dist_series))

model = DiscreteVarSimulation(events, event_probs, sim_time, True)
model.feed_random_events(sim_time)

sim_dist_series = model.get_sim_dist_series()
sim_exp_val = get_discrete_expected_value(sim_dist_series)
sim_dispersion = get_discrete_dispertion(sim_dist_series)
sim_seg_prob = get_discrete_segment_prob(
    SEGMENT_BOTTOM, SEGMENT_TOP, gen_discrete_dist_function(sim_dist_series))

print(f'Simulation dist series: {sim_dist_series}')

prob_polygon_chart(events, event_probs, list(
    model.get_sim_dist_series().values()))

var_attrs_chart(ref_exp_val, ref_dispersion, ref_seg_prob,
                sim_exp_val, sim_dispersion, sim_seg_prob)
