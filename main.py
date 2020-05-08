'''
Required: qtpynodeeditor, qt5 bindings (like pyside2)
'''

import contextlib
import logging
import threading

from qtpy.QtGui import QDoubleValidator
from qtpy.QtWidgets import QApplication, QLabel, QLineEdit, QWidget

import qtpynodeeditor as nodeeditor
from qtpynodeeditor import (NodeData, NodeDataModel, NodeDataType,
                            NodeValidationState, Port, PortType)


from datatypes.DecimalData import DecimalData
from datatypes.IntegerData import IntegerData

from middlewares.MathOperationDataModel import MathOperationDataModel

from sinks.NumberDisplayModel import NumberDisplayModel

from sources.NumberSourceDataModel import NumberSourceDataModel

# from qtpynodeeditor import NodeData, NodeDataType



class AdditionModel(MathOperationDataModel):
    name = "Addition"

    def compute(self):
        self._result = DecimalData(self._number1.number + self._number2.number)


class DivisionModel(MathOperationDataModel):
    name = "Division"
    port_caption = {'input': {0: 'Dividend',
                              1: 'Divisor',
                              },
                    'output': {0: 'Result'},
                    }

    def compute(self):
        if self._number2.number == 0.0:
            self._validation_state = NodeValidationState.error
            self._validation_message = "Division by zero error"
            self._result = None
        else:
            self._validation_state = NodeValidationState.valid
            self._validation_message = ''
            self._result = DecimalData(self._number1.number / self._number2.number)


class ModuloModel(MathOperationDataModel):
    name = 'Modulo'
    data_type = IntegerData.data_type
    port_caption = {'input': {0: 'Dividend',
                              1: 'Divisor',
                              },
                    'output': {0: 'Result'},
                    }

    def compute(self):
        if self._number2.number == 0.0:
            self._validation_state = NodeValidationState.error
            self._validation_message = "Division by zero error"
            self._result = None
        else:
            self._result = IntegerData(self._number1.number % self._number2.number)


class MultiplicationModel(MathOperationDataModel):
    name = 'Multiplication'
    port_caption = {'input': {0: 'A',
                              1: 'B',
                              },
                    'output': {0: 'Result'},
                    }

    def compute(self):
        self._result = DecimalData(self._number1.number * self._number2.number)



class SubtractionModel(MathOperationDataModel):
    name = "Subtraction"
    port_caption = {'input': {0: 'Minuend',
                              1: 'Subtrahend'
                              },
                    'output': {0: 'Result'},
                    }

    def compute(self):
        self._result = DecimalData(self._number1.number - self._number2.number)


def integer_to_decimal_converter(data: IntegerData) -> DecimalData:
    '''
    integer_to_decimal_converter
    Parameters
    ----------
    data : NodeData
    Returns
    -------
    value : NodeData
    '''
    return DecimalData(float(data.number))


def decimal_to_integer_converter(data: DecimalData) -> IntegerData:
    '''
    Convert from DecimalDat to IntegerData
    Parameters
    ----------
    data : DecimalData
    Returns
    -------
    value : IntegerData
    '''
    return IntegerData(int(data.number))


def main(app):
    registry = nodeeditor.DataModelRegistry()

    models = (AdditionModel, DivisionModel, ModuloModel, MultiplicationModel,
              NumberSourceDataModel, SubtractionModel, NumberDisplayModel)
    for model in models:
        registry.register_model(model, category='Operations',
                                style=None)

    registry.register_type_converter(DecimalData, IntegerData,
                                     decimal_to_integer_converter)
    registry.register_type_converter(IntegerData, DecimalData,
                                     decimal_to_integer_converter)

    scene = nodeeditor.FlowScene(registry=registry)

    view = nodeeditor.FlowView(scene)
    view.setWindowTitle("Calculator example")
    view.resize(800, 600)
    view.show()

    inputs = []
    node_add = scene.create_node(AdditionModel)
    node_sub = scene.create_node(SubtractionModel)
    node_mul = scene.create_node(MultiplicationModel)
    node_div = scene.create_node(DivisionModel)
    node_mod = scene.create_node(ModuloModel)

    for node_operation in (node_add, node_sub, node_mul, node_div, node_mod):
        node_a = scene.create_node(NumberSourceDataModel)
        node_a.model.embedded_widget().setText('1.0')
        inputs.append(node_a)

        node_b = scene.create_node(NumberSourceDataModel)
        node_b.model.embedded_widget().setText('2.0')
        inputs.append(node_b)

        scene.create_connection(node_a[PortType.output][0],
                                node_operation[PortType.input][0],
                                )

        scene.create_connection(node_a[PortType.output][0],
                                node_operation[PortType.input][1],
                                )

        node_display = scene.create_node(NumberDisplayModel)

        scene.create_connection(node_operation[PortType.output][0],
                                node_display[PortType.input][0],
                                )

    try:
        scene.auto_arrange(nodes=inputs, layout='bipartite')
    except ImportError:
        ...

    return scene, view, [node_a, node_b]


if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    app = QApplication([])
    scene, view, nodes = main(app)
    view.show()
    app.exec_()
