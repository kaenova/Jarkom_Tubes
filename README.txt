Kaenova Mahendra Auditama
kaenova@student.telkomuniversity.ac.id
Informatics Engineering, Telkom University, Indonesia
2021

Proyek ini merupakan Tugas Besar dari Mata Kuliah Jaringan Komputer. Pada Tugas Besar ini saya diminta untuk mengimplementasikan suatu topologi serta beberapa goal yang ada pada CLO 1, CLO 2, CLO 3, dan CLO 4.  

=== INSTALASI ===
Ada satu dependency yaitu tcpdump. Untuk menginstall harap lakukan:  
------------------------------------------------------
# Arch-based Distros
 $ sudo pacman -Sy mininet tcpdump 
# Debuan-based Distros
 $ sudo apt-get update && apt-get install mininet tcpdump
------------------------------------------------------

Setelah itu lakukan instalasi API Mininet python:  
------------------------------------------------------
$ sudo pip install mininet
------------------------------------------------------

Setelah malakukan instalasi dependency, pastikan ada folder `logs` didalam direktori yang sama dengan `main.py`. Sehingga file tree terlihat seperti:
------------------------------------------------------
Jarkom_Tubes/
├─ README.md
├─ README.txt
├─ logs/
│  ├─ log_file
├─ main.py
------------------------------------------------------

Ketika sudah memenuhi poin-poin di atas, maka anda sudah bisa menjalankan program dengan melakukan
------------------------------------------------------
$ sudo python main.py
------------------------------------------------------

=== PENGGUNAAN ===
### Penggunaan
Setelah menjalankan prorgram tersebut anda akan diminta untuk memasukkan suatu angka. Angka-angka tersebut merepresentasikan CLO yang akan dicapai.  

- Jika memilih untuk menjalankan CLO 1 maka ketika menjalankannya tidak akan terjadi apa-apa, hanya ada masukkan dari mininet, tetapi untuk memenuhi goal yang dicapai yaitu melihat konektivitas network, anda bisa masuk kedalam folder `./logs` untuk melihat output dari goal yang diminta

- Jika memilih untuk menjalankan <b>CLO 2</b> maka ketika menjalankannya hanya diminta untuk memasukkan di dalam mininetnya, dan memeriksa routing secara sendiri dengan melakukan:
    ------------------------------------------------------
    mininet> [host_yang_diinginkan] traceroute [host_tujuan]
    # contoh
    # mininet> c1 traceroute c2
    ------------------------------------------------------

- Jika memilih untuk menjalankan <b>CLO 3</b> maka ketika menjalankannya akan ada file dengan format `.pcap` dimana dapat diinspeksi dengan menggunakan program wireshark ataupun tcpdump.

- Jika memilih untuk menjalankan <b>CLO 4</b> maka ketika menjalankannya akan diminta masukkan dimana masukkan tersebut merupakan besar buffer yang diinginkan. Lalu untuk melihat hasil uji coba ping maka anda harus melihat ke dalam folder `./logs`