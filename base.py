
'''process inputs in basic

# Submodule BASE in Package SmartLOGIC
Use Diode and Triode to process inputs in basic.
Copyright © 2023, Liu One  All rights reserved.

`smartlogic.base` give you two classes, Diode and Triode, to process
inputs in basic. You can use these two classes to build any other
circuit elements such as an AND Gate:
        ┌─────────────────────────────────────────────────────────────┐
In [1]: │ # Leave out the `import` sentence                           │
        │ # Some bits                                                 │
        │ ibit1 = Bit()                                               │
        │ ibit2 = Bit()                                               │
        │ tmpbit = Bit()                                              │
        │ obit = Bit()                                                │
        │ HIGH = Bit(1)                                               │
        └─────────────────────────────────────────────────────────────┘
        ┌─────────────────────────────────────────────────────────────┐
In [2]: │ # two triodes                                               │
        │ tri1 = Triode(HIGH, ibit1, tmpbit)                          │
        │ tri2 = Triode(tmpbit, ibit2, obit)                          │
        │ tri1.run_thread()                                           │
        │ tri2.run_thread()                                           │
        └─────────────────────────────────────────────────────────────┘
        ┌─────────────────────────────────────────────────────────────┐
In [2]: │ # Now use and change ibit1, ibit2, and obit, what happend?  │
        └─────────────────────────────────────────────────────────────┘

TRY IT! GO NOW!
'''

from . import *


__all__ = ['Bit', 'Diode', 'Triode']


class Diode(CircuitElement):
    r'''
    A diode. When `anode_bit` change, `cathode_bit` will change too.
    But if you try to change `cathode_bit`, it won't. Here is the
    symbol of a diode:
    ┌─────────────────────────────────────────────────────────────────┐
    │                             │\　│                               │
    │                  anode ─────┤ 〉├───── cathode                  │
    │                             │/　│                               │
    └─────────────────────────────────────────────────────────────────┘
    '''

    def __init__(self, /, anode_bit: Bit, cathode_bit: Bit):
        '''
        ┌─────────────────────────────────────────────────────────────┐
        │ Parameters:                                                 │
        ├─────────────┬───────────────────────────────────────────────┤
        │ anode_bit   │ bits for input, anode                         │
        │ cathode_bit │ bits for output, cathode                      │
        └─────────────┴───────────────────────────────────────────────┘
        '''
        super().__init__([anode_bit], [cathode_bit])
        self.anode_bit = self.input_bits[0]
        self.cathode_bit = self.output_bits[0]

    def __repr__(self, /):
        return ('smartlogic.base.Diode(\n'
                '    anode_bit={0.anode_bit},\n'
                '    cathode_bit={0.cathode_bit},\n)').format(self)

    def __str__(self, /):
        return '<SmartLOGIC diode at {hexid}>'.format(hexid=hex(id(self)))

    def calc(self, /):
        '''Calculate. See smartlogic.CircuitElement.calc.'''
        self.cathode_bit.setto(self.anode_bit.get())


class Triode(CircuitElement):
    r'''
    A triode. When base is H, signal from emitter will go to collector.
    Here is the symbol of a triode:
    ┌─────────────────────────────────────────────────────────────────┐
    │                           base                                  │
    │                             │                                   │
    │                       ────┬─┴─┬────                             │
    │                           /   \                                 │
    │                          /     \                                │
    │                    emitter     collector                        │
    └─────────────────────────────────────────────────────────────────┘
    '''

    def __init__(self, /, emitter: Bit, base: Bit, collector: Bit):
        '''
        ┌─────────────────────────────────────────────────────────────┐
        │ Parameters:                                                 │
        ├─────────────┬───────────────────────────────────────────────┤
        │ emitter     │ the signal go into the triode from this Bit   │
        │ collector   │ the signal from the triode go into this Bit   │
        │ base        │ just like the switch of the signal            │
        └─────────────┴───────────────────────────────────────────────┘
        '''
        super().__init__([emitter], [collector])
        self.emitter = self.input_bits[0]
        self.collector = self.output_bits[0]
        self.base = base

    def __repr__(self, /):
        return ('smartlogic.base.Triode(\n'
                '    emitter={0.emitter},\n'
                '    base={0.base},\n'
                '    collector={0.collector},\n)').format(self)

    def __str__(self, /):
        return '<SmartLOGIC triode at {hexid}>'.format(hexid=hex(id(self)))

    def calc(self, /):
        '''Calculate. See smartlogic.CircuitElement.calc.'''
        if self.base.get():
            self.collector.setto(self.emitter.get())
        else:
            self.collector.setto(0)
