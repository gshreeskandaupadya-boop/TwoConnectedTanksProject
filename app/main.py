import sys
from pathlib import Path

from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class SimulationWindow(QMainWindow):
    """Main window for launching an OpenModelica simulation."""

    MIN_TIME = 0
    MAX_TIME = 4

    def __init__(self):
        super().__init__()

        self.process = None

        self.setWindowTitle("OpenModelica Simulation Runner")
        self.setMinimumSize(700, 500)

        self._create_widgets()
        self._create_layout()
        self._connect_signals()
        self._set_default_values()

    def _create_widgets(self):
        """Create all GUI widgets."""

        self.executable_input = QLineEdit()
        self.executable_input.setPlaceholderText(
            "Select the OpenModelica executable..."
        )

        self.browse_button = QPushButton("Browse...")

        self.start_time_input = QSpinBox()
        self.start_time_input.setRange(
            self.MIN_TIME,
            self.MAX_TIME,
        )
        self.start_time_input.setValue(0)

        self.stop_time_input = QSpinBox()
        self.stop_time_input.setRange(
            self.MIN_TIME,
            self.MAX_TIME,
        )
        self.stop_time_input.setValue(1)

        self.run_button = QPushButton("Run Simulation")
        self.run_button.setMinimumHeight(40)

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)

        self.status_label = QLabel("Ready")

    def _create_layout(self):
        """Create and arrange the GUI layout."""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        form_layout = QFormLayout()

        executable_layout = QHBoxLayout()
        executable_layout.addWidget(self.executable_input)
        executable_layout.addWidget(self.browse_button)

        form_layout.addRow(
            "Application:",
            executable_layout,
        )
        form_layout.addRow(
            "Start time:",
            self.start_time_input,
        )
        form_layout.addRow(
            "Stop time:",
            self.stop_time_input,
        )

        title = QLabel("OpenModelica Simulation Runner")
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )

        layout = QVBoxLayout(central_widget)
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addLayout(form_layout)
        layout.addSpacing(10)
        layout.addWidget(self.run_button)
        layout.addWidget(QLabel("Simulation output:"))
        layout.addWidget(self.output_box)
        layout.addWidget(self.status_label)

    def _connect_signals(self):
        """Connect widget signals to their handlers."""

        self.browse_button.clicked.connect(
            self._browse_executable
        )
        self.run_button.clicked.connect(
            self._run_simulation
        )

    def _set_default_values(self):
        """Set the default executable path."""

        project_root = Path(__file__).resolve().parent.parent

        executable_path = (
            project_root
            / "model"
            / "build"
            / "TwoConnectedTanks.exe"
        )

        if executable_path.is_file():
            self.executable_input.setText(
                str(executable_path)
            )

    def _browse_executable(self):
        """Open a file dialog for selecting an executable."""

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Application",
            "",
            "Executable Files (*.exe);;All Files (*)",
        )

        if file_path:
            self.executable_input.setText(file_path)

    def _validate_inputs(self):
        """Validate executable path and simulation times."""

        executable = self.executable_input.text().strip()
        start_time = self.start_time_input.value()
        stop_time = self.stop_time_input.value()

        if not executable:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Please select an executable.",
            )
            return False

        executable_path = Path(executable)

        if not executable_path.is_file():
            QMessageBox.warning(
                self,
                "Invalid Application",
                "The selected executable does not exist.",
            )
            return False

        if executable_path.suffix.lower() != ".exe":
            QMessageBox.warning(
                self,
                "Invalid Application",
                "Please select a Windows executable (.exe).",
            )
            return False

        if not (
            0 <= start_time < stop_time < 5
        ):
            QMessageBox.warning(
                self,
                "Invalid Time Range",
                "The required condition is:\n"
                "0 <= start time < stop time < 5",
            )
            return False

        return True

    def _run_simulation(self):
        """Launch the OpenModelica executable."""

        if not self._validate_inputs():
            return

        executable = self.executable_input.text().strip()
        start_time = self.start_time_input.value()
        stop_time = self.stop_time_input.value()

        arguments = [
            "-override",
            f"startTime={start_time},stopTime={stop_time}",
        ]

        self.output_box.clear()

        self._append_output(
            "Starting simulation..."
        )
        self._append_output(
            f"Start time: {start_time}"
        )
        self._append_output(
            f"Stop time: {stop_time}"
        )
        self._append_output(
            f"Executable: {executable}"
        )
        self._append_output("")
        self._append_output("Arguments:")
        self._append_output(
            " ".join(arguments)
        )
        self._append_output("")

        self.run_button.setEnabled(False)
        self.status_label.setText(
            "Simulation running..."
        )

        self.process = QProcess(self)

        executable_path = Path(executable)
        self.process.setWorkingDirectory(
            str(executable_path.parent)
        )

        self.process.readyReadStandardOutput.connect(
            self._read_stdout
        )
        self.process.readyReadStandardError.connect(
            self._read_stderr
        )
        self.process.finished.connect(
            self._process_finished
        )
        self.process.errorOccurred.connect(
            self._process_error
        )

        self.process.start(
            executable,
            arguments,
        )

    def _read_stdout(self):
        """Read standard output from the simulation."""

        if self.process is None:
            return

        data = self.process.readAllStandardOutput()
        text = bytes(data).decode(
            "utf-8",
            errors="replace",
        )

        if text.strip():
            self._append_output(text.rstrip())

    def _read_stderr(self):
        """Read standard error from the simulation."""

        if self.process is None:
            return

        data = self.process.readAllStandardError()
        text = bytes(data).decode(
            "utf-8",
            errors="replace",
        )

        if text.strip():
            self._append_output(text.rstrip())

    def _process_finished(
        self,
        exit_code,
        exit_status,
    ):
        """Handle simulation process completion."""

        self.run_button.setEnabled(True)

        if exit_code == 0:
            self.status_label.setText(
                "Simulation completed successfully."
            )
            self._append_output(
                "\nSimulation completed successfully."
            )
        else:
            self.status_label.setText(
                f"Simulation failed "
                f"(exit code {exit_code})."
            )
            self._append_output(
                "\nSimulation failed. "
                f"Exit code: {exit_code}"
            )

        self.process.deleteLater()
        self.process = None

    def _process_error(self, error):
        """Handle process-launch errors."""

        self.run_button.setEnabled(True)

        self.status_label.setText(
            "Failed to launch simulation."
        )
        self._append_output(
            f"\nProcess error: {error}"
        )

        if self.process is not None:
            self.process.deleteLater()

        self.process = None

    def _append_output(self, text):
        """Append text to the simulation output box."""

        self.output_box.append(text)


def main():
    """Application entry point."""

    app = QApplication(sys.argv)

    window = SimulationWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()