#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""This module defines the photometric objects"""

import os
from glob import glob

from astrobject.utils.tools import load_pkl, dump_pkl
import astrobject.astrobject.transient as t
from astrobject.astrobject.instruments import stella

_DEFAULT_STELLADATA = "./Data"
STELLADATA = os.getenv('STELLAPATH',default=_DEFAULT_STELLADATA)
# -- This is manually made so far

_STELLADICOSOURCE = STELLADATA+"stella_sntarget.pkl"
try:
    STELLASN = load_pkl(_STELLADICOSOURCE)
except:
    print "WARNING no stella sn dictionnary avialable."+"\n"+\
        "-> %s does not exist"%_STELLADICOSOURCE
    if STELLADATA == _DEFAULT_STELLADATA:
        print "The environment variable $STELLADATA is not defined"

####################################
#                                  #
# AstroTarget I/O                  #  
#                                  #
####################################
def get_sn(snname, dico_source=False, safeexit=False):
    """
    this methods


    Parameters
    ----------

    - option -

    safeexit: [bool]               If no transient found, this return a None
                                   if *safeexit* is True. This raise an ValueError
                                   error otherwise.
    
    Return
    ------
    astrotarget or dictionary
    """
    if snname not in STELLASN.keys():
        if not safeexit:
            raise ValueError("'%s' is not a known STELLA target"%snname)
        return None
    return t.snIa(**STELLASN[snname])
    
def add_sn(name,ra,dec,type_,mjd=None,lightcurve=None,
           update=False,**kwargs):
    """
    """
    new_sn = {"name":name,"ra":ra,"dec":dec,"type_":type_,"mjd":mjd,"lightcurve":lightcurve}
    if name in  STELLASN.keys() and not update:
        raise AttributeError("%s already exists. Set update to True to overwrite it")
    # -----------------------
    # - Update of the source
    STELLASN[name] = new_sn
    dump_pkl(STELLASN,_STELLADICOSOURCE)


####################################
#                                  #
# Image I/O                        #  
#                                  #
####################################
def get_sn_images(snname, bandfilter=None,
                  verbose=False):
    """
    """
    files = get_sn_imagefiles(snname,bandfilter=bandfilter)
    target = get_sn(snname,safeexit=True)
    if verbose:
        print "%s: %d files to load"%(snname,len(files))
        
    return [stella.stella(f,astrotarget=target) for f in files]
            
def get_sn_imagefiles(snname, bandfilter=None,
                     verbose=True):
    """
    """
    files = glob(STELLADATA+"%s/*.fits"%snname)
    if len(files) == 0:
        raise IOError("no data found for %s in %s"%(snname,STELLADATA))
    
    if bandfilter is None:
        return files
    if "__iter__" not in dir(bandfilter):
        bandfilter = [bandfilter]

    return [f for f in files if stella.which_band_is_file(f) in bandfilter]
            
