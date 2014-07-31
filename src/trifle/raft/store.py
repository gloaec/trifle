import os
import errno
import uuid

import msgpack  # we're using it anyway...

from trifle import config

def read_state(port):
    sfile = os.path.join(config['TMP_DIR'], "raft-state-%d" % port)
    try:
        with open(sfile) as r:
            return msgpack.unpackb(r.read())
    except IOError as e:
        if not e.errno == errno.ENOENT:
            raise
    # no state file exists; initialize with fresh values
    return 0, None, None, {}, uuid.uuid4().hex


def write_state(port, term, voted, log, peers, uuid):
    try:
        os.makedirs(config['TMP_DIR'])
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(config['TMP_DIR']):
            pass
        else: raise
    sfile = os.path.join(config['TMP_DIR'], "raft-state-%d" % port)
    with open(sfile, 'w') as w:
        w.write(msgpack.packb((term, voted, log, peers, uuid)))
