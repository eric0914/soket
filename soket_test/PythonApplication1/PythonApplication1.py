import socket, subprocess, struct, os, json  #server

share_dir = r'D:\python\soket\soket_test\test2'

while True:
#===================連線基本指令=====================
  print(u'waiting for connect...')
  gd_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  gd_server.bind(('192.168.126.1', 6688))
  gd_server.listen(5)
  conn,  (host, port) = gd_server.accept()
  print(u'the client %s:%s has connected.' % (host, port))
#====================================================

  while True: 
    try:
      res = conn.recv(8096)  #接收編過碼的資料
      if not res: break 
      cmds = res.decode('utf-8') .split()  #將剛剛接收的資料解碼
      filename = cmds[1]     

      #==================定義檔案名稱及檔案大小===================
      header_dic = {
        'filename': filename,      
        'file_size':os.path.getsize(r'%s\%s'%(share_dir, filename)) 
      }
      #===========================================================

      header_json = json.dumps(header_dic)          #將python轉換成json型態
      header_bytes = header_json.encode('utf-8')    #編碼
      conn.send(struct.pack('i',len(header_bytes))) #傳送編過碼header_dic
      conn.send(header_bytes)                  
       #===================讀取檔案=====================
      with open('%s/%s'%(share_dir, filename),'rb') as f:
        for line in f:
          conn.send(line)
    except  ConnectionResetError:
      break
  conn.close()
gd_server.close