import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import energy_efficient_algorithms.compression_emissions as compr

def c_set_page_config(page_title="Energy Efficient Algorithms"):
    st.set_page_config(
        layout="wide",
        page_title=page_title,
        page_icon="⚡")

def create_compressed_text_idx_plot(compressed_text_idx, filename, indices=tuple([10**(i+2) for i in range(11)])):
    disk_emissions = compr.disk_co2_emissions(compr.idx_sizes[filename][compressed_text_idx])
    query_emissions = [compr.query_co2_emissions(c, compr.query_energy_usage[filename][compressed_text_idx]) for c in indices]

    query_emissions_series = pd.Series(
        query_emissions,
        index=indices,
        name="Emissions of queries"
    )

    disk_emissions_series = pd.Series(
        [disk_emissions for _ in range(len(query_emissions))],
        index=indices,
        name="Emissions of disk usage"
    )

    total_emissions_series = pd.Series(
        [disk_emissions + qe for qe in query_emissions],
        index=indices,
        name="Total emissions"
    )

    fig, ax = plt.subplots()
    query_emissions_series.plot(ax=ax, marker="o", logy=True, logx=True)
    disk_emissions_series.plot(ax=ax, marker="o", logy=True, logx=True)
    total_emissions_series.plot(ax=ax, marker="o", logy=True, logx=True)

    ax.set_xlabel("Queries")
    ax.set_ylabel("CO2 eq [g]")
    ax.legend()

    return fig