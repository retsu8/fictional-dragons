import paramiko
import csv

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

print(data)
# Download

#filepath = '/etc/passwd'
#localpath = '/home/remotepasswd'
#sftp.get(filepath, localpath)

# Close

sftp.close()
transport.close()
