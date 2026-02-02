import streamlit as st
import shared.streamlit_utils as su
import plotly.express as px
from shared.references import References
from shared.common_text import EXPERIMENT_SYSTEM_TEXT

########## Data section start ##########
measured_data = {
    "reg": { # register access
        "eng": 50.74641418457031, # in Joule
        "time": 4.513529940995795, # in seconds
        "iter": 20_971_520_000, # accesses
    },
    "32KB": {
        "eng": 7.536773681640625,
        "time": 1.093406922002032,
        "iter": 1_000_000_000,
    },
    "512KB": {
        "eng": 29.092559814453125,
        "time": 4.836264896002831,
        "iter": 1_000_000_000,
    },
    "4MB": {
        "eng": 62.41368103027344,
        "time": 10.614138566001202,
        "iter": 1_000_000_000,
    },
    "32MB": {
        "eng": 18.173782348632812,
        "time": 3.5995127049973235,
        "iter": 100_000_000,
    },
    "256MB": {
        "eng": 53.9232177734375,
        "time": 10.97128734600119,
        "iter": 100_000_000,
    }
}
keys_sorted = measured_data.keys()

for key in measured_data.keys():
    measured_data[key]["joule_per_access"] = measured_data[key]["eng"] / measured_data[key]["iter"]
    measured_data[key]["second_per_access"] = measured_data[key]["time"] / measured_data[key]["iter"]
    measured_data[key]["eng_per_second"] = measured_data[key]["eng"] / measured_data[key]["time"]

time_hits = 4.632522231004259
energy_hits = 50.34429931640625
accesses_hits = 20_971_520_000

time_chase = 106.10380331900524
energy_chase = 561.2737426757812
accesses_chase = 1_000_000_000

joule_per_cache_hit = energy_hits / accesses_hits #2.484585238562431e-09
joule_per_cache_miss = energy_chase / accesses_chase # 3.6213448765920475e-08

second_per_cache_hit = time_hits / accesses_hits # 2.195509086632807e-10
second_per_cache_miss = time_chase / accesses_chase # 4.694784307908429e-09

energy_per_second_cache_hits = energy_hits / time_hits # 11.316670259711712
energy_per_second_cache_misses = energy_chase / time_chase # 7.713548991999147
########### Data section end ###########

references = References()

PAGE_TITLE = "Cache misses are energy-efficient (relative to a time interval)"

su.c_set_page_config(PAGE_TITLE)

st.title(PAGE_TITLE)

st.write("Are cache hits more energy-efficient than cache misses? At first glance, the answer is clear. "
         "A cache miss takes a lot more time than a cache hit. "
         "Hence, we can conclude that one cache miss consumes more energy than one cache hit.")

st.write("But what if we ask a slightly different question? "
         "Do cache hits need more or less energy than cache misses per time interval? "
         "Then the answer is not so trivial. "
         "Cache hits need less energy, but we can also execute a lot more cache hits in a time interval than cache misses.")

st.write("It is known that there are programs where time is not a sufficient proxy for the energy usage of a program,"
         " i.e., there exist programs with the same running time but with significantly different energy usage. "
         "For example, Qiao et al. conducted an experiment where they found out that a CPU-intensive program "
         f"(repeatedly computing SHA256 on long strings) takes about 50% more energy per time interval than a memory-intensive program (repeatedly reading and writing large byte-arrays into heap memory) {references.cite('engAwareScheduling')}. "
         f"Weber et al. also investigated if runtime is a reliable proxy for energy consumption; they acknowledged that the literature gives mixed answers for this {references.cite("weberEtAl")}. "
         f"They found that the correlation between energy consumption and runtime is often strongly positive, but that it also can be none or negative for some programs or configuration options.")

st.write("This leads to an interesting question: What are the factors that contribute to the energy-efficiency of a program? "
         "We investigate the impact of cache efficiency on the energy usage of a program per time interval. ")
# todo "Fur further contributing factors one can look at [TODO]."

st.write("")

# TODO st.write("TODO Background memory hierarchy")

st.write(f"## Experiments\n{EXPERIMENT_SYSTEM_TEXT}"
         "The executed program can be found on [GitHub](https://github.com/jzumbrink/energy-efficiency-cache-misses/blob/main/testing_algorithms.cpp). "
         "We used [energy-toolkit](https://github.com/sse-labs/energy-toolkit) to measure the time and energy usage of our program "
         "(because of an unresolved bug in the tool, we used our own [fork](https://github.com/jzumbrink/energy-toolkit/tree/bugfix/run-on-correct-core) "
         "for the measurements). "
         "") #TODO describe the program we used

st.write("If we take a look at figure 1, we can clearly see, as expected, that a memory access takes longer if more data was allocated. "
         "This stems from the fact that if we have few data allocated, then the data can be stored in the L1/2/3 cache or even in the CPU register and can be accessed fast. "
         "As we increase the amount of memory allocated, the data have to be stored more and more in the L2 and L3 cache or even in the main memory, which leads to slower access times. ")

st.write("The energy usage per access in nano-joules is visualized in figure 2. From the first look, this looks relatively similar to the chart shown in figure 1. "
         "It's undeniably true that higher access times consequently result in higher energy usage. "
         "But if we take a closer look, we can see another pattern. "
         "If we have more data allocated, the ratio of energy used per time interval decreases. "
         "This phenomenon is more clearly visible in figure 3, where we plot the energy per time ratio directly.")

st.write("The energy per time ratio is the highest with {:.2f} J/s if we only access values in the CPU register. ".format(measured_data["reg"]["eng_per_second"]) +
         "This is about {:.2f}% higher than the energy per time ratio if we allocate 256 MB of data. ".format(100 * (measured_data["reg"]["eng_per_second"] - measured_data["256MB"]["eng_per_second"]) / measured_data["256MB"]["eng_per_second"]) +
         "If we look at instances where the values are not in the registers but mostly in the L1 cache, we already see an energy-to-time ratio of {:.2f} for 32 KB of allocated data. ".format(measured_data["32KB"]["eng_per_second"]) +
         "This energy per time ratio is still about {:.2f}% higher than the ratio if we allocate 256 MB.".format(100 * (measured_data["32KB"]["eng_per_second"] - measured_data["256MB"]["eng_per_second"]) / measured_data["256MB"]["eng_per_second"]))

row_bar_charts = st.columns(2)
middle_bar_chart = st.columns([1, 2, 1])

st.write("## Conclusions")
st.write("The experiments clearly show that runtime is not a reliable proxy for energy usage if the cache efficiency is different. "
         "Further, it shows that programs with more cache misses can be used to reduce the energy consumption if they achieve similar runtime performance. "
         "One must to keep this in mind when engineering energy-efficient algorithms. "
         "So, it might be worth it to look at cache-inefficient algorithms that are only a little bit slower (or even similarly fast) than more cache-efficient alternatives and use them if one wants to enhance energy-efficiency. ")

st.write("## Further reading")
st.page_link("pages/2_Compressed_Text_Indices.py", label="Compressed Text Indices: Using Cache Misses for Energy-Efficiency")

st.divider()
st.write(references.make_references_section())

# run-time heavy computation at the end
with row_bar_charts[0]:
    fig = px.bar(
        x=keys_sorted,
        y=[measured_data[key]["second_per_access"] * 1e9 for key in keys_sorted],
        height=500,
        labels={
            "x": "Algorithm",
            "y": "Time for one query [ns]"
        }
    )

    st.plotly_chart(fig, width='content')
    st.caption("Figure 1: TODO.")

with row_bar_charts[1]:
    fig = px.bar(
        x=keys_sorted,
        y=[measured_data[key]["joule_per_access"] * 1e9 for key in keys_sorted],
        height=500,
        labels={
            "x": "Algorithm",
            "y": "Energy for one access [nJ]"
        }
    )

    st.plotly_chart(fig, width='content')
    st.caption("Figure 2: TODO.")

with middle_bar_chart[1]:
    fig = px.bar(
        x=keys_sorted,
        y=[measured_data[key]["eng_per_second"] for key in keys_sorted],
        height=500,
        labels={
            "x": "Algorithm",
            "y": "Energy per time [J/s]"
        }
    )

    st.plotly_chart(fig, width='content')
    st.caption("Figure 3: The energy consumed per time interval is visualized in this figure.")