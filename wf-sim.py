#!/usr/bin/env python
"""
A simple wf simulator.
"""
import argparse
import random
import numpy as np

class Population:
    def __init__(self, N=10, f=0.2, with_np = True):
        self.N = N
        self.f = f
        # Parameter for numpy
        self.with_np = with_np

        # Create the population list
        derived_count = round(N*f)
        if self.with_np:
            self.pop = np.array([0] * (N - derived_count) + [1] * derived_count)
        else:
            self.pop = [0] * (N - derived_count) + [1] * derived_count
        
        # Track allele frequencies over generations
        self.freqs = []

    # Create printable representation of the population
    def __repr__(self):
        return f"Population(N={self.N}, f={self.f})"

    def step(self, ngens=1):
        for i in range(ngens):
            
            # Calculate the frequency of the derived (1) allele
            freq = sum(self.pop)/self.N
            self.freqs.append(freq) # append the new frequency in to the frequency list
            
            # Check whether the popuplation is monomorphic
            if self.isMonomorphic():
                break  # Stop simulation 

            # Simulate the next generation
            if self.with_np:
                self.pop = np.random.choice(self.pop, size=self.N, replace=True)
            else:
                self.pop = random.choices(self.pop, k=self.N)          

    def isMonomorphic(self):
        """
        Returns True if the population is fixed for either allele.
        """
        # Check the latest dirived allel frequency 
        return self.freqs[-1] == 1 or self.freqs[-1] == 0

# Function for iteration
def iterate_wf(N, f, ngens, repeats, verbose=False, outfile=None):
    fixed_count = 0
    log_data = []

    for i in range(repeats):
        if args.verbose:
            print(f"Repeat {i + 1}:")

        pop = Population(N, f)
        pop.step(ngens)
        final_freq = pop.freqs[-1]

        if pop.isMonomorphic():
            fixed_count += 1

        log_entry = {
            "repeat": i + 1,
            "generations_run": len(pop.freqs),
            "final_freq": final_freq,
            "fixation": pop.isMonomorphic()
        }
        log_data.append(log_entry)

        if args.verbose:
            print(f"Generation: {len(pop.freqs)}; Final freq(a): {final_freq}")

    fixation_prob = fixed_count / repeats
    result = f"The probability of allele (a) fixation is: {fixation_prob:.4f}"

    if args.outfile:
        with open(outfile, "w") as f:
            f.write("Repeat,Generations,Final_Freq,Fixation\n")
            for entry in log_data:
                f.write(f"{entry['repeat']},{entry['generations_run']},{entry['final_freq']},{entry['fixation']}\n")
            f.write(f"\n{result}\n")

    return result


# The main programme
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wright-Fisher Population Simulation")

    parser.add_argument("-N", type=int, default=100, help="Population size (default: 100)")
    parser.add_argument("-f", type=float, default=0.2, help="Initial derived allele frequency (default: 0.2)")
    parser.add_argument("-ngens", type=int, default=1000, help="Number of generations (default: 1000)")
    parser.add_argument("-repeats", type=int, default=100, help="Number of repetitions (default: 100)")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-o", "--outfile", type=str, help="File to save simulation results")

    args = parser.parse_args()
    
    result = iterate_wf(args.N, args.f, args.ngens, args.repeats, verbose=args.verbose, outfile=args.outfile)
    
    print(result)