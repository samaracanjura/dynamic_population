import argparse
import networkx as nx
import matplotlib.pyplot as plt
import random
import sys 

SUSCEPTIBLE = "S"
INFECTED = "I"
RECOVERED = "R"
VACCINATED = "V"

def parse_args(): 
    parser = argparse.ArgumentParser(description="Simulate casacade or COVID spread on graph")
    parser.add_argument("graph_file", help="Path to the .gml graph file")
    parser.add_argument("--action", choices=["cascade", "covid"], required=True)
    parser.add_argument("--initiator", required=True, help="Comma-separated list of initiator node IDs")
    parser.add_argument("--threshold", type=float, help="Cascade threshold (0-1)")
    parser.add_argument("--probability_of_infection", type=float, help="Infection probability (0-1)")
    parser.add_argument("--lifespan", type=int, help="Number of time steps to simulate")
    parser.add_argument("--shelter", type=float, help="Sheltering rate (0-1)")
    parser.add_argument("--vaccinations", type=float, help="Vaccination rate (0-1)")
    parser.add_argument("--plot", action="store_true", help="Plot summary at the end")
    parser.add_argument("--interactive", action="store_true", help="Plot each step")
    return parser.parse_args()

def load_graph(path):
    try:
        G = nx.read_gml(path)
        if not isinstance(G, nx.DiGraph):
            G = G.to_directed()
        return G
    except Exception as e:
        print(f"Error loading graph: {e}")
        sys.exit(1)


def cascade_simulation(G, initiators, threshold, interactive):
    active = set(initiators)
    for n in G.nodes: 
        G.nodes[n]["active"] = n in active
        
    changed = True
    round = 0
    while changed: 
        changed = False
        new_active = set()
        for node in G.nodes: 
            if G.nodes[node]["active"]:
                continue
            neighbors = list(G.predecessors(node))
            if not neighbors:
                continue
            active_neighbors = sum(1 for n in neighbors if G.nodes[n]["active"])
            if active_neighbors / len(neighbors) >= threshold:
                new_active.add(node)
        if new_active:
            changed = True
            for n in new_active:
                G.nodes[n]["active"] = True
            active.update(new_active)
        round += 1
        if interactive:
            plot_graph(G, title=f"Cascade Round {round}", node_attr="active")
    return G

def covid_simulation(G, initiators, p_inf, lifespan, shelter, vaccinations, interactive):
    for n in G.nodes:
        G.nodes[n]["state"] = SUSCEPTIBLE
        
    num_vaccinated = int(len(G.nodes) * vaccinations)
    for n in random.sample(list(G.nodes), num_vaccinated):
        G.nodes[n]["State"] =  VACCINATED
        
    num_sheltered= int(len(G.nodes) * shelter)
    sheltered_nodes = set(random.sample(list(G.nodes), num_sheltered))
    
    for n in initiators: 
        if G.nodes[n]["state"] == SUSCEPTIBLE:
            G.nodes[n]["state"] = INFECTED
    
    history = []
    for t in range(lifespan):
        new_states = {}
        counts = {SUSCEPTIBLE: 0, INFECTED: 0, RECOVERED: 0, VACCINATED: 0}
        for n in G.nodes:
            state = G.nodes[n]["state"]
            if state == INFECTED:
                for neighbor in G.successors(n):
                    if G.nodes[neighbor]["state"] == SUSCEPTIBLE and neighbor not in sheltered_nodes:
                        if random.random() < p_inf:
                            new_states[neighbor] = INFECTED
                new_states[n] = RECOVERED
            counts[state] += 1
        for n, state in new_states.items():
            G.nodes[n]["state"] = state
        history.append(counts[INFECTED])
        if interactive:
            plot_graph(G, title=f"COVID Day {t+1}", node_attr="state")
    return history       

def plot_graph(G, title, node_attr):
    color_map = {
        True: "red",
        False: "gray",
        SUSCEPTIBLE: "blue",
        INFECTED: "red",
        RECOVERED: "green",
        VACCINATED: "yellow"
    }
    colors = [color_map[G.nodes[n][node_attr]] for n in G.nodes]
    nx.draw(G, with_labels=True, node_color=colors)
    plt.title(title)
    plt.show()


def plot_history(history):
    plt.plot(history)
    plt.xlabel("Day")
    plt.ylabel("New Infections")
    plt.title("COVID Infection Spread")
    plt.grid()
    plt.show()
    
def main():
    args = parse_args()
    G = load_graph(args.graph_file)
    initiators = [str(i.strip()) for i in args.initiator.split(",")]

    if args.action == "cascade":
        if args.threshold is None:
            print("--threshold is required for cascade simulation.")
            sys.exit(1)
        G = cascade_simulation(G, initiators, args.threshold, args.interactive)
        if args.plot:
            plot_graph(G, title="Final Cascade State", node_attr="active")

    elif args.action == "covid":
        if None in (args.probability_of_infection, args.lifespan, args.shelter, args.vaccinations):
            print("--probability_of_infection, --lifespan, --shelter, and --vaccinations are required for COVID simulation.")
            sys.exit(1)
        history = covid_simulation(
            G, initiators,
            args.probability_of_infection,
            args.lifespan,
            args.shelter,
            args.vaccinations,
            args.interactive
        )
        if args.plot:
            plot_history(history)


if __name__ == "__main__":
    main()
