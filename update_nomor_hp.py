import pandas as pd
import mysql.connector

df = pd.read_csv("static/data_pelanggan.csv")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="promosi_db"
)
cursor = conn.cursor()

for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO pelanggan (id_pelanggan, nama, nomor_hp, jumlah_transaksi, total_pengeluaran, rata_pengeluaran, terakhir_belanja)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            nama = VALUES(nama),
            nomor_hp = VALUES(nomor_hp),
            jumlah_transaksi = VALUES(jumlah_transaksi),
            total_pengeluaran = VALUES(total_pengeluaran),
            rata_pengeluaran = VALUES(rata_pengeluaran),
            terakhir_belanja = VALUES(terakhir_belanja)
    """, (
        row['Id Pelanggan'],
        row['Nama Pelanggan'],
        row['Nomor HP'],
        row['jumlah_transaksi'],
        row['total_pengeluaran'],
        row['Rata-rata Pengeluaran'],
        row['Terakhir Belanja']
    ))

conn.commit()
cursor.close()
conn.close()
