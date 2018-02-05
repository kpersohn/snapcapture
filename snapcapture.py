import datetime
import logging
import os
import urllib2
from os import path


def main():
    ROOTDIR = path.basedir(path.abspath(__file__))
    LOGFILE = path.join(ROOTDIR, 'log.txt')

    logging.basicConfig(
        filename=LOGFILE, format='%(asctime)s %(message)s', level=logging.DEBUG
    )

    try:
        URL = None
        execfile(path.join(ROOTDIR, 'settings.py'))
    except StandardError:
        logging.exception('Error loading settings.py')
        raise

    dt = datetime.datetime.now()
    savepath = path.join(
        ROOTDIR,
        dt.year,
        '%02d'.format(dt.month),
        '%02d'.format(dt.day)
    )
    savefile = path.join(savepath, dt.strftime('%Y%m%d-%H%M%S.jpg'))

    try:
        os.makedirs(savepath)
    except OSError:
        # Ignore if directory already exists.
        pass
    except StandardError:
        logging.exception('Error creating download directory')
        raise

    try:
        remote = urllib2.urlopen(URL)
        with open(savefile, 'wb') as local:
            local.write(remote.read())
    except urllib2.HTTPError:
        logging.exception('HTTP error')
        raise
    except urllib2.HTTPError:
        logging.exception('URL error')
        raise
    except StandardError:
        logging.exception('Unspecified error')
        raise


if __name__ == '__main__':
    main()
