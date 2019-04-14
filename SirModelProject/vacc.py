import networkx as nx
import matplotlib.pyplot as plt
import numpy
import random

z = [3 for i in range(1000)]  # average degree 3
Gc = nx.expected_degree_graph(z)
G = max(nx.connected_component_subgraphs(Gc), key=len)

num_sim = 1000  ## number of simulations
inf_rate = 0.8  ## infectionn rate
rec_rate = 0.5  ## recovery rate
ar = []
atr = []
atri = []
atrr = []

init = 1  ## number of individuals infected at time t = 0
vaccined = random.sample((G.nodes()), 9)
G.remove_nodes_from(vaccined)
print(vaccined)


def showBarabashiGraph():
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    nx.draw_networkx(G, with_labels=True)
    ax1.title.set_text('Barabashi Graph')
    plt.show()


def showgraph():
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    nx.draw_networkx(Gc, with_labels=True)

    ax2 = fig.add_subplot(122)
    nx.draw_networkx(G, with_labels=True)

    ax1.title.set_text('Random Graph')
    ax2.title.set_text('Connected Graph')

    plt.show()


def changeGraphToBarabashi():
    global G
    G = nx.barabasi_albert_graph(1000, 3, )


def simulation():
    for m in range(0, num_sim):

        n_infected = [10]
        n_susceptible = [G.number_of_nodes()]
        new_infected = []
        n_removed = [0]

        state = [0] * (max(G.nodes()) + 1)

        ## if any network has some missing nodes, then the following takes care of it

        state[0] = 5
        for i in range(len(state)):
            if i not in G.nodes():
                state[i] = 5

        infected = random.sample((G.nodes()), init)  ## select one node at random
        #    print(infected)

        for i in range(len(infected)):
            state[infected[i]] = 1

        ## the simulation will run as long as the number of infected > 0

        while len(infected) > 0:

            ### Spreading infection
            for j in infected:
                neighbors = G.neighbors(j)  ## find neighbors of infected node
                for k in neighbors:
                    # print k
                    if state[
                        k] == 0 and random.random() < inf_rate:  ## if the neighboring node is not already infected, infect with prob = infected rate
                        state[k] = 1
                        new_infected.append(k)
            ### Recovering from infection
            for k in infected[:]:
                if random.random() < rec_rate:  ## for every infected node, change them into recovered state with prob = 1 (recovery rate)
                    state[k] = 2
                    infected.remove(k)  ## remove the recovered nodes from the infected nodes list

            infected = new_infected + infected  ## cumulative number of infected nodes
            new_infected = []  ## initialize newly infected nodes for every step
            n_infected.append(state.count(1))  ## count the total number of infected nodes (state 1 nodes)
            n_susceptible.append(state.count(0))  ## count the total number of susceptible nodes (state 0 nodes)
            n_removed.append(state.count(2))  ## count the total number of recovered nodes (state 2 nodes)

        atr.append(list(n_susceptible[t] / G.number_of_nodes() for t in
                        range(len(n_susceptible))))  ## count of the fraction of people infected for each simulation
        atri.append(list(n_infected[t] / G.number_of_nodes() for t in
                         range(len(n_susceptible))))  ## count of the fraction of people infected for each simulation
        atrr.append(list(n_removed[t] / G.number_of_nodes() for t in
                         range(len(n_susceptible))))  ## count of the fraction of people infected for each simulation
        ar.append(n_removed[-1] / G.number_of_nodes())  ## the average attack rate for each simulation

    print(round(numpy.mean(ar), 4))
    print(round(numpy.std(ar) / numpy.sqrt(num_sim), 4))
    ## print the mean and the standard deviation of the average attack rate after N number of simulations

    atr_mean = [numpy.mean([x[i] for x in atr if len(x) > i]) for i in range(len(max(atr, key=len)))]
    ## mean of fraction of infected nodes after N simulations

    atri_mean = [numpy.mean([x[i] for x in atri if len(x) > i]) for i in range(len(max(atri, key=len)))]
    ## mean of fraction of infected nodes after N simulations

    atrr_mean = [numpy.mean([x[i] for x in atrr if len(x) > i]) for i in range(len(max(atrr, key=len)))]
    ## mean of fraction of infected nodes after N simulations

    st = [numpy.std([x[i] for x in atr if len(x) > i]) for i in range(len(max(atr, key=len)))]
    ## standard deviation of fraction of infected nodes after N simulations

    plt.figure(figsize=(10, 10))  ## define figure size

    axis_font = {'size': '18', 'color': 'black'}
    # axis_tick_font = {'size': '25', 'color': 'black'}

    for i in range(len(atr)):
        plt.subplot(221)
        plt.plot(atr[i], color='grey')
    ## plot the epidemic curve for each simulation

    plt.errorbar(range(len(atr_mean)), atr_mean, yerr=st / numpy.sqrt(len(max(atr))),
                 color='black', markersize=8, ecolor='black',
                 fmt='-o', markeredgewidth=2, capsize=5, elinewidth=2)
    ## plot the mean epidemic curve after N simulations with error bars representing the probable error in estimating the mean

    plt.xlabel('time', **axis_font)
    plt.ylabel('fraction susceptible', **axis_font)
    # plt.xticks(**axis_tick_font)
    # plt.yticks(**axis_tick_font)

    for i in range(len(atri)):
        plt.subplot(222)
        plt.plot(atri[i], color='grey')
    ## plot the epidemic curve for each simulation

    plt.errorbar(range(len(atri_mean)), atri_mean, yerr=st / numpy.sqrt(len(max(atri))),
                 color='black', markersize=8, ecolor='black',
                 fmt='-o', markeredgewidth=2, capsize=5, elinewidth=2)
    ## plot the mean epidemic curve after N simulations with error bars representing the probable error in estimating the mean
    plt.xlabel('time', **axis_font)
    plt.ylabel('fraction infected', **axis_font)
    # plt.xticks(**axis_tick_font)
    # plt.yticks(**axis_tick_font)

    for i in range(len(atrr)):
        plt.subplot(223)
        plt.plot(atrr[i], color='grey')
    ## plot the epidemic curve for each simulation

    plt.errorbar(range(len(atrr_mean)), atrr_mean, yerr=st / numpy.sqrt(len(max(atrr))),
                 color='black', markersize=8, ecolor='black',
                 fmt='-o', markeredgewidth=2, capsize=5, elinewidth=2)
    ## plot the mean epidemic curve after N simulations with error bars representing the probable error in estimating the mean

    plt.xlabel('time', **axis_font)
    plt.ylabel('fraction recovered', **axis_font)
    # plt.xticks(**axis_tick_font)
    # plt.yticks(**axis_tick_font)

    # plt.xlabel('time', **axis_font)
    # plt.ylabel('fraction infected', **axis_font)
    # plt.xticks(**axis_tick_font)
    # plt.yticks(**axis_tick_font)

    plt.savefig('sirsim.png')
    plt.show()


if __name__ == "__main__":
    global inf_rate, rec_rate

    for i in numpy.arange(0.1, 1, 0.1):
        inf_rate = i
        for y in numpy.arange(0.1, 1, 0.1):
            rec_rate = y
            simulation()
    showgraph()

    changeGraphToBarabashi()

    for i in numpy.arange(0.1, 1, 0.1):
        inf_rate = i
        for y in numpy.arange(0.1, 1, 0.1):
            rec_rate = y
            simulation()
    showBarabashiGraph()
