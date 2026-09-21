# Rona's Portofolio Website

## About Me
Nama : Rona Mahira
NPM : 2506657314
Kelas : PBP E

## Deskripsi
Website portofolio pribadi berbasis Django untuk menampilkan profile, skills, experience, education, dan projects secara dinamis.

### Fitur
1. Menampilkan profil pribadi
2. Menampilkan skills
3. Menampilkan experience
4. Menampilkan riwayat pendidikan
5. Menampilkan projects
6. Menampilkan social links
7. Menambahkan, mengubah, dan menghapus data education dan projects
8. Fitur pencarian berdasarkan nama institusi dan nama project
9. Menyediakan data education dan projects dalam format JSON melalui API
10. Responsive layout untuk desktop dan mobile
11. Form dengan validasi menggunakan Django ModelForm 

## Pertanyaan Reflektif 1
1. Ya, saya menggunakan section dalam merancang struktur HTML. Penggunaan section membantu saya membagi halaman web menjadi beberapa bagian (untuk saat ini masih 2 bagian), yaitu Profile dan Skill-Experience. Selain itu, styling menggunakan CSS menjadi lebih mudah karena pembagian halaman web tersebut.
2. Tantangan yang saya temukan adalah menyusun layout Skill-Experience yang berupa dua kolom dalam desktop menjadi satu kolom dalam mobile. Karena kedua elemen tersebut tingkat kepentingannya sama, maka saya memilih elemen paling kanan untuk diubah posisinya menjadi di bawah elemen yang lebih kiri (Experience di bawah Skill) dalam tampilan mobile. Untuk ukuran tidak ada prioritas, saya mengubah keduanya sama besar.
3. Batasan yang saya rasakan adalah informasi pada website masih bersifat statis dan ditulis langsung pada HTML. Pada iterasi berikutnya, saya ingin menambahkan fitur dinamis seperti pop up untuk menampilkan informasi dan fitur scrolling pada frame (misal frame Skill dan Experience) agar halaman web tidak terlalu panjang.

## Deklarasi AI
Saya menggunakan ChatGPT untuk membantu pembuatan website portofolio ini dengan rincian sebagai berikut.

### Penggunaan AI
1. Menjelaskan fungsi syntax HTML dan CSS
2. Membantu debugging CSS, seperti memperbaiki hover pada Skill dan Experience
3. Membantu menyelesaikan masalah terkait GitHub

### Strategi Prompting
Saya memberikan potongan kode dan permasalahan yang muncul. AI kemudian breakdown permasalahan tersebut dan saya mengevaluasi kembali output yang diberikan. 

## Pertanyaan reflektif 2
1. Ketika user membuka halaman education, browser mengirimkan request ke URL /education/. Request tersebut akan diterima oleh urls.py pada level proyek yang menggunakan include("main.urls") untuk meneruskan request ke main/urls.py. main/urls.py kemudian mencocokkan URL /education/ dengan show_education dan meneruskan ke view show_education. View ini kemudian mengambil data dari model dan memasukkan context dengan nama education_list. Setelah itu, view meneruskan context tersebut ke template education.html. Template akan menampilkan pesan kondisi kosong jika tidak ada data, sedangkan jika ada akan menampilkan data tersebut pada halaman. Setelah template selesai dirender menjadi HTML, Django mengirimkan respons tersebut ke browser untuk ditampilkan kepada pengguna.
2. Dengan menyimpan data pada model, informasi seperti institusi, deskripsi, dan waktu pendidikan dapat dikelola melalui database tanpa harus mengubah kode HTML (hard code). Hal ini membuat pemeliharaan aplikasi lebih mudah karena perubahan atau penambahan data tidak mengharuskan mengubah template.
3. makemigrations untuk membuat berkas migrasi yang mencatat perubahan pada model yang belum diterapkan ke database. Sementara migrate digunakan untuk menerapkan perubahan yang terdapat pada berkas migrasi ke database.

## Deklarasi AI
Saya menggunakan ChatGPT untuk membantu pembuatan website portofolio ini dengan rincian sebagai berikut.

### Penggunaan AI
1. Menjelaskan lebih lanjut mengenai MVT
2. Membantu debugging
3. Membantu menyelesaikan masalah terkait GitHub

### Strategi Prompting
Saya memberikan potongan kode dan permasalahan yang muncul. AI kemudian breakdown permasalahan tersebut dan saya mengevaluasi kembali output yang diberikan. 

## Pertanyaan reflektif 3
1. Penggunaan ModelForm memungkinkan Django membuat form berdasarkan model yang telah didefinisikan. Dengan begitu tidak perlu membuat setiap input HTML dan proses validasinya secara manual. ModelForm juga membantu memastikan data yang dimasukkan sesuai dengan field dan aturan yang telah ditentukan pada model.
{% csrf_token %} digunakan untuk memberikan CSRF protection pada form, sehingga dapat dipastikan request yang melakukan perubahan data berasal dari form yang dibuat oleh aplikasi kita. Dengan demikian, aplikasi akan mencegah request palsu dari pihak lain yang mencoba melakukan aksi menggunakan sesi pengguna.
2. JSON lebih banyak digunakan karena formatnya lebih sederhana dan ringan dibanding XML. Struktur JSON menggunakan pasangan key-value dan array sehingga lebih mudah dibaca dan diproses oleh aplikasi.
3. Client mengirimkan request ke URL API yang sudah diarahkan ke view get_projects_json > View mengambil data dari database > Data masih berupa object Django dalam bentuk QuerySet > Data diubah menjadi forman JSON > Data JSON dikembalikan sebagai respons > Client menerima respons tersebut dan dapat menggunakan data project dalam format JSON.

## Deklarasi AI
Saya menggunakan ChatGPT untuk membantu pembuatan website portofolio ini dengan rincian sebagai berikut.

### Penggunaan AI
1. Menjelaskan lebih lanjut mengenai ModelForm pada Django
2. Membantu debugging
3. Membantu menyelesaikan masalah desain css

### Strategi Prompting
Saya memberikan potongan kode dan permasalahan yang muncul. AI kemudian breakdown permasalahan tersebut dan saya mengevaluasi kembali output yang diberikan. 