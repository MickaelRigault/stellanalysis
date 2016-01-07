#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""This module defines the photometric objects"""


import .iostella as io
from astrobject.astrobject.baseobject import BaseObject

class ImageCollection( BaseObject ):
    """
    This class enabvle to gather in one bloc a bunch of images
    """
    _properties_keys = ["images"]
    _side_properties_keys = ["target"]
    
    def __init__(self,images=None,empty=False):
        """
        """
        self.__build__()
        if empty:
            return

    def create(self):
        """
        """
    # ========================== #
    # = Set Target             = #
    # ========================== #
    def set_target(self,newtarget):
        """
        Change (or create) an object associated to the given image.
        This function will test if the object is withing the image
        boundaries (expect if *test_inclusion* is set to False).
        Set newtarget to None to remove the association between this
        object and a target
        """
        if newtarget is None:
            self._side_properties['target'] = None
            return
        
        # -- Input Test -- #
        if newtarget.__nature__ != "AstroTarget":
            raise TypeError("'newtarget' should be (or inherite) an AstroTarget")
        
        # -- Seems Ok -- #
        self._side_properties["target"] = newtarget.copy()

    # ========================== #
    # = Properties             = #
    # ========================== #
    
    # -- Target
    @property
    def target(self):
        return self._side_properties['target']

    def has_target(self):
        return False if self.target is None \
          else True
