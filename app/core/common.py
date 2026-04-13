import datetime, time
import os
import sqlite3
import shutil


from app.core.constants import VOTERS_DB, VOTES_LOG





#==============================================================================
# Return current date+time in "%Y-%m-%d %H:%M (%A)" format
# YYYY-MM-DD hh:mm
def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

#------------------------------------------------------------------------------
# YYYYMMDDhhmmss
def compact_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H%M%%S")

#------------------------------------------------------------------------------
# Copy file or directory with metadata and following symlinks:
def fcopysl(src_path, dest_path):
    shutil.copy2(src_path, dest_path, follow_symlinks=True)

#------------------------------------------------------------------------------
# Copy file or directory with metadata but without following symlinks:
def fcopy(src_path, dest_path):
    newpath = shutil.copy2(src_path, dest_path, follow_symlinks=False)
    if newpath == dest_path:
        return(newpath)
    else:
        return("")
    # Returns empty string if unsuccessful

#------------------------------------------------------------------------------
