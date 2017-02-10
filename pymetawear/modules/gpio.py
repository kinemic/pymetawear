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
from ctypes import cast, POINTER, c_float

from pymetawear import libmetawear
from pymetawear.exceptions import PyMetaWearException
from pymetawear.mbientlab.metawear.core import DataTypeId
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