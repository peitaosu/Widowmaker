import urllib2

CHUNK_SIZE = 16 * 1024

def download(url, file_path, header):
    print "Start download from: {}".format(url)
    request = urllib2.Request(url, headers=header)
    response = urllib2.urlopen(request)

    bytes_received = 0
    download_size = int(response.info().getheader("Content-Length"))

    try:
        with open(file_path, 'wb') as dst_file:
            while True:
                buffer = response.read(CHUNK_SIZE)
                if not buffer and bytes_received == download_size:
                    break
                bytes_received += len(buffer)
                dst_file.write(buffer)
        print "Download Finished."
    except Exception as err:
        print "Download Failed: {}".format(err)
