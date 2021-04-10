import socket, struct, json, os       

download_dir = r'D:\python\soket\socket_test_client\client\test'   #client端的下載路徑 

gd_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          #soket基礎設定
gd_client.connect(('192.168.126.1', 6688))                             #本地IP位置

while True:
  cmd=input('>>: ')        #輸入要接收資料的名稱 

  gd_client.send(cmd.encode('utf-8'))         #以utf-8的方式編碼並傳送至server端
  obj=gd_client.recv(4)                       #接收資料
  
  header_size=struct.unpack('i',obj)[0]      #打包二進制數據
  header_bytes = gd_client.recv(header_size) #接收打包為二進制後的大小 
  header_json = header_bytes.decode('utf-8') #解碼
  header_dic = json.loads(header_json)       #將json轉換成python型態

  file_name = header_dic['filename']
  total_size =  header_dic['file_size']
  #===================寫入檔案=====================
  with open('%s/%s'%(download_dir, file_name),'wb') as f:
    recv_size = 0
    while recv_size < total_size:
      line = gd_client.recv(1024)
      f.write(line)
      recv_size += len(line)
      print('總大小：%s  已下載大小：%s' % (total_size, recv_size))
  #================================================
gd_client.close