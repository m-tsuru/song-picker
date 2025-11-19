export default function(component) {
    const { data, parentElement, setTriggerValue } = component;

    // 与えられた props (data.songs) を使って各方向のコンテナを埋める
    // data.songs.${angle} は中心側から外側に向かって並んでいることになる
    const angles = ["left", "right", "top", "bottom", "center"];
    for (const angle of angles) {
        const container = parentElement.querySelector(`.${angle}`);
        container.innerHTML = data.songs[angle]
            .map(song => `
                <div>
                    <img src="${song.album_image_url}"
                        alt="${song.track_name}"
                        data-spotify-track-id="${song.track_id}" />
                </div>
            `)
            .join("");
    }

    // マウスオーバされた時、選択された曲の data-spotify-track-id を Streamlit バックエンドに送信
    const imgElements = parentElement.querySelectorAll("img");
    imgElements.forEach(img => {
        img.addEventListener("mouseover", (event) => {
            setTriggerValue("mouseovered", event.target.getAttribute("data-spotify-track-id"));
        });
        img.addEventListener("click", (event) => {
            setTriggerValue("clicked", event.target.getAttribute("data-spotify-track-id"));
        });
    });
}
