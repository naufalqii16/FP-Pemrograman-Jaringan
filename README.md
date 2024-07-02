## Daftar Isi
<div align=justify>

- [i. Daftar Isi](#daftar-isi)
- [ii. Panduan Menjalankan Program](#panduan-menjalankan-program)
- [iii. Pembagian Tugas](#pembagian-tugas)
- [1. Definisi Protokol Chat](#definisi-protokol-chat)
  - [1.1. Private Messaging](#private-messaging)
  - [1.2. Group Messaging](#group-messaging)
  - [1.3. Send and Receive File](#send-and-receive-file)
- [2. Definisi Protokol Pertukaran Antar Server](#definisi-protokol-pertukaran-antar-server)
- [3. Arsitektur Implementasi](#arsitektur-implementasi)
  - [3.1. IP Address](#ip-address)
  - [3.2. Port dari Server](#port-dari-server)
  - [3.3. Bagaimana Menjalankan Server dan Client](#bagaimana-menjalankan-server-dan-client)
- [4. Uji Awal dari Komunikasi](#uji-awal-dari-komunikasi)

## Pembagian Tugas

| Nama  | NRP | Tugas |
| ------------- | ------------- | ------------- |
| Andika Laksana Putra  | 5025211001  | Backend  |
| M Naufal Baihaqi  | 5025211103  | Frontend  |
| Dewangga Dika Darmawan  | 502521109  | Frontend  |
| Kalyana Putri Al Kanza  | 5025211137  | Documentation, Integration  |
| Akmal Ariq Romadhon  | 5025211188  | Documentation, Integration  |
| Alfa Fakhrur Rizal Zaini  | 5025211214  | Backend  |

## Panduan Menjalankan Program

### Step 1
```python
pip install flet
```

### Step 2
masuk ke directory project lalu jalankan program
```python
flet run main.py
```

## Definisi Protokol Chat 

### **_Private Messaging_**

- #### **Autentikasi Pengguna (_Login_)**

Untuk mengirim dan menerima pesan pribadi, pengguna harus terautentikasi terlebih dahulu dengan menggunakan perintah `auth`, dengan protokol untuk autentikasi mencakup:

- _username_: Nama pengguna.
- _password_: Kata sandi pengguna.

Format pesan yang dikirim ke server untuk autentikasi adalah sebagai berikut:

```shell
auth {username} {password}
```

- #### **Pendaftaran Pengguna (_Register_)**

Pengguna baru dapat mendaftar dengan menggunakan perintah `register`. Saat mendaftar, protokol yang digunakan adalah sebagai berikut: 

- _username_: Nama pengguna yang akan didaftarkan.
- _password_: Kata sandi pengguna yang akan didaftarkan.
<!-- - realm_id: ID realm tempat pengguna akan terdaftar. -->

Format pesan yang dikirim ke server untuk pendaftaran adalah:

```shell
register {username} {password}
```

- #### **Pengiriman Pesan Pribadi (_Send Private Message_)**

Pesan pribadi dikirim dengan menggunakan perintah `sendprivate`, dengan protokol untuk mengirim pesan pribadi

<!-- - sessionid: ID sesi pengguna yang mengirim pesan. -->
- _usernameto_: Nama pengguna yang akan menerima pesan.
<!-- - usernamefrom: Nama pengguna yang mengirim pesan. -->
- _message_: Isi pesan yang dikirim.

Format pesan yang dikirim ke server untuk pengiriman pesan pribadi (_Private Message_) adalah:

```
sendprivate {usernameto} {message} 
```

- #### **Penerimaan Pesan Pribadi (_Receive Private Message)_**

Pengguna dapat mengambil pesan pribadi dengan menggunakan perintah `inbox`, dengan protokol yang digunakan untuk mengambil pesan pribadi mencakup:

<!-- - username: Nama pengguna yang meminta pesan. -->

Format pesan yang dikirim ke server untuk mengambil pesan pribadi adalah:

```shell
inbox 
```

### **_Group Messaging_**

- #### **Pembuatan Grup (_Create Group_)**

Grup baru dapat dibuat dengan menggunakan perintah `creategroup`. Protokol yang digunakan untuk membuat grup adalah:

- _groupname_: Nama grup yang akan dibuat.

Format pesan yang dikirim ke server untuk membuat grup adalah:

```shell
creategroup {groupname} 
```

- #### **Bergabung ke Grup (_Join Group_)**

Pengguna dapat bergabung ke grup dengan menggunakan perintah `joingroup` dan menggunakan Protokol sebagai berikut:

<!-- - username: Nama pengguna yang bergabung. -->
- _groupname_: Nama grup yang akan diikuti.
<!-- - realmid: ID realm di mana grup berada. -->

Format pesan yang dikirim ke server untuk bergabung ke grup adalah:

```shell
joingroup {groupname}
```

- #### **Pengiriman Pesan Grup (_Send Group Messages_)**

Pesan grup dikirim dengan menggunakan perintah `sendgroup`. Protokol yang digunakan untuk mengirim pesan grup adalah sebagai berikut:

- _groupto_: Nama grup yang akan menerima pesan.
- _message_: Isi pesan yang dikirim.

Format pesan yang dikirim ke server adalah:

```shell
sendgroup {groupto} {message} 
```

- #### **Penerimaan Pesan Grup (_Receive Group Messages_)**

Pengguna dapat mengambil pesan grup dengan menggunakan perintah `inboxgroup`. Protokol yang digunakan untuk 

- _groupname_: Nama grup dari mana pesan diambil.

Format pesan yang dikirim ke server untuk mengambil pesan grup adalah:

```shell
inboxgroup {groupname} 
```

### **File**
Pengguna dapat mengirim dan menerima file dengan menggunakan perintah `adios`. Format pesan yang dikirim ke server untuk mengirim dan menerima file adalah sebagai berikut:

- #### **Mengirim File (_Send File_)**

Pengguna dapat mengirim file ke private message menggunakan perintah `sendfile` dan menggunakan Protokol sebagai berikut:
- _usernameto_: Nama pengguna yang akan dikirimkan file.
- _PATH_: Lokasi atau directory dari _file_ yang dikirim.

Format pesan yang dikirim ke server untuk bergabung ke grup adalah:

```shell
sendfile {usernameto} {PATH}
```

- #### **Menerima File (_Receive File_)**

Pengguna dapat mengirim file ke private message menggunakan perintah `receivefile` dan menggunakan Protokol sebagai berikut:

```shell
receivefile
```
Format pesan yang dikirim ke server untuk bergabung ke grup adalah:

```shell
receivefile
``` 


## Definisi Protokol Pertukaran Antar Server
Pada arsitektur chat multi realm kami, terdapat 1 server utama yang menjadi
handler untuk keseluruhan operasi. Main server akan melakukan proses permintaan proses
yang diberikan oleh client. Server realm merupakan server yang menjadi handler untuk permintaan
user di realm, serta menjadi session handler dari setiap user yang terhubung dengan service 
utama. Setiap permintaan user akan melewati server realm sebelum dikirimkan ke server
utama untuk diproses. chat-cli merupakan service local yang terhubung dengan aplikasi frontend
untuk memproses permintaan user ke realm server.

## Arsitektur Implementasi
Berikut adalah arsitektur implementasi dari aplikasi yang dibuat untuk _final project_ dari kelompok kami (Kelompok 14)

### IP Address
Main Server: 192.168.xxx.xxx <br>
Realm Server: 192.168.xxx.xxx

### Port dari Server
_Main server_ memiliki nilai port 8080 untuk terhubung dengan server realm, realm server memiliki nilai port 8000 untuk terhubung dengan client.

### Bagaimana Menjalankan Server dan Client
Untuk menjalankan server, main server harus menyala dan siap menerima koneksi terlebih dahulu di port 8080. Sebelum client bisa berkomunikasi, realm server harus menyala terlebih dahulu. Pada port 8000 untuk terhubung dengan client. aplikasi frontend akan menggunakan service dari chat-cli untuk bisa berkomunikasi dengan realm server dan melakukan segala operasi chat.

## Uji Awal dari Komunikasi