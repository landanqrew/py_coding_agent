# Project Overview

### Preface ###
#### This README.md file was generated with the following command: ####
python main.py "read the contents of all of my python files and update the ./README.md file to provide a comprehensive overview of the features of this directory and how to use them." --verbose --agent --iter-limit=20

This project contains a simple calculator application and related utilities.

## Key Files and Functionality:

*   **main.py:** This is the main entry point of the calculator application. It takes a mathematical expression as a command-line argument and evaluates it using the `Calculator` class.
    *   **Usage:** `python main.py "<expression>"`
    *   **Example:** `python main.py "3 + 5"`
*   **function_declaration.py:** This file defines the function declarations.
*   **tests.py:** This file contains unit tests for the `Calculator` class, ensuring the correctness of its calculations.
*   **lorem.py:** This file generates lorem ipsum text and saves it to a file named 'lorem.txt' inside the 'calculator' directory.

## Calculator Class:

The `Calculator` class (defined in `pkg/calculator.py`) is responsible for evaluating mathematical expressions. It supports the following operations:

*   Addition (+)
*   Subtraction (-)
*   Multiplication (*)
*   Division (/)

## Running the Tests:

To run the unit tests, execute the `tests.py` file:

```bash
python tests.py
```
## Example Usage:

To use the calculator, provide a mathematical expression as a command-line argument when running `main.py`. The application will evaluate the expression and print the result.

## Notes

Ensure that you have the required dependencies installed (see `requirements.txt`). You can install them using pip:
```bash
pip install -r requirements.txt
```