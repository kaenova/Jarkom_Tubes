# Jarkom_Tubes

Kaenova Mahendra Auditama<br>
<a href="kaenova@student.telkomuniversity.ac.id">kaenova@student.telkomuniversity.ac.id</a><br>
Informatics Engineering, Telkom University, Indonesia<br>
2021

<!-- 
## [English]

This project is second of three project from course Artificial Intelligence Introduction. This project implement searching reasoning in Artificial Intelligence with Fuzzy Logic. In this case, we need to rank from 100 restaurants to get 10 best restaurant using Fuzzy Logic based on how good is the service and the food.

This Algorithm need some external libraries, before you run this algorithm please install dependencies using:

```sh
$ python -m pip install -r requirements.txt
```

After installing all dependencies, now you can run the main files:

```sh
$ python main.py
``` -->

## [Bahasa Indonesia]

Proyek ini merupakan Tugas Besar dari Mata Kuliah Jaringan Komputer. Pada Tugas Besar ini saya diminta untuk mengimplementasikan suatu topologi serta beberapa goal yang ada pada CLO 1, CLO 2, CLO 3, dan CLO 4.  

### Instalasi
Ada satu dependency yaitu tcpdump. Untuk menginstall harap lakukan:  
```sh
# Arch-based Distros
$ sudo pacman -Sy mininet tcpdump 
# Debuan-based Distros
$ sudo apt-get update && apt-get install mininet tcpdump
``` 
Setelah itu lakukan instalasi API Mininet python:  
```
$ sudo pip install mininet
```

Setelah malakukan instalasi dependency, <b>pastikan ada folder `logs` didalam direktori yang sama dengan `main.py`</b>. Sehingga file tree terlihat seperti:
```
Jarkom_Tubes/
├─ README.md
├─ README.txt
├─ logs/
│  ├─ log_file
├─ main.py
```
Ketika sudah memenuhi poin-poin di atas, maka anda sudah bisa menjalankan program dengan melakukan:
```
$ sudo python main.py
```

### Penggunaan
Setelah menjalankan prorgram tersebut anda akan diminta untuk memasukkan suatu angka. Angka-angka tersebut merepresentasikan CLO yang akan dicapai.  
- Jika memilih untuk menjalankan <b>CLO 1</b> maka ketika menjalankannya tidak akan terjadi apa-apa, hanya ada masukkan dari mininet, tetapi untuk memenuhi goal yang dicapai yaitu melihat konektivitas network, anda bisa masuk kedalam folder `./logs` untuk melihat output dari goal yang diminta
- Jika memilih untuk menjalankan <b>CLO 2</b> maka ketika menjalankannya hanya diminta untuk memasukkan di dalam mininetnya, dan memeriksa routing secara sendiri dengan melakukan:
    ```sh
    mininet> [host_yang_diinginkan] traceroute [host_tujuan]
    # contoh
    # mininet> h1 traceroute h2
    ```
- Jika memilih untuk menjalankan <b>CLO 3</b> maka ketika menjalankannya akan ada file dengan format `.pcap` dimana dapat diinspeksi dengan menggunakan program wireshark ataupun tcpdump.
- Jika memilih untuk menjalankan <b>CLO 4</b> maka ketika menjalankannya akan diminta masukkan dimana masukkan tersebut merupakan besar buffer yang diinginkan. Lalu untuk melihat hasil uji coba ping maka anda harus melihat ke dalam folder `./logs`

<p align="center">
<br><br>
<img src="https://cdn.discordapp.com/attachments/829581469936386079/830470865190912081/K-Gif.gif" height="60px"/>
</p>
