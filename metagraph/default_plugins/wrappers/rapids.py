from ... import ConcreteType, Wrapper
from ..abstract_types import DataFrame, Graph, WeightedGraph
from .. import registry


try:
    import cugraph
except ImportError:
    cugraph = None

try:
    import cudf
except ImportError:
    cudf = None


if cugraph is not None:

    @registry.register
    class CuGraphType(ConcreteType, abstract=Graph):
        value_type = cugraph.DiGraph

    @registry.register
    class CuGraphWeighted(Wrapper, abstract=WeightedGraph):
        def __init__(self, graph, weight_label="weight"):
            self.obj = graph
            self.weight_label = weight_label
            assert isinstance(graph, cugraph.DiGraph)
            assert (
                weight_label in graph.nodes(data=True)[0]
            ), f"Graph is missing specified weight label: {weight_label}"


if cudf is not None:

    @registry.register
    class CuDFType(ConcreteType, abstract=DataFrame):
        value_class = cudf.DataFrame

    @registry.register
    class CuDFEdgeList(Wrapper, abstract=Graph):
        def __init__(self, df, src_label="source", dest_label="destination"):
            self.obj = df
            self.src_label = src_label
            self.dest_label = dest_label
            assert isinstance(df, cudf.DataFrame)
            assert src_label in df, f"Indicated src_label not found: {src_label}"
            assert dest_label in df, f"Indicated dest_label not found: {dest_label}"

    @registry.register
    class CuDFWeightedEdgeList(CuDFEdgeList, abstract=WeightedGraph):
        def __init__(
            self,
            df,
            src_label="source",
            dest_label="destination",
            weight_label="weight",
        ):
            super().__init__(df, src_label, dest_label)
            self.weight_label = weight_label
            assert (
                weight_label in df
            ), f"Indicated weight_label not found: {weight_label}"
