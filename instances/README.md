# vrp-gen-alg - Instances

Here are described three different types of structural instances that the application uses, two of which are used during initialization and one is used actively.

## Table of Contents

- [ParamsVRP](#paramsvrp)
- [ParamsGENALG](#paramsgenalg)
- [VRP](#vrp)

### ParamsVRP

ParamsVRP is the object instance that contains settings for VRP-related parameters. These settings are configured from the variables subfolder "parameter_settings/vrp" by the parameter builder "param_builder", situated in "algorithms" folder. The settings within the instance are used during GA initialization. ParamsVRP also handles path table creation whenever coordinates are being used.

### ParamsGENALG

ParamsGENALG is the object instance that contains settings for GA-related parameters. These settings are configured from the variables subfolder "parameter_settings/genalg" by the parameter builder "param_builder", situated in "algorithms" folder. The settings within the instance are used during GA initialization.

### VRP

VRP is the object instance that represents an individual in a population that GA maintains. It keeps track of its solution to the problem instance described by instance ParamsVRP. The solution's fitness value and record of validity is also kept track of, although these values are provided by validators and evaluators.
