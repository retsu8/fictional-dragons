#! /usr/local/env python3.6

from deluge_client import DelugeRPCClient
from fuzzywuzzy import fuzz, process
import PTN
import paramiko, sys

def get_movie(my_call, search_lst):
    for item, var in my_call.items():
        search_me = str(var[b'name'], 'utf-8')
        new_srch = PTN.parse(search_me.lower())
        if 'episode' in new_srch and 'season' in new_srch:
            continue
        choice = process.extractOne(new_srch['title'], search_lst)
        if choice[1] > 95:
            print(choice)
            print(item, var)
            
paramiko.util.log_to_file('/tmp/paramiko.log')

transport = paramiko.Transport(("dragoncave8.ddns.net", 1889))
transport.connect(None, "retsu", "dragon1991!")

sftp = paramiko.SFTPClient.from_transport(transport)
movies = sftp.listdir("/mnt/Media/Movies")
search_lst = [PTN.parse(item.lower())['title'] for item in movies]

client = DelugeRPCClient('perses.feralhosting.com', 53305, 'retsu8', 'yf-AXshN8_FjXTZA')
client.connect()
my_call = client.call('core.get_torrents_status', {}, ['name', 'ratio'])



if transport is not None:
    transport.close()
