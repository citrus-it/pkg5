#!/usr/bin/python3.7
#
# {{{ CDDL HEADER
#
# This file and its contents are supplied under the terms of the
# Common Development and Distribution License ("CDDL"), version 1.0.
# You may only use this file in accordance with the terms of version
# 1.0 of the CDDL.
#
# A full copy of the text of the CDDL should have accompanied this
# source. A copy of the CDDL is also available via the Internet at
# http://www.illumos.org/license/CDDL.
# }}}

# Copyright 2020 OmniOS Community Edition (OmniOSce) Association.

"""
json module abstraction for the packaging system.
"""

############################################################################
# Standard version

from orjson import loads, dumps as odumps, JSONDecodeError, OPT_INDENT_2, \
    OPT_SORT_KEYS
from jsonschema import validate, ValidationError

# wrappers for orjson
def kwargs(**kw):
    _kwargs = {
        'option': 0
    }
    if 'indent' in kw and kw['indent']:
        _kwargs['option'] |= OPT_INDENT_2
    if 'sort_keys' in kw and kw['sort_keys']:
        _kwargs['option'] |= OPT_SORT_KEYS
    if 'default' in kw:
        _kwargs['default'] = kw['default']

    return _kwargs

def load(stream, **kw):
    return loads(stream.read())

def dumps(obj, as_bytes=False, **kw):
    kwa = kwargs(**kw)

    if as_bytes:
        return odumps(obj, **kwa)

    # return str for compatibility with core JSON module
    return odumps(obj, **kwa).decode('utf-8')

def dump(obj, stream, **kw):
    if 'ensure_ascii' in kw and kw['ensure_ascii']:
        from rapidjson import dump as rdump
        return rdump(obj, stream, **kw)

    kwa = kwargs(**kw)

    if hasattr(stream, 'encoding'):
        return stream.write(odumps(obj, **kwa).decode('utf-8'))

    return stream.write(odumps(obj, **kwa))

############################################################################
# Debug/profiling version

##from pkg.client.debugvalues import DebugValues
##import pkg.misc as misc
##
##import os, time
##import rapidjson as _json
##
##JSONDecodeError = _json.JSONDecodeError
##
##def _start():
##    global rss, start
##    psinfo = misc.ProcFS.psinfo()
##    rss = psinfo.pr_rssize
##    start = time.time()
##
##def _end(func, param, ret):
##    taken = time.time() - start
##    psinfo = misc.ProcFS.psinfo()
##    mem = (psinfo.pr_rssize - rss) / 1024.0
##    print("JSON Mem +{:.2f} MiB - Time {:.2f}s - {}({}) = {}"
##        .format(mem, taken, func, param, ret))
##
##def _file(stream):
##        try:
##            name = stream.name
##            size = os.path.getsize(name) / (1024.0 * 1024.0)
##            return "{:.2f} MiB {}".format(size, name)
##        except:
##            return str(stream)
##
##def load(stream, **kw):
##    if "json" in DebugValues:
##        _start()
##        ret = _json.load(stream, **kw)
##        _end('load', _file(stream), '')
##        return ret
##    else:
##        return _json.load(stream, **kw)
##
##def loads(str, **kw):
##    if "json" in DebugValues:
##        _start()
##        ret = _json.loads(str, **kw)
##        _end('loads', len(str), '')
##        return ret
##    else:
##        return _json.loads(str, **kw)
##
##def dump(obj, stream, **kw):
##    if "json" in DebugValues:
##        _start()
##        ret = _json.dump(obj, stream, **kw)
##        _end('dump', _file(stream), ret)
##        return ret
##    else:
##        return _json.dump(obj, stream, **kw)
##
##def dumps(obj, **kw):
##    if "json" in DebugValues:
##        _start()
##        ret = _json.dumps(obj, **kw)
##        _end('dumps', '', len(ret))
##        return ret
##    else:
##        return _json.dumps(obj, **kw)

# Vim hints
# vim:ts=4:sw=4:et:fdm=marker
