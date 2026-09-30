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
* Python 3.x installed on your system.
* No external libraries required (uses the native `random` module).

**Execution:**
1. Clone this repository:
   ```bash
   git clone [https://github.com/your-username/repo-name.git](https://github.com/your-username/repo-name.git)
   ```
2. Run the main script from the terminal:
   ```bash
   python simulacion_monedas.py
   ```

## 🛠️ Code Structure

The script is divided into two main functions:
* `experimento_continuo()`: Models a single trial of the experiment by tossing coins and accumulating a streak until reaching 12. Returns the total number of tosses used.
* `simulacion_monte_carlo_continuo(num_simulaciones)`: An iterator that repeats the trial $N$ times (default is 10,000) and calculates the arithmetic mean of the results.

## 📝 Conclusions

This simulation provides a practical visualization of an advanced theoretical probability concept. It demonstrates the effectiveness of the Monte Carlo method in estimating expected values in dynamic systems where direct combinatorial calculation can be counterintuitive.
