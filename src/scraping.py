import argparse
import csv
import os

import requests
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

parser = argparse.ArgumentParser(description="Spotify Playlist Scraper")
parser.add_argument("id", type=str, help="Spotify Playlist ID")
parser.add_argument(
    "skip",
    type=bool,
    default=False,
    help="Skip non-featured tracks",
)
args = parser.parse_args()

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
spotify_credentials = SpotifyClientCredentials(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret,
)
sp = spotipy.Spotify(client_credentials_manager=spotify_credentials)


def get_spotify_playlist_tracks(playlist_id: str):
    """
    Spotifyプレイリストから全ての曲を取得(ページネーション対応)

    Args:
        playlist_id: SpotifyプレイリストID

    Returns:
        tuple: (track_ids のリスト, 全プレイリストデータ)
    """
    all_items = []
    track_ids = []

    # 初回リクエスト (limit=100で最大件数を取得)
    results = sp.playlist_tracks(
        playlist_id,
        fields="items(track(name,id,artists(name,id),album(name,id,images))),next,total",
        market="JP",
        limit=100,
    )

    items = results.get("items", [])
    all_items.extend(items)

    # track_idsを収集
    for item in items:
        if item.get("track") and item["track"].get("id"):
            track_ids.append(item["track"]["id"])

    # 次のページがある場合は繰り返し取得
    next_url = results.get("next")
    total = results.get("total", 0)

    print(f"Total tracks in playlist: {total}")
    print(f"Fetched: {len(all_items)}/{total}")

    while next_url:
        # 次のページを取得
        results = sp.next(results)
        if not results:
            break

        items = results.get("items", [])
        all_items.extend(items)

        # track_idsを収集
        for item in items:
            if item.get("track") and item["track"].get("id"):
                track_ids.append(item["track"]["id"])

        next_url = results.get("next")

        print(f"Fetched: {len(all_items)}/{total}")

    # 結果を元の形式で返す (sp.playlistの戻り値形式に合わせる)
    full_results = {
        "tracks": {
            "items": all_items,
            "total": total,
        }
    }

    print(f"Completed: Fetched {len(track_ids)} tracks")

    return track_ids, full_results


def get_reccobeats_id_from_spotify_id(spotify_track_ids: list[str]):
    all_id_mapping = {}

    # 40件ごとに分割して処理
    for i in range(0, len(spotify_track_ids), 40):
        batch = spotify_track_ids[i : i + 40]
        r = ",".join(batch)
        print(f"Processing batch {i // 40 + 1}: {len(batch)} tracks")

        with requests.get(
            "https://api.reccobeats.com/v1/track?ids=" + r,
        ) as res:
            if res.status_code != 200:
                print(f"Error in batch {i // 40 + 1}: {res.status_code}")
                continue
            data = res.json()
            # SpotifyトラックIDとReccobeats IDの対応辞書を作成
            for item in data.get("content", []):
                href = item.get("href", "")
                reccobeats_id = item.get("id", "")
                # hrefからSpotifyトラックIDを抽出 (track/の後の部分)
                if href and reccobeats_id:
                    spotify_id = href.split("/track/")[-1]
                    all_id_mapping[spotify_id] = reccobeats_id

    return all_id_mapping


def get_reccobeats_id_from_audio_features(id_mapping: dict[str, str]):
    # id_mappingのvalues(Reccobeats ID)を取得
    reccobeats_ids = list(id_mapping.values())

    if not reccobeats_ids:
        return {}

    all_audio_features = {}

    # 40件ごとに分割して処理
    for i in range(0, len(reccobeats_ids), 40):
        batch = reccobeats_ids[i : i + 40]
        ids_param = ",".join(batch)
        print(f"Processing audio features batch {i // 40 + 1}: {len(batch)} tracks")

        with requests.get(
            f"https://api.reccobeats.com/v1/audio-features?ids={ids_param}",
        ) as res:
            if res.status_code != 200:
                print(f"Error in batch {i // 40 + 1}: {res.status_code}")
                continue
            data = res.json()

            # Spotify IDをキーとしたオーディオ特徴の辞書を作成
            for item in data.get("content", []):
                reccobeats_id = item.get("id", "")
                # Reccobeats IDに対応するSpotify IDを逆引き
                spotify_id = next(
                    (k for k, v in id_mapping.items() if v == reccobeats_id), None
                )
                if spotify_id:
                    all_audio_features[spotify_id] = {
                        "key": item.get("key"),
                        "tempo": item.get("tempo"),
                        "acousticness": item.get("acousticness"),
                        "danceability": item.get("danceability"),
                        "energy": item.get("energy"),
                        "instrumentalness": item.get("instrumentalness"),
                        "liveness": item.get("liveness"),
                        "loudness": item.get("loudness"),
                        "mode": item.get("mode"),
                        "speechiness": item.get("speechiness"),
                        "valence": item.get("valence"),
                    }

    return all_audio_features


def export_to_csv(playlist_data: dict, audio_features: dict, output_file: str):
    """CSVファイルにエクスポート"""
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "album_image_url",
            "track_id",
            "track_name",
            "artist_id",
            "artist",
            "album_id",
            "album",
            "tempo",
            "key",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in playlist_data.get("tracks", {}).get("items", []):
            if not item.get("track"):
                continue

            track = item["track"]
            track_id = track.get("id", "")
            features = audio_features.get(track_id, {})

            if args.skip and features.get("tempo", "") == "":
                continue

            # アルバム画像URL (最初の画像を取得)
            images = track.get("album", {}).get("images", [])
            album_image_url = images[0].get("url", "") if images else ""

            # アーティスト情報 (最初のアーティストを取得)
            artists = track.get("artists", [])
            artist_id = artists[0].get("id", "") if artists else ""
            artist_name = artists[0].get("name", "") if artists else ""

            # アルバム情報
            album = track.get("album", {})
            album_id = album.get("id", "")
            album_name = album.get("name", "")

            writer.writerow(
                {
                    "album_image_url": album_image_url,
                    "track_id": track_id,
                    "track_name": track.get("name", ""),
                    "artist_id": artist_id,
                    "artist": artist_name,
                    "album_id": album_id,
                    "album": album_name,
                    "tempo": features.get("tempo", ""),
                    "key": features.get("key", ""),
                }
            )

    print(f"CSV exported to {output_file}")


if __name__ == "__main__":
    if args.id:
        playlist_id = args.id
        ids, songs = get_spotify_playlist_tracks(playlist_id)
        print(ids)

        id_mapping = get_reccobeats_id_from_spotify_id(ids)
        print("ID Mapping:", id_mapping)

        audio_features = get_reccobeats_id_from_audio_features(id_mapping)
        print("Audio Features:", audio_features)

        export_to_csv(songs, audio_features, "playlist_export.csv")
        print("CSV export completed.")
    else:
        print("Please provide a Spotify Playlist ID as an argument.")
