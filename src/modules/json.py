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

from orjson import loads as oloads, dumps as odumps, JSONDecodeError, \
    OPT_INDENT_2, OPT_SORT_KEYS
from jsonschema import validate, ValidationError
from pkg.client.debugvalues import DebugValues
import pkg.misc as misc
import os, time

def _start():
    global rss, start
    psinfo = misc.ProcFS.psinfo()
    rss = psinfo.pr_rssize
    start = time.time()

def _end(func, param, ret):
    taken = time.time() - start
    psinfo = misc.ProcFS.psinfo()
    mem = (psinfo.pr_rssize - rss) / 1024.0
    print("JSON Mem +{:.2f} MiB - Time {:.2f}s - {}({}) = {}"
        .format(mem, taken, func, param, ret))

def _file(stream):
    try:
        name = stream.name
        size = os.path.getsize(name) / (1024.0 * 1024.0)
        return "{:.2f} MiB {}".format(size, name)
    except:
        return str(stream)

def _kwargs(**kw):
    kwargs = {
        'option': 0
    }
    if 'indent' in kw and kw['indent']:
        kwargs['option'] |= OPT_INDENT_2
    if 'sort_keys' in kw and kw['sort_keys']:
        kwargs['option'] |= OPT_SORT_KEYS
    if 'default' in kw:
        kwargs['default'] = kw['default']

    return kwargs

def _dumps(obj, as_bytes=False, **kw):
    kwa = _kwargs(**kw)

    if as_bytes:
        return odumps(obj, **kwa)

    # return str for compatibility with core JSON module
    return odumps(obj, **kwa).decode('utf-8')

def _dump(obj, stream, **kw):
    if 'ensure_ascii' in kw and kw['ensure_ascii']:
        from rapidjson import dump as rdump
        return rdump(obj, stream, **kw)

    kwa = _kwargs(**kw)

    if hasattr(stream, 'encoding'):
        return stream.write(odumps(obj, **kwa).decode('utf-8'))

    return stream.write(odumps(obj, **kwa))

def load(stream, **kw):
    if 'json' in DebugValues:
        _start()
        ret = oloads(stream.read())
        _end('load', _file(stream), '')
        return ret

    return oloads(stream.read())

def loads(str, **kw):
    if 'json' in DebugValues:
        _start()
        ret = oloads(str, **kw)
        _end('loads', len(str), '')
        return ret

    return oloads(str, **kw)

def dump(obj, stream, **kw):
    if 'json' in DebugValues:
        _start()
        ret = _dump(obj, stream, **kw)
        _end('dump', _file(stream), ret)
        return ret

    return _dump(obj, stream, **kw)

def dumps(obj, **kw):
    if 'json' in DebugValues:
        _start()
        ret = _dumps(obj, **kw)
        _end('dumps', '', len(ret))
        return ret

    return _dumps(obj, **kw)

# Vim hints
# vim:ts=4:sw=4:et:fdm=marker
