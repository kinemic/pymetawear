#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. moduleauthor:: jhennrich <johannes.hennrich@kinemic.de>
Created: 2017-02-17
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import warnings
import logging
from functools import wraps
from ctypes import cast, POINTER, c_float, c_uint, c_void_p, byref

from pymetawear import libmetawear
from pymetawear.exceptions import PyMetaWearException
from pymetawear.mbientlab.metawear.core import DataTypeId, Fn_DataPtr, Fn_VoidPtr_Int
from pymetawear.modules.base import PyMetaWearModule, Modules


log = logging.getLogger(__name__)

class EventRecordingContextManager:
    def __init__(self, event_module, event, callback):
        self.event_module = event_module
        self.event = event
        self.callback = callback

    def __enter__(self):
        self.event_module._start_record(self.event)
        return self.event

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.event_module._end_record(self.event, self.callback)
        return False



class EventModule(PyMetaWearModule):
    """MetaWear Event module implementation.
    :param ctypes.c_long board: The MetaWear board pointer value.
    :param bool debug: If ``True``, module prints out debug information.
    """
    def __init__(self, board, module_id, debug=False):
            super(EventModule, self).__init__(board, debug)
            self.module_id = module_id
            self.callback_dict = {}

            if self.module_id == Modules.MBL_MW_MODULE_NA:
                # No event present!
                self.available = False
            else:
                self.available = True

            if debug:
                log.setLevel(logging.DEBUG)

    def __str__(self):
        return "{0}".format(self.module_name)

    def __repr__(self):
        return str(self)

    @property
    def module_name(self):
        return "Event"

    def notifications(self, callback=None):
        raise PyMetaWearException(
            "Notifications not available for {0} module.".format(self))

    def _start_record(self, event):
        libmetawear.mbl_mw_event_record_commands(event)

    def _end_record(self, event, callback):
        libmetawear.mbl_mw_event_end_record(event, Fn_VoidPtr_Int(callback))

    def record(self, event, callback=lambda *args: None):
        """
        Record a series of commands for the specified event.

        Use the "with" Syntax:
        with .record(event, callback) as ev:
            pat = c.led.load_preset_pattern('blink', repeat_count=3)
            c.led.write_pattern(pat, 'r')
            c.led.play()

        @param event: The event or timer to record commands for.
        @param callback: (Optional) Is run when the recording is finished/aborted. Parameters: event, status(int).
        @return: An EventRecordingContextManager object.
        """
        return EventRecordingContextManager(self, event, callback)
