import matplotlib.pyplot as plt
import streamlit as st

from itunes_api import ambil_lagu_itunes
from playlist import pilih_lagu, format_durasi
from gemini_ai import (
    buat_rekomendasi_ai,
    terapkan_urutan_ai,
    nama_playlist_default,
)
from exports import buat_dataframe, buat_file_excel, buat_data_json


# ---------------------------------------------------------
# TAMPILAN UTAMA
# ---------------------------------------------------------
if "playlist" not in st.session_state:
    st.session_state.playlist = None
if "nama_playlist" not in st.session_state:
    st.session_state.nama_playlist = ""
if "alasan_ai" not in st.session_state:
    st.session_state.alasan_ai = ""
if "kegiatan" not in st.session_state:
    st.session_state.kegiatan = ""
if "target_menit" not in st.session_state:
    st.session_state.target_menit = 0


with st.sidebar:
    st.markdown("## 🎧 Music Playlist")
    st.caption("Atur playlist sesuai waktu kegiatanmu.")
    st.divider()

    st.markdown("### Pengaturan Playlist")

    target_menit = st.number_input(
        "Durasi kegiatan (menit)",
        min_value=10,
        max_value=360,
        value=90,
        step=5,
        help="Masukkan waktu kegiatan yang ingin ditemani musik."
    )

    kegiatan = st.selectbox(
        "Jenis kegiatan",
        ["Belajar", "Lari", "Olahraga", "Santai", "Perjalanan", "Bekerja"]
    )

    genre = st.selectbox(
        "Genre musik",
        [
            "Semua genre", "Pop", "Rock", "Hip-Hop/Rap", "R&B/Soul",
            "Dance", "Electronic", "Indie", "Jazz", "Classical",
            "Alternative", "K-Pop", "Soundtrack"
        ]
    )

    artis = st.text_input(
        "Artis (opsional)",
        placeholder="Contoh: Taylor Swift"
    )

    st.caption("Sumber lagu: iTunes Search API")
    buat_playlist = st.button(
        "✨ Buat Playlist",
        type="primary",
        use_container_width=True
    )

    st.divider()
    st.caption("Music Playlist • Project Praktikum Struktur Data")


st.markdown(
    """
    <div class="hero">
        <h1>🎧 Music Playlist</h1>
        <p>Playlist yang pas dengan durasi kegiatanmu.</p>
        <p style="font-size:.9rem; margin-top:16px;">
            Temukan susunan lagu yang sesuai dengan waktu dan aktivitasmu.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

if buat_playlist:
    if not artis.strip() and genre == "Semua genre":
        kata_kunci = "popular music"
    elif artis.strip():
        kata_kunci = artis.strip()
    else:
        kata_kunci = genre

    with st.spinner("Sedang mencari lagu dari iTunes..."):
        semua_lagu, pesan_error = ambil_lagu_itunes(kata_kunci)

    if pesan_error:
        st.error(pesan_error)
        st.session_state.playlist = None

    elif not semua_lagu:
        st.warning("Lagu tidak ditemukan. Coba kata kunci atau artis lain.")
        st.session_state.playlist = None

    else:
        lagu_filter = semua_lagu

        if genre != "Semua genre":
            hasil_filter = [
                lagu for lagu in semua_lagu
                if genre.lower() in lagu["genre"].lower()
            ]

            if hasil_filter:
                lagu_filter = hasil_filter
            else:
                st.info(
                    "Genre yang dipilih tidak ditemukan pada hasil pencarian. "
                    "Aplikasi menampilkan hasil lagu dari pencarian utama."
                )

        if not lagu_filter:
            st.warning("Tidak ada lagu yang cocok dengan pilihan tersebut.")
            st.session_state.playlist = None
        else:
            with st.spinner("Menyusun lagu sesuai durasi kegiatan..."):
                hasil_playlist = pilih_lagu(lagu_filter, target_menit)

            if not hasil_playlist:
                st.warning("Belum ada lagu yang dapat dimasukkan ke playlist.")
                st.session_state.playlist = None
            else:
                with st.spinner("Gemini sedang menyusun nama dan urutan lagu..."):
                    rekomendasi, pesan_ai = buat_rekomendasi_ai(
                        hasil_playlist, kegiatan, target_menit
                    )

                if rekomendasi:
                    hasil_playlist = terapkan_urutan_ai(
                        hasil_playlist, rekomendasi
                    )
                    nama = rekomendasi.get(
                        "nama_playlist", nama_playlist_default(kegiatan)
                    )
                    alasan = rekomendasi.get(
                        "alasan", "Playlist disusun sesuai jenis kegiatan."
                    )
                    st.session_state.ai_aktif = True
                else:
                    nama = nama_playlist_default(kegiatan)
                    alasan = (
                        "Urutan lagu dibuat berdasarkan hasil pemilihan durasi. "
                        "Tambahkan GEMINI_API_KEY untuk mendapatkan nama dan "
                        "penjelasan playlist dari Gemini AI."
                    )
                    st.session_state.ai_aktif = False

                st.session_state.playlist = hasil_playlist
                st.session_state.nama_playlist = nama
                st.session_state.alasan_ai = alasan
                st.session_state.kegiatan = kegiatan
                st.session_state.target_menit = target_menit
                st.session_state.pesan_ai = pesan_ai


# ---------------------------------------------------------
# HASIL PLAYLIST
# ---------------------------------------------------------
if st.session_state.playlist:
    playlist = st.session_state.playlist
    nama = st.session_state.nama_playlist
    alasan = st.session_state.alasan_ai
    kegiatan_hasil = st.session_state.kegiatan
    target_hasil = st.session_state.target_menit

    total_detik = sum(lagu["durasi_detik"] for lagu in playlist)
    total_menit = total_detik / 60
    selisih = abs(target_hasil - total_menit)

    st.markdown(f"## 🎶 {nama}")
    st.markdown(
        f"<span class='muted'>Playlist untuk kegiatan {kegiatan_hasil.lower()}.</span>",
        unsafe_allow_html=True
    )

    if st.session_state.get("ai_aktif", False):
        st.success("Gemini AI berhasil membuat rekomendasi playlist.")
    else:
        st.info(
            "Playlist berhasil dibuat. Gemini AI belum aktif, "
            "jadi nama dan penjelasan menggunakan rekomendasi dasar."
        )
        if st.session_state.get("pesan_ai"):
            st.caption(st.session_state.pesan_ai)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Durasi Target", f"{target_hasil} menit")
    col2.metric("Durasi Playlist", f"{total_menit:.1f} menit")
    col3.metric("Jumlah Lagu", len(playlist))
    col4.metric("Selisih Waktu", f"{selisih:.1f} menit")

    st.markdown("### 💡 Alasan Penyusunan")
    st.write(alasan)

    st.markdown("### 📋 Daftar Lagu")
    for nomor, lagu in enumerate(playlist, start=1):
        kolom_gambar, kolom_info, kolom_durasi = st.columns([1, 6, 1])

        with kolom_gambar:
            if lagu["gambar"]:
                st.image(lagu["gambar"], width=62)
            else:
                st.markdown("🎵")

        with kolom_info:
            st.markdown(f"**{nomor}. {lagu['judul']}**")
            st.caption(
                f"{lagu['artis']} • {lagu['album']} • {lagu['genre']}"
            )
            if lagu["tautan"]:
                st.markdown(
                    f"[Buka lagu di iTunes]({lagu['tautan']})",
                    unsafe_allow_html=False
                )
            if lagu["preview"]:
                with st.expander("Dengarkan preview"):
                    st.audio(lagu["preview"])

        with kolom_durasi:
            st.markdown(f"**{format_durasi(lagu['durasi_detik'])}**")

        st.divider()

    # -----------------------------------------------------
    # VISUALISASI DATA 1 DAN 2
    # -----------------------------------------------------
    st.markdown("## 📊 Visualisasi Playlist")

    df_playlist = buat_dataframe(playlist)

    tab1, tab2 = st.tabs(["Durasi setiap lagu", "Akumulasi durasi"])

    with tab1:
        fig1, ax1 = plt.subplots(figsize=(10, max(4, len(playlist) * 0.32)))
        nama_lagu = [
            f"{lagu['judul'][:28]} - {lagu['artis'][:18]}"
            for lagu in playlist
        ]
        durasi_lagu = [
            lagu["durasi_detik"] / 60 for lagu in playlist
        ]

        ax1.barh(nama_lagu[::-1], durasi_lagu[::-1])
        ax1.set_title("Durasi Setiap Lagu")
        ax1.set_xlabel("Durasi (menit)")
        ax1.set_ylabel("Lagu")
        ax1.grid(axis="x", alpha=0.25)
        fig1.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)

    with tab2:
        urutan = list(range(1, len(playlist) + 1))
        akumulasi = []
        total_sementara = 0

        for lagu in playlist:
            total_sementara += lagu["durasi_detik"]
            akumulasi.append(total_sementara / 60)

        fig2, ax2 = plt.subplots(figsize=(10, 4.5))
        ax2.plot(
            urutan, akumulasi,
            marker="o", linewidth=2,
            label="Akumulasi durasi playlist"
        )
        ax2.axhline(
            y=target_hasil,
            linestyle="--",
            linewidth=2,
            label=f"Target {target_hasil} menit"
        )
        ax2.set_title("Perkembangan Durasi Playlist")
        ax2.set_xlabel("Jumlah lagu")
        ax2.set_ylabel("Total durasi (menit)")
        ax2.legend()
        ax2.grid(alpha=0.25)
        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    # -----------------------------------------------------
    # EKSPOR FILE
    # -----------------------------------------------------
    st.markdown("## 📥 Download Playlist")
    df_export = buat_dataframe(playlist)

    col_csv, col_excel, col_json = st.columns(3)

    with col_csv:
        csv_data = df_export.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "Download CSV",
            data=csv_data,
            file_name="music_playlist.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_excel:
        excel_data = buat_file_excel(
            playlist, nama, kegiatan_hasil,
            target_hasil, alasan
        )
        st.download_button(
            "Download Excel",
            data=excel_data,
            file_name="music_playlist.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col_json:
        json_data = buat_data_json(
            playlist, nama, kegiatan_hasil,
            target_hasil, alasan
        )
        st.download_button(
            "Download JSON",
            data=json_data.encode("utf-8"),
            file_name="music_playlist.json",
            mime="application/json",
            use_container_width=True
        )

else:
    st.markdown("## Mulai buat playlist")
    st.write(
        "Atur durasi dan kegiatan melalui panel di sebelah kiri, "
        "lalu tekan **Buat Playlist**."
    )

    info1, info2, info3 = st.columns(3)
    with info1:
        st.markdown("### ⏱️ Sesuai Waktu")
        st.caption("Pilih durasi kegiatan dari 10 sampai 360 menit.")
    with info2:
        st.markdown("### 🎼 Sesuai Selera")
        st.caption("Cari lagu berdasarkan genre atau artis favorit.")
    with info3:
        st.markdown("### ✨ Dibantu AI")
        st.caption("Gemini membantu memberi nama dan mengurutkan playlist.")

    st.markdown("---")
    st.caption(
        "Catatan: ketersediaan lagu dan preview mengikuti data yang "
        "disediakan oleh iTunes Search API."
    )
