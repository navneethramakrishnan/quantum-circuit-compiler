# Quantum circuit compiler
This is the solution to Task 3 of the QOSF challenge. Given a quantum circuit with gates from the set {I, H, X, Y, Z, RX, RY, RZ, CNOT, CZ}, the goal is to compile it into a circuit that only uses gates from the set {RX, RZ, CZ}. 

Follow these instruction to install Qiskit - https://qiskit.org/documentation/install.html

The file circuit_compiler.py contains the compiler. The file utilities.py contains various helper functions. The file example.py shows an example of an arbitrary input circuit that is compiled. A quick test is done to check that the compiled circuit matches the input circuit.
