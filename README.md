# Traffic Data Analyzer

A suite of Python tools designed to parse, process, and visualize traffic survey data.

## Overview
This project takes raw CSV data containing daily traffic metrics—such as vehicle types, speeds, junction names, and weather conditions—and computes high-level statistics and visualizations. 

It consists of two main scripts:
- **`W2119764 - abc.py`**: Computes aggregated data such as total vehicle counts, percentage of trucks, electric vehicle counts, speed limit violations, and more. Results are printed to the console and saved continuously to `results.txt`.
- **`W2119764 - de.py`**: Processes the same CSV data to generate a native, interactive grouped bar chart displaying the hourly traffic flow for two specific junctions (Hanley Highway / Westway vs. Elm Avenue / Rabbit Road).

## Requirements
The project uses `pandas` for highly optimized data processing and `matplotlib` for dynamic visualization.

Install the required dependencies using pip:
```bash
pip install pandas matplotlib
```

## How to Run

You can run the application in two ways depending on your needs.

### 1. Interactive Mode
Run the scripts normally to launch an interactive questionnaire. You'll be prompted to enter a specific Day, Month, and Year to load the corresponding CSV dataset.
```bash
python "W2119764 - abc.py"
python "W2119764 - de.py"
```

### 2. Command-Line Interface (CLI) Mode
If you prefer to bypass the interactive prompts (for example, to automate the script via batch processes), you can supply the `--date` flag directly.
```bash
python "W2119764 - abc.py" --date 15 06 2024
python "W2119764 - de.py" --date 15 06 2024
```
In CLI mode, the script processes the single specified file, generates the output/chart, and gracefully exits.

## Project Structure
- `W2119764 - abc.py`: Primary data aggregation and processing script.
- `W2119764 - de.py`: Histogram visualization script.
- `utils.py`: Shared utilities containing leap year calculations, interactive input validation, and CLI argument parsing.
- `results.txt`: The text file where all `abc.py` and `de.py` outputs are permanently logged.
