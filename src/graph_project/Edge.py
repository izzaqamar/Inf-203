# Task: 03 + Task 05


class Edge:
    """Represents a directed edge between two nodes.

    Parameters
    label : A descriptive label for the edge (not required to be unique).
    source : The node from which the edge originates.
    target : The node at which the edge terminates.

    Attributes
    label : The edge label.
    source : The source node.
    target : The target node.
    """

    def __init__(self, label, source, target):
        self._label = label
        self._source = source
        self._target = target

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    def __repr__(self):
        return f"Edge({self.label}, {self.source.label} -> {self.target.label})"
