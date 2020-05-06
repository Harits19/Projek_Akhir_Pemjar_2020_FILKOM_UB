import socket
import threading
import json


# Inisiasi socket TCP/IPv4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind ke IP dan port tertentu
sock.bind( ("0.0.0.0", 9999) )

# Listen permintaan koneksi dari client
# - Param : berapa jumlah permintaan koneksi yang diterima
sock.listen(10)

connection = []

def send_all(conn, message) :
    message = json.dumps(message)
    conn.send(message.encode('ascii'))


# Membuat method untuk mengirim response
def send_response(conn, response_code, response_phrase, message) :
    length = len(message)
    response = ("HTTP/1.1 " +str(response_code)+" "+response_phrase+"\r\n"+
                "Content-Type: text/html\r\n"+
                "Content-Length: "+str(length)+"\r\n"+
                "Connection: close\r\n"+
                "\r\n"+
                message) 
    conn.send(response.encode('ascii'))



# Definisikan fungsi yang akan dieksekusi pada setiap thread
def handleThread(conn):
    try :
        # baca headers
        headers = ""
        http_header_dict = {}
        #varibel penghubung
        method = ""
        url = ""
        version = ""

        connection.append(conn)
        jadwal_dict = {}

        # already_send = False

        # for allconn in connection :
        #     if jadwal_dict != {} and already_send == True :
        #         send_all(allconn, jadwal_dict)
                
        #     else :
        #         send_all(allconn, "Jadwal Belum Tersedia")
                

        # file = ""
            # recv data setiap 4 byte
        while True :
            temp = conn.recv(4)
            temp = temp.decode('ascii')
            headers = headers + temp
            if "\r\n\r\n" in headers :
                headers = headers.replace("\r\n\r\n", "")
                break

        # cetak header
        # print(headers + "\n\n")

        is_first_line = True
        parsed_headers = headers.split("\r\n")
            
        for line in parsed_headers :
            if is_first_line :
                parsed_line = line.split(" ")
                method = parsed_line[0]
                url = parsed_line[1]
                version = parsed_line[2]
                is_first_line = False
            
            else :
                parsed_line = line.split(": ")
                http_header_dict[parsed_line[0].lower()] = parsed_line[1]
                
        if method == "GET" :
            try :
                f = open('.'+url, "r")
                message = f.read()
                send_response(conn, 200, "OK", message)
            except IOError :
                send_response(conn, 404, "Not found", "File tidak ditemukan")    
        
        elif method == "POST" :
            content_length = int(http_header_dict["content-length"])
            body = conn.recv(content_length)
            body = body.decode('ascii')
            #sebelum di split dengan &
            # print(body)

            jadwal = body
            jadwal = jadwal.split("&")
            # key value
            # shubuh 18.00
            #setelah di split dengan &
            # print(jadwal)

            for jam in jadwal :
                # print(jadwal)
                jadwal_terpisah = jam.split("=")
                # output
                # jadwal_terpisah[0] = shubuh
                # jadwal_terpisah[1] = 12.00

                jadwal_dict[jadwal_terpisah[0]]=jadwal_terpisah[1]
                
            send_response(conn, 200, "OK", "Jadwal Telah Terkirim")
            # print(jadwal_dict)

            for allconn in connection :
                send_all(allconn, jadwal_dict)
                
            # already_send = True
            
            

    except (socket.error,KeyboardInterrupt) :
        conn.close()
        print("Client menutup koneksi")

try : 
    while True :
        conn, client_addr = sock.accept()
        #Buat thread baru
        clientThread = threading.Thread(target=handleThread, args=(conn,))
        clientThread.start()
except (KeyboardInterrupt) :
    print("Server mati")