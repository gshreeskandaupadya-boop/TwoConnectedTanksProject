# OpenModelica Simulation Runner

A PyQt6 desktop application for running a compiled OpenModelica `TwoConnectedTanks` simulation with configurable start and stop times.

## Features

- Select an OpenModelica executable from the GUI.
- Use the bundled executable by default when it is available.
- Configure integer start and stop times.
- Validate the executable path and simulation time range before starting.
- Stream simulation output and errors to the application window.
- Display clear completion and failure statuses.
- Run without a separate OpenModelica installation when the bundled runtime is included.

## Requirements

- Windows 10 or later
- Python 3.8 or later
- PyQt6

The compiled simulation executable and its Windows runtime files are included in `model/build`.

## Project Structure

```text
TwoConnectedTanksProject/
├── app/
│   ├── main.py
│   └── requirements.txt
├── model/
│   ├── FlowConnect.mo
│   ├── package.mo
│   ├── package.order
│   ├── Tank.mo
│   ├── Tank2.mo
│   ├── TwoConnectedTanks.mo
│   └── build/
│       ├── TwoConnectedTanks.exe
│       └── OpenModelica runtime files
├── original_model/
│   └── Original Modelica source files
├── .gitignore
└── README.md
```

## Installation

From the project root, install the application dependency:

```powershell
python -m pip install -r app/requirements.txt
```

## Run the Application

```powershell
python app/main.py
```

The application opens with the bundled executable selected automatically when `model/build/TwoConnectedTanks.exe` exists. Otherwise, use **Browse...** to select an `.exe` file.

The valid simulation time range is:

```text
0 <= start time < stop time < 5
```

For example, a start time of `2` and a stop time of `4` is valid.

## Run the Simulation Directly

The compiled executable accepts OpenModelica override arguments:

```powershell
model\build\TwoConnectedTanks.exe -override startTime=2,stopTime=4
```

The GUI starts the process with the same override values.

## Model

The OpenModelica model is composed of:

- `Tank`
- `Tank2`
- `FlowConnect`
- `TwoConnectedTanks`

The Modelica source is stored in `model`. The original supplied source files are preserved in `original_model`.

## Error Handling

Before launching a simulation, the application checks for:

- A selected executable
- An existing `.exe` file
- A valid start and stop time range

During execution, the GUI reports process-launch errors, simulation output, standard error, and non-zero exit codes.

## License

This project was created for educational and screening-task evaluation purposes.