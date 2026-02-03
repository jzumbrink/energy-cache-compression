import streamlit as st
import shared.streamlit_utils as su
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

import energy_efficient_algorithms.compression_emissions as compr
from shared.references import References
from shared.common_text import EXPERIMENT_SYSTEM_TEXT

references = References()

PAGE_TITLE = "Emissions and Compression"

su.c_set_page_config(PAGE_TITLE)

CO2 = "$\\text{CO}_2$"
CO2_EQ = "$\\text{CO}_2 \\, \\text{eq}$"
CO2_EQ_INL = "\\text{CO}_2 \\, \\text{eq}"
GRAM = "\\text{g}"
KGRAM = "\\text{kg}"
KMETER = "\\text{km}"

st.title(PAGE_TITLE)

st.write("We talk about compressed text indices as they were introduced on the previous page. "
         "If you haven't read it, you can do it by clicking the following button.")

st.page_link("pages/2_Compressed_Text_Indices.py", label="Compressed Text Indices")

st.write("When we talk about how many emissions are emitted from using compression algorithms, we must first define our scope. "
         "We will talk about the emissions generated when:")
st.write("1. Constructing the compressed text index.")
st.write("2. Decompressing parts of the compressed data. In our case, this means running locate-queries on the indices.")
st.write("3. Storing the compressed text index, i.e., the disk space that is occupied.")

st.write("For the first two points, we are already very far in measuring them. "
         f"With the measured energy consumption of construction and of locate queries, we must only convert this into {CO2} equivalent emissions. "
         f"For this, we take the average {CO2_EQ} emissions for a kilowatt hour in Germany; which was $363\\, {GRAM}$ in 2024 {references.cite('strommix')}. "
         f"One kilowatt hour is equivalent to 3600 kilojoules. "
         f"So, the {CO2_EQ} emissions per kilojoule are")
st.write("$$\\frac{363\\, \\text{g} \\, \\text{CO}_2\\,\\text{eq.}}{3600 \\,\\text{kJ}} \\approx 0.101 \\, \\text{g CO}_2\\,\\text{eq.} / \\text{kJ}.$$")
st.write(f"Now, we can successfully calculate the {CO2_EQ} emissions for the construction and the queries. "
         f"Note that the real {CO2_EQ} emissions can vary greatly depending on the time of day or the location.")

st.write("Coming up with a number for our third point, the emissions generated because of the occupied disk space, is a bit more tricky. "
         "And it's even more dependent on the individual situation. "
         "If one already has a disk and has enough space left, then one could argue that there are nearly no emissions generated. "
         "But if we apply this to all our files and data, we surely all would need bigger hard drives, so this is too short-sighted. "
         "We make the simplification to assume that the data is stored in an online storage. "
         "In times of massive data centers and a shift to store all things in a cloud, this may not be so far-fetched. "
         f"A report from the German Environment Agency concluded that that $166-280 \\,{KGRAM}\\, {CO2_EQ_INL}$ are emitted for storing a TB of "
         f"data for a year in an online storage {references.cite('gcc')}. "
         f"We take the average of their values and proceed with a value of $209.5 \\,{KGRAM}\\, {CO2_EQ_INL}$ per TB and year.")

st.write(f"## Experiments\n{EXPERIMENT_SYSTEM_TEXT}")

st.write(f"The computed emissions for our three indices are shown in figure {references.ref_figure('em_size')}. "
         f"It is no surprise that the storage of the move-r-rlz index emits twice as much {CO2_EQ} as the move-r index, "
         f"as the emissions are strictly linear to the compressed index size. "
         f"They are approximately in the range of $5-10\\, {GRAM}\\, {CO2_EQ_INL}$ per year, which is fairly small and less than a petrol car emits when traveling $0.1 \\,{KMETER}$ {references.cite('car_em')}. "
         f"But these emissions can still be significant if one has vastly bigger data to compress and store.")

uncompressed_file_disk_emissions = compr.disk_co2_emissions(compr.file_sizes['einstein'])
disk_emissions_move_r = compr.disk_co2_emissions(compr.idx_sizes['einstein']['move-r'])
disk_emissions_move_r_rlz = compr.disk_co2_emissions(compr.idx_sizes['einstein']['move-r-rlz'])
st.write("The uncompressed file would emit ${:.2f} \\,{}\\, {}$ per year. ".format(uncompressed_file_disk_emissions, GRAM, CO2_EQ_INL) +
         "Thus, choosing a compressed representation would save from {:.2f}% up to {:.2f}% of {} emissions for storage.".format(
             (uncompressed_file_disk_emissions - disk_emissions_move_r_rlz) / uncompressed_file_disk_emissions * 100,
             (uncompressed_file_disk_emissions - disk_emissions_move_r) / uncompressed_file_disk_emissions * 100,
             CO2_EQ
         ))

emissions_variant_row = st.columns([1, 2, 1])

st.write("Now, we can add the emissions from the storage to the emissions from the construction and the queries. "
         f"The total emissions per year and per query amount can be seen in figure {references.ref_figure('cmb')}. "
         f"It is apparent that the emissions for the construction of a compressed text index combined with the reduced "
         f"storage emissions are drastically lower than to store the uncompressed file directly. "
         f"If one plans to execute less than 5 million locate queries, then the move-r or move-r-lzend index would be the best choice to reduce emissions. "
         f"Furthermore, move-r emits less than move-r-lzend for every reasonable large amount of queries, " +
         "even though move-r is about {:.2f}% slower than move-r-lzend. ".format(100 * (compr.measured_locate_data['einstein']['8']['time']['move-r'] - compr.measured_locate_data['einstein']['8']['time']['move-r-lzend']) / compr.measured_locate_data['einstein']['8']['time']['move-r']) +
         f"Move-r-rlz emits the least amount of {CO2_EQ} when the amount of queries exceeds 7 million.")

emissions_all_row = st.columns([1, 2, 1])

st.write("## Further resources")
st.page_link("pages/4_Emission_Calculator_for_Compression.py", label="Emission Calculator for Compression")

st.divider()

st.write(references.make_references_section())

# run-time heavy loading at the end
used_algos = ["move-r", "move-r-lzend", "move-r-rlz"]
with emissions_variant_row[1]:
    fig = px.bar(
        x=used_algos,
        y=[compr.disk_co2_emissions(compr.idx_sizes["einstein"][algo]) for algo in used_algos],
        height=500,
        labels={
            "x": "Emissions for the storage of the compressed text indices",
            "y": f"CO2 eq. per year [g/y]"
        }
    )

    st.plotly_chart(fig, width='content')
    st.caption(f"Figure {references.ref_figure('em_size')}")

with emissions_all_row[1]:
    all_emissions_tabs = st.tabs(["all", "move-r", "move-r-lzend", "move-r-rlz"])


with all_emissions_tabs[0]:
    log_scale = st.toggle("Logarithmic scale", value=True)

    coordinates = [200_000 * i for i in range(1, 1000)]

    emission_series = [pd.Series(
        [compr.all_co2_emissions(
            compr.idx_sizes["einstein"][key],
            compr.measured_construction_data["einstein"]["eng"][key],
            compr.measured_locate_data["einstein"]["8"]["eng"][key] / compr.measured_locate_data["einstein"]["8"]["iter"],
            c
        ) for c in coordinates],
        index=coordinates,
        name=key
    ) for key in used_algos]

    fig, ax = plt.subplots()

    for series, color in zip(emission_series, ["#009E73", "#0072B2", "#E69F00"]):
        series.plot(ax=ax, marker=None, color=color, logy=log_scale, logx=log_scale)

    uncompressed_series = pd.Series([uncompressed_file_disk_emissions], index=coordinates[0:1], name="uncompressed")
    uncompressed_series.plot(ax=ax, marker="o", color="black", logy=log_scale, logx=log_scale)

    ax.set_xlabel("Queries")
    ax.set_ylabel(f"{CO2_EQ} per year and queries [g]")
    ax.legend()

    st.pyplot(fig)
    st.caption(f"Figure {references.ref_figure('cmb')}")

log_scales: list[None | bool] = [None, None, None]
for i, algo in enumerate(used_algos):
    with all_emissions_tabs[i+1]:
        log_scales[i] = st.toggle("Logarithmic scale", value=True, key=str(i))

        coordinates = [200_000 * i for i in range(1, 1000)]

        em_storage = [compr.disk_co2_emissions(compr.idx_sizes["einstein"][algo]) for _ in coordinates]
        em_construction = [compr.joule_to_co2(compr.measured_construction_data["einstein"]["eng"][algo]) for _ in coordinates]
        em_query = [compr.joule_to_co2((compr.measured_locate_data["einstein"]["8"]["eng"][algo] / compr.measured_locate_data["einstein"]["8"]["iter"]) * c) for c in coordinates]

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
            series.plot(ax=ax, marker=None, color=color, logy=log_scales[i], logx=log_scales[i])

        ax.set_xlabel("Queries")
        ax.set_ylabel(f"{CO2_EQ} per year and queries [g]")
        ax.legend()

        st.pyplot(fig)
        st.caption(f"Figure {references.ref_figure(f'solo_{i}')}")