# What it's For

You can create a small python program using these modules which will predict your financial future based on your pay, bills, loans, etc. Charts using matplotlib.

# How to use it

To invoke it, run:

    python model.py your_model_module

You will need to install the required items into your activated virtualenv first. Requirements are listed in `requirements.txt`. You will probably need to create your virtualenv with --system-site-packages to make matplotlib work properly on recent Ubuntu (at least this is true on Ubuntu 14.10).

## Matplotlib display in GUI

In order for this to work on python 3.6 on Ubuntu: sudo apt-get install python3.6-tk

## How to Build a Model Module

Define a module that has a function createModel in it.  This function should return an instance of model.Model. Other details TBD..

# Does Not Care About

* taxes
* assumes monthly compounding
* does not account for drift between when you pay and when interest is compounded

# Things to do

* make this README cover how to use the modules
* pylint a bit - some bad usage
* pep8 compliance
* tests

