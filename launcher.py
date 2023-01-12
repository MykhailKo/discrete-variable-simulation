from sys import argv
from statistics import mean

from simulation_model import DiscreteVarSimulation
from probability_theory_utils import *
from chart_builder import *

# Task constant givens
SEGMENT_BOTTOM = 3
SEGMENT_TOP = 5
EVENTS = [0, 1, 2, 3, 4, 5]


class Launcher:
    def run_individual_experiment(self, disc_var_model=None, events=[], event_probs=[], sim_time=0, demo=True):
        # construct given distribution series
        base_dist_series = {events[i]: event_probs[i]
                            for i in range(len(events))}
        # find reference theoretical results
        ref_exp_val = get_discrete_expected_value(base_dist_series)
        ref_dispersion = get_discrete_dispertion(base_dist_series)
        ref_seg_prob = get_discrete_segment_prob(
            SEGMENT_BOTTOM, SEGMENT_TOP, gen_discrete_dist_function(base_dist_series))
        # create simulation model
        model = disc_var_model if disc_var_model else DiscreteVarSimulation(
            events, event_probs, sim_time, demo)
        model.feed_random_events(sim_time)
        # get simulated distribution series
        sim_dist_series = model.get_sim_dist_series()
        # find simulation results
        sim_exp_val = get_discrete_expected_value(sim_dist_series)
        sim_dispersion = get_discrete_dispertion(sim_dist_series)
        sim_seg_prob = get_discrete_segment_prob(
            SEGMENT_BOTTOM, SEGMENT_TOP, gen_discrete_dist_function(sim_dist_series))
        if demo:
            print(f'Given distribution series: \n{base_dist_series}')
            print(
                f'Thoretical results: E(X)={ref_exp_val}, D(X)={ref_dispersion}, P(3≤X≤5)={ref_seg_prob}')
            print(f'Simulated distribution series: \n{sim_dist_series}')
            print(
                f'Simulation results: E(X)={sim_exp_val}, D(X)={sim_dispersion}, P(3≤X≤5)={sim_seg_prob}')
            prob_polygon_chart(events, event_probs,
                               list(sim_dist_series.values()))
            var_attrs_chart(ref_exp_val, ref_dispersion, ref_seg_prob,
                            sim_exp_val, sim_dispersion, sim_seg_prob)
        return {
            'ref': {
                'exp_val': ref_exp_val, 'dispersion': ref_dispersion, 'seg_prob': ref_seg_prob
            },
            'sim': {
                'exp_val': sim_exp_val, 'dispersion': sim_dispersion, 'seg_prob': sim_seg_prob
            }
        }

    def run_statistical_experiment(self, events, exp_number, sim_time_from, sim_time_to, sim_time_step, demo):
        # validate simulation time inputs
        if(sim_time_from > sim_time_to):
            raise ValueError(
                f'Simulation time segment bottom value is bigger than top value: {sim_time_from}>{sim_time_to}')
        if((sim_time_to-sim_time_from) % sim_time_step != 0):
            raise ValueError(
                f'Simulation time segment size is not a multiple of step size: ({sim_time_to}-{sim_time_from})/${sim_time_step} is not integer')
        # loop through experiment time sizes
        for time in range(sim_time_from, sim_time_to, sim_time_step):
            # generate random probs for full events set
            event_probs = gen_exact_full_event_set_probs(len(events))
            print(f'Generated event probs: {event_probs}')
            # create simulation model
            model = DiscreteVarSimulation(events, event_probs, time)
            # create list for experiment records
            experimet_records = []
            # repeat experiment for given number of times
            for i in range(exp_number):
                experiment_result = self.run_individual_experiment(
                    model, events, event_probs, time, demo)
                # save record
                experimet_records.append(experiment_result)
                # reset model to initial state
                model.reset()
            average_errors = {
                'exp_val': round(mean([get_abs_error(rec['ref']['exp_val'], rec['sim']['exp_val']) for rec in experimet_records]), 4),
                'dispersion': round(mean([get_abs_error(rec['ref']['dispersion'], rec['sim']['dispersion']) for rec in experimet_records]), 4),
                'seg_prob': round(mean([get_abs_error(rec['ref']['seg_prob'], rec['sim']['seg_prob']) for rec in experimet_records]), 4)
            }
            print(
                f'Average absolute errors: ε(E(X))={average_errors["exp_val"]}, ε(D(X))={average_errors["dispersion"]}, ε(P(3≤X≤5))={average_errors["seg_prob"]}')


# sim_time = 120
# event_probs = [0.1, 0.15, 0.3, 0.2, 0.13, 0.12]
launcher = Launcher()
params = {'run': None, 'sim-time': None, 'event-probs': None, 'experiments-number': None,
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
        EVENTS, int(params['experiments-number']), int(params['sim-time-from']), int(params['sim-time-to']), int(params['sim-time-step']), params['demo'])
