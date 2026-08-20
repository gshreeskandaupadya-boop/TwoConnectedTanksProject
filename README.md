# OpenModelica Simulation Runner

A PyQt6 desktop application for executing an OpenModelica-generated
`TwoConnectedTanks` simulation with user-defined start and stop times.

This project was developed as a screening-task submission.

## Features

- PyQt6 desktop GUI
- Select an OpenModelica executable
- Enter simulation start time
- Enter simulation stop time
- Validates simulation time constraints
- Executes the OpenModelica executable using command-line arguments
- Captures simulation output
- Displays success or failure status to the user
- Uses an object-oriented Python application structure
- Includes the OpenModelica executable and Windows runtime dependencies

## Technology Stack

- Python 3.6+
- PyQt6
- OpenModelica
- Windows 10/11
- Git/GitHub

## Project Structure

```text
TwoConnectedTanksProject/
│
├── app/
│   ├── main.py
│   └── requirements.txt
│
├── model/
│   ├── FlowConnect.mo
│   ├── package.mo
│   ├── package.order
│   ├── Tank.mo
│   ├── Tank2.mo
│   ├── TwoConnectedTanks.mo
│   │
│   └── build/
│       ├── TwoConnectedTanks.exe
│       ├── OpenModelica runtime DLLs
│       └── required runtime files
│
├── original_model/
│   ├── FlowConnect.mo
│   ├── package.mo
│   ├── package.order
│   ├── Tank.mo
│   ├── Tank2.mo
│   └── TwoConnectedTanks.mo
│
├── .gitignore
└── README.md

The application follows this workflow:

User
  │
  ▼
PyQt6 GUI
  │
  ├── Select executable
  ├── Start time
  └── Stop time
  │
  ▼
Input validation
  │
  ▼
Python subprocess
  │
  ▼
TwoConnectedTanks.exe
  │
  ▼
OpenModelica simulation
  │
  ▼
Simulation result / status
  │
  ▼
GUI status message


1. Install Python:
Python 3.6 or later is required.

2. Install Python dependencies
Open a terminal in the app directory:
cd app
python -m pip install -r requirements.txt

Running the Application
From the project root:
python app/main.py

Running the Application
From the project root:
model/build/TwoConnectedTanks.exe
Command-Line Execution:
TwoConnectedTanks.exe -override=startTime=2,stopTime=4

OpenModelica Model

The application executes the compiled:

NonInteractingTanks.TwoConnectedTanks

model.

The model consists of:

Tank
Tank2
FlowConnect
TwoConnectedTanks

The model is compiled using OpenModelica and the resulting executable
is included in the model/build directory together with its required
Windows runtime libraries.

Input Validation

The application validates:

0 <= start_time < stop_time < 5

Invalid input is rejected before launching the simulation.

This prevents invalid simulation requests from being passed to the
OpenModelica executable.

Error Handling

The application handles:

Missing executable
Invalid time values
Invalid time ranges
Process execution errors
Non-zero process exit codes
Simulation failures

The user receives an appropriate status message through the GUI.

Reproducibility

The compiled OpenModelica executable and required runtime dependencies
are included in the repository so that the application does not require
OpenModelica to be installed separately for execution on the target
Windows environment.

Development Notes

The Python application separates GUI responsibilities from simulation
execution logic using classes and follows standard Python practices.

License

### Important

Don't change `main.py` right now.

Don't change the OpenModelica model.

Just replace the README with the above and save it.

Then tell me:

**README done**

and we'll do the final code-quality check before creating the GitHub repository.