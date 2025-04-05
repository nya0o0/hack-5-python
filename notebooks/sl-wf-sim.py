import streamlit as st
import pandas as pd
import numpy as np
import time # <- We'll need this later as well

from wf_script import Population

st.title('Simple Wright-Fisher Simulation of Genetic Drift')

# Sidebar Header
st.sidebar.header("Simulation Controls")

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
init_pop = st.sidebar.slider("Initial generation size", 10, 200, 10, 10)
init_f = st.sidebar.slider("Initial allele frequency", 0.1, 0.9, 0.2, 0.1)
generation = st.sidebar.slider("Generation for stimulation", 10, 200, 50, 10)

# Initialize a placeholder for the end message
end_message = st.empty()

# Create a new Population
# As a reminder these are the default values for population size (N)
# and initial derived allele frequency (f).
#   N=10, f=0.2
p = Population(N = init_pop, f = init_f)

# Initialize the chart with the initial allele frequency of the derived
# allele. `line_chart` expects a list, so we must wrap `p.f` in square
# brackets to pass a list
chart = st.line_chart([p.f])

for i in range (1,generation + 1):
    p.step(ngens = 1)
    freq = freq = np.sum(p.pop)/len(p.pop)
    # Update status message
    status_text.text(f"Generation: {i}, Allele Frequency: {freq:.4f}")
    progress_bar.progress(i/generation)

    #Check the status
    if p.isMonomorphic():
        end_message.success(f"Simulation ended at generation {i} with allele frequency {freq}.")
        break
    
    # Update the chart to add the current allele frequency
    chart.add_rows([freq])
    # sleep for a small amount of time so you can watch the animation
    time.sleep(0.25)

# Add a button to rerun the simulation
st.button("Rerun")


