import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px

import shared.streamlit_utils as su
from shared.references import References
from shared.common_text import EXPERIMENT_SYSTEM_TEXT
import energy_efficient_algorithms.compression_emissions as compr


references = References()

PAGE_TITLE = "Compressed Text Indices: Using Cache Misses for Energy-Efficiency"

su.c_set_page_config(PAGE_TITLE)

st.title(PAGE_TITLE)

st.write("Compressing large texts or large data has been an important issue for a long time. "
         "Compression in itself can be energy-efficient because it can arrange data in a more succinct manner and therefore save energy when storing or transferring such data. "
         "But another aspect is the decompression part. If the decompression takes too much energy, then we may have an issue. "
         "In general, there is always a conflict, higher compression ratio tends to infer that the decompression part takes more energy. "
         "This relationship does not hold for some compression tools, but is mostly true, trivially, if we compare uncompressed data with highly compressed data.")

st.write("We want to take a closer look at compressed text indices. "
         "These are indices that support the following queries with the text in compressed form:")
st.write("- *count*: counting how many times a pattern occurs in the text.")
st.write("- *locate*: enumeration of all the occurrences of a pattern in the text.")

st.write("We want to investigate the energy-efficiency of locate queries using three different compressed text indices.")

st.write(f"- `move-r`: "
         f"A compressed text index based on the run-length encoding of the Burrows-Wheeler-Transform {references.cite('move-r')}. "
         f"Improvement of the r-index by using the move data structure {references.cite('r-index', 'move')}. "
         f"It achieves high locate performance in comparison to the r-index and most other contemporary compressed text indices. ")
st.write(f"- `move-r-lzend`: Based on the move-r index, it replaces the locate function of move-r {references.cite('move-r-lzend-rlz')}. "
         f"Instead, it answers locate queries by compressing the differential suffix array with LZ-End {references.cite('lzend')}. "
         f"The idea is to improve the locate performance of the move-r index. It comes with the cost of a worse compression ratio.")
st.write(f"- `move-r-rlz`: Replaces the locate function of move-r with the RLZ-compressed differential suffix array {references.cite('move-r-lzend-rlz', 'rlz')}. "
         f"Similar to move-r-lzend. ")

### Experiment section
st.write(f"## Experiments\n{EXPERIMENT_SYSTEM_TEXT} "
         f"For our measurements, we used the implementations of Dinklage et al. {references.cite('move-r-lzend-rlz')}. "
         f"They can be found [here](https://github.com/LukasNalbach/Move-r). "
         f"We run our tests on the file `einstein`, a file consisting of different version of wikipedia articles about einstein concatenated together. "
         f"Because of the repetitive nature of the einstein file, it is very suitable for compression.")

st.write(f"First, we measured the average runtime and energy usage of 20,000 locate queries with random patterns of the length 8, "
         f"the results can be found in figure {references.ref_figure('loc_all')}. "
         f"Clearly, move-r-rlz is the fastest index for locate queries and it also consumes the least energy. "
         f"The move-r and move-r-lzend index are much more similar matched. " +
         "Even though move-r is about {:.2f}% slower than move-r-lzend, their energy consumption is nearly identical. ".format(100 * (compr.measured_locate_data['einstein']['8']['time']['move-r'] - compr.measured_locate_data['einstein']['8']['time']['move-r-lzend']) / compr.measured_locate_data['einstein']['8']['time']['move-r']))

st.image("webapp/static/compressed_text_indices_einstein_8.png", caption=f"Figure {references.ref_figure('loc_all')}: results for 20,000 locate queries on the text `einstein` with patterns of the length 8. "
                                                                  "There was an average of 63,761 occurrences per pattern.")

eng_to_time_move_r = compr.measured_locate_data["einstein"]["8"]["eng"]["move-r"] / compr.measured_locate_data["einstein"]["8"]["time"]["move-r"]
eng_to_time_move_r_rlz = compr.measured_locate_data["einstein"]["8"]["eng"]["move-r-rlz"] / compr.measured_locate_data["einstein"]["8"]["time"]["move-r-rlz"]
st.write(f"To find out why this is the case, we change the representation of our data a bit. "
         f"The figure {references.ref_figure('loc_eng_per_time')} shows now the energy that is consumed per time. "
         f"We no longer look at the absolute energy of a program, but rather their ratio of energy per runtime. " +
         "Now we get a different picture, relative to a time interval move-r-rlz consumes the most energy. About {:.2f}% more than move-r. ".format(100 * (eng_to_time_move_r_rlz - eng_to_time_move_r) / eng_to_time_move_r) +
         "This most probably stems from the fact, that move-r-rlz is much more cache efficient than move-r and move-r-lzend. "
         "As we learned on the previous page, cache efficient programs tend to consume more energy per time interval. ")

row_2 = st.columns([1, 2, 1])

st.write("But not only runtime and energy efficiency are important for compressed text indices, "
         "another big factor is the compression ratio achieved. "
         "A better compression ratio means that the compressed text index is smaller. "
         f"The resulting index sizes for einstein can be seen in figure {references.ref_figure('size')}. " +
         "We can see that move-r and move-r-lzend are significantly smaller than move-r-rlz with move-r having a {:.2f}% smaller index size than move-r-rlz. ".format(100 * (compr.idx_sizes['einstein']['move-r-rlz'] - compr.idx_sizes['einstein']['move-r']) / compr.idx_sizes['einstein']['move-r-rlz']) +
         "Having energy consumption and runtime for locate queries and compression ratio as factors, one wonders what the optimal compressed text index is?")

row_3 = st.columns([1, 2, 1])

st.write("This question can't be answered in generality because the optimal index depends on the use case and individual preferences. "
         f"If we combine runtime and compression ratio in figure {references.ref_figure('size_time')}, "
         f"it is evident that every index is pareto-optimal if we look at runtime and compression ratio. "
         f"If we look at energy usage and compression ratio in figure {references.ref_figure('size_eng')}, the picture changes. "
         f"Practically, move-r-lzend is dominated by move-r because it only has a negligible lower energy consumption. So, we remain with only move-r and move-r-rlz as pareto-optimal options for this case.")

row_4 = st.columns(2)

st.write("### Construction costs")
st.write("But what about the construction of these indices? This, of course, consumes energy too. "
         f"As you can see in Figure {references.ref_figure('cst_all')}. the construction of move-r-lzend consumes the most energy and takes the most time by a big margin. "
         f"Move-r and move-r-rlz are relatively close to another.")

st.image("webapp/static/compressed_text_indices_einstein_construct.png", caption=f"Figure {references.ref_figure('cst_all')}")

st.write("### Adding construction and query costs together")

st.write("Let's take a look at the combination of construction costs and costs for locate queries. "
         f"The energy usage, dependent on the amount of locate queries executed, is visualized in figure {references.ref_figure('cmb')}. "
         f"If one executes up to approximately 20,000 locate queries, then the construction costs outweigh and move-r is the most energy-efficient choice. "
         f"For more queries, move-r-rlz becomes the most energy-efficient index. "
         f"Note, that we excluded the compression ratio in this figure again, these three factors will be merged on the following page.")

row_construction = st.columns([1,2,1])

st.write("## Conclusions")

st.write("The results from the previous chapter were helpful to understand the difference in energy per time interval ratios across algorithms for the same purpose. "
         "This even helped to find situations were algorithms were pareto-optimal if one minimizes runtime, but become dominated if one minimizes energy consumption. "
         "Which shows that runtime is also in the praxis insufficient to be a proxy for energy-consumption.")

st.write("## Further reading")
st.page_link("pages/3_Emissions_and_Compression.py", label="Emissions and Compression")

st.divider()
st.write(references.make_references_section())

# run-time heavy loading at the end
used_algos = ["move-r", "move-r-lzend", "move-r-rlz"]
with row_2[1]:
    fig = px.bar(
        x=used_algos,
        y=[compr.measured_locate_data["einstein"]["8"]["eng"][algo] / compr.measured_locate_data["einstein"]["8"]["time"][algo] for algo in used_algos],
        height=500,
        labels={
            "x": "Algorithm - locate",
            "y": "Energy per time [J/s]"
        }
    )

    st.plotly_chart(fig, width='content')
    st.caption(f"Figure {references.ref_figure('loc_eng_per_time')}")

with row_3[1]:
    fig = px.bar(
        x=used_algos,
        y=[compr.idx_sizes["einstein"][algo] for algo in used_algos],
        height=500,
        labels={
            "x": "Algorithm - locate",
            "y": "Size of the compressed text index [MB]"
        }
    )

    st.plotly_chart(fig, width='content')
    st.caption(f"Figure {references.ref_figure('size')}: The original file has a size of {compr.file_sizes['einstein']} MB.")

for y, y_label, i, y_lim_max, fig_label in zip([[compr.measured_locate_data["einstein"]["8"]["time"][algo] for algo in used_algos],
                            [compr.measured_locate_data["einstein"]["8"]["eng"][algo] for algo in used_algos]],
                            ["Runtime [s]", "Energy [J]"],
                            [0, 1],
                            [20, 200],
                            ['size_time', 'size_eng']):
    with row_4[i]:
        fig, ax = plt.subplots()

        x = [compr.idx_sizes["einstein"][algo] for algo in used_algos]

        ax.scatter(x[0], y[0], s=120, color="#009E73", marker="s")
        ax.scatter(x[1], y[1], s=120, color="#0072B2", marker="^")
        ax.scatter(x[2], y[2], s=120, color="#E69F00", marker="o")

        ax.set_xlim(0, 60)
        ax.set_ylim(0, y_lim_max)

        ax.grid(False)

        ax.set_xlabel("Size of compressed text index [MB]")
        ax.set_ylabel(y_label)

        for j, offset in enumerate([(-35, 12), (-15, -22), (-25, 10)]):
            ax.annotate(used_algos[j], (x[j], y[j]), xytext=offset, textcoords="offset points", fontsize=12)

        st.pyplot(fig)
        st.caption(f"Figure {references.ref_figure(fig_label)}")

with row_construction[1]:
    log_scale = st.toggle("Logarithmic scale", value=True)

    coordinates = [2_000 * i for i in range(1, 1000)]

    energy_usage_series = [pd.Series(
        [compr.measured_construction_data["einstein"]["eng"][key] + (compr.measured_locate_data["einstein"]["8"]["eng"][key] / 20_000) * c for c in coordinates],
        index=coordinates,
        name=key
    ) for key in used_algos]

    fig, ax = plt.subplots()

    for series, color in zip(energy_usage_series, ["#009E73", "#0072B2", "#E69F00"]):
        series.plot(ax=ax, marker=None, color=color, logy=log_scale, logx=log_scale)

    ax.set_xlabel("Queries")
    ax.set_ylabel("Energy usage locate queries + construction [J]")
    ax.legend()

    st.pyplot(fig)
    st.caption(f"Figure {references.ref_figure('cmb')}")
