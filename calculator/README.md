# Calculator App

This is a simple command-line calculator application that evaluates mathematical expressions.

## How to Run

To run the calculator, execute the `main.py` file with your desired expression as an argument:

```bash
python main.py "<expression>"
```

**Example:**

```bash
python main.py "3 + 5"
```

This will output the result of the expression in JSON format.

## Features

- Supports basic arithmetic operations: addition (+), subtraction (-), multiplication (*), and division (/)
- Handles nested expressions.
- Provides error handling for invalid expressions or insufficient operands.

## Testing

The project includes unit tests to ensure the correctness of the calculator's functionality. To run the tests, execute `tests.py`:

```bash
python tests.py
```
