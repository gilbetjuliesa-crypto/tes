import requests
import streamlit as st


@st.cache_data(ttl=600, show_spinner=False)
def ambil_lagu_itunes(kata_kunci, jumlah=100):
    """Mengambil daftar lagu dari iTunes Search API."""
    url = "https://itunes.apple.com/search"
    parameter = {
        "term": kata_kunci,
        "entity": "song",
        "limit": jumlah,
        "country": "ID"
    }

    try:
        response = requests.get(url, params=parameter, timeout=20)
        response.raise_for_status()
        hasil = response.json()

        daftar_lagu = []
        for item in hasil.get("results", []):
            durasi = item.get("trackTimeMillis")

            if not durasi:
                continue

            lagu = {
                "id": str(item.get("trackId", "")),
                "judul": item.get("trackName", "Tanpa judul"),
                "artis": item.get("artistName", "Artis tidak diketahui"),
                "album": item.get("collectionName", "-"),
                "genre": item.get("primaryGenreName", "Lainnya"),
                "durasi_ms": int(durasi),
                "durasi_detik": int(durasi // 1000),
                "preview": item.get("previewUrl", ""),
                "gambar": item.get("artworkUrl100", ""),
                "tautan": item.get("trackViewUrl", "")
            }

            daftar_lagu.append(lagu)

        # Menghindari lagu yang sama muncul lebih dari satu kali.
        lagu_unik = {}
        for lagu in daftar_lagu:
            lagu_unik[lagu["id"]] = lagu

        return list(lagu_unik.values()), None

    except requests.exceptions.Timeout:
        return [], "Koneksi ke iTunes terlalu lama. Coba beberapa saat lagi."
    except requests.exceptions.RequestException as error:
        return [], f"Tidak dapat mengambil data dari iTunes: {error}"
    except (ValueError, TypeError):
        return [], "Data dari iTunes tidak dapat dibaca."


def format_durasi(detik):
    menit = int(detik) // 60
    sisa_detik = int(detik) % 60
    return f"{menit}:{sisa_detik:02d}"
