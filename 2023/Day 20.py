from utils.data import *
from math import lcm


TYPES = {"broadcaster": 0, "%": 1, "&": 2}


class Module:
    def __init__(self, name, type, targets):
        self.name = name
        self.type = type
        self.targets = targets
        self.memory = {}
        self.state = False if type == 1 else None

    def handle_signal(self, signal, source):
        if signal == "low":
            if self.type == 0:
                pulse = "low"
            elif self.type == 1:
                if self.state:  # flip-flop module is on
                    pulse = "low"
                else:
                    pulse = "high"
                self.state = not self.state
            else:
                self.memory[source] = "low"
                pulse = "high"
            return [(tar, pulse, self.name) for tar in self.targets]
        else:
            if self.type == 0:
                return [(tar, "high", self.name) for tar in self.targets]
            elif self.type == 1:
                return []
            else:
                self.memory[source] = "high"
                if all(v == "high" for v in self.memory.values()):
                    pulse = "low"
                else:
                    pulse = "high"
                return [(tar, pulse, self.name) for tar in self.targets]


def parse(data):
    res = {}
    for line in data.splitlines():
        module, dest = line.split(" -> ")
        if module == "broadcaster":
            name = module
            type = module
        else:
            name = module[1:]
            type = module[0]
        res[name] = Module(name, TYPES[type], dest.split(", "))

    for line in data.splitlines():
        module, dest = line.split(" -> ")
        if module == "broadcaster":
            name = module
        else:
            name = module[1:]
        for d in dest.split(", "):
            if d in res and res[d].type == 2:
                res[d].memory[name] = "low"
    return res


def part1(modules):
    low = high = 0
    for _ in range(1000):
        signals = [("broadcaster", "low", "")]
        while signals:
            next_signals = []
            for name, signal, source in signals:
                if signal == "high":
                    high += 1
                else:
                    low += 1
                if name in modules:
                    next_signals.extend(modules[name].handle_signal(signal, source))
            signals = next_signals
    return low * high


def part2(modules):
    src = ""
    for k, v in modules.items():
        # Assumption 1: rx always has a single source which is a conjunction module
        # This means that for rx to receive a low pulse, that source conjunction module needs to have
        # high pulses from all of its inputs as the most recent signal
        if "rx" in v.targets:
            src = k
            break
    targets = list(modules[src].memory.keys())

    # Assumption 2: All of the source modules for the source conjunction module of rx are again conjunction modules
    # which each have a single source which means they all need to receive a low pulse
    # during the same iteration so they can in turn send a high pulse
    target_dict = {tar: [] for tar in targets}
    i = 1

    # Assumption 3: There are cycles for each of the sources, so run the simulation and save at least
    # two iterations for each of the source modules defined in target_dict where they received a low pulse
    # so you can calculate the cycle length for each of them (for me all cycles started at 0 so a single iteration
    # for each would have sufficed). Then you can just calculate the LCM of the cycle lengths to get the result.
    while any(len(tar) < 2 for tar in target_dict.values()):
        signals = [("broadcaster", "low", "")]
        while signals:
            next_signals = []
            for name, signal, source in signals:
                if name in target_dict and signal == "low":
                    target_dict[name].append(i)
                if name in modules:
                    next_signals.extend(modules[name].handle_signal(signal, source))
            signals = next_signals
        i += 1
    diffs = [tar[1] - tar[0] for tar in target_dict.values()]
    return lcm(*diffs)


data = get_and_write_data(20, 2023)
print_output(part1(parse(data)), part2(parse(data)))
