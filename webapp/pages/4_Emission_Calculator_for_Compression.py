import streamlit as st
import shared.streamlit_utils as su
import pandas as pd
import matplotlib.pyplot as plt

import energy_efficient_algorithms.compression_emissions as compr
from shared.references import References

references = References()

PAGE_TITLE = "Emission Calculator for Compression"

su.c_set_page_config(PAGE_TITLE)

st.title(PAGE_TITLE)

idx_size = st.number_input("Size in MB of your index", value=10.0)
joule_construction = st.number_input("Energy needed for construction [Joule]", value=150.0)
joule_per_1000_queries = st.number_input("Joule per 1000 queries", value=4.0, help="Queries can be whatever you like, e.g. locate-queries, count-queries or plain decompression of intervals.")

log_scale = st.toggle("Logarithmic scale", value=True)

if st.button("Calculate"):
    indices = [10**i for i in range(11)]

    st.write("## Results")

    coordinates = [200_000 * i for i in range(1, 1000)]

    em_storage = [compr.disk_co2_emissions(idx_size) for _ in coordinates]
    em_construction = [compr.joule_to_co2(joule_construction) for _ in coordinates]
    em_query = [compr.joule_to_co2((joule_per_1000_queries / 1000) * c) for c in coordinates]

    size_series = pd.Series(
        em_storage,
        index=coordinates,
        name="emissions from storage"
    )

    construction_series = pd.Series(
        em_construction,
        index=coordinates,
        name="emissions from construction"
    )

    query_series = pd.Series(
        em_query,
        index=coordinates,
        name="emissions from queries"
    )

    total_series = pd.Series(
        [srg + cst + qry for srg, cst, qry in zip(em_storage, em_construction, em_query)],
        index=coordinates,
        name="total emissions"
    )

    fig, ax = plt.subplots()

    for series, color in zip([size_series, construction_series, query_series, total_series], ["#009E73", "#0072B2", "#E69F00", "black"]):
        series.plot(ax=ax, marker=None, color=color, logy=log_scale, logx=log_scale)

    ax.set_xlabel("Queries")
    ax.set_ylabel("CO2 eq per year and queries [g]")
    ax.legend()

    st.pyplot(fig)
    st.caption(f"Figure {references.ref_figure(f'solo')}")

    st.write("Curious how this is calculated? Take a loot at:")
    st.page_link("pages/3_Emissions_and_Compression.py", label="Emissions and Compression")
