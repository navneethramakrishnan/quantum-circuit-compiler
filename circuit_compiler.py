#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 18:18:40 2020

@author: navneethramakrishnan
"""

from utilities import *
from qiskit import QuantumCircuit

def compiler(input_circuit):
    number_of_qubits = input_circuit.num_qubits
    
    # Convert circuit into a list of gates and qubits they act on. List elements take the format [gate_name, [qubit1, qubit2], gate_parameter]
    gate_list = get_gate_list_from_circuit(input_circuit)   
        
    # Decompose into allowed gates
    decomposed_gate_list = decompose_gates(gate_list)
    
    ## Optimization to reduce overhead
    prev_gate_list = []
    curr_gate_list = decomposed_gate_list
    while curr_gate_list != prev_gate_list: 
        # Create a dictionary with each qubit as a key and a list of gates acting on that qubit as the value
        qubit_gate_dict = get_qubit_gate_dict(number_of_qubits, curr_gate_list)
    
        # Reorder the gates such single qubit gates of a given qubit that can be combined are consecutive elements in the list 
        grouped_gate_list = get_grouped_gate_list(qubit_gate_dict, curr_gate_list)
        
        # Combine consecutive single qubit gates of same type
        compressed_gate_list = compress_gates(grouped_gate_list)
        
        # Remove any identity gates
        compressed_gate_list = [x for x in compressed_gate_list if x[2] != 0]        
        
        # Remove pairs of consecutive cz gates acting on same qubits
        compressed_gate_list = combine_consecutive_cz_gates(compressed_gate_list)
        
        prev_gate_list = curr_gate_list
        curr_gate_list = compressed_gate_list
    
    #Rebuild circuit from final gate list
    output_circuit = get_circuit_from_gate_list(number_of_qubits, curr_gate_list)  
    
    return output_circuit