#!/usr/bin/env python3.6

#When using this script make sure to set the api in .env and source it or atleast comment out notification
import os,subprocess, sys, ffmpy, argparse,json
from ffprobe3 import FFProbe
from urllib.request import Request, urlopen
from urllib.parse import urlencode

scale = None
cwd = os.getcwd()

def notify_me(insert_str):
    url = 'https://api.pushbullet.com/v2/pushes'
    data = json.dumps({"type":"note","title":"ffmpy","body":insert_str}).encode('utf8')
    req = Request(url, data=data, headers={'Access-Token':'o.HbruEwaF0buw4mxXP2BlghVfs9G9C6Hf','Content-Type':'application/json'})
    resp = urlopen(req)
    data = json.loads(resp.read())
    print(data)

def simpleConvert(vid, skip):
    dir_path = os.path.dirname(os.path.realpath(vid))
    video, stream = checkFile(vid)
    print(video, stream)
    if video:
        convert(vid, dir_path, stream, skip)
        notify_me("I have finished converting {0}".format(vid))

def batchConvert(skip):
    for(dirpath, dirnames, filename)in os.walk(cwd):
        for vid in filename:
            video, stream = checkFile(vid)
            print(video, stream)
            if video:
                convert(vid, dirpath, stream, skip)
                notify_me("I have finished converting {0}".format(vid))
            else:
                notify_me('not convertable {0} {1}'.format(dirpath, vid))

def checkFile(vid):
    try:
        fileInfo = FFProbe(vid)
    except:
        return False, []

    size = os.stat(vid).st_size
    print(size)
    if size < 10000000:
        return False, []
    filename, ext = os.path.splitext(vid)
    index = []
    for item in fileInfo.streams:
        index.append(item.__dict__)

    for stream in fileInfo.streams:
        if stream.is_video():
            my_stream = dict(stream.__dict__)
            print(my_stream)
            if (('TAG:DURATION' in my_stream and my_stream['TAG:DURATION'] > '00:10:00.000000000') or ('codec_type' in my_stream and my_stream['codec_type'] == 'video')) and my_stream['codec_name'] != 'ansi':
                return True, index
    return False, []

def convert(vid, source, stream, skip):
    print(vid+source)
    video = vid

    filename, ext = os.path.splitext(vid)
    filename = filename.replace("'", "")
    streams = []
    for item in stream:
        if item['codec_type'] == 'video':
            my_video = item
            streams.append("-map 0:{}".format(item['index']))
        elif item['codec_type'] == 'audio':
            mapper = "-map 0:{}".format(item['index'])
            streams.append(mapper)
    if 'srr' in ext:
        return
    elif skip and 'mp4' in ext:
        return
    elif 'mp4' in ext:
        rename_me = os.path.join(source, filename + '.m4v')
        path = os.path.join(source, vid)
        os.rename(path, rename_me)
        video = rename_me
        ext = 'mp4'
    else:
        ext = 'mp4'

    print('file: {} ext: {}'.format(filename, ext))
    my_stream = " ".join(streams)
    if int(my_video['width']) > 720:
        opts = "-c:v libx265 -crf 20 -vf '{}:trunc(ow/a/2)*2' -metadata title='{}' -map_metadata 0 {}".format(scale, filename.replace("'",""), my_stream)
    else:
        opts = "-c:v libx265 -crf 20 -metadata title='{}' -metadata:s:a:0 language=eng -map_metadata 0 {}".format(filename.replace("'",""), my_stream)

    out_vid = '{}.{}'.format(filename,ext)
    if os.path.isfile(out_vid):
        print(os.getsize(out_vid))
        if os.getsize(out_vid) > 10000000:
            print("File has already been converted")
            return
        else:
            os.remove(out_vid)

    ff = ffmpy.FFmpeg(inputs={video:None},outputs={out_vid:opts})

    print(ff.cmd)
    ff.run()
    return

def scaleme(size):
    return 'scale={}'.format(size)

def check_my_audio():
    convert

def main(arg):
    global scale
    scale = scaleme(arg.size)
    if arg.file:
        print('Found file now converting')
        simpleConvert(arg.file, arg.skip)
    else:
        print('got directory now converting')
        batchConvert(arg.skip)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--size", help="get the size 720, 1080, 1280, 1920", type=int, default=720)
    parser.add_argument("-f", "--file", help="get the file to convert", type=str, default=False)
    parser.add_argument("-s", "--skip", help="This will set skipping for mp4", action='store_true', default=False)
    args = parser.parse_args()
    main(args)
