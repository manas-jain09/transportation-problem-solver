# transportation-problem-solver
A Python-based tool for solving balanced and unbalanced transportation problems using NorthWest Corner Method, Least Cost Method, and Vogel's Approximation Method. This application, built with tkinter, provides a user-friendly interface for entering data and visualizes the steps and algorithms involved in finding the optimal solution.

## Features
  1. Solve both balanced and unbalanced transportation problems.
  
  2. Implement three methods: NorthWest Corner Method, Least Cost Method, and Vogel's Approximation Method.
  
  3. Visualize the steps and algorithms used in each method.
  
  4. User-friendly interface built with tkinter.

## Methods
### 1. NorthWest Corner Method:
The NorthWest Corner Method is a basic approach that starts at the top-left (northwest) cell of the cost matrix and allocates as much as possible to that cell, then moves either down or right, repeating the process until all supply and demand values are satisfied.

### 2. Least Cost Method:
The Least Cost Method allocates as much as possible to the cell with the smallest cost, then adjusts the supply and demand and repeats the process until all supply and demand values are satisfied.

### 3. Vogel's Approximation Method:
Vogel's Approximation Method (VAM) calculates penalties for not using the cheapest routes and allocates as much as possible to the cell with the highest penalty. It then adjusts the supply and demand and repeats the process until all values are satisfied.

## Screenshots
![Image 1](screenshots/Screenshot%202024-06-19%20134132.png)

![Image 2](screenshots/Screenshot%202024-06-19%20134314.png)

![Image 3](screenshots/Screenshot%202024-06-19%20134337.png)

![Image 4](screenshots/Screenshot%202024-06-19%20134402.png)

