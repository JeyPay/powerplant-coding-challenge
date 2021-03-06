# powerplant-coding-challenge
Author: Ryan Danenberg

# How to build and launch
Using Python >= 3.7
```
pip install -r requirements.txt
python main.py
```

# Design choices
The structure of the code was done in a way that the project can be expanded at large scale without having to change the whole file tree

# Computation choices
The merit-order was defined considering the price per MWh and the efficiency. Following that, the windturbine are prioritized over all other powerplants.
