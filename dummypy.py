# ===== CELL 1: Import Libraries =====
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

print("Libraries berhasil diimport!")

# ===== CELL 2: Load Data =====
# Membaca file CSV
file_path = 'Rata-Rata Upah_Gaji Bersih Sebulan Buruh_Karyawan_Pegawai Menurut Pendidikan Tertinggi yang Ditamatkan dan Lapangan Pekerjaan Utama di 17 Sektor, 2024.csv'

# Membaca dengan header yang kompleks
df_raw = pd.read_csv(file_path, header=None)

print("Data berhasil dimuat!")
print(f"Shape data: {df_raw.shape}")
print("\nPreview 5 baris pertama:")
print(df_raw.head())

# ===== CELL 3: Eksplorasi Struktur Data =====
print("=== EKSPLORASI STRUKTUR DATA ===")
print(f"Jumlah baris: {df_raw.shape[0]}")
print(f"Jumlah kolom: {df_raw.shape[1]}")
print("\nTipe data:")
print(df_raw.dtypes.value_counts())

# Melihat beberapa baris pertama untuk memahami struktur
print("\n10 baris pertama:")
for i in range(min(10, len(df_raw))):
    print(f"Baris {i}: {df_raw.iloc[i, 0] if pd.notna(df_raw.iloc[i, 0]) else 'NaN'}")

# ===== CELL 4: Identifikasi Header dan Data =====
print("=== IDENTIFIKASI HEADER DAN DATA ===")

# Mencari baris yang berisi nama sektor (biasanya di baris ke-2 atau ke-3)
header_row = None
data_start_row = None

for i in range(len(df_raw)):
    if pd.notna(df_raw.iloc[i, 1]) and "Pertanian" in str(df_raw.iloc[i, 1]):
        header_row = i
        print(f"Header ditemukan di baris: {i}")
        break

# Mencari baris mulai data (biasanya setelah header tahun/periode)
for i in range(header_row + 1 if header_row else 0, len(df_raw)):
    if pd.notna(df_raw.iloc[i, 0]) and any(keyword in str(df_raw.iloc[i, 0]).lower() 
                                          for keyword in ['tidak', 'sekolah', 'diploma', 'universitas']):
        data_start_row = i
        print(f"Data mulai di baris: {i}")
        break

print(f"\nHeader row: {header_row}")
print(f"Data start row: {data_start_row}")

# ===== CELL 4: Identifikasi Header dan Data =====
print("=== IDENTIFIKASI HEADER DAN DATA ===")

# Mencari baris yang berisi nama sektor (biasanya di baris ke-2 atau ke-3)
header_row = None
data_start_row = None

for i in range(len(df_raw)):
    if pd.notna(df_raw.iloc[i, 1]) and "Pertanian" in str(df_raw.iloc[i, 1]):
        header_row = i
        print(f"Header ditemukan di baris: {i}")
        break

# Mencari baris mulai data (biasanya setelah header tahun/periode)
for i in range(header_row + 1 if header_row else 0, len(df_raw)):
    if pd.notna(df_raw.iloc[i, 0]) and any(keyword in str(df_raw.iloc[i, 0]).lower() 
                                          for keyword in ['tidak', 'sekolah', 'diploma', 'universitas']):
        data_start_row = i
        print(f"Data mulai di baris: {i}")
        break

print(f"\nHeader row: {header_row}")
print(f"Data start row: {data_start_row}")

# ===== CELL 5: Ekstrak Header Sektor =====
print("=== EKSTRAK HEADER SEKTOR ===")

# Ekstrak nama-nama sektor dari header
sectors = []
if header_row is not None:
    header_data = df_raw.iloc[header_row].values
    for i, val in enumerate(header_data):
        if pd.notna(val) and i > 0:  # Skip kolom pertama (pendidikan)
            sector_name = str(val).strip()
            if sector_name and sector_name not in ['Rata', '2024', 'Februari', 'Agustus', 'Tahunan']:
                sectors.append(sector_name)

print(f"Sektor yang ditemukan ({len(sectors)}):")
for i, sector in enumerate(sectors, 1):
    print(f"{i}. {sector}")

# ===== CELL 6: Ekstrak Data Pendidikan dan Gaji =====
print("=== EKSTRAK DATA PENDIDIKAN DAN GAJI ===")

# Ekstrak level pendidikan
education_levels = []
if data_start_row is not None:
    for i in range(data_start_row, len(df_raw)):
        education = df_raw.iloc[i, 0]
        if pd.notna(education):
            education_str = str(education).strip()
            if education_str and education_str != 'Rata-Rata':  # Skip baris rata-rata
                education_levels.append(education_str)

print(f"Level pendidikan yang ditemukan ({len(education_levels)}):")
for i, edu in enumerate(education_levels, 1):
    print(f"{i}. {edu}")

# ===== CELL 7: Struktur Data untuk Transformasi =====
print("=== PERSIAPAN TRANSFORMASI DATA ===")

# Menentukan posisi kolom untuk setiap sektor
# Setiap sektor memiliki 3 kolom (Februari, Agustus, Tahunan)
sector_columns = {}
col_start = 1  # Mulai dari kolom ke-1 (setelah kolom pendidikan)

for i, sector in enumerate(sectors):
    sector_columns[sector] = {
        'februari': col_start + (i * 3),
        'agustus': col_start + (i * 3) + 1,
        'tahunan': col_start + (i * 3) + 2
    }

print("Mapping kolom per sektor:")
for sector, cols in list(sector_columns.items())[:3]:  # Tampilkan 3 pertama sebagai contoh
    print(f"{sector}: Februari={cols['februari']}, Agustus={cols['agustus']}, Tahunan={cols['tahunan']}")
print("...")

# ===== CELL 8: Buat DataFrame Terstruktur =====
print("=== MEMBUAT DATAFRAME TERSTRUKTUR ===")

# Buat list untuk menyimpan data yang sudah dibersihkan
cleaned_data = []

# Ekstrak data untuk setiap kombinasi pendidikan dan sektor
if data_start_row is not None:
    for i in range(data_start_row, len(df_raw)):
        education = df_raw.iloc[i, 0]
        if pd.notna(education):
            education_str = str(education).strip()
            if education_str and education_str != 'Rata-Rata':
                
                # Untuk setiap sektor, ambil data gaji
                for sector, cols in sector_columns.items():
                    try:
                        # Ambil data Februari dan Agustus (kita akan fokus pada data aktual)
                        gaji_feb = df_raw.iloc[i, cols['februari']] if cols['februari'] < df_raw.shape[1] else np.nan
                        gaji_aug = df_raw.iloc[i, cols['agustus']] if cols['agustus'] < df_raw.shape[1] else np.nan
                        
                        # Konversi ke float jika memungkinkan
                        if pd.notna(gaji_feb) and str(gaji_feb) != '-':
                            try:
                                gaji_feb = float(str(gaji_feb).replace(',', ''))
                                cleaned_data.append({
                                    'pendidikan': education_str,
                                    'sektor': sector,
                                    'periode': 'Februari',
                                    'gaji': gaji_feb
                                })
                            except:
                                pass
                        
                        if pd.notna(gaji_aug) and str(gaji_aug) != '-':
                            try:
                                gaji_aug = float(str(gaji_aug).replace(',', ''))
                                cleaned_data.append({
                                    'pendidikan': education_str,
                                    'sektor': sector,
                                    'periode': 'Agustus',
                                    'gaji': gaji_aug
                                })
                            except:
                                pass
                                
                    except Exception as e:
                        continue

# Buat DataFrame dari data yang sudah dibersihkan
df_clean = pd.DataFrame(cleaned_data)

print(f"Data berhasil dibersihkan!")
print(f"Shape data bersih: {df_clean.shape}")
print(f"Jumlah records: {len(df_clean)}")

# ===== CELL 9: Eksplorasi Data Bersih =====
print("=== EKSPLORASI DATA BERSIH ===")

print("Info DataFrame:")
print(df_clean.info())

print(f"\nJumlah data per pendidikan:")
print(df_clean['pendidikan'].value_counts())

print(f"\nJumlah data per sektor:")
print(df_clean['sektor'].value_counts())

print(f"\nJumlah data per periode:")
print(df_clean['periode'].value_counts())

print(f"\nStatistik gaji:")
print(df_clean['gaji'].describe())

# ===== CELL 10: Pembersihan Data Lanjutan =====
print("=== PEMBERSIHAN DATA LANJUTAN ===")

# Cek missing values
print("Missing values:")
print(df_clean.isnull().sum())

# Cek dan hapus duplikat
print(f"\nJumlah duplikat: {df_clean.duplicated().sum()}")
df_clean = df_clean.drop_duplicates()

# Cek outliers menggunakan IQR
Q1 = df_clean['gaji'].quantile(0.25)
Q3 = df_clean['gaji'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"\nOutlier detection (IQR method):")
print(f"Q1: {Q1:,.2f}")
print(f"Q3: {Q3:,.2f}")
print(f"IQR: {IQR:,.2f}")
print(f"Lower bound: {lower_bound:,.2f}")
print(f"Upper bound: {upper_bound:,.2f}")

outliers = df_clean[(df_clean['gaji'] < lower_bound) | (df_clean['gaji'] > upper_bound)]
print(f"Jumlah outliers: {len(outliers)}")

# Tampilkan beberapa outliers
if len(outliers) > 0:
    print("\nContoh outliers:")
    print(outliers.head())

# ===== CELL 11: Encoding Variabel Kategorikal =====
print("=== ENCODING VARIABEL KATEGORIKAL ===")

# Buat copy untuk encoding
df_encoded = df_clean.copy()

# Label encoding untuk pendidikan (berdasarkan tingkat pendidikan)
education_mapping = {
    'Tidak/Belum Pernah Sekolah': 0,
    'Tidak/Belum Tamat SD': 1,
    'Sekolah Dasar': 2,
    'Sekolah Menegah Pertama': 3,
    'Sekolah Menengah Atas (Umum)': 4,
    'Sekolah Menengah Atas (Kejuruan)': 5,
    'Diploma I/II/III/Akademi': 6,
    'Universitas': 7
}

df_encoded['pendidikan_encoded'] = df_encoded['pendidikan'].map(education_mapping)

# One-hot encoding untuk sektor
sektor_dummies = pd.get_dummies(df_encoded['sektor'], prefix='sektor')
df_encoded = pd.concat([df_encoded, sektor_dummies], axis=1)

# Encoding untuk periode
periode_mapping = {'Februari': 0, 'Agustus': 1}
df_encoded['periode_encoded'] = df_encoded['periode'].map(periode_mapping)

print("Encoding selesai!")
print(f"Shape data setelah encoding: {df_encoded.shape}")

# Tampilkan mapping pendidikan
print("\nMapping pendidikan:")
for edu, code in education_mapping.items():
    print(f"{code}: {edu}")

# ===== CELL 12: Agregasi Data (Rata-rata per Pendidikan-Sektor) =====
print("=== AGREGASI DATA ===")

# Buat dataset agregat untuk modeling (rata-rata gaji per pendidikan-sektor)
df_agg = df_clean.groupby(['pendidikan', 'sektor'])['gaji'].agg(['mean', 'count']).reset_index()
df_agg.columns = ['pendidikan', 'sektor', 'gaji_rata', 'jumlah_data']

# Tambahkan encoding
df_agg['pendidikan_encoded'] = df_agg['pendidikan'].map(education_mapping)

# One-hot encoding untuk sektor di data agregat
sektor_dummies_agg = pd.get_dummies(df_agg['sektor'], prefix='sektor')
df_final = pd.concat([df_agg, sektor_dummies_agg], axis=1)

print(f"Data agregat berhasil dibuat!")
print(f"Shape data agregat: {df_final.shape}")
print(f"Jumlah kombinasi pendidikan-sektor: {len(df_final)}")

print("\nContoh data agregat:")
print(df_final.head())

# ===== CELL 13: Simpan Data Bersih =====
print("=== MENYIMPAN DATA BERSIH ===")

# Simpan data mentah yang sudah dibersihkan
df_clean.to_csv('data_gaji_clean.csv', index=False)
print("✓ Data mentah bersih disimpan: data_gaji_clean.csv")

# Simpan data dengan encoding lengkap
df_encoded.to_csv('data_gaji_encoded.csv', index=False)
print("✓ Data dengan encoding disimpan: data_gaji_encoded.csv")

# Simpan data agregat untuk modeling
df_final.to_csv('data_gaji_final.csv', index=False)
print("✓ Data final untuk modeling disimpan: data_gaji_final.csv")

print("\n=== RINGKASAN PREPROCESSING ===")
print(f"📊 Data asli: {df_raw.shape}")
print(f"🧹 Data bersih: {df_clean.shape}")
print(f"🔢 Data encoded: {df_encoded.shape}")
print(f"📈 Data final: {df_final.shape}")
print(f"🎯 Siap untuk tahap modeling!")# ===== CELL 13: Simpan Data Bersih =====
print("=== MENYIMPAN DATA BERSIH ===")

# Simpan data mentah yang sudah dibersihkan
df_clean.to_csv('data_gaji_clean.csv', index=False)
print("✓ Data mentah bersih disimpan: data_gaji_clean.csv")

# Simpan data dengan encoding lengkap
df_encoded.to_csv('data_gaji_encoded.csv', index=False)
print("✓ Data dengan encoding disimpan: data_gaji_encoded.csv")

# Simpan data agregat untuk modeling
df_final.to_csv('data_gaji_final.csv', index=False)
print("✓ Data final untuk modeling disimpan: data_gaji_final.csv")

print("\n=== RINGKASAN PREPROCESSING ===")
print(f"📊 Data asli: {df_raw.shape}")
print(f"🧹 Data bersih: {df_clean.shape}")
print(f"🔢 Data encoded: {df_encoded.shape}")
print(f"📈 Data final: {df_final.shape}")
print(f"🎯 Siap untuk tahap modeling!")