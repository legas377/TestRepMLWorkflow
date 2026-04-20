# Scalable Linear Regression Project

This project implements a scalable linear regression model that can handle datasets by processing data in batches. There are 3 scenarios used to manage workflow: basic, background (embedded), and CRON-based.

## Project Structure

```
scalable-linear-regression
├── src
│   ├── data_loader.py    # Loads data in batches
│   ├── model.py          # Manages the training process
│   └── utils.py
├── doc
│   ├── YAML_MAIN.md      # Description of base workflow
│   ├── YAML_BT.md        # Description of background training
│   └── YAML_CT.md        # Description of CRON-based iterative training
├── main.py               # Entry point of the application
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
└── .github/workflows     # YAML files of workflow management
```

## Usage

1. **Load Data**: Utilize the `data_loader.py` to fetch data in batches.
2. **Train Model**: Run the `main.py` file to start the training process of the linear regression model.

## Running the Project

To run the project, execute the following command in your terminal:

```
python main.py --mode "<mode>"
```

This will initialize the data generation, loading, and model training processes.

### Modes

#### 1. **`mode="all"`**
   - **Description:** This mode runs the entire training process in a loop for a fixed number of iterations (`n_iter=10` by default).
   - **Behavior:**
     - A new `DataLoader` instance is created to stream data in batches.
     - A new `ProjectModel` instance is initialized with a `LinearRegression` model.
     - The `step` function is called repeatedly for `n_iter` iterations, simulating real-time data processing.
     - After each iteration, the program pauses for 5 seconds (`sleep(5)`) to mimic real-time delays.
   - **Use Case:** This mode is suitable for running the full training process in one go, typically for batch processing or testing the entire pipeline.

#### 2. **`mode="single"`**
   - **Description:** This mode performs a single step of the training process and saves the current state of the `DataLoader` and `ProjectModel` to disk for later continuation.
   - **Behavior:**
     - The program attempts to load previously saved `DataLoader` and `ProjectModel` objects from disk (`DataLoader.pkl` and `Model.pkl`).
     - If no saved objects are found, new instances of `DataLoader` and `ProjectModel` are created.
     - The `step` function is executed once to process a single batch of data.
     - The updated `DataLoader` and `ProjectModel` objects are saved back to disk for future use.
   - **Use Case:** This mode is ideal for incremental or stepwise training, where the model is updated periodically (e.g., in a production environment with streaming data).

### Summary of Key Differences

| Feature                | `mode="all"`                          | `mode="single"`                       |
|------------------------|---------------------------------------|---------------------------------------|
| **Execution**          | Runs the full training loop.          | Executes a single training step.      |
| **State Persistence**  | Does not save intermediate states.    | Saves and loads state from disk.      |
| **Use Case**           | Batch processing or testing.          | Incremental/streaming data training.  |
| **Real-Time Simulation** | Includes a delay (`sleep(5)`) for each iteration. | No delay; processes one batch instantly. |

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.