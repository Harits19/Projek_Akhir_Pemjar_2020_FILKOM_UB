import socket
import json
import datetime
import os
import time


def run_azan(sholat, data_azan) :
    data_azan = data_azan.split('.')
    jam = int(data_azan[0])
    menit = int(data_azan[1])

    now = datetime.datetime.now()
    azan_time = datetime.datetime.combine(now.date(), datetime.time(jam, menit, 0))
    if(azan_time>=now):
        time.sleep((azan_time - now).total_seconds())
        os.system("azan.mp3")
    else :
        print("Azan " + key + " Telah Terlewat" )

    os.system("azan.mp3")

# Inisiasi socket TCP/IPv4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kirim permintaan koneksi ke server
sock.connect( ("127.0.0.2", 9999) )

while True :
    # # Kirim data ke server
    # data = input("Masukkan string yang akan dikirim : ")
    # sock.send(data.encode('ascii'))
    # # Terima kembalian dari server
    data = sock.recv(100)
    data = data.decode('ascii')
    data = json.loads(data)
    print(data)
    # print(data['dzuhur'])
    for key in data :
        run_azan(key, data[key])
    


# import datetime
# import os
# import time




