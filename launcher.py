from email.mime import base
from sys import argv

from simulation_model import DiscreteVarSimulation
from probability_theory_utils import *
from chart_builder import *

# Task constant givens
SEGMENT_BOTTOM = 3
SEGMENT_TOP = 5
EVENTS = [0, 1, 2, 3, 4, 5]


class Launcher:
    def run_individual_experiment(self, events, event_probs, sim_time, demo=True):
        # construct given distribution series
        base_dist_series = {events[i]: event_probs[i]
                            for i in range(len(events))}
        # find reference theoretical results
        ref_exp_val = get_discrete_expected_value(base_dist_series)
        ref_dispersion = get_discrete_dispertion(base_dist_series)
        ref_seg_prob = get_discrete_segment_prob(
            SEGMENT_BOTTOM, SEGMENT_TOP, gen_discrete_dist_function(base_dist_series))
        if demo:
            print(f'Given distribution series: \n{base_dist_series}')
            print(
                f'Thoretical results: E(X)={ref_exp_val}, D(X)={ref_dispersion}, P(3≤X≤5)={ref_seg_prob}')
        # create simuation model
        model = DiscreteVarSimulation(events, event_probs, sim_time, demo)
        model.feed_random_events(sim_time)
        # get simulated distribution series
        sim_dist_series = model.get_sim_dist_series()
        # find simulation results
        sim_exp_val = get_discrete_expected_value(sim_dist_series)
        sim_dispersion = get_discrete_dispertion(sim_dist_series)
        sim_seg_prob = get_discrete_segment_prob(
            SEGMENT_BOTTOM, SEGMENT_TOP, gen_discrete_dist_function(sim_dist_series))
        if demo:
            print(f'Simulated distribution series: \n{sim_dist_series}')
            print(
                f'Simulation results: E(X)={sim_exp_val}, D(X)={sim_dispersion}, P(3≤X≤5)={sim_seg_prob}')
            prob_polygon_chart(events, event_probs,
                               list(sim_dist_series.values()))
            var_attrs_chart(ref_exp_val, ref_dispersion, ref_seg_prob,
                            sim_exp_val, sim_dispersion, sim_seg_prob)

    def run_statistical_experiment(self, events, sim_time_from, sim_time_to, sim_time_step, demo):
        None


# sim_time = 120
# event_probs = [0.1, 0.15, 0.3, 0.2, 0.13, 0.12]
launcher = Launcher()
params = {'run': None, 'sim-time': None, 'event-probs': None,
          'sim-time-from': None, 'sim-time-to': None, 'sim-time-step': None, 'demo': False}
for p in argv[1:]:
    key = p.split('=')[0] if '=' in p else p
    value = p.split('=')[1] if '=' in p else True
    params[key] = value
    print(f'Setting param {key} to {value}')
if params['run'] == 'individual':
    event_probs = list(map(float, params['event-probs'].split(',')))
    launcher.run_individual_experiment(
        EVENTS, event_probs, int(params['sim-time']))
elif params['run'] == 'statistical':
    launcher.run_statistical_experiment(
        EVENTS, int(params['sim-time-from']), int(params['sim-time-to']), int(params['sim-time-step']), params['demo'])
