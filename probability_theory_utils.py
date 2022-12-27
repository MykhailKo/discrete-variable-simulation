def get_discrete_expected_value(dist_series):
    return sum([e*dist_series[e] for e in dist_series])


def get_discrete_dispertion(dist_series):
    squared_var = {e**2: dist_series[e] for e in dist_series}
    return get_discrete_expected_value(squared_var) - get_discrete_expected_value(dist_series)**2


def gen_discrete_dist_function(dist_series):
    events = list(dist_series.keys())
    probs = list(dist_series.values())
    dist_function = {str(0): [float('-inf'), events[0]]}
    for i in range(1, len(events)):
        dist_function[str(sum(probs[0:i]))] = [events[i-1], events[i]]
    dist_function[str(sum(probs))] = [events[-1], float('inf')]
    return dist_function


def get_prob_from_dist_func(event, dist_func, max=False):
    pos = 0 if max else 1
    return float(list(filter(lambda eq: eq[1][pos] == event, list(dist_func.items())))[0][0])


def get_discrete_segment_prob(bottom, top, dist_func):
    if top < bottom:
        raise ValueError(
            'Bottom boundary of segment is bigger than top boundary')
    bottom_max_prob = get_prob_from_dist_func(bottom, dist_func, True)
    top_max_prob = get_prob_from_dist_func(top, dist_func, True)
    bottom_prob = get_prob_from_dist_func(bottom, dist_func)
    return bottom_max_prob - 2*bottom_prob + top_max_prob
