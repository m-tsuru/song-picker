from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Song Picker",
    page_icon=":musical_note:",
    layout="wide",
)

f = Path("picker_component/index.html")
component_html = f.read_text()

f = Path("picker_component/style.css")
component_css = f.read_text()

f = Path("picker_component/script.js")
component_js = f.read_text()


song_picker = st.components.v2.component(
    "song_picker",
    html=component_html,
    css=component_css,
    js=component_js,
)

st.title("Song Picker Component")
st.divider()

# コンポーネントから選択された曲情報を取得
song_picker = song_picker()
