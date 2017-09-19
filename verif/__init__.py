#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 jinhuan<jinhuanzhu@seniverse.com>. All rights reserved.

import os
from .driver import verif
import verif.driver as driver
from .statistics_utils import StatsUtils
from .verif_methods import VerifStandard, VerifDiagnostic

modu_dir = verif_path = os.path.split(os.path.dirname(__file__))[0]
