#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#
# Copyright 2008 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#

MACH:sh = uname -p

top_srcdir = ..
ROOT = ../../proto/root_$(MACH)
ROOTLOCALE = $(ROOT)/usr/share/locale

POFILES:sh = echo *.po
MOFILES = $(POFILES:%.po=%.mo)
LINGUAS = $(POFILES:%.po=%)
MOFILENAME = pkg.mo

ROOTLOCALEDIRS = $(LINGUAS:%=$(ROOTLOCALE)/%)
ROOTMESSAGEDIRS = $(ROOTLOCALEDIRS:%=%/LC_MESSAGES)

ROOTMOFILES = $(ROOTMESSAGEDIRS:%=%/$(MOFILENAME))

all: $(MOFILES)

install: $(ROOTMESSAGEDIRS) $(ROOTMOFILES)

%.mo: %.po
	msgfmt -o $@ $<

clean:
	rm -f $(MOFILES)

clobber: clean

$(ROOTMESSAGEDIRS):
	mkdir -m 0755 -p $@

$(ROOTLOCALE)/%/LC_MESSAGES/$(MOFILENAME): %.mo
	rm -f $@; cp $< $@; chmod 644 $@