import paramiko, csv, sys, os
from trakt import Trakt
from imdb import IMDb

#Check the media
ia = IMDb('http')

Trakt.configuration.defaults.client(
    id='<client-id>',
    secret='<client-secret>'
)

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
filepath = '/mnt/Media/Movies/'

def printTotals(transferred, toBeTransferred):
    print "Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred)

def match(matching):
    for item in matching:
        print ia.search_keyword(item)
    return matching
def download(csvlist, location):
    #print(data)
    with open(csvlist, 'rb') as f:
        reader = csv.reader(f)
        search = list(reader)

    for item in search[0]:
        print(item)
        matching = [s for s in data if item.lower() in s.lower()]
    matching = match(matching)
    print(matching)

    for item in matching:
        file_list = sftp.listdir(filepath+item)
        if not os.path.exists(location+'/'+item):
            os.makedirs(location+'/'+item)
        for sect in file_list:
            toget = filepath+item+'/'+sect
            toput = location+'/'+item+'/'+sect
            print(toput)
            sftp.get(toget, toput, callback=printTotals)
        break

def main(argv):
    print(len(argv))
    if len(argv) > 2:
        location = os.getcwd()
    elif len(argv) > 1:
        csvlist = argv[1]
    else:
        csvlist = 'movielist.csv'
        location = os.getcwd()
        print(location)
    download(csvlist, location)

if __name__ == "__main__":
    main(sys.argv)


# Close

sftp.close()
transport.close()
