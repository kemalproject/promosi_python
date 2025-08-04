import mysql.connector
from sklearn.cluster import KMeans
import numpy as np

def train_and_update_clusters():
    # Koneksi ke database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="promosi_db"
    )
    cursor = conn.cursor()

    # Ambil data yang akan digunakan untuk clustering
    cursor.execute("SELECT id_pelanggan, jumlah_transaksi, total_pengeluaran, rata_pengeluaran FROM pelanggan")
    rows = cursor.fetchall()

    if not rows:
        print("Tidak ada data pelanggan untuk dianalisis.")
        return

    ids = [row[0] for row in rows]
    data = [row[1:] for row in rows]  # Ambil kolom jumlah_transaksi, total_pengeluaran, rata_pengeluaran

    X = np.array(data)

    # Jalankan K-Means
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    kmeans.fit(X)
    labels = kmeans.labels_

    # Mapping label ke nama cluster yang lebih deskriptif
    label_mapping = {
        0: "VIP",
        1: "Reguler",
        2: "Pasif",
        3: "Potensial"
    }

    for i in range(len(ids)):
        cluster_name = label_mapping[labels[i]]
        cursor.execute("UPDATE pelanggan SET cluster = %s WHERE id_pelanggan = %s", (cluster_name, ids[i]))

    conn.commit()
    cursor.close()
    conn.close()
