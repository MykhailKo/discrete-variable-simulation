import random


class DiscreteVarSimulation:
    def __init__(self, events, probs, sim_time, log=False):
        self._events = events
        self._probs = probs
        self._sim_time = sim_time
        self._sim_time_left = sim_time
        self._sim_history = []
        self._log = log
        self.validate_series()
        self.gen_sim_event_pool()

    def gen_sim_event_pool(self):
        time, e, p = self._sim_time, self._events, self._probs
        self._event_pool = [event for repeats in [[e[i] for j in range(
            round(p[i]*time + 0.01))] for i in range(len(e))] for event in repeats]
        event_count_left = [p[i]*time -
                            round(p[i]*time) for i in range(len(p))]
        for i in range(time - len(self._event_pool)):
            self._event_pool.append(event_count_left.pop(
                event_count_left.index(max(event_count_left))))

    def random_event(self):
        cur_event = random.choice(self._event_pool)
        self._event_pool.remove(cur_event)
        self._sim_time_left -= 1
        self._sim_history.append(cur_event)
        return cur_event

    def feed_random_events(self, time):
        if time > self._sim_time_left:
            raise ValueError(
                'Feed time is longer than leftover simulation time')
        for t in range(time):
            cur_event = self.random_event()
            # if self._log:
            #     print(f'T:{self._sim_time-self._sim_time_left} E:{cur_event}')

    def get_sim_dist_series(self):
        hist = self._sim_history
        events = self._events
        time_elapsed = self._sim_time - self._sim_time_left
        dist_series = {e: hist.count(e)/time_elapsed for e in events}
        return dist_series

    def validate_series(self):
        if len(self._events) != len(self._probs):
            raise ValueError(
                'Events and probabilities list lengths are not equal')
        if sum(self._probs) != 1.0:
            raise ValueError(
                'Full event set probabilities sum is not equal to 1')

    def reset(self):
        self._sim_time_left = self._sim_time
        self._sim_history = []
        self.gen_sim_event_pool()
