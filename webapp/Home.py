import streamlit as st
import shared.streamlit_utils as su

import shared.common_text as ctxt

PAGE_TITLE = "Energy-efficiency: Cache Misses & Compression Algorithms"

su.c_set_page_config(PAGE_TITLE)

st.title(PAGE_TITLE)

cells = st.columns(2) + st.columns(2)

st.markdown(ctxt.MAIN_LINK_BUTTON_STYLE, unsafe_allow_html=True)

labels = ["Cache Misses are Energy Efficient", "Compressed Text Indices", "Emissions and Compression", "Emission Calculator for Compression"]
sites = ["Cache_Misses_are_Energy_Efficient", "Compressed_Text_Indices", "Emissions_and_Compression", "Emission_Calculator_for_Compression"]

for i, label, site in zip(range(4), labels, sites):
    with cells[i]:
        st.markdown(f'<form action="{site}" method="get"><button class="button-link">{label}</button></form>',
        unsafe_allow_html=True)