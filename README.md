# Monte Carlo Streak Simulation: The 12 Heads Problem 🪙

This repository contains a statistical simulation developed in Python using the Monte Carlo method. The main objective is to demonstrate the stochastic difference between calculating probabilities in discrete blocks versus the waiting time in a continuous sequence of independent events.

Developed by Carlos Eduardo Torres Manzanares for the Statistics and Probability unit at Universidad Nacional de Ingeniería.

## 📊 Problem Description

The experiment consists of flipping a fair coin until an uninterrupted streak of **12 consecutive heads** is achieved.

Intuitively, one might think that since the probability of getting 12 heads is $1/4096$, it would take approximately $4096 \times 12 = 49,152$ tosses. However, this only applies if we group the tosses into rigid, independent blocks. In a **continuous sequence**, streaks overlap (a failure immediately resets the counter, leveraging subsequent tosses instantly), which significantly alters the expected value.

## 🧮 Theoretical Framework

The simulation empirically verifies the model based on **Markov Chains**. The expected time (number of tosses $E$) to observe a streak of $n$ consecutive successes in continuous tosses of a fair coin (probability $p=0.5$) is given by the formula:

$$E = 2^{n+1} - 2$$

For our experiment where $n = 12$:

$$E = 2^{13} - 2 = 8192 - 2 = 8190$$

This code runs thousands of simulations to demonstrate how, due to the **Law of Large Numbers**, the empirical average converges to this theoretical value of 8,190 total tosses.

## 🚀 How to Run the Simulation

**Prerequisites:**
* Python 3.9+ installed on your system.
* The simulation logic has no external dependencies (uses the native `random` module).
* The web interface requires `streamlit`, `pandas` and `altair` (see `requirements.txt`).

**Setup:**
1. Clone this repository:
   ```bash
   git clone https://github.com/charly05tr/Monte-Carlo-Streak-Simulation.git
   cd Monte-Carlo-Streak-Simulation
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

**Option A: Web interface (recommended)**

```bash
streamlit run app.py
```

If the `streamlit` command is not recognized, use `python -m streamlit run app.py`. The app opens in your browser at `http://localhost:8501`.

> The app must be launched with `streamlit run`, not `python app.py`. Streamlit starts a web server and runs the script itself.

**Option B: Command line**

```bash
python simulacion.py
```

Runs 10,000 simulations with a 12-heads streak and prints the empirical average next to the theoretical value.

## 🖥️ Web Interface

From the sidebar you can configure:
* **Consecutive heads (N):** streak length, from 1 to 16 (default 12).
* **Number of simulations:** how many times the experiment is repeated.
* **Fixed seed:** optional, to make results reproducible.

After running, the app shows:
* **Key metrics:** simulated average (with its deviation from the theoretical value), theoretical value, median, minimum and maximum.
* **Distribution histogram:** how many tosses each trial needed.
* **Convergence chart:** the cumulative average approaching the theoretical value as more simulations run (Law of Large Numbers).
* **Raw data:** a table of every result, downloadable as CSV.

Both charts mark the theoretical value $2^{N+1} - 2$ with a dashed red line.

> **Performance note:** with N = 12 each trial takes ~8,000 tosses, so 10,000 simulations mean ~80 million loop iterations in pure Python. This can take tens of seconds; the interface defaults to 2,000 simulations.

## 🛠️ Code Structure

The project separates the simulation logic from the presentation layer:

```
├── simulacion.py      # Simulation logic (no UI dependencies)
├── app.py             # Streamlit web interface
└── requirements.txt   # Interface dependencies
```

**`simulacion.py`**
* `experimento_continuo(largo_racha, rng)`: Models a single trial by tossing coins until reaching a streak of `largo_racha` heads (default 12). Returns the total number of tosses used.
* `simulacion_monte_carlo_continuo(num_simulaciones, largo_racha, semilla, al_progresar)`: Repeats the trial `num_simulaciones` times (default 10,000). Accepts an optional seed for reproducibility and a progress callback, so any interface can report progress without the logic depending on it.
* `valor_esperado_teorico(largo_racha)`: Returns the exact expected value $2^{n+1} - 2$.
* `ResultadoSimulacion`: Holds the results and exposes the average, median, minimum, maximum, theoretical value and cumulative averages.

**`app.py`**
* Reads the parameters from the UI, calls the logic in `simulacion.py` and renders the metrics and charts. It contains no simulation logic of its own.

## 📝 Conclusions

This simulation provides a practical visualization of an advanced theoretical probability concept. It demonstrates the effectiveness of the Monte Carlo method in estimating expected values in dynamic systems where direct combinatorial calculation can be counterintuitive.
