# killawattr

A power usage data wrangler & visualizer.

Fetches data from an API, gets rid of bad data, outputs and visualizes the resulting clean data.

## Running

### Installing dependencies

Clone the repository, get Python, and then:

```sh
$ python3 -m venv venv
$ . venv/bin/activate
$ (venv) pip3 install -r requirements.txt
```

### Running the example

Modify the settings in [example.py](examples/example.py) and

```sh
$ (venv) PYTHONPATH=src python3 examples/example.py
```

For the interactive example that supports fetching multiple files, see [example_interactive.py](examples/example_interactive.py)

```sh
$ (venv) PYTHONPATH=src python3 examples/example_interactive.py

```

### Testing

```sh
$ (venv) pytest
```

## Building

```sh
$ ...
```
