
'''create and run logic circuits on your computer

# Package SmartLOGIC
Create and run logic circuits on your computer.
Copyright © 2023, Liu One  All rights reserved.

If you only write down `import smartlogic`, you won't get anything
useful except smartlogic.Bit and smartlogic.CircuitElement, so this
package give you other functions in these submodules:
┌──────────────────┬──────────────────────────────────────────────────┐
│ smartlogic.base  │ give you Diode and Triode to process inputs in   │
│                  │ basic                                            │
├──────────────────┼──────────────────────────────────────────────────┤
│ smartlogic.gates │ use gates to build more complex logic circuits   │
└──────────────────┴──────────────────────────────────────────────────┘

Here is an example about AND Gates:
        ┌─────────────────────────────────────────────────────────────┐
In [1]: │ from smartlogic.base import *                               │
        │ from smartlogic.gates import *                              │
        └─────────────────────────────────────────────────────────────┘
        ┌─────────────────────────────────────────────────────────────┐
In [2]: │ ibit1 = Bit()                             # one bit         │
        │ ibit2 = Bit()                                               │
        │ obit = Bit()                                                │
        │ and_gate = ANDGate([ibit1, ibit2], obit)  # AND Gate        │
        │ and_gate.run_thread()                                       │
        └─────────────────────────────────────────────────────────────┘
        ┌─────────────────────────────────────────────────────────────┐
In [3]: │ ibit1, ibit2, obit                        # 0 & 0 == 0      │
        └─────────────────────────────────────────────────────────────┘
Out[3]: (0, 0, 0)
        ┌─────────────────────────────────────────────────────────────┐
In [4]: │ ibit1.setto(1)                            # set ibit1 to 1  │
        │ ibit1, ibit2, obit                        # 1 & 0 == 0      │
        └─────────────────────────────────────────────────────────────┘
Out[4]: (1, 0, 0)
        ┌─────────────────────────────────────────────────────────────┐
In [5]: │ ibit2.setto(1)                            # set ibit2 to 1  │
        │ ibit1, ibit2, obit                        # 1 & 1 == 1      │
        └─────────────────────────────────────────────────────────────┘
Out[5]: (1, 1, 1)

TRY IT! GO NOW!
'''

import threading


__all__ = ['Bit', 'CircuitElement']


class Bit(object):
    '''
    One bit. The base element of circuits. Logic circuits's elements
    use this class to transfer data. The Bit object save a bool value
    (self.state, True or False). True means high level, and False means
    low level. The default is False.
    '''
    def __init__(self, state: bool | int = False, /):
        '''
        Initialize. If the parameter `state` isn't a bool value,
        convert it to a bool value (call `bool()`).
        '''
        self.state = bool(state)
        self.change_lock = threading.Lock()

    def __repr__(self, /):
        return str(int(self.get()))

    def __str__(self, /):
        return '<SmartLOGIC bit ({state}) at {hexid}>'.format(
            state=int(self.get()), hexid=hex(id(self)))

    def __bool__(self, /):
        return self.get()

    def _setto(self, newstate: bool | int, /):
        '''
        Set the state to `newstate`. It's not safe, please use
        self.setto.
        '''
        self.state = bool(newstate)

    def _get(self, /):
        '''
        Get the state, but not safe. Please use self.get.
        '''
        return self.state

    def setto(self, newstate: bool | int, /):
        '''
        This function will try to acquire `self.change_lock` and set
        the state to `newstate`.
        '''
        self.change_lock.acquire()
        self._setto(newstate)
        self.change_lock.release()

    def get(self, /):
        '''
        Get the state of the Bit. Don't use `self.state` to get state,
        because it maybe incorrect when you have many threads.
        '''
        self.change_lock.acquire()
        state = self._get()
        self.change_lock.release()
        return state


class Bits(object):

    def __init__(self, /, states: list = None):
        self.states = []
        if states is not None:
            self.states = [bool(state) for state in states]
        self.length = len(states)
        self.change_lock = threading.Lock()

    def _set(self, index, /, state):
        self.states[index] = bool(state)

    def _get(self, index, /):
        return self.states[index]

    def __setitem__(self, index, state, /):
        self.change_lock.acquire()
        self._set(index, state)
        self.change_lock.release()

    def __getitem__(self, index, /):
        self.change_lock.acquire()
        state = self._get(index)
        self.change_lock.release()
        return state

    def __int__(self, /):
        self.change_lock.acquire()
        num = int(''.join(str(int(state)) for state in self.states), 2)
        self.change_lock.release()
        return num


class BitsElem(object):

    def __init__(self, master, index):
        self.master = master
        self.index = index

    def setto(self, newstate):
        self.master[index] = newstate

    def get(self):
        return self.master[index]


class CircuitElement(object):
    '''
    The base class for ALL elements in a logic circuit. ALL classes in
    this package, except this class and Bit, are this class's
    subclasses.
    If you only create a circuit element, it won't start running until
    you call self.run. so you should remember to call self.run or
    self.run_thread.
    '''
    def __init__(self, /,
            input_bits: list, output_bits: list):
        '''
        ┌─────────────────────────────────────────────────────────────┐
        │ Parameters:                                                 │
        ├─────────────┬───────────────────────────────────────────────┤
        │ input_bits  │ bits for input, iterable                      │
        │ output_bits │ bits for output, iterable                     │
        └─────────────┴───────────────────────────────────────────────┘
        '''
        self.input_bits = input_bits
        self.output_bits = output_bits

    def __repr__(self, /):
        return ('smartlogic.CircuitElement(\n'
                '    input_bits={0.input_bits},\n'
                '    output_bits={0.output_bits},\n)').format(self)

    def __str__(self, /):
        return '<SmartLOGIC object at {hexid}>'.format(hexid=hex(id(self)))

    def run_thread(self, /):
        '''
        Create a self.run thread and start the thread. See self.run.
        '''
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self, /):
        '''
        This method is an infinite loop, and it never stops until there
        is an interruption. It will run `self.calc` repeatedly.

        This method is an infinite loop, if you call this method, your
        process (or thread) will go into the method and cannot do
        anything. So, we often use self.run_thread but not self.run.

        This example is adapted from the example in the DESCRIPTION:
                ┌─────────────────────────────────────────────────────┐
        In [1]: │ from smartlogic.base import *                       │
                │ from smartlogic.gates import *                      │
                │                                                     │
                │ ibit1 = Bit()                                       │
                │ ibit2 = Bit()                                       │
                │ obit = Bit()                                        │
                │ and_gate = ANDGate([ibit1, ibit2], obit)            │
                │ # everything is OK                                  │
                └─────────────────────────────────────────────────────┘
                ┌─────────────────────────────────────────────────────┐
        In [2]: │ and_gate.run()                                      │
                │ # Stuck here! Can't do anything!                    │
                └─────────────────────────────────────────────────────┘
            # Waiting
        ^C  # Press control-C
        KeyboardInterrupt
        '''
        while True:
            self.calc()

    def calc(self, /):
        '''
        Calculate new bits for output.
        This method won't do anything, so this class's subclass will
        redefine this method, for example, an AND gate (see
        smartlogic.gates.ANDGate):
            ┌─────────────────────────────────────────────────────────┐
          1 │ self.output.setto(all(self.inputs))                     │
            └─────────────────────────────────────────────────────────┘
        '''
        pass
