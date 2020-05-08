from qtpynodeeditor import NodeData, NodeDataType

class IntegerData(NodeData):
    'Node data holding an integer value'
    data_type = NodeDataType("integer", "Integer")

    def __init__(self, number: int = 0):
        self._number = number
        # self._lock = threading.RLock()

    @property
    def lock(self):
        return self._lock

    def number(self) -> int:
        'The number data'
        return self._number

    def number_as_text(self) -> str:
        'Number as a string'
        return str(self._number)

