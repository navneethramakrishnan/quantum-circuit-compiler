#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 03:44:00 2020

@author: navneethramakrishnan
"""
import numpy as np
from qiskit import QuantumCircuit

def decompose_gates(gate_list): 
    #Decomposes gates from input set into rx, rz and cz gates
    new_gate_list = []
    for [gate_name, [qubit1, qubit2], gate_parameter] in gate_list:
        if gate_name == 'h':
            new_gate_list.append(['rz', [qubit1, qubit2], np.pi/2])
            new_gate_list.append(['rx', [qubit1, qubit2], np.pi/2])
            new_gate_list.append(['rz', [qubit1, qubit2], np.pi/2])
            continue
        elif gate_name == 'i':
            continue
        elif gate_name == 'x':
            new_gate_list.append(['rx', [qubit1, qubit2], np.pi])
            continue
        elif gate_name == 'z':    
            new_gate_list.append(['rz', [qubit1, qubit2], np.pi])
            continue
        elif gate_name == 'y':    
            new_gate_list.append(['rz', [qubit1, qubit2], np.pi])
            new_gate_list.append(['rx', [qubit1, qubit2], np.pi])
            continue
        elif gate_name == 'ry':
            new_gate_list.append(['rz', [qubit1, qubit2], -1*np.pi/2])
            new_gate_list.append(['rx', [qubit1, qubit2], gate_parameter])
            new_gate_list.append(['rz', [qubit1, qubit2], np.pi/2])
            continue
        elif gate_name == 'rz':
            new_gate_list.append(['rz', [qubit1, qubit2], gate_parameter])
            continue
        elif gate_name == 'rx':
            new_gate_list.append(['rx', [qubit1, qubit2], gate_parameter])
            continue
        elif gate_name == 'cz':
            new_gate_list.append(['cz', [qubit1, qubit2], gate_parameter])
            continue
        elif gate_name == 'cx':
            new_gate_list.append(['rz', [qubit2, None], np.pi/2])
            new_gate_list.append(['rx', [qubit2, None], np.pi/2])
            new_gate_list.append(['rz', [qubit2, None], np.pi/2])
            new_gate_list.append(['cz', [qubit1, qubit2], gate_parameter])
            new_gate_list.append(['rz', [qubit2, None], np.pi/2])
            new_gate_list.append(['rx', [qubit2, None], np.pi/2])
            new_gate_list.append(['rz', [qubit2, None], np.pi/2])
        else:
            print('Warning: Input circuit has a gate that is not allowed')
            return []
    return new_gate_list


def get_gate_list_from_circuit(circuit):
    #Get a list of gates from the circuit and preserve the ordering of gates
    gate_list = []
    for gate in circuit.data:
        name = gate[0].name
        qubit1 = gate[1][0].index
        qubit2 = None
        param = None
        if len(gate[1]) == 2:
            qubit2 = gate[1][1].index
        if len(gate[0].params) == 1:
            param = gate[0].params[0]       
        gate_list.append([name, [qubit1, qubit2], param])   
    return gate_list   


def get_circuit_from_gate_list(number_of_qubits, gate_list):
    #Take a list of gates and add them to a circuit
    output_circuit = QuantumCircuit(number_of_qubits, number_of_qubits)
    for gate in gate_list:
        name = gate[0]
        qubit1 = gate[1][0]
        qubit2 = gate[1][1]
        param = gate[2]
        if qubit2 == None: #Single qubit gate
            if param == None:
                getattr(output_circuit, name)(qubit1)
            else:
                getattr(output_circuit, name)(param, qubit1)
        else: #Two qubit gate (these have no parameter since they are cx or cz)
            getattr(output_circuit, name)(qubit1, qubit2)   
            
    return output_circuit        


def get_qubit_gate_dict(number_of_qubits, gate_list):
    # Create a dictionary where each qubit is the key and the value is a list of gates acting on it
    qubit_gate_dict = {}
    for i in range(number_of_qubits):
        qubit_gate_dict[i] = []
    
    for gate in gate_list:
        qubit_gate_dict[gate[1][0]].append(gate)
        if gate[1][1] is not None:
            qubit_gate_dict[gate[1][1]].append(gate)
    
    return qubit_gate_dict       



def get_grouped_gate_list(qubit_gate_dict, gate_list):
    # Gates acting on different qubits always commute. 
    # We exploit this to reorder the list such that gates acting on the same qubit that could be combined appear as consecutive elements in the list.
    grouped_gate_list = []
    for gate in gate_list: 
        if gate[1][1] is not None: #Look for a two qubit gate in the list
            qubit1 = gate[1][0] 
            qubit2 = gate[1][1]   
            
            idx1 = qubit_gate_dict[qubit1].index(gate) #Get number of single qubit gates on qubit 1 before the two qubit gate
            idx2 = qubit_gate_dict[qubit2].index(gate) #Get number of single qubit gates on qubit 2 before the two qubit gate
            
            grouped_gate_list.extend(qubit_gate_dict[qubit1][0:idx1]) #Implement all the single qubit gates of qubit 1 before the two qubit gate
            grouped_gate_list.extend(qubit_gate_dict[qubit2][0:idx2]) #Implement all the single qubit gates of qubit 2 before the two qubit gate
            grouped_gate_list.append(gate) #Implement the two qubit gate
            
            qubit_gate_dict[qubit1] = qubit_gate_dict[qubit1][idx1+1:] #Remove the gates that have been implemented from qubit1's list
            qubit_gate_dict[qubit2] = qubit_gate_dict[qubit2][idx2+1:] #Remove the gates that have been implemented from qubit2's list
    
    for key in qubit_gate_dict: #Add all leftover gates sorted by qubit
        grouped_gate_list.extend(qubit_gate_dict[key]) 
    
    return grouped_gate_list    



def compress_gates(gate_list):
    #If consecutive single qubit gates are the same (i.e. rx or ry rotations) and act on the same qubit, we just add the rotation angles
    compressed_gate_list = []
    if len(gate_list) > 0:
        gate_to_be_added = gate_list[0]
    else:
        return compressed_gate_list
    for idx, gate in enumerate(gate_list[1:]):
        if gate[1][1] is None and gate_to_be_added[1][1] is None and gate[1][0] == gate_to_be_added[1][0] and gate[0] == gate_to_be_added[0]:
            gate_to_be_added = [gate[0], gate[1], gate[2] + gate_to_be_added[2]] 
        else:
            compressed_gate_list.append(gate_to_be_added)
            gate_to_be_added = gate
    compressed_gate_list.append(gate_to_be_added)
    
    return compressed_gate_list


def combine_consecutive_cz_gates(gate_list):
    #If we have two consecutive cz gates, we can delete both
    i= 0
    while i < len(gate_list)-1:
        if gate_list[i][1][1] is not None and gate_list[i] == gate_list[i+1]:
            del gate_list[i]
            del gate_list[i]
            i = i - 1
        else:
            i = i+1
    return gate_list            