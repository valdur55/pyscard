#! /usr/bin/env python
"""
Sample for python PCSC wrapper module: get card ATR in first pcsc reader

__author__ = "Ludovic Rousseau"

Copyright 2007 Ludovic Rousseau
Author: Ludovic Rousseau, mailto:ludovic.rousseau@free.fr

This file is part of pyscard.

pyscard is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or
(at your option) any later version.

pyscard is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyscard; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

from smartcard.scard import *

try:
    hresult, hcontext = SCardEstablishContext( SCARD_SCOPE_USER )
    if hresult!=0:
        raise  'Failed to establish context: ' + SCardGetErrorMessage(hresult)
    print 'Context established!'

    try:
        hresult, readers = SCardListReaders( hcontext, [] )
        if hresult!=0:
            raise error, 'Failed to list readers: ' + SCardGetErrorMessage(hresult)
        print 'PCSC Readers:', readers

        if len(readers)<1:
            raise error, 'No smart card readers'

        for zreader in readers:

            print 'Trying to Control reader:', zreader

            try:
                hresult, hcard, dwActiveProtocol = SCardConnect(
                    hcontext, zreader, SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0 )
                if hresult!=0:
                    raise error, 'Unable to connect: ' + SCardGetErrorMessage(hresult)
                print 'Connected with active protocol', dwActiveProtocol

                try:
                    # get firmware on Gemplus readers
                    hresult, response = SCardControl( hcard, 0x42000001, [ 0x02])
                    if hresult!=SCARD_S_SUCCESS:
                        raise  error, 'SCardControl failed: ' + SCardGetErrorMessage(hresult)
                    r = ""
                    for i in xrange(len(response)):
                        r += "%c" % response[i]
                    print 'Control:', r
                finally:
                    hresult = SCardDisconnect( hcard, SCARD_UNPOWER_CARD )
                    if hresult!=0:
                        raise error, 'Failed to disconnect: ' + SCardGetErrorMessage(hresult)
                    print 'Disconnected'

            except error:
                print error, SCardGetErrorMessage(hresult)


    finally:
        hresult = SCardReleaseContext( hcontext )
        if hresult!=SCARD_S_SUCCESS:
            raise  'Failed to release context: ' + SCardGetErrorMessage(hresult)
        print 'Released context.'

except:
    import sys
    print sys.exc_info()[0], ':', sys.exc_info()[1]

import sys
if 'win32'==sys.platform:
    print 'press Enter to continue'
    sys.stdin.read(1)
