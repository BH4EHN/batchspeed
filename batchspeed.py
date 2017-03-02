import socket
import urllib2
import time
import optparse


def str_speed_in_kb(val):
    val_in_kb = val / 1024
    return '%.2f KB/s' % val_in_kb


def download_speed(url, time_limit, is_verbose):
    print 'Downloading %s, time-limit %d sec' % url, time_limit
    average_speed = 0.0
    maximum_speed = 0.0
    try:
        response = urllib2.urlopen(url, None, 15)

        chunk_size = 4096
        maximum_download_time_limit = time_limit
        bytes_downloaded = 0
        last_calc_time = time.time()
        last_calc_downloaded = 0
        calc_count = 0
        start_download_time = time.time()

        while 1:
            chunk = response.read(chunk_size)
            bytes_downloaded += len(chunk)

            if not chunk:
                break
            current_time = time.time()
            time_diff = current_time - last_calc_time
            if time_diff > 1:
                bytes_diff = bytes_downloaded - last_calc_downloaded
                current_speed = bytes_diff / time_diff

                last_calc_time = current_time
                last_calc_downloaded = bytes_downloaded
                if current_speed > maximum_speed:
                    maximum_speed = current_speed
                calc_count += 1
                average_speed += (current_speed - average_speed) / calc_count
                if is_verbose:
                    print str_speed_in_kb(current_speed)

            download_time = time.time() - start_download_time
            if download_time > maximum_download_time_limit:
                break
        response.close()

    except socket.timeout:
        print 'timed out'

    print 'average: ' + str_speed_in_kb(average_speed)
    print 'maximum: ' + str_speed_in_kb(maximum_speed)

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-u', '--url', dest='url', default=None)
    parser.add_option('-l', '--limit', dest='limit', type='int', default=30)
    parser.add_option('-v', '--verbose', dest='verbose', action="store_true")
    (options, args) = parser.parse_args()
    if not options.url:
        print 'url is required'
    download_speed(options.url, options.limit, not not options.verbose)

