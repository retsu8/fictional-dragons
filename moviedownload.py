import paramiko, csv

paramiko.util.log_to_file('/tmp/paramiko.log')

# Open a transport

host = "dragoncave8.ddns.net"
port = 1888
transport = paramiko.Transport((host, port))

# Auth

password = "dragon1991!"
username = "retsu"
transport.connect(username = username, password = password)

# Go!

sftp = paramiko.SFTPClient.from_transport(transport)

data = sftp.listdir('/mnt/Media/Movies')


#print(data)
with open('movielist.csv', 'rb') as f:
    reader = csv.reader(f)
    search = list(reader)

for item in search[0]:
    print(item)
    matching = [s for s in data if item.lower() in s.lower()]
print(matching)



#filepath = '/etc/passwd'
#localpath = '/home/remotepasswd'
#sftp.get(filepath, localpath)

# Close

sftp.close()
transport.close()
