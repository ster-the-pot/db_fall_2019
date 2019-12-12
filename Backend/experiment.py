class ExperimentReturn:
    iD = -1
    sequence = ""
    conditions = {}
    measurements = {}


class Experiment:
    sequence = ""
    conditions = {}
    measurements = {}


def experimentConstruct(sequence, conditions, measurements):
    experiment = Experiment()
    experiment.sequence = sequence
    experiment.conditions = conditions
    experiment.measurements = measurements

    return experiment
