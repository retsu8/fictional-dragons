#!/usr/bin/env python3

import paramiko, csv, sys, os, subprocess, re, shutil, tarfile, zipfile, patoolib, magic
from trakt import Trakt
from pymediainfo import MediaInfo

mime = magic.Magic(mime=True)

Trakt.configuration.defaults.client(
    id='<client-id>',
    secret='<client-secret>'
)

paramiko.util.log_to_file('/tmp/paramiko.log')

# Open a transport

host = "192.168.1.128"
port = 22
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
    print("Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred))

def purge(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            try:
                os.remove(os.path.join(dir, f))
            except:
                shutil.rmtree(os.path.join(dir,f))
def checkFile(vid):
    fileInfo = MediaInfo.parse(vid)
    filename, ext = os.path.splitext(vid)
    for track in fileInfo.tracks:
        if track.track_type == "Video" and ext != 'srr':
            return True

def upload(location):
    #print(data)
    search = []

    for item in os.listdir(location):
        purgls = []
        path = os.path.join(location, item)
        #if item in data:
        #    shutil.rmtree(path)
        #    continue
        print('Choosing what to do with '+item)
        if os.path.isfile(item):
            filename, ext = os.path.splitext(item)
            path = os.path.join(location, filename)
            try:
                os.makedirs(path)
            except:
                print('Directory exists '+item)
            os.rename(item, path+'/'+item)
            item = path
            path = os.path.join(location, item)

        if not os.listdir(path):
            os.rmdir(path)
            continue
        extracted = False
        for wal in os.listdir(path):
            npath = os.path.join(path, wal)
            if os.path.isfile(npath):
                thismime = mime.from_file(npath)
                tys, mimer = thismime.split('/')
                #sprint(mimer)
                if mimer in ('rar','zip','7z','tar','x-rar') and not extracted:
                    #print('extracting')
                    try:
                        patoolib.extract_archive(npath, outdir=path)
                        extracted = True
                    except:
                        print('need new archive, this one is damaged')
                        extracted = True

        prsl = ['.txt', '.nfo','trailer','sample','.jpg', 'RARBG','Screens Cap', 'Sample', 'screenshots', 'Proof', '.apk', '.sfvs']
        purgls.extend(prsl)

        #for item in purgls:
        #    purge(path, item)


        subprocess.run(["filebot", "-rename", path])
        try:
            for wal in os.listdir(path):
                if not os.listdir(os.path.join(path,wal)):
                    os.rmdir(os.path.join(path,wal))
                if wal == 'subs':
                    for f in wal:
                        f = os.path.join(path,item, f)
                        pathf = os.path.join(path, f)
                        os.rename(f, pathf)
            for wal in os.listdir(path):
                if os.path.getsize(pathf) > 1000000:
                    filename, ext = os.path.splitext(wal)
                    newpaht = os.path.join(location, filename)
                    print(newpaht)
                    shutil.move(path, newpaht)
                    path = newpaht
                    item = filename
        except:
            print('Already done')
        subprocess.run(['filebot', '-get-subtitles', path])
        subprocess.run(['filebot', '-script', 'fn:artwork.tmdb', path])

def main(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.

    if len(opts) > 1:
        if ()
        location = argv[1]
    else:
        location = os.getcwd()
    upload(location)

if __name__ == "__main__":
    main(sys.argv)


# Close

sftp.close()
transport.close()
