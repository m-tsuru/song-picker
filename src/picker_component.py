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

if __name__ == "__main__":
    st.title("Song Picker Component")

    st.markdown(
        "When Moused Over, Song Preview is Shown. When Clicked, You can re-select the song.",
    )

    # session_stateの初期化
    if "pick" not in st.session_state:
        st.session_state.pick = {
            "artist_name": "アーティスト名",
            "track_name": "曲名",
            "album_name": "アルバム名",
            "spotify_track_id": "4xGTfPquIRvZQyTrbInyZU",
            "artwork_url": "https://i.scdn.co/image/ab67616d00001e02dbdd908a5638656cdd6cd3f2",
        }

    # session_state の pick を使用して UI を表示
    pick = st.session_state.pick

    with st.container(border=True):
        selected_col_thumbnail, selected_col_detail, selected_col_iframe = st.columns(
            [1, 2, 2],
            vertical_alignment="center",
        )
        selected_col_thumbnail.image(
            pick["artwork_url"],
            width=152,
        )

        with selected_col_detail.container():
            st.subheader(pick["track_name"])
            st.markdown(
                f"**{pick['artist_name']}** / {pick['album_name']} - [Open in Spotify](https://open.spotify.com/track/{pick['spotify_track_id']})",
            )

        with selected_col_iframe.container():
            st.components.v1.iframe(
                f"https://open.spotify.com/embed/track/{pick['spotify_track_id']}?utm_source=generator&theme=0",
                width="100%",
                height=152,
            )

    st.divider()

    # コンポーネントから選択された曲情報を取得
    props = song_picker(
        data={"songs": sample_songs},
        on_mouseovered_change=lambda: None,
        on_clicked_change=lambda: None,
    )

    # マウスオーバーされた曲を取得して session_state を更新
    if props.get("mouseovered"):
        new_pick = get_pick_song(props.get("mouseovered"))
        if new_pick and new_pick != st.session_state.pick:
            st.session_state.pick = new_pick
            st.rerun()

    st.divider()
