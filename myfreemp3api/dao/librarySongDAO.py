#!/usr/bin/env python

import os

class LibrarySongDAO:

    def delete(songDB):
        os.remove(songDB.path)
        songDB.delete()