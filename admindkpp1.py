import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime

st.title("Workflow TPD - Simulasi Proses SIM TPD - Penunjukkan Majelis TPD")

# Sidebar menu
menu = ["Admin DKPP", "Kabag", "Kasubag", "Pimpinan", "Majelis TPD", "Sekretaris", "Staf DKPP", "Drafter TA"]
choice = st.sidebar.selectbox("Pilih Menu", menu, format_func=lambda x: x.replace("DKPP", "**DKPP**").replace("TPD", "**TPD**"))

# Initialize Excel file and load data
excel_file = "data_majelis_tpd.xlsx"

def load_data():
    """Load data from Excel file with proper column initialization"""
    columns = ["No", "Nomor Registrasi", "Nomor Pengaduan", "Nomor Perkara", 
               "Nama Pengadu", "Nama Teradu", "Majelis TPD", "Jadwal Sidang", 
               "Lokasi Sidang", "Status", "Pilih", "Notifikasi", "Terima", "SuratPenolakan", "SK_Downloaded", "Skor Kinerja", "Resume_Filename"]
    
    if os.path.exists(excel_file):
        try:
            df = pd.read_excel(excel_file)
            for col in columns:
                if col not in df.columns:
                    if col in ["Pilih", "Notifikasi", "Terima", "SK_Downloaded"]:
                        df[col] = False
                    elif col == "Skor Kinerja":
                        df[col] = None
                    elif col == "Resume_Filename":
                        df[col] = ""
                    else:
                        df[col] = ""
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return pd.DataFrame(columns=columns)
    else:
        return pd.DataFrame(columns=columns)

def save_data(df):
    """Save dataframe to Excel file"""
    try:
        df.to_excel(excel_file, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

# Load all data
all_data = load_data()

# Enhanced CSS for better UI/UX
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f5;
        padding: 20px;
        border-radius: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
    }
    .stButton>button {
        background-color: #1e90ff;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #104e8b;
    }
    .table-container {
        overflow-x: auto;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 15px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        table-layout: auto;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 0;
    }
    th {
        background-color: #1e90ff;
        color: white;
        font-weight: bold;
        position: sticky;
        top: 0;
    }
    .stTextInput > div > div > input {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 8px;
    }
    .large-message {
        font-size: 24px;
        font-weight: bold;
        color: #2e7d32;
        text-align: center;
        margin-top: 20px;
        padding: 10px;
        background-color: #e8f5e9;
        border-radius: 5px;
    }
    .stSuccess {
        background-color: #e8f5e9;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for messages and archived state
if "message" not in st.session_state:
    st.session_state.message = ""
if "archived" not in st.session_state:
    st.session_state.archived = {}

# Admin DKPP section
if choice == "Admin DKPP":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Semua Data Terkini")
    with col2:
        if st.button("Reset Data Excel"):
            if not all_data.empty:
                last_data = all_data[all_data["No"] == all_data["No"].max()].copy()
                all_data = last_data
                if save_data(all_data):
                    st.session_state.message = "Data Excel telah direset, hanya data terakhir yang disimpan."
                    st.rerun()
            else:
                st.warning("Tidak ada data untuk direset.")
    
    if not all_data.empty:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        display_cols = ["No", "Nomor Registrasi", "Nomor Pengaduan", "Nomor Perkara", 
                       "Nama Pengadu", "Nama Teradu", "Majelis TPD", "Jadwal Sidang", 
                       "Lokasi Sidang", "Status"]
        st.table(all_data[display_cols].style.set_properties(**{'max-width': '200px', 'word-wrap': 'break-word'}))
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("Tidak ada data tersedia.")

    # Input form
    majelis_input = st.text_input("Masukkan Nama Majelis TPD (pisahkan dengan koma jika lebih dari satu)", "")
    
    if st.button("Simpan"):
        if majelis_input:
            majelis_list = [name.strip() for name in majelis_input.split(",")]
            
            # Generate unique numbers
            def generate_unique_number(prefix, existing_numbers, length=3):
                while True:
                    random_num = random.randint(100, 999)  # Generate a 3-digit random number
                    new_number = f"{prefix}{random_num}"
                    if new_number not in existing_numbers:
                        return new_number
            
            existing_registrasi = all_data["Nomor Registrasi"].dropna().tolist()
            existing_pengaduan = all_data["Nomor Pengaduan"].dropna().tolist()
            existing_perkara = all_data["Nomor Perkara"].dropna().tolist()
            
            nomor_registrasi = generate_unique_number("150/02-07/SET-02/V/2025-", existing_registrasi)
            nomor_pengaduan = generate_unique_number("171-P/L-DKPP/V/2025-", existing_pengaduan)
            nomor_perkara = generate_unique_number("137 – PKE – DKPP/IV/2025-", existing_perkara)
            
            new_data = {
                "No": int(all_data["No"].max()) + 1 if not all_data.empty and not all_data["No"].isna().all() else 1,
                "Nomor Registrasi": nomor_registrasi,
                "Nomor Pengaduan": nomor_pengaduan,
                "Nomor Perkara": nomor_perkara,
                "Nama Pengadu": "Supriadi Lawani",
                "Nama Teradu": "Santo Gotia, Hidayat Hilengo",
                "Majelis TPD": ", ".join(majelis_list),
                "Jadwal Sidang": "28 Juni 2026",
                "Lokasi Sidang": "Bandung",
                "Status": "Menunggu Verifikasi Kabag",
                "Pilih": False,
                "Notifikasi": False,
                "Terima": False,
                "SuratPenolakan": "",
                "SK_Downloaded": False,
                "Skor Kinerja": None,
                "Resume_Filename": ""
            }
            
            new_df = pd.DataFrame([new_data])
            all_data = pd.concat([all_data, new_df], ignore_index=True)
            
            if save_data(all_data):
                st.session_state.message = "Data berhasil disimpan ke {}. Langkah selanjutnya: Data telah dikirim ke Kabag untuk verifikasi.".format(excel_file)
                st.rerun()
        else:
            st.error("Mohon masukkan setidaknya satu nama Majelis TPD.")

    if st.session_state.message:
        st.success(st.session_state.message)
        st.session_state.message = ""

    st.subheader("Data yang Telah Disetujui oleh Pimpinan")
    approved_data = all_data[all_data["Status"] == "Disetujui"].copy()
    
    if not approved_data.empty:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        updated_data = approved_data.copy()
        selected_indices = []
        
        for i, (idx, row) in enumerate(approved_data.iterrows()):
            checked = st.checkbox(
                f"Notifikasi ke Majelis TPD untuk No {row['No']}", 
                key=f"notif_{row['No']}", 
                value=bool(row["Notifikasi"])
            )
            if checked:
                selected_indices.append(idx)
            updated_data.loc[idx, "Notifikasi"] = checked
        
        if st.button("Kirim Notifikasi"):
            if selected_indices:
                all_data.loc[selected_indices, "Notifikasi"] = True
                if save_data(all_data):
                    st.session_state.message = "Notifikasi telah dikirim ke Majelis TPD untuk data terpilih. Langkah selanjutnya: Tunggu keputusan dari Majelis TPD."
                    st.rerun()
            else:
                st.warning("Pilih setidaknya satu data untuk mengirim notifikasi.")
        
        display_cols = ["No", "Nomor Registrasi", "Nomor Pengaduan", "Nomor Perkara", 
                       "Nama Pengadu", "Nama Teradu", "Majelis TPD", "Jadwal Sidang", 
                       "Lokasi Sidang", "Status", "Notifikasi"]
        st.table(approved_data[display_cols].style.set_properties(**{'max-width': '200px', 'word-wrap': 'break-word'}))
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("Tidak ada data yang telah disetujui.")

    st.subheader("Data Majelis dengan SK Penunjukkan yang Sudah Diunduh")
    sk_downloaded_data = all_data[all_data["SK_Downloaded"] == True].copy()
    if not sk_downloaded_data.empty:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        selected_indices = []
        for i, (idx, row) in enumerate(sk_downloaded_data.iterrows()):
            checked = st.checkbox(f"Kirim SK untuk No {row['No']}", key=f"send_sk_{row['No']}")
            if checked:
                selected_indices.append(idx)
        
        if st.button("Kirim SK Penunjukkan Ke Majelis TPD"):
            if selected_indices:
                messages = []
                for idx in selected_indices:
                    all_data.loc[idx, "Status"] = "SK Terkirim ke Majelis TPD"
                    messages.append(f"SK Penunjukkan No {all_data.loc[idx, 'No']} telah dikirim ke Majelis DKPP bersangkutan.")
                if save_data(all_data):
                    st.session_state.message = "\n".join(messages)
                    st.rerun()
            else:
                st.warning("Pilih setidaknya satu data untuk mengirim SK Penunjukkan.")
        
        display_cols = ["No", "Nomor Registrasi", "Nomor Pengaduan", "Nomor Perkara", 
                       "Nama Pengadu", "Nama Teradu", "Majelis TPD", "Jadwal Sidang", 
                       "Lokasi Sidang", "Status", "SK_Downloaded"]
        st.table(sk_downloaded_data[display_cols].style.set_properties(**{'max-width': '200px', 'word-wrap': 'break-word'}))
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("Tidak ada data dengan SK Penunjukkan yang sudah diunduh.")

    st.subheader("Kirim Notifikasi 'Sidang Selesai' Silahkan Upload Resume Max 2 hari setelah sidang")
    eligible_data = all_data[all_data["Status"].isin(["Disetujui", "SK Terkirim ke Majelis TPD"])].copy()
    if not eligible_data.empty:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        selected_indices = []
        for i, (idx, row) in enumerate(eligible_data.iterrows()):
            if not row["Notifikasi"]:  # Only show unchecked data for notification
                checked = st.checkbox(
                    f"Kirim Notifikasi 'Sidang Selesai' untuk No {row['No']}", 
                    key=f"sidang_notif_{row['No']}",
                    value=False
                )
                if checked:
                    selected_indices.append(idx)
        
        if st.button("Kirim Notifikasi Sidang Selesai"):
            if selected_indices:
                all_data.loc[selected_indices, "Notifikasi"] = True
                if save_data(all_data):
                    st.session_state.message = "Notifikasi Sidang Selesai telah terkirim ke Majelis TPD."
                    st.rerun()
            else:
                st.warning("Pilih setidaknya satu data untuk mengirim notifikasi.")
        
        display_cols = ["No", "Nomor Registrasi", "Nomor Pengaduan", "Nomor Perkara", 
                       "Nama Pengadu", "Nama Teradu", "Majelis TPD", "Jadwal Sidang", 
                       "Lokasi Sidang", "Status", "Notifikasi"]
        st.table(eligible_data[display_cols].style.set_properties(**{'max-width': '200px', 'word-wrap': 'break-word'}))
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("Tidak ada data yang memenuhi syarat untuk notifikasi 'Sidang Selesai'.")

# Kabag section
elif choice == "Kabag":
    df = load_data()
    st.subheader("Data untuk Verifikasi")
    new_data = df[df["Status"] == "Menunggu Verifikasi Kabag"].sort_values("No", ascending=False).head(1)
    
    if not new_data.empty:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        selected_indices = []
        for i, (idx, row) in enumerate(new_data.iterrows()):
            checked = st.checkbox(f"Pilih Data No {row['No']}", key=f"kabag_{row['No']}")
            if checked:
                selected_indices.append(idx)
        
        if st.button("Verifikasi Terpilih"):
            if selected_indices:
                df.loc[selected_indices, "Status"] = "Terverifikasi Kabag"
                df.loc[selected_indices, "Pilih"] = False
                if save_data(df):
                    st.session_state.message = "Data terpilih telah diverifikasi dan status diubah ke 'Terverifikasi Kabag'. Langkah selanjutnya: Data siap diproses oleh Kasubag."
                    st.rerun()
            else:
                st.warning("Pilih setidaknya satu data untuk diverifikasi.")
        
        display_cols = ["No", "Nomor Registrasi", "Nomor Pengaduan", "Nomor Perkara", 
                       "Nama Pengadu", "Nama Teradu", "Majelis TPD", "Jadwal Sidang", 
                       "Lokasi Sidang", "Status"]
        st.table(new_data[display_cols].style.set_properties(**{'max-width': '200px', 'word-wrap': 'break-word'}))
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Tidak ada data yang menunggu verifikasi.")
    
    st.info("Langkah selanjutnya: Data yang diverifikasi siap diproses oleh Kasubag.")
    if st.session_state.message:
        st.success(st.session_state.message)
        st.session_state.message = ""

# Kasubag section
elif choice == "Kasubag":
    df = load_data()
    st.subheader("Data untuk Diproses")
    new_data = df[df["Status"] == "Terverifikasi Kabag"].sort_values("No", ascending=False).head(1)
    
    if not new_data.empty:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        selected_indices = []
        for i, (idx, row) in enumerate(new_data.iterrows()):
            checked = st.checkbox(f"Pilih Data No {row['No']}", key=f"kasubag_{row['No']}")
            if checked:
                selected_indices.append(idx)
        
        if st.button("Proses dan Kirim ke Pimpinan"):
            if selected_indices:
                df.loc[selected_indices, "Status"] = "Menunggu Approval Pimpinan"
                df.loc[selected_indices, "Waktu Proses"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                df.loc[selected_indices, "Pilih"] = False
                if save_data(df):
                    st.session_state.message = "Data terpilih telah diproses dan dikirim ke Pimpinan untuk approval. Langkah selanjutnya: Tunggu approval dari Pimpinan."
                    st.rerun()
            else:
                st.warning("Pilih setidaknya satu data untuk diproses.")
        
        display_cols = ["No", "Nomor Registrasi", "Nomor Pengaduan", "Nomor Perkara", 
                       "Nama Pengadu", "Nama Teradu", "Majelis TPD", "Jadwal Sidang", 
                       "Lokasi Sidang", "Status"]
        st.table(new_data[display_cols].style.set_properties(**{'max-width': '200px', 'word-wrap': 'break-word'}))
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Tidak ada data yang siap diproses.")
    
    st.info("Langkah selanjutnya: Data telah dikirim ke Pimpinan untuk approval.")
    if st.session_state.message:
        st.success(st.session_state.message)
        st.session_state.message = ""

# Pimpinan section
elif choice == "Pimpinan":
    df = load_data()
    st.subheader("Data untuk Approval")
    new_data = df[df["Status"] == "Menunggu Approval Pimpinan"].sort_values("No", ascending=False).head(1)
    
    if not new_data.empty:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        selected_indices = []
        for i, (idx, row) in enumerate(new_data.iterrows()):
            checked = st.checkbox(f"Pilih Data No {row['No']}", key=f"pimpinan_{row['No']}")
            if checked:
                selected_indices.append(idx)
        
        if st.button("Setujui"):
            if selected_indices:
                df.loc[selected_indices, "Status"] = "Disetujui"
                df.loc[selected_indices, "Waktu Approval"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                df.loc[selected_indices, "Pilih"] = False
                if save_data(df):
                    st.session_state.message = "Data terpilih telah disetujui. Langkah selanjutnya: Data siap untuk notifikasi ke Majelis TPD."
                    st.rerun()
            else:
                st.warning("Pilih setidaknya satu data untuk disetujui.")
        
        display_cols = ["No", "Nomor Registrasi", "Nomor Pengaduan", "Nomor Perkara", 
                       "Nama Pengadu", "Nama Teradu", "Majelis TPD", "Jadwal Sidang", 
                       "Lokasi Sidang", "Status"]
        st.table(new_data[display_cols].style.set_properties(**{'max-width': '200px', 'word-wrap': 'break-word'}))
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Tidak ada data yang menunggu approval.")
    
    st.info("Langkah selanjutnya: Proses selesai setelah approval.")
    if st.session_state.message:
        st.success(st.session_state.message)
        st.session_state.message = ""

    st.subheader("Data Kinerja Majelis TPD")
    performance_data = df[df["SK_Downloaded"] == True].copy()
    if not performance_data.empty:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        display_cols = ["No", "Nomor Registrasi", "Nomor Pengaduan", "Nomor Perkara", 
                       "Nama Pengadu", "Nama Teradu", "Majelis TPD", "Jadwal Sidang", 
                       "Lokasi Sidang", "Status", "SK_Downloaded", "Skor Kinerja"]
        st.table(performance_data[display_cols].style.set_properties(**{'max-width': '200px', 'word-wrap': 'break-word'}))
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("Tidak ada data dengan SK Downloaded True.")

# Majelis TPD section
elif choice == "Majelis TPD":
    df = load_data()
    st.subheader("Notifikasi dari Admin DKPP (Data Terakhir)")
    notified_data = df[df["Notifikasi"] == True].sort_values("No", ascending=False).head(1)
    
    if not notified_data.empty:
        for idx, row in notified_data.iterrows():
            st.write(f"**Notifikasi: Sidang Telah Selesai untuk Nomor Perkara {row['Nomor Perkara']}**")
        for i, (idx, row) in enumerate(notified_data.iterrows()):
            st.write(f"**Data No {row['No']}**")
            col1, col2 = st.columns(2)
            
            with col1:
                decision = st.radio(
                    "Pilih Aksi", 
                    ["Terima", "Tolak"], 
                    key=f"decision_{row['No']}", 
                    index=0 if row["Terima"] else 1 if row["SuratPenolakan"] else 0
                )
            
            with col2:
                if decision == "Terima":
                    notified_data.loc[idx, "Terima"] = True
                    notified_data.loc[idx, "SuratPenolakan"] = ""
                elif decision == "Tolak":
                    notified_data.loc[idx, "Terima"] = False
                    surat_penolakan = (
                        f"\\documentclass{{article}}\n"
                        f"\\usepackage[utf8]{{inputenc}}\n"
                        f"\\usepackage[a4paper, margin=1in]{{geometry}}\n"
                        f"\\usepackage{{times}}\n"
                        f"\\begin{{document}}\n"
                        f"\\section{{Surat Pernyataan Penolakan}}\n"
                        f"\\noindent Kepada Yth. Admin DKPP\\\\\n"
                        f"Tempat\\\\\n"
                        f"Tanggal: {datetime.now().strftime('%d %B %Y')}\n"
                        f"\\vspace{{1cm}}\n"
                        f"\\noindent Dengan hormat,\n"
                        f"\\vspace{{0.5cm}}\n"
                        f"\\noindent Saya, {row['Majelis TPD']}, dengan ini menyatakan penolakan untuk ditunjuk sebagai Majelis TPD "
                        f"untuk perkara dengan Nomor Perkara {row['Nomor Perkara']} karena alasan pribadi. "
                        f"Mohon untuk mempertimbangkan penunjukan lain.\n"
                        f"\\vspace{{1cm}}\n"
                        f"\\noindent Hormat saya,\n"
                        f"\\vspace{{1cm}}\n"
                        f"\\noindent {row['Majelis TPD']}\n"
                        f"\\end{{document}}"
                    )
                    notified_data.loc[idx, "SuratPenolakan"] = surat_penolakan
        
        if st.button("Simpan Keputusan"):
            for idx, row in notified_data.iterrows():
                df.loc[idx] = row
            
            if save_data(df):
                st.session_state.message = "Keputusan telah disimpan. Langkah selanjutnya: Jika 'Terima', lanjut ke Sekretaris untuk SK Penunjukkan; jika 'Tolak', notifikasi akan dikirim ke Admin DKPP."
                st.rerun()
        
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        display_cols = ["No", "Nomor Registrasi", "Nomor Pengaduan", "Nomor Perkara", 
                       "Nama Pengadu", "Nama Teradu", "Majelis TPD", "Jadwal Sidang", 
                       "Lokasi Sidang", "Status", "Notifikasi", "Terima"]
        st.table(notified_data[display_cols].style.set_properties(**{'max-width': '200px', 'word-wrap': 'break-word'}))
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader("Upload Resume Sidang")
    if not notified_data.empty:
        nomor_perkara = notified_data["Nomor Perkara"].iloc[0]
        uploaded_file = st.file_uploader(f"Unggah Resume Sidang untuk Nomor Perkara {nomor_perkara} (PDF atau DOCX)", type=["pdf", "docx"], key="resume_upload")
        if uploaded_file is not None:
            if st.button("Simpan Resume"):
                file_path = os.path.join(os.getcwd(), uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                idx = notified_data.index[0]
                all_data.loc[idx, "Resume_Filename"] = uploaded_file.name
                if save_data(all_data):
                    st.session_state.message = f"Resume {uploaded_file.name} berhasil diunggah untuk Nomor Perkara {nomor_perkara}."
                    st.rerun()
    else:
        st.write("Tidak ada sidang yang telah selesai untuk diunggah resume-nya.")
    
    st.info("Pilih 'Terima' untuk melanjutkan ke SK Penunjukkan oleh Sekretaris, atau 'Tolak' untuk mengirim surat penolakan.")
    if st.session_state.message:
        st.success(st.session_state.message)
        st.session_state.message = ""

# Sekretaris section
elif choice == "Sekretaris":
    df = load_data()
    st.subheader("Data yang Diterima oleh Majelis TPD")
    accepted_data = df[df["Terima"] == True].copy()
    
    if not accepted_data.empty:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        
        for idx, row in accepted_data.iterrows():
            st.write(f"**Data No {row['No']}**")
            sk_penunjukkan = (
                f"\\documentclass{{article}}\n"
                f"\\usepackage[utf8]{{inputenc}}\n"
                f"\\usepackage[a4paper, margin=1in]{{geometry}}\n"
                f"\\usepackage{{times}}\n"
                f"\\begin{{document}}\n"
                f"\\section{{Surat Keputusan Penunjukkan Majelis TPD}}\n"
                f"\\noindent Nomor: SK/TPD/{row['No']}/{datetime.now().strftime('%m')}/{datetime.now().strftime('%Y')}\n"
                f"\\vspace{{1cm}}\n"
                f"\\noindent Dengan ini menyatakan bahwa {row['Majelis TPD']} ditunjuk sebagai Majelis TPD "
                f"untuk perkara dengan Nomor Perkara {row['Nomor Perkara']} yang akan dilaksanakan pada "
                f"{row['Jadwal Sidang']} di {row['Lokasi Sidang']}.\n"
                f"\\vspace{{1cm}}\n"
                f"\\noindent Ditandatangani,\n"
                f"\\vspace{{1cm}}\n"
                f"\\noindent Sekretaris DKPP\n"
                f"\\end{{document}}"
            )
            
            if st.download_button(
                label=f"Unduh SK Penunjukkan No {row['No']}",
                data=sk_penunjukkan,
                file_name=f"SK_Penunjukkan_No{row['No']}.tex",
                key=f"download_{row['No']}"
            ):
                df.loc[idx, "SK_Downloaded"] = True
                save_data(df)
        
        display_cols = ["No", "Nomor Registrasi", "Nomor Pengaduan", "Nomor Perkara", 
                       "Nama Pengadu", "Nama Teradu", "Majelis TPD", "Jadwal Sidang", 
                       "Lokasi Sidang", "Status", "Terima", "SK_Downloaded"]
        st.table(accepted_data[display_cols].style.set_properties(**{'max-width': '200px', 'word-wrap': 'break-word'}))
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Tidak ada data yang diterima oleh Majelis TPD.")
    
    st.info("Klik 'Unduh SK Penunjukkan' untuk menghasilkan dokumen LaTeX yang dapat diproses via Srikandi.")
    if st.session_state.message:
        st.success(st.session_state.message)
        st.session_state.message = ""

# Staf DKPP section
elif choice == "Staf DKPP":
    df = load_data()
    st.subheader("Data Majelis TPD dengan SK Terkirim")
    filtered_data = df[(df["Status"] == "SK Terkirim ke Majelis TPD") & (df["SK_Downloaded"] == True)].copy()
    
    if not filtered_data.empty:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        selected_indices = []
        for i, (idx, row) in enumerate(filtered_data.iterrows()):
            checked = st.checkbox(f"Nilai Kinerja untuk No {row['No']}", key=f"eval_{row['No']}")
            if checked:
                selected_indices.append(idx)
        
        display_cols = ["No", "Nomor Registrasi", "Nomor Pengaduan", "Nomor Perkara", 
                       "Nama Pengadu", "Nama Teradu", "Majelis TPD", "Jadwal Sidang", 
                       "Lokasi Sidang", "Status", "SK_Downloaded"]
        st.table(filtered_data[display_cols].style.set_properties(**{'max-width': '200px', 'word-wrap': 'break-word'}))
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Tidak ada data dengan status SK Terkirim dan SK Downloaded True.")
    
    evaluate = st.radio("Apakah akan menilai kinerja Majelis DKPP?", ("Tidak", "Ya"), key="evaluate")
    
    if evaluate == "Ya" and selected_indices:
        st.subheader("Formulir Penilaian Kinerja Majelis DKPP")
        for idx in selected_indices:
            row = filtered_data.loc[idx]
            st.write(f"**Penilaian untuk No {row['No']} - {row['Majelis TPD']}**")
            
            indicator1 = st.number_input("Indikator 1: Ketepatan Waktu", min_value=0.0, max_value=5.0, step=0.5, key=f"ind1_{idx}")
            indicator2 = st.number_input("Indikator 2: Kepatuhan Aturan", min_value=0.0, max_value=5.0, step=0.5, key=f"ind2_{idx}")
            indicator3 = st.number_input("Indikator 3: Kualitas Keputusan", min_value=0.0, max_value=5.0, step=0.5, key=f"ind3_{idx}")
            indicator4 = st.number_input("Indikator 4: Kerjasama Tim", min_value=0.0, max_value=5.0, step=0.5, key=f"ind4_{idx}")
            indicator5 = st.number_input("Indikator 5: Komunikasi", min_value=0.0, max_value=5.0, step=0.5, key=f"ind5_{idx}")
            indicator6 = st.number_input("Indikator 6: Integritas", min_value=0.0, max_value=5.0, step=0.5, key=f"ind6_{idx}")
            indicator7 = st.number_input("Indikator 7: Efisiensi", min_value=0.0, max_value=5.0, step=0.5, key=f"ind7_{idx}")
            indicator8 = st.number_input("Indikator 8: Inisiatif", min_value=0.0, max_value=5.0, step=0.5, key=f"ind8_{idx}")
            indicator9 = st.number_input("Indikator 9: Penyelesaian Masalah", min_value=0.0, max_value=5.0, step=0.5, key=f"ind9_{idx}")
            indicator10 = st.number_input("Indikator 10: Dokumentasi", min_value=0.0, max_value=5.0, step=0.5, key=f"ind10_{idx}")
            indicator11 = st.number_input("Indikator 11: Kepemimpinan", min_value=0.0, max_value=5.0, step=0.5, key=f"ind11_{idx}")
            indicator12 = st.number_input("Indikator 12: Etika Profesional", min_value=0.0, max_value=5.0, step=0.5, key=f"ind12_{idx}")
            
            if st.button("Simpan Penilaian", key=f"save_{idx}"):
                indicators = [indicator1, indicator2, indicator3, indicator4, indicator5, indicator6,
                             indicator7, indicator8, indicator9, indicator10, indicator11, indicator12]
                avg_score = sum(indicators) / len(indicators) if all(pd.notna(indicators)) else None
                
                evaluation = {
                    "Indikator 1": indicator1, "Indikator 2": indicator2, "Indikator 3": indicator3,
                    "Indikator 4": indicator4, "Indikator 5": indicator5, "Indikator 6": indicator6,
                    "Indikator 7": indicator7, "Indikator 8": indicator8, "Indikator 9": indicator9,
                    "Indikator 10": indicator10, "Indikator 11": indicator11, "Indikator 12": indicator12
                }
                df.loc[idx, "Penilaian_Kinerja"] = str(evaluation)
                df.loc[idx, "Skor Kinerja"] = avg_score
                if save_data(df):
                    st.session_state.message = f"Penilaian kinerja untuk No {row['No']} telah disimpan. Skor Kinerja: {avg_score if avg_score is not None else 'N/A'}."
                    st.rerun()
    
    if st.session_state.message:
        st.success(st.session_state.message)
        st.session_state.message = ""

# Drafter TA section
elif choice == "Drafter TA":
    df = load_data()
    st.subheader("Data dengan Resume Sidang yang Diunggah")
    resume_data = df[df["Resume_Filename"] != ""].copy()
    
    if not resume_data.empty:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        display_cols = ["No", "Nomor Registrasi", "Nomor Pengaduan", "Nomor Perkara", 
                       "Nama Pengadu", "Nama Teradu", "Majelis TPD", "Jadwal Sidang", 
                       "Lokasi Sidang", "Status", "Notifikasi", "Resume_Filename"]
        st.table(resume_data[display_cols].style.set_properties(**{'max-width': '200px', 'word-wrap': 'break-word'}))
        st.markdown('</div>', unsafe_allow_html=True)
        
        for idx, row in resume_data.iterrows():
            st.write(f"**Data No {row['No']} - Nomor Perkara {row['Nomor Perkara']}**")
            file_name = str(row["Resume_Filename"])
            if file_name:
                file_path = os.path.join(os.getcwd(), file_name)
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.download_button(label=f"Lihat PDF {file_name}", data=f, file_name=file_name, mime="application/pdf", key=f"view_pdf_{idx}")
                else:
                    st.warning(f"File {file_name} tidak ditemukan di direktori.")
            else:
                st.warning("Nama file resume tidak tersedia.")
            
            if st.button("Arsipkan", key=f"archive_{idx}"):
                st.session_state.archived[idx] = True
                st.rerun()
            
            if st.session_state.archived.get(idx, False):
                st.markdown('<div class="large-message">DATA MASUK PROSES SELANJUTNYA</div>', unsafe_allow_html=True)
    else:
        st.write("Tidak ada data dengan resume sidang yang diunggah.")

    st.info("Klik 'Arsipkan' untuk memproses data lebih lanjut.")
    if st.session_state.message:
        st.success(st.session_state.message)
        st.session_state.message = ""
