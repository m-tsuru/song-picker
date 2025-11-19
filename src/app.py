import os
import random

import pandas as pd
import requests
import spotipy
import streamlit as st
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

from picker_component import song_picker

load_dotenv(verbose=True)

sample_songs = {
    "left": [
        {
            "album_image_url": "https://i.scdn.co/image/ab67616d0000b273ef6c77a0c55525ca56fa7fce",
            "track_id": "31kEZjFiRjB9fqcfqqaI6e",
            "track_name": "azure",
            "artist_id": "3YmAt9U9INQwxAwfgMVfKD",
            "artist": "TrySail",
            "album_id": "1Wap9CfRYVOT6YbGWa9mox",
            "album": "TryAgain",
        },
        {
            "album_image_url": "https://i.scdn.co/image/ab67616d0000b27381d4cd032e66b11e0ea4b1a5",
            "track_id": "2kj06TYMx03lA8YBWMpRXM",
            "track_name": "相合学舎",
            "artist_id": "274c1FFqS8HAIeL7XgK0Hz",
            "artist": "HO-KA-GO CLIMAX GIRLS, ノクチル",
            "album_id": "7rg9RfJGUbH8aLeqHLGBst",
            "album": "THE IDOLM@STER SHINY COLORS Synthe-Side 02",
        },
        {
            "album_image_url": "https://i.scdn.co/image/ab67616d0000b273aa313fca872ea4c0563d7112",
            "track_id": "7y7Cs6GoOXZJudXOopmiO7",
            "track_name": "whiz",
            "artist_id": "3YmAt9U9INQwxAwfgMVfKD",
            "artist": "TrySail",
            "album_id": "5gbH0hTUkbcDDM9Z2i1D76",
            "album": "Sail Canvas",
        },
        {
            "album_image_url": "https://i.scdn.co/image/ab67616d0000b27395ad700402ecf6204bb956fd",
            "track_id": "452pQ1WuBZjzjx9lkXVstl",
            "track_name": "あおぞらサイダー",
            "artist_id": "6tmX0pNtuRyYat4zyxRTes",
            "artist": "市川雛菜 (CV.岡咲美保)",
            "album_id": "6gEqUT48U8C9GK6QhpoJeG",
            "album": "THE IDOLM@STER SHINY COLORS COLORFUL FE@THERS",
        },
    ],
    "top": [
        {
            "album_image_url": "https://i.scdn.co/image/ab67616d0000b2730e85079de6ce50ccda1bdf98",
            "track_id": "3vW2EZcRS0JtADChw8oKP8",
            "track_name": "星座になれたら",
            "artist_id": "2nvl0N9GwyX69RRBMEZ4OD",
            "artist": "結束バンド",
            "album_id": "45zwTVu2P0jYhlwr0ORNNP",
            "album": "星座になれたら",
        },
        {
            "album_image_url": "https://i.scdn.co/image/ab67616d0000b2736b3c1cb03763ad4c437730fb",
            "track_id": "6DCOPYnwHSpJ0GCKaXdjn5",
            "track_name": "forget-me-not",
            "artist_id": "2SIBY7Jwq1kYng12Zguo3C",
            "artist": "ReoNa",
            "album_id": "4PwgqiO9jB02M92C6YfGo2",
            "album": "forget-me-not",
        },
    ],
    "right": [
        {
            "album_image_url": "https://i.scdn.co/image/ab67616d0000b273ef3add34c410b770f9c638c8",
            "track_id": "31EVU4Hqjnz3DqH2zdpWZE",
            "track_name": "Agapē",
            "artist_id": "7sW7rerkVb9XV7vgsVuMHq",
            "artist": "メロキュア",
            "album_id": "1c0wPUwhC8meB2YnOVpVOT",
            "album": "メロディック・スーパー・ハード・キュア",
        },
        {
            "album_image_url": "https://i.scdn.co/image/ab67616d0000b273375cf58cf4772919203c355b",
            "track_id": "72ghOwtaZ0vggvWspdJiE9",
            "track_name": "アンインストール",
            "artist_id": "4S7mAJFFsYYZE3gTYuf254",
            "artist": "Chiaki Ishikawa",
            "album_id": "3pDK2zBTymHAafUL9oNbuD",
            "album": "「ぼくらの」オープニングテーマ\u3000アンインストール",
        },
        {
            "album_image_url": "https://i.scdn.co/image/ab67616d0000b2737ad8e9d28e1137f0cd42f5ea",
            "track_id": "2P0NKKycnAxIt5Yi2a8ORx",
            "track_name": "Gravitation",
            "artist_id": "4SLTgwsFXbomwbNjsAvs3E",
            "artist": "黒崎真音",
            "album_id": "4yjeUJ5cZExNRXG8ceFTOy",
            "album": "Gravitation",
        },
        {
            "album_image_url": "https://i.scdn.co/image/ab67616d0000b2733447c12971a59f928c58c7c8",
            "track_id": "5UZVUKqRUmHxT8RmZZHojc",
            "track_name": "あんなに一緒だったのに",
            "artist_id": "7FVrkZcfwIc1ZwlQPatdUw",
            "artist": "See-Saw",
            "album_id": "5pc46oCGZxvCOs0DJXTimZ",
            "album": "機動戦士ガンダム SEED ~ SEED DESTINY THE BRIDGE Across the Songs from GUNDUM SEED & SEED DESTINY",
        },
    ],
    "bottom": [
        {
            "album_image_url": "https://i.scdn.co/image/ab67616d0000b2739c2805d72617a245d5835fee",
            "track_id": "3EHS9oZ7rdHebZpJPrRT1X",
            "track_name": "Real Force",
            "artist_id": "0205qmZS0XVeT43KQWCnpv",
            "artist": "Elisa",
            "album_id": "7cLwC2X2vkZ4fS5oQ4Lw7F",
            "album": "Rouge Adolescence",
        },
        {
            "album_image_url": "https://i.scdn.co/image/ab67616d0000b2731e7cfb82da103b090ae9e179",
            "track_id": "325oystEUVGQ7eHNRDi8eI",
            "track_name": "Magic∞world",
            "artist_id": "4SLTgwsFXbomwbNjsAvs3E",
            "artist": "黒崎真音",
            "album_id": "5ofzZbSSAY1C5qH4A8zk2H",
            "album": "Butterfly Effect",
        },
    ],
    "center": [
        {
            "album_image_url": "https://i.scdn.co/image/ab67616d0000b273d33b001e30c42fb06fadfe82",
            "track_id": "3DtNlxjaeUaB4rB3Se7dqK",
            "track_name": "メモリーズ･ラスト",
            "artist_id": "4SLTgwsFXbomwbNjsAvs3E",
            "artist": "黒崎真音",
            "album_id": "00IgCjDJQwQFB46IJ3Shcn",
            "album": "MAON KUROSAKI BEST ALBUM -M.A.O.N.-",
        },
    ],
}


def generate_sample_songs_from_dataframe(df: pd.DataFrame) -> dict:
    """
    DataFrameからランダムに中心曲を選び、テンポとキーに基づいてsample_songsを生成

    Args:
        df: プレイリストのDataFrame (tempo, key列を含む)

    Returns:
        sample_songs形式の辞書
    """
    # tempoとkeyが有効な曲のみをフィルタリング
    valid_df = df[
        (df["tempo"] != "-")
        & (df["key"] != "-")
        & df["tempo"].notna()
        & df["key"].notna()
    ].copy()

    if valid_df.empty:
        return {"left": [], "right": [], "top": [], "bottom": [], "center": []}

    # tempoとkeyを数値型に変換
    valid_df["tempo"] = pd.to_numeric(valid_df["tempo"], errors="coerce")
    valid_df["key"] = pd.to_numeric(valid_df["key"], errors="coerce")

    # NaNを除外
    valid_df = valid_df.dropna(subset=["tempo", "key"])

    if valid_df.empty:
        return {"left": [], "right": [], "top": [], "bottom": [], "center": []}

    # ランダムに中心曲を選択
    center_song = valid_df.sample(n=1).iloc[0]
    center_tempo = center_song["tempo"]
    center_key = int(center_song["key"])

    # centerを辞書形式に変換
    center = [
        {
            "album_image_url": center_song["album_image_url"],
            "track_id": center_song["track_id"],
            "track_name": center_song["track_name"],
            "artist_id": center_song["artist_id"],
            "artist": center_song["artist"],
            "album_id": center_song["album_id"],
            "album": center_song["album"],
            "tempo": float(center_song["tempo"]),
            "key": int(center_song["key"]),
        }
    ]

    # left: centerよりテンポが小さい曲を、テンポが大きい順に最大4曲
    left_df = (
        valid_df[valid_df["tempo"] < center_tempo]
        .sort_values("tempo", ascending=False)
        .head(4)
    )

    # right: centerよりテンポが大きい曲を、テンポが小さい順に最大4曲
    right_df = (
        valid_df[valid_df["tempo"] > center_tempo]
        .sort_values("tempo", ascending=True)
        .head(4)
    )

    # top: centerよりキーが1つ高い曲を最大2曲
    top_key = (center_key + 1) % 12
    top_df = valid_df[valid_df["key"] == top_key].head(2)

    # bottom: centerよりキーが1つ低い曲を最大2曲
    bottom_key = (center_key - 1) % 12
    bottom_df = valid_df[valid_df["key"] == bottom_key].head(2)

    # DataFrameを辞書のリストに変換する関数
    def df_to_song_list(dataframe):
        songs = []
        for _, row in dataframe.iterrows():
            songs.append(
                {
                    "album_image_url": row["album_image_url"],
                    "track_id": row["track_id"],
                    "track_name": row["track_name"],
                    "artist_id": row["artist_id"],
                    "artist": row["artist"],
                    "album_id": row["album_id"],
                    "album": row["album"],
                    "tempo": float(row["tempo"]),
                    "key": int(row["key"]),
                }
            )
        return songs

    res = {
        "left": df_to_song_list(left_df),
        "right": df_to_song_list(right_df),
        "top": df_to_song_list(top_df),
        "bottom": df_to_song_list(bottom_df),
        "center": center,
    }
    print(res)
    return res


def find_song_by_track_id(songs: dict, track_id: str) -> dict | None:
    return next((song for song in songs if song["track_id"] == track_id), None)


def get_pick_song(spotify_track_id: str, songs_data: dict) -> dict | None:
    song = find_song_by_track_id(
        [song for songs in songs_data.values() for song in songs],
        spotify_track_id,
    )
    if song:
        pick = {
            "artist": song["artist"],
            "track_name": song["track_name"],
            "album": song["album"],
            "track_id": song["track_id"],
            "album_image_url": song["album_image_url"],
            "tempo": song.get("tempo", "-"),
            "key": song.get("key", "-"),
        }
        return pick
    return None


def get_audio_features_from_rapidapi(track_ids: list) -> dict:
    """
    RapidAPIのtrack-analysisエンドポイントを使用してオーディオ特徴を取得

    Returns:
        dict: track_id -> audio features のマッピング
    """
    rapidapi_key = os.environ.get("RAPIDAPI_KEY")
    if not rapidapi_key:
        return {}

    audio_features_map = {}

    for track_id in track_ids:
        url = f"https://track-analysis.p.rapidapi.com/pktx/spotify/{track_id}"
        headers = {
            "x-rapidapi-key": rapidapi_key,
            "x-rapidapi-host": "track-analysis.p.rapidapi.com",
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                audio_features_map[track_id] = result
        except Exception as e:
            st.warning(f"Failed to fetch audio features for track {track_id}: {e}")
            continue

    return audio_features_map


def convert_playlist_to_dataframe(
    items: list, sp: spotipy.Spotify = None
) -> pd.DataFrame:
    """
    Convert a Spotify playlist items list into a DataFrame.

    Accepts items in either of these shapes:
    - [{'track': {...}}, ...]
    - [{...track dict...}, ...]

    Handles dict-based responses from the Spotipy client as well as
    simple nested dicts returned from other sources (e.g., sample data).

    If sp (Spotipy client) is provided, fetches audio features for tempo and key.
    """
    prettier = []

    def _get(obj: object, key: str, default: object = "-") -> object:
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    for item in items:
        # Accept either {'track': {...}} or the track dict/object itself
        track = None
        if isinstance(item, dict) and "track" in item:
            track = item.get("track")
        elif hasattr(item, "track"):
            track = item.track
        else:
            track = item

        if not track:
            # skip empty/None entries
            continue

        track_id = _get(track, "id")
        track_name = _get(track, "name")

        artists = _get(track, "artists", []) or []
        artist_id = "-"
        artist_names = []
        if artists:
            first = artists[0]
            if isinstance(first, dict):
                artist_id = first.get("id", "-")
                artist_names = [a.get("name", "-") for a in artists]
            else:
                artist_id = first.id if hasattr(first, "id") else "-"
                artist_names = [a.name if hasattr(a, "name") else "-" for a in artists]

        artist = ", ".join(artist_names)

        album = _get(track, "album", {}) or {}
        if isinstance(album, dict):
            album_id = album.get("id", "-")
            album_name = album.get("name", "-")
            images = album.get("images", []) or []
            album_image_url = images[0].get("url", "-") if images else "-"
        else:
            album_id = album.id if hasattr(album, "id") else "-"
            album_name = album.name if hasattr(album, "name") else "-"
            images = album.images if hasattr(album, "images") else []
            # images may be list of dicts or objects
            if images:
                first_img = images[0]
                if isinstance(first_img, dict):
                    album_image_url = first_img.get("url", "-")
                else:
                    album_image_url = (
                        first_img.url if hasattr(first_img, "url") else "-"
                    )
            else:
                album_image_url = "-"

        prettier.append(
            {
                "album_image_url": album_image_url,
                "track_id": track_id,
                "track_name": track_name,
                "artist_id": artist_id,
                "artist": artist,
                "album_id": album_id,
                "album": album_name,
            },
        )

    df = pd.DataFrame(prettier)


if __name__ == "__main__":
    # session_stateの初期化
    if "pick" not in st.session_state:
        st.session_state.pick = {
            "artist": "アーティスト名",
            "track_name": "曲名",
            "album": "アルバム名",
            "track_id": "4xGTfPquIRvZQyTrbInyZU",
            "album_image_url": "https://i.scdn.co/image/ab67616d00001e02dbdd908a5638656cdd6cd3f2",
            "tempo": "-",
            "key": "-",
        }

    if "df" not in st.session_state:
        st.session_state.df = None

    if "sample_songs" not in st.session_state:
        st.session_state.sample_songs = sample_songs

    with st.popover("Configure"):
        MARKET = st.text_input(
            "Markets (Localization)",
            value="JP",
            help="Specify the market for localization, e.g., 'JP' for Japan.",
        )
        FIELDS = st.text_input(
            "Fields to Retrieve",
            value="tracks.items(track(name,id,artists(name,id),album(name,id,images.url.0)).0)",
            help="Specify the fields to retrieve from the Spotify API.",
            disabled=False,
        )
        LIMIT = st.number_input(
            "Number of Items to Retrieve",
            min_value=1,
            max_value=100,
            value=10,
            step=1,
            help="Specify the number of items to retrieve from the playlist.",
        )

    st.set_page_config(
        page_title="Song Picker",
        page_icon=":musical_note:",
        layout="wide",
    )

    st.title("Song Picker")

    col_playlist_url, col_fetch = st.columns(
        [4, 1],
        vertical_alignment="bottom",
    )

    col_result_popover = st.popover("Result", use_container_width=True)

    playlist_filename = col_playlist_url.text_input(
        "Enter Retrieve Filename:",
        "playlist_export.csv",
    )

    if col_fetch.button("Fetch", use_container_width=True):
        # CSVファイルを読み込む
        if playlist_filename:
            try:
                with st.spinner(f"Loading {playlist_filename}..."):
                    df = pd.read_csv(playlist_filename)
                    st.session_state.df = df

                    # DataFrameからsample_songsを生成
                    generated_songs = generate_sample_songs_from_dataframe(df)
                    st.session_state.sample_songs = generated_songs

                    # centerの曲をpickとして設定
                    if generated_songs["center"]:
                        st.session_state.pick = generated_songs["center"][0]

                    st.success(f"Loaded {len(df)} tracks from {playlist_filename}")
            except FileNotFoundError:
                st.error(f"File not found: {playlist_filename}")
            except Exception as e:
                st.error(f"Error loading file: {e}")
        else:
            st.warning("Please enter a filename.")

        # DataFrameを表示
        if st.session_state.df is not None:
            col_result_popover.data_editor(
                st.session_state.df,
                column_config={
                    "album_image_url": st.column_config.ImageColumn(
                        "Album Art",
                    ),
                    "tempo": st.column_config.NumberColumn(
                        "Tempo (BPM)",
                        format="%.1f",
                    ),
                },
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No data loaded. Please fetch a CSV file first.")

    # session_state の pick を使用して UI を表示
    pick = st.session_state.pick

    with st.container(border=True):
        selected_col_thumbnail, selected_col_detail, selected_col_iframe = st.columns(
            [1, 2, 2],
            vertical_alignment="center",
        )
        selected_col_thumbnail.image(
            pick["album_image_url"],
            width=152,
        )

        with selected_col_detail.container():
            st.subheader(pick["track_name"])
            st.markdown(
                f"**{pick['artist']}** / {pick['album']} - [Open in Spotify](https://open.spotify.com/track/{pick['track_id']})",
            )
            st.markdown(
                f"🎵 **Tempo:** {pick['tempo']} BPM | 🎹 **Key:** {pick['key']}"
            )

        with selected_col_iframe.container():
            st.components.v1.iframe(
                f"https://open.spotify.com/embed/track/{pick['track_id']}?utm_source=generator&theme=0",
                width="100%",
                height=152,
            )

    # コンポーネントから選択された曲情報を取得
    props = song_picker(
        data={"songs": st.session_state.sample_songs},
        on_mouseovered_change=lambda: None,
        on_clicked_change=lambda: None,
    )

    # マウスオーバーされた曲を取得して session_state を更新
    if props.get("mouseovered"):
        new_pick = get_pick_song(
            props.get("mouseovered"), st.session_state.sample_songs
        )
        if new_pick and new_pick != st.session_state.pick:
            st.session_state.pick = new_pick
            st.rerun()
