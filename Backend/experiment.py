class ExperimentReturn:
    iD = -1
    sequence = ""
    conditions = {}
    measurements = {}

    def __init__(self):
        self.iD = -1
        self.sequence = ""
        self.conditions = {}
        self.measurements = {}


class Experiment:
    sequence = ""
    conditions = {}
    measurements = {}

    def __init__(self):
        self.sequence = ""
        self.conditions = {}
        self.measurements = {}


def experimentConstruct(sequence, conditions, measurements):
    experiment = Experiment()
    experiment.sequence = sequence
    experiment.conditions = conditions
    experiment.measurements = measurements

    return experiment
