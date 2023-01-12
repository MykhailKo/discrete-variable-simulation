import random
import uuid
import math


def get_discrete_expected_value(dist_series):
    return sum([e*dist_series[e] for e in dist_series])


def get_discrete_dispertion(dist_series):
    squared_var = {e**2: dist_series[e] for e in dist_series}
    return get_discrete_expected_value(squared_var) - get_discrete_expected_value(dist_series)**2


def gen_discrete_dist_function(dist_series):
    events = list(dist_series.keys())
    probs = list(dist_series.values())
    dist_function = {f'{0}:{uuid.uuid4()}': [float('-inf'), events[0]]}
    for i in range(1, len(events)):
        dist_function[f'{sum(probs[0:i])}:{uuid.uuid4()}'] = [
            events[i-1], events[i]]
    dist_function[f'{sum(probs)}:{uuid.uuid4()}'] = [events[-1], float('inf')]
    return dist_function


def get_prob_from_dist_func(event, dist_func, max=False):
    pos = 0 if max else 1
    return float(list(filter(lambda eq: eq[1][pos] == event, list(dist_func.items())))[0][0].split(':')[0])


def get_discrete_segment_prob(bottom, top, dist_func):
    if top < bottom:
        raise ValueError(
            'Bottom boundary of segment is bigger than top boundary')
    bottom_max_prob = get_prob_from_dist_func(bottom, dist_func, True)
    top_max_prob = get_prob_from_dist_func(top, dist_func, True)
    bottom_prob = get_prob_from_dist_func(bottom, dist_func)
    return bottom_max_prob - 2*bottom_prob + top_max_prob


def gen_full_event_set_probs(events_num, prob_prec):
    probs = []
    for i in range(int(round(events_num*0.6))):
        new_prob = round(random.uniform(0, 1/(events_num/1.8)), prob_prec)
        probs.append(new_prob)
    for i in range(int(round(events_num*0.4))-1):
        new_prob = round(random.uniform(0, 1-sum(probs)), prob_prec)
        probs.append(new_prob)
    probs.append(round(1-sum(probs), prob_prec))
    random.shuffle(probs)
    if len(probs) > events_num:
        for i in range(len(probs) - events_num):
            if probs.pop(probs.index(0)) != 0:
                probs.pop(-1)
    return probs


def gen_exact_full_event_set_probs(events_num, prob_prec=2):
    sum_check = 0.0
    probs = []
    while sum_check != 1.0 or math.prod(probs) < 0:
        probs = gen_full_event_set_probs(events_num, prob_prec)
        sum_check = sum(probs)
    return probs
