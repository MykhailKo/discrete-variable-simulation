import matplotlib.pyplot as plt


def create_comparisson_chart(x1, x2, y1, y2, x_label, y_label, name, label1, label2, line=True):
    format = '-' if line else 'o'
    plt.figure(1)
    plt.title(name)
    plt.plot(x1, y1, f'{format}b', label=label1)
    plt.plot(x2, y2, f'{format}y', label=label2)
    plt.legend()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def prob_polygon_chart(events, ref_probs, sim_probs):
    create_comparisson_chart(
        events,
        events,
        ref_probs,
        sim_probs,
        'x',
        'P(x)',
        'Probability polygon',
        'reference',
        'simulation'
    )


def var_attrs_chart(ref_ev, ref_disp, ref_seg_prob, sim_ev, sim_disp, sim_seg_prob):
    attr_names = ['Expected value', 'Dispersion', 'Segment probability']
    create_comparisson_chart(
        attr_names,
        attr_names,
        [ref_ev, ref_disp, ref_seg_prob],
        [sim_ev, sim_disp, sim_seg_prob],
        'attribute',
        'value',
        'Random variable numeric attributes',
        'reference',
        'simulation',
        False
    )
