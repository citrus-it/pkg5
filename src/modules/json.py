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
import os, sys, time

def _start():
    psinfo = misc.ProcFS.psinfo()
    _start.rss = psinfo.pr_rssize
    _start.start = time.time()
    if int(DebugValues['json']) > 1:
        _start.trace = True
_start.rss = 0
_start.maxrss = 0
_start.start = 0
_start.trace = False

def _end(func, param, ret):
    taken = time.time() - _start.start
    psinfo = misc.ProcFS.psinfo()
    mem = (psinfo.pr_rssize - _start.rss) / 1024.0
    if psinfo.pr_rssize > _start.maxrss:
        _start.maxrss = psinfo.pr_rssize
    print("JSON Mem +{:.2f}={:.2f} Max {:.2f} MiB - Time {:.2f}s - {}({}) = {}"
        .format(mem, psinfo.pr_rssize / 1024.0, _start.maxrss / 1024.0,
                taken, func, param, ret),
        file=sys.stderr)

def _stack(note, limit=5):
    from traceback import extract_stack, format_list
    stack = extract_stack(limit=limit)[:-3]
    print("{}:".format(note), file=sys.stderr)
    for l in format_list(stack):
        for m in l.split("\n"):
            if m.strip() == '': continue
            print("    >> {}".format(m), file=sys.stderr)

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

    if _start.trace: _stack("DUMPS str")

    # return str for compatibility with core JSON module
    return odumps(obj, **kwa).decode('utf-8')

def _dump(obj, stream, **kw):
    if 'ensure_ascii' in kw and kw['ensure_ascii']:
        if _start.trace: _stack("DUMP ascii")
        from rapidjson import dump as rdump
        return rdump(obj, stream, **kw)

    kwa = _kwargs(**kw)

    if hasattr(stream, 'encoding'):
        if _start.trace: _stack("DUMP strfile")
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
