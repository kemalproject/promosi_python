from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
import psycopg2.extras
import pandas as pd
from trainingmodel import train_and_update_clusters
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'rahasia'

# Koneksi langsung ke Supabase PostgreSQL
conn = psycopg2.connect(
    host="db.ptjkotzvwejydrlxibcd.supabase.co",
    database="postgres",
    user="postgres",
    password="123456",  # Ganti ini
    port=5432
)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# ========== ROUTING ==========

# Login page
@app.route('/')
def login():
    return render_template('login.html')

# Proses login
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        session['user'] = user['username']
        session['role'] = user.get('role', 'admin')
        return redirect('/dashboard')
    else:
        return redirect('/')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    cursor.execute("SELECT COUNT(*) AS transaksi FROM transaksi")
    transaksi = cursor.fetchone()['transaksi']

    cursor.execute("SELECT COUNT(*) AS pelanggan FROM pelanggan")
    pelanggan = cursor.fetchone()['pelanggan']

    cursor.execute("SELECT COUNT(*) AS vip FROM pelanggan WHERE cluster = 'VIP'")
    vip = cursor.fetchone()['vip']

    cursor.execute("SELECT COUNT(*) AS reguler FROM pelanggan WHERE cluster = 'Reguler'")
    reguler = cursor.fetchone()['reguler']

    cursor.execute("SELECT COUNT(*) AS pasif FROM pelanggan WHERE cluster = 'Pasif'")
    pasif = cursor.fetchone()['pasif']

    cursor.execute("SELECT COUNT(*) AS potensial FROM pelanggan WHERE cluster = 'Potensial'")
    potensial = cursor.fetchone()['potensial']

    cursor.execute("SELECT COUNT(*) AS produk FROM produk")
    produk = cursor.fetchone()['produk']

    return render_template('dashboard.html',
        user=session['user'],
        transaksi=transaksi,
        pelanggan=pelanggan,
        vip=vip,
        reguler=reguler,
        pasif=pasif,
        potensial=potensial,
        produk=produk
    )

# Data Pelanggan
@app.route('/data-pelanggan')
def data_pelanggan():
    conn = psycopg2.connect(
        host='db.ptjkotzvwejydrlxibcd.supabase.co',
        user='postgres',
        password='123456',
        database='postgres'
    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("SELECT * FROM pelanggan")
    pelanggan = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('data_pelanggan.html', pelanggan=pelanggan)

# Analisis Cluster
@app.route('/analisis_cluster')
def analisis_cluster():
    train_and_update_clusters()  # Panggil KMeans dari trainingmodel.py

    # Koneksi ke DB
    conn = psycopg2.connect(
        host='db.ptjkotzvwejydrlxibcd.supabase.co',
        user='postgres',
        password='123456',
        database='postgres'
    )
    cursor = conn.cursor()

    # Ambil jumlah per cluster
    cursor.execute("SELECT cluster, COUNT(*) FROM pelanggan GROUP BY cluster")
    results = cursor.fetchall()

    data_cluster = {}
    for cluster, count in results:
        # Pastikan cluster berupa string
        cluster_str = "null" if cluster is None else str(cluster)
        try:
            count_int = int(count)
        except:
            count_int = 0
        data_cluster[cluster_str] = count_int

    cursor.close()
    conn.close()

    # Debug (boleh kamu hapus nanti)
    import json
    print("data_cluster:", data_cluster)
    print("JSON check:", json.dumps(data_cluster))

    cluster_data = [
    {"cluster": k, "jumlah": v}
    for k, v in data_cluster.items()
]

    return render_template("analisis_cluster.html", cluster_data=cluster_data)
# Kirim Promosi
@app.route('/kirim_promosi')
def kirim_promosi():
    if 'user' not in session:
        return redirect('/')

    cursor.execute("SELECT * FROM pelanggan WHERE cluster = 'VIP' AND nomor_hp IS NOT NULL")
    vip = cursor.fetchall()

    cursor.execute("SELECT * FROM pelanggan WHERE cluster = 'Reguler' AND nomor_hp IS NOT NULL")
    reguler = cursor.fetchall()

    cursor.execute("SELECT * FROM pelanggan WHERE cluster = 'Pasif' AND nomor_hp IS NOT NULL")
    pasif = cursor.fetchall()

    cursor.execute("SELECT * FROM pelanggan WHERE cluster = 'Potensial' AND nomor_hp IS NOT NULL")
    potensial = cursor.fetchall()

    return render_template(
        'kirim_promosi.html',
        vip=vip,
        reguler=reguler,
        pasif=pasif,
        potensial=potensial
    )
@app.route('/proses_kirim_promosi', methods=['POST'])
def proses_kirim_promosi():
    if 'user' not in session:
        return redirect('/')

    cluster = request.form.get('cluster')
    jenis_promosi = request.form.get('jenis_promosi', 'Umum')

    # Ambil data pelanggan cluster
    cursor.execute("""
        SELECT nama, nomor_hp FROM pelanggan
        WHERE cluster = %s AND nomor_hp IS NOT NULL
    """, (cluster,))
    data = cursor.fetchall()

    for row in data:
        cursor.execute("""
            INSERT INTO laporan_promosi (nama_pelanggan, nomor_hp, cluster, waktu_kirim, jenis_promosi)
            VALUES (%s, %s, %s, NOW(), %s)
        """, (row['nama'], row['nomor_hp'], cluster, jenis_promosi))

    conn.commit()
    return redirect(url_for('laporan_promosi'))


@app.route('/data-barang')
def data_barang():
    if 'user' not in session:
        return redirect('/')

    cursor.execute("SELECT * FROM barang")
    data = cursor.fetchall()

    return render_template('data_barang.html', data=data)


@app.route('/tambah_barang', methods=['POST'])
def tambah_barang():
    if 'user' not in session:
        return redirect('/')

    nama = request.form['nama']
    kategori = request.form['kategori']
    stok = request.form['stok']
    harga = request.form['harga']

    cursor.execute("""
        INSERT INTO barang (nama_barang, kategori, stok, harga_satuan)
        VALUES (%s, %s, %s, %s)
    """, (nama, kategori, stok, harga))
    conn.commit()

    return redirect(url_for('data_barang'))

@app.route('/tambah_pelanggan', methods=['POST'])
def tambah_pelanggan():
    # Ambil data dari form
    nama = request.form['nama']
    nomor_hp = request.form['nomor_hp']
    nominal = request.form['nominal']
    tanggal = request.form['tanggal']
    jumlah_transaksi = request.form['jumlah']

    # Hitung rata-rata dan total pengeluaran dari nominal dan jumlah transaksi
    try:
        total_pengeluaran = int(nominal)
        jumlah_transaksi = int(jumlah_transaksi)
        rata_pengeluaran = total_pengeluaran // jumlah_transaksi if jumlah_transaksi else 0
    except:
        total_pengeluaran = 0
        rata_pengeluaran = 0

    # Simpan ke database
    conn = psycopg2.connect(
        host='db.ptjkotzvwejydrlxibcd.supabase.co',
        user='postgres',
        password='123456',
        database='postgres'
    )
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pelanggan (nama, nomor_hp, jumlah_transaksi, total_pengeluaran, rata_pengeluaran, terakhir_belanja)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nama, nomor_hp, jumlah_transaksi, total_pengeluaran, rata_pengeluaran, tanggal))

    conn.commit()
    cursor.close()
    conn.close()

    # Proses clustering (jika kamu sudah buat fungsinya di trainingmodel.py)
    try:
        import trainingmodel
        trainingmodel.proses_cluster()
    except Exception as e:
        print(f"Gagal menjalankan clustering: {e}")

    return redirect(url_for('data_pelanggan'))


# ==============================

if __name__ == '__main__':
    app.run(debug=True)