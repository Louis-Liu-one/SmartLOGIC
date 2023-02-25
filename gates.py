
'''build complex logic circuits on your computer

# Submodule GATES in Package SmartLOGIC
Use SmartLOGIC.GATES to build complex logic circuits on your computer.
Copyright © 2023, Liu One  All rights reserved.

`smartlogic.gates`build some gates to build more complex logic
circuits. All gates will attach a truth table, for example, NOR Gate's
truth table (left):
             ┌─┬───────┬───┐
             │N│   I   │ O │    GATES LIST:
             │O├───┬───┼───┤    ┌─────┬──────┬─────┬──────┐
             │R│ L │ L │ H │    │ NOT │  AND │  OR │  XOR │
             │ │ L │ H │ L │    ├─────┼──────┼─────┼──────┤
             │ │ H │ L │ L │    │     │ NAND │ NOR │ NXOR │
             │ │ H │ H │ L │    └─────┴──────┴─────┴──────┘
             └─┴───┴───┴───┘
(NOTE: We didn't use triodes to build gates, because it maybe very slow)
'''

from . import *
from .base import *


__all__ = ['NOTGate', 'ANDGate']


class Gate(CircuitElement):

    def __init__(
            self, /,
            input_bits: list, output_bit: Bit,
            *, in_not: list = None, out_not: bool = False):
        super().__init__(input_bits, [output_bit])
        self.inputs = input_bits
        self.output = output_bit
        self.in_not = []
        if in_not is not None:
            self.in_not = in_not
        self.out_not = out_not

    def __repr__(self, /):
        return ('smartlogic.gates.Gate(\n'
                '    input_bits={0.inputs},\n'
                '    output_bit={0.output},\n'
                '    in_not={0.in_not},\n'
                '    out_not={0.out_not},\n)').format(self)

    def __str__(self, /):
        return '<SmartLOGIC gate at {hexid}>'.format(hexid=hex(id(self)))

    def gate_op(self, /, inputs: list):
        pass

    def calc(self, /):
        result = self.gate_op([
                (not bool(bit) if isnot else bool(bit))
                for bit, isnot in zip(self.inputs, self.in_not)
            ]
        )
        self.output.setto(not result if self.out_not else result)


class NOTGate(CircuitElement):
    r'''
                  ┌─┬───┬───┐    the symbol of a NOT Gate:
                  │N│ I │ O │    ┌─────────────────────┐
                  │O├───┼───┤    │        │\　         │
                  │T│ L │ H │    │ I ─────┤ 〉O───── O │
                  │ │ H │ L │    │        │/　         │
                  └─┴───┴───┘    └─────────────────────┘
    '''

    def __init__(self, /, input_bit: Bit, output_bit: Bit):
        '''
        ┌─────────────────────────────────────────────────────────────┐
        │ Parameters:                                                 │
        ├─────────────┬───────────────────────────────────────────────┤
        │ input_bit   │ I (see the truth table)                       │
        │ output_bit  │ O (see the truth table)                       │
        └─────────────┴───────────────────────────────────────────────┘
        '''
        super().__init__([input_bit], [output_bit])
        self.input = self.input_bits[0]
        self.output = self.output_bits[0]

    def __repr__(self, /):
        return ('smartlogic.gates.NOTGate(\n'
                '    input_bit={0.input},\n'
                '    output_bit={0.output},\n)').format(self)

    def __str__(self, /):
        return '<SmartLOGIC NOT gate at {hexid}>'.format(hexid=hex(id(self)))

    def calc(self, /):
        '''
        See smartlogic.CircuitElement.calc. This method uses keyword
        `not` to get the result.
        '''
        self.output.setto(not self.input.get())


class ANDGate(CircuitElement):
    r'''
    ┌─┬─────────────────┬───┐
    │A│       I         │ O │    This truth table maybe not very lucid.
    │N├─────────────────┼───┤    The truth table means, when all inputs
    │D│    ALL IS L     │ L │    are HIGH, the output is HIGH, LOW
    │ ├─────────────────┼───┤    otherwise.
    │ │ SOME L & SOME H │ L │
    │ ├─────────────────┼───┤
    │ │    ALL IS H     │ H │
    └─┴─────────────────┴───┘
                  The symbol of an AND Gate:
                  ┌──────────────────────────────────────┐
                  │             ┌──────────\             │
                  │ I.1 ────────┤           \            │
                  │ I.2 ────────┤            \           │
                  │ I.3 ────────┤    AND     ├──────── O │
                  │ I.. ........│            /           │
                  │ I.n ────────┤           /            │
                  │             └──────────/             │
                  └──────────────────────────────────────┘
    '''

    def __init__(self, /, input_bits: list, output_bit: Bit):
        '''
        ┌─────────────────────────────────────────────────────────────┐
        │ Parameters:                                                 │
        ├─────────────┬───────────────────────────────────────────────┤
        │ input_bits  │ I(s) (see the truth table)                    │
        │ output_bit  │ O (see the truth table)                       │
        └─────────────┴───────────────────────────────────────────────┘
        '''
        super().__init__(input_bits, [output_bit])
        self.inputs = input_bits
        self.output = self.output_bits[0]

    def __repr__(self, /):
        return ('smartlogic.gates.ANDGate(\n'
                '    input_bits={0.inputs},\n'
                '    output_bit={0.output},\n)').format(self)

    def __str__(self, /):
        return '<SmartLOGIC AND gate at {hexid}>'.format(hexid=hex(id(self)))

    def calc(self, /):
        '''
        See smartlogic.CircuitElement.calc. This method calls built-in
        function `all` to get the result.
        '''
        self.output.setto(all(self.inputs))
