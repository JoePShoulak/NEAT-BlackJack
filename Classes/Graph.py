from matplotlib import style
import matplotlib.pyplot as plt

from config import C_FITNESS_THRESHOLD, C_MIN_GRAPH_WIDTH, C_HANDS_PER_GENERATION, C_POP_PER_GEN
from helper import bottom_margin


class Graph:
    def __init__(self, fitness_threshold, hands_per_gen, pop_per_gen):
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        plt.ion()

        self.fitness_threshold = fitness_threshold
        self.hall_of_fame = []
        self.threshold_line = []
        self.ao10 = []
        self.gen = 0
        self.width = 0
        self.simulations = 0
        self.hands_per_gen = hands_per_gen
        self.pop_per_gen = pop_per_gen

    def update(self, hall_of_fame, ao10, gen):
        self.hall_of_fame = hall_of_fame
        self.ao10 = ao10
        self.gen = gen

        style.use('fivethirtyeight')

        self.simulations = "{:,}".format(self.hands_per_gen * self.pop_per_gen * gen)

        plt.title("NEAT Learning BlackJack -- Gen: %s -- Simulations: %s" % (self.gen - 1, self.simulations))
        plt.xlabel("Generations")
        plt.ylabel("Fitness")

        self.width = C_MIN_GRAPH_WIDTH if len(hall_of_fame) - 1 < C_MIN_GRAPH_WIDTH else len(hall_of_fame) - 1
        self.width = round(self.width*1.05)

        self.threshold_line = [C_FITNESS_THRESHOLD] * (self.width + 1)

        plt.plot(self.hall_of_fame, 'g-', label="Best")
        plt.plot(self.ao10, 'b--', label="Average of 10")
        plt.plot(self.threshold_line, 'r-', label="Goal")

        if self.hall_of_fame[-1] > self.fitness_threshold:
            # plt.plot([gen-1], [self.hall_of_fame[-1]], 'yo')
            plt.text((gen-1), (self.hall_of_fame[-1]), round(self.hall_of_fame[-1]))

        plt.legend()

        top = max(C_FITNESS_THRESHOLD * 1.5, max(self.hall_of_fame) * 1.5)
        bottom = bottom_margin(min(hall_of_fame))

        plt.axis([0, self.width, bottom, top])

        plt.draw()
        plt.pause(0.0001)

        if self.hall_of_fame[-1] > self.fitness_threshold:
            print("Press enter to exit close graph and view results")
            input()

        plt.clf()
