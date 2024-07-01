## Daftar Isi

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

## Pembagian Tugas

| Nama  | NRP | Tugas |
| ------------- | ------------- | ------------- |
| Andika Laksana Putra  | 5025211001  | Content Cell  |
| M Naufal Baihaqi  | 5025211103  | Content Cell  |
| Dewangga Dika Darmawan  | 502521109  | Content Cell  |
| Kalyana Putri Al Kanza  | 5025211137  | Content Cell  |
| Akmal Ariq Ramadhan  | 5025211188  | Content Cell  |
| Alfa Fakhrur Rizal Zaini  | 5025211214  | Content Cell  |

## Definisi Protokol Chat 

### Private Messaging

#### Autentikasi Pengguna

Untuk mengirim dan menerima pesan pribadi, pengguna harus terautentikasi terlebih dahulu dengan menggunakan perintah `auth`.

Protokol untuk autentikasi mencakup:

- username: Nama pengguna.
- password: Kata sandi pengguna.

Format pesan yang dikirim ke server untuk autentikasi adalah:

```shell
auth {username} {password}
```

#### Pendaftaran Pengguna

Pengguna baru dapat mendaftar dengan menggunakan perintah `register`.

Protokol untuk pendaftaran mencakup:

- username: Nama pengguna yang akan didaftarkan.
- password: Kata sandi pengguna yang akan didaftarkan.
<!-- - realm_id: ID realm tempat pengguna akan terdaftar. -->

Format pesan yang dikirim ke server untuk pendaftaran adalah:

```shell
register {username} {password}
```

#### Pengiriman Pesan Pribadi

Pesan pribadi dikirim dengan menggunakan perintah `sendprivate`.

Protokol untuk mengirim pesan pribadi mencakup:

<!-- - sessionid: ID sesi pengguna yang mengirim pesan. -->
- usernameto: Nama pengguna yang akan menerima pesan.
<!-- - usernamefrom: Nama pengguna yang mengirim pesan. -->
- message: Isi pesan yang dikirim.

Format pesan yang dikirim ke server adalah:

```
sendprivate {usernameto} {message} 
```

#### Penerimaan Pesan Pribadi

Pengguna dapat mengambil pesan pribadi dengan menggunakan perintah `inbox`.
<!-- 
Protokol untuk mengambil pesan pribadi mencakup:

- username: Nama pengguna yang meminta pesan. -->

Format pesan yang dikirim ke server untuk mengambil pesan pribadi adalah:

```shell
inbox 
```

### Group Messaging

#### Pembuatan Grup

Grup baru dapat dibuat dengan menggunakan perintah `creategroup`.

Protokol untuk membuat grup mencakup:

- groupname: Nama grup yang akan dibuat.

Format pesan yang dikirim ke server untuk membuat grup adalah:

```shell
creategroup {groupname} 
```

#### Bergabung ke Grup

Pengguna dapat bergabung ke grup dengan menggunakan perintah `joingroup`.

Protokol untuk bergabung ke grup mencakup:

<!-- - username: Nama pengguna yang bergabung. -->
- groupname: Nama grup yang akan diikuti.
<!-- - realmid: ID realm di mana grup berada. -->

Format pesan yang dikirim ke server untuk bergabung ke grup adalah:

```shell
joingroup {groupname}
```

#### Pengiriman Pesan Grup

Pesan grup dikirim dengan menggunakan perintah `sendgroup`.

Protokol untuk mengirim pesan grup mencakup:

<!-- - usernamefrom: Nama pengguna yang mengirim pesan. -->
- groupto: Nama grup yang akan menerima pesan.
- message: Isi pesan yang dikirim.

Format pesan yang dikirim ke server adalah:

```shell
sendgroup {groupto} {message} 
```

#### Penerimaan Pesan Grup

Pengguna dapat mengambil pesan grup dengan menggunakan perintah `inboxgroup`.

Protokol untuk mengambil pesan grup mencakup:

<!-- - username: Nama pengguna yang meminta pesan. -->
- groupname: Nama grup dari mana pesan diambil.

Format pesan yang dikirim ke server untuk mengambil pesan grup adalah:

```shell
inboxgroup {groupname} 
```

### Send and Receive File
## Definisi Protokol Pertukaran Antar Server
## Arsitektur Implementasi
### IP Address
### Port dari Server
### Bagaimana Menjalankan Server dan Client
## Uji Awal dari Komunikasi