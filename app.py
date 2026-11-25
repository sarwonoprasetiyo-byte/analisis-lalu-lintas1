import streamlit as st
import matplotlib.pyplot as plt

from analisis_data import (
    df,
    baca_data,
    hitung_volume,
    rekap_per_arah,
    rekap_per_jam,
    hitung_persentase,
)

st.set_page_config(
    page_title="Analisis Volume Lalu Lintas",
    page_icon="🚦",
    layout="wide"
)

st.title("Analisis Volume Lalu Lintas")
st.write("Data kendaraan arah Utara dan Selatan selama 24 jam.")

# Mengolah data dari program Python
data_valid = baca_data(df.copy())
hasil = hitung_volume(data_valid)
rekap_arah = rekap_per_arah(hasil)
rekap_jam = rekap_per_jam(hasil)
persentase = hitung_persentase(hasil)

total_kendaraan = int(hasil["total"].sum())
jam_puncak = rekap_jam.loc[rekap_jam["total"].idxmax()]

# Ringkasan
k1, k2, k3 = st.columns(3)

k1.metric("Total kendaraan", f"{total_kendaraan:,}")
k2.metric("Jam puncak", f"{int(jam_puncak['jam']):02d}.00")
k3.metric(
    "Volume jam puncak",
    f"{int(jam_puncak['total']):,} kendaraan/jam"
)

st.divider()

# Pilihan tabel
pilihan = st.selectbox(
    "Pilih data yang ingin ditampilkan",
    [
        "Rekap per jam",
        "Rekap per arah",
        "Persentase jenis kendaraan",
        "Data lengkap"
    ]
)

if pilihan == "Rekap per jam":
    st.subheader("Rekap Volume per Jam")
    st.dataframe(rekap_jam, use_container_width=True)

elif pilihan == "Rekap per arah":
    st.subheader("Rekap Volume per Arah")
    st.dataframe(rekap_arah, use_container_width=True)

elif pilihan == "Persentase jenis kendaraan":
    st.subheader("Persentase Jenis Kendaraan")
    st.dataframe(
        persentase.rename("Persentase (%)").to_frame(),
        use_container_width=True
    )

else:
    st.subheader("Data Lengkap")
    st.dataframe(hasil, use_container_width=True)

st.divider()

# Grafik volume gabungan
st.subheader("Grafik Volume Lalu Lintas Gabungan")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(rekap_jam["jam"], rekap_jam["total"], marker="o")
ax.set_xlabel("Jam")
ax.set_ylabel("Kendaraan per jam")
ax.set_xticks(range(24))
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# Grafik per arah
st.subheader("Perbandingan Arah Utara dan Selatan")

pivot = hasil.pivot(
    index="jam",
    columns="arah",
    values="total"
).sort_index()

fig2, ax2 = plt.subplots(figsize=(10, 4))

for arah in ["Utara", "Selatan"]:
    ax2.plot(
        pivot.index,
        pivot[arah],
        marker="o",
        label=arah
    )

ax2.set_xlabel("Jam")
ax2.set_ylabel("Kendaraan per jam")
ax2.set_xticks(range(24))
ax2.grid(True, alpha=0.3)
ax2.legend()
st.pyplot(fig2)

# Tombol unduh CSV
st.subheader("Unduh Data Hasil")

csv_data = hasil.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="Unduh data lengkap (CSV)",
    data=csv_data,
    file_name="data_volume_lalu_lintas.csv",
    mime="text/csv"
)

st.success("Analisis volume lalu lintas berhasil ditampilkan.")
