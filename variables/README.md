# vrp-gen-alg - Variables

This folder contains all of the variables that the application uses. Any variables that one would want to use have to placed in the proper subfolders. Each subfolder contains an example file "sample.txt" that can be used as reference for each variable type.

## Table of Contents

- [Coordinates](#coordinates)
- [Cost matrices](#cost-matrices)
- [Node demands](#node-demands)
- [Node penalties](#node-penalties)
- [Node profits](#node-profits)
- [Node service times](#node-service-times)
- [Node time windows](#node-time-windows)
- [Parameter settings](#parameter-settings)
- [Plot data](#plot-data)

### Coordinates

Coordinates represent the locations of the nodes in a 2-dimensional space. They are placed in the "coordinates" subfolder as text files. The format is as follows:
- n x 2 matrix, where n is the number of nodes.
- First column represents location on the x-axis, and the second that of y-axis.
- Whitespace between columns and a line break between rows.
- Readable by NumPy function "loadtxt".

### Cost matrices

Cost matrices (a.k.a path tables, distance matrices and time matrices) represent distances between nodes. They are placed in the "cost_matrices" subfolder as text files. The format is as follows:
- n x n matrix, where n is the number of nodes.
- Diagonal values are expected to be zero.
- Row represents the starting node. Column represents the target node.
- Whitespace between columns and a line break between rows.
- Readable by NumPy function "loadtxt".

### Node demands

Node demands represent the goods that are requested of the vehicles that visit them. They are placed in the "node_demands" subfolder as text files. The format is as follows:
- n x 1 matrix, where n is the number of nodes.
- Line break between values.
- Readable by NumPy function "loadtxt".

### Node penalties

Node penalties represent coefficients that each node uses to calculate a penalty whenever a vehicle arrives late. A penalty is calculated by multiplying the coefficient with the amount of time that a vehicle is late. Penalty coefficients are placed in the "node_penalties" subfolder as text files. The format is as follows:
- n x 1 matrix, where n is the number of nodes.
- Line break between values.
- Readable by NumPy function "loadtxt".

### Node profits

Node profits represent the amount of profit that is made upon visiting the nodes. They are placed in the "node_profits" subfolder as text files. The format is as follows:
- n x 1 matrix, where n is the number of nodes.
- Line break between values.
- Readable by NumPy function "loadtxt".

### Node service times

Node service times represent the amount of time needed to deliver goods from a vehicle to a customer upon arrival. They are placed in the "node_service_times" subfolder as text files. The format is as follows:
- n x 1 matrix, where n is the number of nodes.
- Line break between values.
- Readable by NumPy function "loadtxt".

### Node time windows

Node time windows represent intervals in time during which nodes can be serviced. Arriving sooner than the lower bound of it results in waiting time, while arriving later than the upper bound results in either a penalty or the solution becoming invalid. Time windows are placed in the "node_time_windows" subfolder as text files. The format is as follows:
- n x 2 matrix, where n is the number of nodes.
- First column represents the lower bound of the time windows, and the second that of upper bound.
- Lower bound must be lower than the upper bound.
- Whitespace between columns and a line break between rows.
- Readable by NumPy function "loadtxt".

### Parameter settings

This folder contains specific parameter settings that dictate how something is supposed to be done. Multiple instances of these can be maintained for ease of use. Check the README.md in subfolder "parameter_settings" for details.

### Plot data

This folder contains data created as a result of using the application. Folder "ResultSetX", where X is an integer (1 or higher), contains the results of one execution of the Genetic Algorithm. Subfolders inside aforementioned folder contain details of presented results and results themselves. These are presented as n x 2 matrices, where n is the number of entries that varies. The "sample" folder contains files that are expected to be created by the application.
