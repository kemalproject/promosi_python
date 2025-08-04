DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `role` varchar(50) DEFAULT 'admin',
  PRIMARY KEY (`id`)
);
INSERT INTO `users` VALUES
(1,'admin','admin123','admin');


DROP TABLE IF EXISTS `pelanggan`;
CREATE TABLE `pelanggan` (
  `id_pelanggan` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) DEFAULT NULL,
  `nomor_hp` varchar(20) DEFAULT NULL,
  `jumlah_transaksi` int(11) DEFAULT NULL,
  `total_pengeluaran` int(11) DEFAULT NULL,
  `rata_pengeluaran` int(11) DEFAULT NULL,
  `terakhir_belanja` date DEFAULT NULL,
  `cluster` varchar(50) DEFAULT NULL,
  `alamat` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_pelanggan`)
);

INSERT INTO `pelanggan` (`id_pelanggan`, `nama`, `nomor_hp`, `jumlah_transaksi`, `total_pengeluaran`, `rata_pengeluaran`, `terakhir_belanja`, `cluster`, `alamat`) VALUES
(1,'anon','08978657422',15,0,0,'2025-05-21','Pasif',NULL),
(10,'Bulin','0816 1722 4972',20,2280360,114018,'2025-03-20','VIP',NULL),
(100,'Adel','0888 8755 6329',6,568272,94712,'2025-03-07','Pasif',NULL),
(101,'Icha','0856 0329 1423',22,4291496,195068,'2025-03-17','Potensial',NULL),
(102,'Icha','0856 0329 1423',38,7495158,197241,'2025-04-18','Reguler',NULL),
(103,'Windy','0856 9267 8469',40,7030760,175769,'2025-02-16','Reguler',NULL),
(104,'Empilk &','0888 6136 1925',2,389494,194747,'2025-03-23','Pasif',NULL),
(105,'Bpk Emplok','0887 929 306',49,9635458,196642,'2025-04-28','Reguler',NULL),
(106,'Kemal','085217853508',40,6208960,155224,'2025-04-09','Reguler',NULL),
(107,'Amak Asep FF','7901005766',27,2250855,83365,'2025-04-19','VIP',NULL),
(108,'Bu Hilda','536111973531',46,6810898,148063,'2025-03-08','Reguler',NULL),
(109,'Kemal','085217853508',10,158630,15863,'2025-04-17','Pasif',NULL),
(11,'P. Aji','0821 2231 6325',31,3096094,99874,'2025-03-23','VIP',NULL),
(110,'Keman','0821 3781 308',16,1005376,62836,'2025-04-26','Pasif',NULL),
(111,'Kemal','085217853508',49,3028886,61814,'2025-03-11','VIP',NULL),
(112,'Empilk &','0888 6136 1925',14,1241450,88675,'2025-03-04','Pasif',NULL),
(113,'Kemal','085217853508',40,6245680,156142,'2025-03-03','Reguler',NULL),
(114,'Windy','0856 9267 8469',18,1739394,96633,'2025-03-27','VIP',NULL),
(115,'Ibu Melly','53611193740',33,2015442,61074,'2025-02-05','VIP',NULL),
(116,'P. Agil','0821 2316 625',36,6645852,184607,'2025-02-25','Reguler',NULL),
(117,'Bulin','0816 1722 4972',22,3064776,139308,'2025-04-13','VIP',NULL),
(118,'Emplok A','0888 6166 1925',23,3306802,143774,'2025-04-22','Potensial',NULL),
(119,'Windy','0856 9267 8469',12,967308,80609,'2025-03-17','Pasif',NULL),
(12,'Empilk Toko','450 4603 3200',8,354800,44350,'2025-04-19','Pasif',NULL),
(120,'Bu Hilda','536111973531',21,3357669,159889,'2025-03-14','Potensial',NULL);



-- Tabel: produk
DROP TABLE IF EXISTS `produk`;
CREATE TABLE `produk` (
  `id_produk` int(11) NOT NULL AUTO_INCREMENT,
  `nama_produk` varchar(100),
  `kategori` varchar(50),
  `harga` int(11),
  PRIMARY KEY (`id_produk`)
);
INSERT INTO `produk` VALUES
(1,'Teh Botol','Minuman',3000),
(2,'Indomie','Makanan',2500),
(3,'Roti','Makanan',5000);

-- Tabel: barang
DROP TABLE IF EXISTS `barang`;
CREATE TABLE `barang` (
  `id_produk` int(11) NOT NULL AUTO_INCREMENT,
  `nama_barang` varchar(100),
  `kategori` varchar(50),
  `stok` int(11),
  `harga_satuan` int(11),
  PRIMARY KEY (`id_produk`)
);
INSERT INTO `barang` VALUES
(1,'mie','makanan',1,5000),
(2,'kopi','minuman',60,2500);

-- Tabel: transaksi
DROP TABLE IF EXISTS `transaksi`;
CREATE TABLE `transaksi` (
  `id_transaksi` int(11) NOT NULL AUTO_INCREMENT,
  `id_pelanggan` int(11),
  `id_produk` int(11),
  `jumlah` int(11),
  `total_harga` int(11),
  `tanggal` date,
  PRIMARY KEY (`id_transaksi`)
);
INSERT INTO `transaksi` VALUES
(1,1,1,2,10000,'2023-06-10'),
(2,2,2,1,2500,'2023-06-11');

-- Tabel: laporan_promosi
DROP TABLE IF EXISTS `laporan_promosi`;
CREATE TABLE `laporan_promosi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_pelanggan` varchar(100),
  `nomor_hp` varchar(20),
  `cluster` varchar(50),
  `waktu_kirim` datetime,
  `jenis_promosi` varchar(100),
  PRIMARY KEY (`id`)
);
INSERT INTO `laporan_promosi` VALUES
(1,'Asep','08123456789','VIP','2023-06-30 09:00:00','Diskon'),
(2,'Budi','08987654321','Reguler','2023-06-30 10:00:00','Voucher');
