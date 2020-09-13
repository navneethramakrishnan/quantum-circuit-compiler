#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 22:09:21 2020

@author: navneethramakrishnan
"""
# Import packages.
from circuit_compiler import compiler
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Set up the qubits
number_of_qubits = 5

#Generate a circuit with some gates from the set {I, H, X, Y, Z, RX, RY, RZ, CNOT, CZ}
input_circuit = QuantumCircuit(number_of_qubits, number_of_qubits)
input_circuit.x(3)
input_circuit.cx(1, 2)
input_circuit.x(0)
input_circuit.z(4)
input_circuit.y(0)
input_circuit.cx(0, 4)
input_circuit.rx(0.2, 1)
input_circuit.rx(0.3, 1)
input_circuit.rx(0.2, 1)
input_circuit.cz(1, 3)
input_circuit.ry(0.5, 2)
input_circuit.cz(1, 3)
input_circuit.ry(0.23, 4)
input_circuit.rx(0.5, 1)

#Compile circuit
output_circuit = compiler(input_circuit)


# Test that the circuits match 
if (Statevector.from_instruction(input_circuit).equiv(Statevector.from_instruction(output_circuit))):
    print('Compiled circuit matches given circuit')
