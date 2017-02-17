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
from pymetawear.mbientlab.metawear.core import DataTypeId, Fn_DataPtr, Fn_VoidPtr
from pymetawear.modules.base import PyMetaWearModule, Modules


log = logging.getLogger(__name__)


class TimerModule(PyMetaWearModule):
    """MetaWear Event module implementation.
    :param ctypes.c_long board: The MetaWear board pointer value.
    :param bool debug: If ``True``, module prints out debug information.
    """
    def __init__(self, board, module_id, debug=False):
            super(TimerModule, self).__init__(board, debug)
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
        return "Timer"

    def notifications(self, callback=None):
        raise PyMetaWearException(
            "Notifications not available for {0} module.".format(self))

    def create_timer(self, period, repetitions, delay, callback):
        libmetawear.mbl_mw_timer_create(self.board, period, repetitions, delay, Fn_VoidPtr(callback))

    def create_timer_indefinite(self, period, delay, callback):
        libmetawear.mbl_mw_timer_create_indefinite(self.board, period, delay, Fn_VoidPtr(callback))

    def remove(self, timer):
        libmetawear.mbl_mw_timer_remove(timer)

    def start(self, timer):
        libmetawear.mbl_mw_timer_start(timer)

    def stop(self, timer):
        libmetawear.mbl_mw_timer_stop(timer)
