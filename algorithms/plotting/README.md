# vrp-gen-alg - Plotting

Here are described modules related to plotting the results that come from using the application.

## Table of Contents

- [Plot Data](#plot-data)
- [Plot Manager](#plot-manager)
- [Plot Window](#plot-window)

### Plot Data

In this application figures are drawn using PlotData-objects and customized plotting functions that are defined here.

PlotData-objects contain information on an xy-axis with support for multiple datasets. Additionally it contains the strings for various labels. Results saved in the PlotData-object can also be saved into a collection of text files.

There are three plotting functions: one makes a line graph, another a bar graph and the other a map. These are used by the plot manager.

### Plot Manager

The plot manager is the interface that the application uses to create various figures of the results it gets from running the GA. The following figures are created:
- Generation 0 Population, sorted in ascending/descending order
 - X: Population individual
 - Y: Fitness
- Population Development (populations of multiple generations), sorted in ascending/descending order
 - One line represents one generation
 - X: Population individual
 - Y: Fitness
- Best individual by generation
 - X: Generation
 - Y: Fitness of generation's best individual
- Best overall individual by time
 - Best overall individual is tracked separately. Once a new best individual is found, the previous one is replaced.
 - X: Time (milliseconds)
 - Y: Fitness of the best overall individual
- Map of the best individual of generation 0
 - Dots represent node locations
 - Lines represent vehicle routes. Different colors indicate different vehicles.
- New best overall individuals with respect to generations of discovery
 - X: Generation
 - Y: Fitness of best overall individual
- Collection of maps demonstrating development of the best overall individual
 - Dots represent node locations
 - Lines represent vehicle routes. Different colors indicate different vehicles.

### Plot Window

PlotWindow is an implementation of the application's GUI. It is a simple window that showcases multiple figures (one at a time) with simple next/previous button navigation. Since matplotlib is used to make the figures, they can be modified and saved for later use.

Plot manager's function "summon_window" is used to create an instance of PlotWindow. Once the window is visible, execution is halted. That'll continue once the window is closed.
