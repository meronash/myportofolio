# Rona's Portofolio Website

Website portofolio pribadi berbasis Django yang dibangun bertahap sepanjang semester untuk mata kuliah Pemrograman Berbasis Platform, Fakultas Ilmu Komputer, Universitas Indonesia.

| | |
|---|---|
| Nama | Rona Mahira |
| NPM | 2506657314 |
| Kelas | PBP E |

## Daftar Isi

- [Deskripsi](#deskripsi)
- [Fitur](#fitur)
- [Teknologi](#teknologi)
- [Progres Mingguan](#progres-mingguan)
- [Peran dan Hak Akses](#peran-dan-hak-akses)
- [Pertanyaan Reflektif](#pertanyaan-reflektif)
- [Deklarasi Penggunaan AI](#deklarasi-penggunaan-ai)

## Deskripsi

Website ini menampilkan profil, skills, experience, education, dan projects secara dinamis. Halaman portofolio dapat dibaca siapa saja tanpa login. Tindakan yang mengubah data dibatasi berdasarkan peran pengguna, dan seluruh interaksi pada halaman Experience, Education, dan Projects berjalan tanpa reload melalui REST API.

## Fitur

**Konten**
1. Menampilkan profil pribadi, skills, dan social links
2. Menampilkan experience, riwayat pendidikan (education), dan projects
3. Responsive layout untuk desktop dan mobile

**Akun dan hak akses**
4. Register, login, dan logout memakai autentikasi bawaan Django
5. Cookie `last_login` yang dipasang saat login dan dihapus saat logout
6. Empat peran: pengunjung, pengguna biasa, editor, dan pemilik portofolio (superuser)
7. Fitur star pada experience, education, dan projects untuk pengguna yang sudah login

**Interaksi tanpa reload**
8. Menambah, mengubah, dan menghapus data experience, education, dan projects lewat modal
9. Pencarian dengan debouncing 300 ms (berdasarkan judul, atau nama institusi pada education)
10. Notifikasi toast untuk hasil sukses, galat validasi (400), dan penolakan (403)

**API dan keamanan**
11. REST API dengan Django REST Framework di `/api/v1/`
12. Validasi input di serializer dan pembersihan tag HTML dengan `strip_tags`
13. Hak akses diperiksa di server dengan permission class, bukan hanya dengan menyembunyikan tombol
14. Perlindungan CSRF pada setiap request yang mengubah data, dan escaping semua teks yang disisipkan ke HTML

## Teknologi

- Python dan Django
- Django REST Framework (`@api_view`, `SessionAuthentication`, permission class)
- SQLite untuk pengembangan lokal, WhiteNoise untuk berkas statis
- HTML, CSS, dan JavaScript (Fetch API, Popover API)

## Progres Mingguan

| Minggu | Topik | Yang dikerjakan |
|---|---|---|
| 1 | HTML dan CSS | Halaman profil dengan section Profile dan Skill-Experience, layout responsive |
| 2 | Django MVT | Proyek Django, model `Experience` dan `Education`, view, template, dan migrasi |
| 3 | Form dan JSON | `ModelForm` dengan validasi, form tambah dan hapus data, endpoint JSON |
| 4 | Autentikasi | Register, login, logout, cookie `last_login`, hak akses berdasarkan peran, dan star |
| 5 | JavaScript dan AJAX | `fetch()`, pencarian dengan debouncing, modal, toast, dan perlindungan XSS |
| 6 | Django REST Framework | Serializer, permission class, API view, halaman yang memakai API, dan test `APITestCase` |

## Peran dan Hak Akses

Aturan yang sama berlaku untuk halaman dan API pada ketiga modul (Projects, Experience, Education).

| Aksi | Pengunjung | Pengguna biasa | Editor | Pemilik (superuser) |
|---|---|---|---|---|
| Melihat daftar dan detail, mencari | ✅ | ✅ | ✅ | ✅ |
| Memberi atau membatalkan star | ❌ | ✅ | ✅ | ✅ |
| Mengubah data (PUT, PATCH) | ❌ | ❌ | ✅ | ✅ |
| Menambah data (POST) | ❌ | ❌ | ❌ | ✅ |
| Menghapus data (DELETE) | ❌ | ❌ | ❌ | ✅ |

## Pertanyaan Reflektif

### Tugas 1
1. Ya, saya menggunakan section dalam merancang struktur HTML. Penggunaan section membantu saya membagi halaman web menjadi beberapa bagian (untuk saat ini masih 2 bagian), yaitu Profile dan Skill-Experience. Selain itu, styling menggunakan CSS menjadi lebih mudah karena pembagian halaman web tersebut.
2. Tantangan yang saya temukan adalah menyusun layout Skill-Experience yang berupa dua kolom dalam desktop menjadi satu kolom dalam mobile. Karena kedua elemen tersebut tingkat kepentingannya sama, maka saya memilih elemen paling kanan untuk diubah posisinya menjadi di bawah elemen yang lebih kiri (Experience di bawah Skill) dalam tampilan mobile. Untuk ukuran tidak ada prioritas, saya mengubah keduanya sama besar.
3. Batasan yang saya rasakan adalah informasi pada website masih bersifat statis dan ditulis langsung pada HTML. Pada iterasi berikutnya, saya ingin menambahkan fitur dinamis seperti pop up untuk menampilkan informasi dan fitur scrolling pada frame (misal frame Skill dan Experience) agar halaman web tidak terlalu panjang.

### Tugas 2
1. Ketika user membuka halaman education, browser mengirimkan request ke URL `/education/`. Request tersebut akan diterima oleh `urls.py` pada level proyek yang menggunakan `include("main.urls")` untuk meneruskan request ke `main/urls.py`. `main/urls.py` kemudian mencocokkan URL `/education/` dengan `show_education` dan meneruskan ke view `show_education`. View ini kemudian mengambil data dari model dan memasukkan context dengan nama `education_list`. Setelah itu, view meneruskan context tersebut ke template `education.html`. Template akan menampilkan pesan kondisi kosong jika tidak ada data, sedangkan jika ada akan menampilkan data tersebut pada halaman. Setelah template selesai dirender menjadi HTML, Django mengirimkan respons tersebut ke browser untuk ditampilkan kepada pengguna.
2. Dengan menyimpan data pada model, informasi seperti institusi, deskripsi, dan waktu pendidikan dapat dikelola melalui database tanpa harus mengubah kode HTML (hard code). Hal ini membuat pemeliharaan aplikasi lebih mudah karena perubahan atau penambahan data tidak mengharuskan mengubah template.
3. `makemigrations` untuk membuat berkas migrasi yang mencatat perubahan pada model yang belum diterapkan ke database. Sementara `migrate` digunakan untuk menerapkan perubahan yang terdapat pada berkas migrasi ke database.

### Tugas 3
1. Penggunaan `ModelForm` memungkinkan Django membuat form berdasarkan model yang telah didefinisikan. Dengan begitu tidak perlu membuat setiap input HTML dan proses validasinya secara manual. `ModelForm` juga membantu memastikan data yang dimasukkan sesuai dengan field dan aturan yang telah ditentukan pada model. `{% csrf_token %}` digunakan untuk memberikan CSRF protection pada form, sehingga dapat dipastikan request yang melakukan perubahan data berasal dari form yang dibuat oleh aplikasi kita. Dengan demikian, aplikasi akan mencegah request palsu dari pihak lain yang mencoba melakukan aksi menggunakan sesi pengguna.
2. JSON lebih banyak digunakan karena formatnya lebih sederhana dan ringan dibanding XML. Struktur JSON menggunakan pasangan key-value dan array sehingga lebih mudah dibaca dan diproses oleh aplikasi.
3. Client mengirimkan request ke URL API yang sudah diarahkan ke view `get_projects_json` > View mengambil data dari database > Data masih berupa object Django dalam bentuk QuerySet > Data diubah menjadi format JSON > Data JSON dikembalikan sebagai respons > Client menerima respons tersebut dan dapat menggunakan data project dalam format JSON.

### Tugas 4

### Tugas 5
1. Debouncing adalah teknik yang digunakan untuk menunda eksekusi sebuah fungsi sampai jeda waktu tertentu telah berakhir sejak terakhir kali fungsi tersebut dipanggil. Pentingnya dalam penggunaan AJAX adalah untuk mencegah terjadinya overloading pada server, menghemat bandwidth, serta memberikan user experience yang lebih baik.
2. `fetch()` bekerja secara asinkronus dan mengembalikan sebuah Promise, dan `await` digunakan untuk menunggu sampai Promise tersebut selesai sebelum kode melanjutkan ke baris berikutnya. Jika tidak menggunakan `await`, `fetch()` yang bersifat asinkronus tadi akan langsung mengembalikan objek Promise yang berstatus pending dan bukan data respons yang sebenarnya. Program akan langsung mengeksekusi baris kode berikutnya sebelum jaringan selesai mengunduh data JSON, yang berujung pada error atau data gagal dirender.
3. XSS adalah kerentanan keamanan di mana penyerang dapat menyuntikkan skrip berbahaya ke dalam halaman web yang dilihat oleh pengguna lain. Skrip ini dapat mencuri cookie, token sesi, atau membajak akun pengguna. Serangan XSS pada AJAX dan JavaScript lebih rentan daripada Django Template karena browser mengeksekusi string HTML secara mentah tanpa pengamanan otomatis. Sedangkan template Django secara default melakukan escaping terhadap variabel yang ditampilkan menggunakan `{{ variabel }}`.

### Tugas 6
1. REST adalah gaya arsitektur di mana data dipandang sebagai resource dengan alamat sendiri (misalnya /api/v1/experience/<id>/) yang dimanipulasi lewat method HTTP standar (GET, POST, PUT, PATCH, DELETE), bersifat stateless, dan melaporkan hasil lewat status HTTP yang tepat (201, 400, 403, 404, 204). JSON saja belum cukup karena JSON hanya format data. Pada Tugas 5, view delete_experience_ajax memakai POST untuk menghapus, sehingga aksinya ditentukan oleh nama view, bukan method HTTP. Versi RESTful-nya adalah DELETE /api/v1/experience/<id>/ dengan hasil 204. PUT mengganti seluruh resource sehingga semua field wajib dikirim, cocok untuk form edit yang mengirim semua isian. PATCH hanya mengubah field yang dikirim, cocok untuk perubahan kecil seperti mengisi ended_at ketika sebuah pengalaman selesai.
2. Serializer menerjemahkan objek model menjadi data JSON (serialisasi) dan data JSON dari client menjadi data tervalidasi yang dapat disimpan (deserialisasi lewat is_valid() dan save()). Pada proyek ini serializer mendeklarasikan fields secara eksplisit, field hasil perhitungan yang read-only (star_count, is_starred), validasi validate_<field> dengan strip_tags, dan validasi tanggal di validate(). Dibandingkan JsonResponse manual pada Tutorial 05, validasi dan bentuk output berada di satu tempat (sebelumnya terpisah di ModelForm dan get_*_json), konversi tipe berjalan otomatis, field read-only dan daftar fields eksplisit mencegah pemalsuan star_count atau kebocoran data akun, format galat 400 konsisten, dan satu serializer dipakai ulang untuk list, detail, create, dan update.
3. Autentikasi menjawab "siapa kamu?" dan dilakukan oleh SessionAuthentication, yang membaca cookie sessionid lalu mengisi request.user. Otorisasi menjawab "boleh melakukan apa?" dan dilakukan oleh permission class: IsPortfolioOwnerOrEditorOrReadOnly (baca untuk semua, PUT dan PATCH untuk Editor dan superuser, POST dan DELETE untuk superuser) serta IsAuthenticated untuk star. Permission yang gagal menghasilkan 403. Pemeriksaan harus di server karena menyembunyikan tombol hanya mengubah tampilan, sedangkan siapa pun dapat menjalankan fetch(url, { method: 'DELETE' }) dari Console. Pada test, pengguna biasa dan Editor yang mencoba menghapus mendapat 403 dan barisnya tetap ada di database.
4. Pada SessionAuthentication, browser otomatis menyertakan cookie sessionid ke setiap request ke domain yang sama, termasuk yang dipicu situs lain, sehingga penyerang dapat mengirim DELETE memakai sesi korban (CSRF). Karena itu DRF mewajibkan token dari cookie csrftoken pada header X-CSRFToken untuk POST, PUT, PATCH, dan DELETE, dan situs lain tidak dapat membacanya (Same-Origin Policy). force_authenticate tidak cukup karena menyisipkan user langsung dan melewati SessionAuthentication, tempat pemeriksaan CSRF berjalan, sehingga test tetap lulus walaupun proteksi CSRF mati. Karena itu saya memakai APIClient(enforce_csrf_checks=True) dan .login() untuk membuktikan request tanpa token ditolak 403.

## Deklarasi Penggunaan AI

### Tugas 1 sampai 5

**Alat:** ChatGPT.

**Strategi prompting:** Saya memberikan potongan kode dan permasalahan yang muncul. AI kemudian breakdown permasalahan tersebut dan saya mengevaluasi kembali output yang diberikan.

| Tugas | Penggunaan AI |
|---|---|
| 1 | Menjelaskan fungsi syntax HTML dan CSS; membantu debugging CSS, seperti memperbaiki hover pada Skill dan Experience; membantu menyelesaikan masalah terkait GitHub |
| 2 | Menjelaskan lebih lanjut mengenai MVT; membantu debugging; membantu menyelesaikan masalah terkait GitHub |
| 3 | Menjelaskan lebih lanjut mengenai ModelForm pada Django; membantu debugging; membantu menyelesaikan masalah desain CSS |
| 4 | Menjelaskan lebih lanjut mengenai autentikasi pada Django; membantu debugging; membantu menyelesaikan masalah desain CSS |
| 5 | Menjelaskan lebih lanjut mengenai AJAX, debouncing, fetch API, dan perlindungan dari XSS; membantu debugging; membantu menyelesaikan masalah desain CSS |

### Tugas 6

**Alat:** Claude.

**Bagian yang dibantu AI:**
1. Merangkum PDF Tutorial 07 dan instruksi Tugas 6 menjadi daftar langkah pengerjaan.
2. Meninjau dan memperbaiki `serializers.py`: base class bersama untuk field star dan validasi tanggal, serta `validate_<field>` dengan `strip_tags`.
3. Meninjau `api_views.py` dan `api_urls.py`, termasuk menemukan tiga bug (dua `@permission_classes` yang bertumpuk, pencarian Education yang memakai field `title` yang tidak ada, dan star Education yang mencari di model Experience).
4. Membantu menyesuaikan template dan JavaScript halaman Projects, Experience, dan Education: `fetch()` ke `/api/v1/`, modal update dengan PATCH, modal konfirmasi hapus, toast, dan pengiriman `ended_at` sebagai `null`.

**Strategi prompting:**
- Mengunggah PDF tugas dan tutorial sebagai konteks, lalu meminta penjelasan atau daftar langkah.
- Menempelkan kode utuh (`serializers.py`, `api_views.py`, template, `models.py`, `forms.py`, `views.py`) dan meminta pemeriksaan "sudah benar atau belum".
- Menempelkan keluaran `python manage.py test` dan meminta analisis penyebab kegagalan.
- Membatasi cakupan jawaban ("jangan kerjakan yang belum saya minta") dan mengoreksi asumsi AI.
- Menjalankan sendiri semua kode dan test, karena AI tidak dapat menjalankan proyek ini.