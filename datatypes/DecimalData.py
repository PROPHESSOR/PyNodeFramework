from qtpynodeeditor import NodeData, NodeDataType

class DecimalData(NodeData):
    'Node data holding a decimal (floating point) number'
    data_type = NodeDataType("decimal", "Decimal")

    def __init__(self, number: float = 0.0):
        self._number = number
        # self._lock = threading.RLock()

    @property
    def lock(self):
        return self._lock

    @property
    def number(self) -> float:
        'The number data'
        return self._number

    def number_as_text(self) -> str:
        'Number as a string'
        return '%g' % self._number
