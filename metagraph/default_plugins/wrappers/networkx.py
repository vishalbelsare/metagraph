from ... import ConcreteType, Wrapper
from ..abstract_types import Graph, WeightedGraph
from .. import registry

try:
    import networkx as nx
except ImportError:
    nx = None


if nx is not None:

    @registry.register
    class NetworkXGraph(ConcreteType, abstract=Graph):
        value_type = nx.DiGraph

    @registry.register
    class NetworkXWeightedGraph(Wrapper, abstract=WeightedGraph):
        def __init__(self, graph, weight_label="weight"):
            self.obj = graph
            self.weight_label = weight_label
            assert isinstance(graph, nx.DiGraph)
            assert (
                weight_label in graph.nodes(data=True)[0]
            ), f"Graph is missing specified weight label: {weight_label}"
