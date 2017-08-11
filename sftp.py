import paramiko, os, csv, glob

paramiko.util.log_to_file('/tmp/paramiko.log')

# Open a transport

host = "37.48.119.251"
port = 2222
transport = paramiko.Transport((host, port))

# Auth

username = "user"
password = "2ebc42dc4e"
transport.connect(username = username, password = password, compress=True)

# Go!

sftp = paramiko.SFTPClient.from_transport(transport)

data = sftp.listdir('Downloads')

# Download

os.chdir("/home/retsu/Downloads")
filepath = "/home/retsu/Downloads/"
for file in os.listdir(filepath):
    name, ext = os.path.splitext(file)
    if ext == '.torrent':
        print('Moving torrent '+file+' into Downloads')
        start = os.path.join(filepath, file)
        finish = os.path.join('Downloads/', file)
        print(start)
        sftp.put(start, finish)
        print('Now Deleting '+file)
        os.remove(file)

# Close

sftp.close()
transport.close()
