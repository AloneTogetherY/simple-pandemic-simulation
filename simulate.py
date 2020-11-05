import argparse
import random
import time
from math import isclose

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pylab
from matplotlib.animation import FuncAnimation


def decision(probability):
    return random.random() < probability


def get_max_length(line_rs, line_ds):
    length = 5
    if not all(v == 0 for v in line_rs) or not all(v == 0 for v in line_ds):
        length = max(line_ds)
        if max(line_rs) > length:
            length = max(line_rs)
    return length + 2


def create_legend():
    classes = ['not infected', 'infected', 'recovered', 'died']
    class_colors = ['grey', 'red', 'lime', 'black', ]
    recs = []
    for i in range(0, len(class_colors)):
        recs.append(mpatches.Rectangle((0, 0), 1, 1, fc=class_colors[i]))
    plt.legend(recs, classes, loc='upper center', bbox_to_anchor=(0.50, 2.6), ncol=4)


def random_condition_change(infection_map, confirmed_deaths, confirmed_immune, line_deaths, line_recoveries,
                            scatter_plots):
    milliseconds = 1000
    d = 0
    r = 0
    for this in range(no_of_points):
        if decision(0.9):
            # shuffle infected persons to create more randomness regarding the ones which recover or die
            shuffled_dict = list(infection_map.items())
            random.shuffle(shuffled_dict)
            for key, value in dict(shuffled_dict).items():
                time_to_recover = random.sample(range(min_time_to_recover, max_time_to_recover), 1)[0]
                time_to_death = random.sample(range(min_time_to_death, max_time_to_death), 1)[0]
                if decision(0.5):
                    if key in infected_indices and key == this and (
                            round(time.time() * milliseconds) - value) >= time_to_recover:
                        if len(confirmed_immune) < int(immunity_rate):
                            scatter_plots[this].set_color('lime')
                            confirmed_immune.append(this)
                            infected_indices.remove(key)
                            r += 1
                else:
                    if key in infected_indices and key == this and (
                            round(time.time() * milliseconds) - value) >= time_to_death and decision(0.2):
                        if len(confirmed_deaths) < int(death_rate):
                            scatter_plots[this].set_color('black')
                            scatter_plots[this].set_marker('P')
                            confirmed_deaths.append(this)
                            infected_indices.remove(key)
                            d += 1

    line_deaths.append(d)
    line_recoveries.append(r)


def create_simulation_data(no_of_pts, dirs, sim_steps, xrange, yrange):
    xs, ys = [], []
    x = [random.uniform(xrange[0], xrange[1]) for _ in range(no_of_pts)]
    y = [random.uniform(yrange[0], yrange[1]) for _ in range(no_of_pts)]
    for index, (xtemp, ytemp) in enumerate(zip(x, y)):
        x_list, y_list = [], []
        x_list.append(xtemp)
        y_list.append(ytemp)
        for _ in range(sim_steps):
            x_list.append(x_list[-1] + dirs[random.randrange(dirs.shape[0])])
            y_list.append(y_list[-1] + dirs[random.randrange(dirs.shape[0])])
        xs.append(x_list)
        ys.append(y_list)

    return xs, ys


def setup_plots():
    fig, (ax, ax1, ax2) = plt.subplots(3, 1, figsize=(8, 8))
    scatter_plots = [ax.plot([], [], 'o', c='red', markersize=5)[0] if i < no_of_initial_infected else
                     ax.plot([], [], 'o', c='silver', markersize=5)[0] for i in range(no_of_points)]
    fig.subplots_adjust(bottom=0.4)
    fig.tight_layout(pad=3.0)
    fig = pylab.gcf()
    fig.canvas.set_window_title('Simulation')

    line_plot = ax1.plot([], [], c='red', linewidth=1.0)[0]
    line_plots = [
        ax2.plot([], [], c='lime', linewidth=1.0)[0],
        ax2.plot([], [], c='black', linewidth=1.0)[0]]
    ax1.set_ylabel('infected')
    ax1.set_xlabel('step')
    ax2.set_ylabel('recovered / died')
    ax2.set_xlabel('step')
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    return fig, ax, ax1, ax2, scatter_plots, line_plot, line_plots


def animate():
    directions = np.array([0, .1, .2, .3, -.1, -.2, -.3])
    x_range_minus = -5
    x_range = 5
    y_range_minus = -5
    y_range = 5

    fig, ax, ax1, ax2, scatter_plots, line_plot, line_plots = setup_plots()
    xs, ys = create_simulation_data(no_of_points, directions, simulation_steps, [x_range_minus, x_range],
                                    [y_range_minus, y_range])
    infection_frame_map = {}
    confirmed_deaths = []
    confirmed_immune = []
    line_deaths = []
    line_recoveries = []
    line_infections = []

    def init():
        ax.set_xlim(np.min(xs), np.max(xs))
        ax.set_ylim(np.min(ys), np.max(ys))

    def update(frame, xss, yss, inf_map):
        x_values = []
        y_values = []
        temp_infected_indices = []

        for this in range(no_of_points):
            for inf in infected_indices:
                if inf not in inf_map:
                    inf_map[inf] = int(round(time.time() * 1000))
                if isclose(xss[inf][frame], xss[this][frame], abs_tol=distance_tolerance) \
                        and isclose(yss[inf][frame], yss[this][frame],
                                    abs_tol=distance_tolerance) and this not in confirmed_immune and this not in confirmed_deaths:
                    temp_infected_indices.append(this)
                    scatter_plots[this].set_color('red')
        # Append new infections to existing infections list
        for ii in list(set(infected_indices) ^ set(temp_infected_indices)):
            infected_indices.append(ii)

        infected = len(infected_indices)
        line_infections.append(infected)

        # random choose persons which recover or die
        random_condition_change(inf_map, confirmed_deaths, confirmed_immune, line_deaths, line_recoveries,
                                scatter_plots)

        frames_till_now = [i for i in range(frame)]
        for index, (s, n) in enumerate(zip(scatter_plots, range(no_of_points))):
            x = xss[n][frame]
            y = yss[n][frame]
            x_values.append(x)
            y_values.append(y)
            if index not in confirmed_deaths:
                s.set_data(x, y)

        line_plot.set_data(frames_till_now, line_infections[:frame])
        line_plots[0].set_data(frames_till_now, line_recoveries[:frame])
        line_plots[1].set_data(frames_till_now, line_deaths[:frame])

        ax1.set_xlim(0, simulation_steps)
        ax1.set_ylim(0, no_of_points)

        ax2.set_xlim(0, simulation_steps)
        ax2.set_ylim(0, get_max_length(line_recoveries, line_deaths))

    ax.set_title('Pandemic Simulation')
    create_legend()
    ani = FuncAnimation(fig, update, interval=args.interval, frames=simulation_steps,
                        fargs=(xs, ys, infection_frame_map),
                        init_func=init, repeat=False)
    if args.save_simulation:
        name = '1.gif'
        ani.save(name, writer='imagemagick', fps=80)
    else:
        plt.show()


def define_args():
    # constraints
    parser = argparse.ArgumentParser()
    parser.add_argument("-simulation_steps", default=300, help="Define the number of simulation steps",
                        type=int)
    parser.add_argument("-no_of_points", default=100, help="Define the number of points / population",
                        type=int)
    parser.add_argument("-no_of_initial_infected", default=1, help="Define the number of initially infected",
                        type=int)
    parser.add_argument("-distance_tolerance", default=0.5, help="Define the distance tolerance as a decimal",
                        type=float)
    parser.add_argument("-death_rate", default=0.20, help="Define the death rate as a percentage from 0.01 to 0.99",
                        type=float)
    parser.add_argument("-immunity_rate", default=0.80,
                        help="Define the immunity rate as a percentage from 0.01 to 0.99",
                        type=float)  # death rate and immunity rate have to be changed together and equal 1.0
    parser.add_argument("-min_time_to_recover", default=15000,
                        help="Define the minimum time to recover in ms",
                        type=int)
    parser.add_argument("-max_time_to_recover", default=50000,
                        help="Define the maximum time to recover in ms",
                        type=int)
    parser.add_argument("-min_time_to_death", default=15000,
                        help="Define the minimum time to die in ms",
                        type=int)
    parser.add_argument("-max_time_to_death", default=50000,
                        help="Define the maximum time to die in ms",
                        type=int)
    parser.add_argument("-interval", default=200,
                        help="Define the the delay between frames in ms ",
                        type=int)
    parser.add_argument("-save_simulation", default=False,
                        help="(True/False) Save simulation as gif",
                        type=bool)
    return parser.parse_args()


if __name__ == '__main__':
    args = define_args()

    simulation_steps = args.simulation_steps
    no_of_points = args.no_of_points
    no_of_initial_infected = args.no_of_initial_infected
    distance_tolerance = args.distance_tolerance
    death_rate = no_of_points * args.death_rate
    immunity_rate = no_of_points * args.immunity_rate
    min_time_to_recover = args.min_time_to_recover  # ms
    max_time_to_recover = args.max_time_to_recover  # ms
    min_time_to_death = args.min_time_to_death  # ms
    max_time_to_death = args.max_time_to_death  # ms
    infected_indices = [i for i in range(no_of_initial_infected)]

    animate()
