# FINAL PROJECT JARINGAN NIRKABEL

## Anggota:
1. Faizal Khilmi Muzakki **05111640000120**
2. Fadli Wildan Firjatullah **05111640000126**
3. Fahrizal Naufal Ahmad **05111640000135**
4. Mohammad Haekal Alawy **05111640000141**


step:
1. pertama gunakan wifi yang sama untuk memastikan device berada di dalam 1 jaringan
2. run program receive.py,receive2.py, receive_1.py,receive2_1.py dan sender.py
3. melalui sender.py masukan inputan (distance_treshold,hop,message dan lifetime)
4. setelah memasukan input yang diatas, maka receiver akan menunggu message lalu menampilkan pesan (waiting to receive message)
5. jika hop yang di input berjumlah 1 maka yang akan menerima pesan hanya terminal yang menjalankan program receive.py dan         receive2.py
6. jika hop yang di input berjumlah lebih dari 1 maka terminal yang menjalankan receive_1.py dan receive2_1.py
7. ketika receiver menerima  message, receiver juga menerima informasi distance_treshold, hop, message dan message expired
8. jika distance nya lebih dari distance_treshold maka message tidak di print
9. jika hop lebih dari limit hop maka message tidak akan di forward
10. jika lifetime nya sudah habis maka message nya dihapus dari array message
