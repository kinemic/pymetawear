#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

.. moduleauthor:: jhennrich <johannes.hennrich@kinemic.de>

Created: 2017-02-10

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import warnings
import logging
from functools import wraps
from ctypes import cast, POINTER, c_float, c_uint

from pymetawear import libmetawear
from pymetawear.exceptions import PyMetaWearException
from pymetawear.mbientlab.metawear.core import DataTypeId, Fn_DataPtr
from pymetawear.modules.base import PyMetaWearModule, Modules


log = logging.getLogger(__name__)


class GPIOModule(PyMetaWearModule):
    """MetaWear GPIO module implementation.

    :param ctypes.c_long board: The MetaWear board pointer value.
    :param bool debug: If ``True``, module prints out debug information.

    """
    def __init__(self, board, module_id, debug=False):
            super(GPIOModule, self).__init__(board, debug)
            self.module_id = module_id
            self.callback_dict = {}

            if self.module_id == Modules.MBL_MW_MODULE_NA:
                # No gpio present!
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
        return "GPIO"

    def set_digital_output(self, pin):
        libmetawear.mbl_mw_gpio_set_digital_output(self.board, pin)

    def clear_digital_output(self, pin):
        libmetawear.mbl_mw_gpio_clear_digital_output(self.board, pin)

    def get_digital_input_data_signal(self, pin):
        return libmetawear.mbl_mw_gpio_get_digital_input_data_signal(self.board, pin)

    def subscribe(self, data_signal, callback):
        callback_ptr = Fn_DataPtr(sensor_data(callback))
        self.callback_dict[data_signal] = callback_ptr
        libmetawear.mbl_mw_datasignal_subscribe(data_signal, callback_ptr)

    def unsubscribe(self, data_signal):
        libmetawear.mbl_mw_datasignal_unsubscribe(data_signal)
        del self.callback_dict[data_signal]

    def read(self, data_signal):
        libmetawear.mbl_mw_datasignal_read(data_signal)


def sensor_data(func):
    @wraps(func)
    def wrapper(data):
        if data.contents.type_id == DataTypeId.UINT32:
            epoch = int(data.contents.epoch)
            data_ptr = cast(data.contents.value, POINTER(c_uint))
            func((epoch, data_ptr.contents.value))
        else:
            raise PyMetaWearException('Incorrect data type id: {0}'.format(
                data.contents.type_id))
    return wrapper