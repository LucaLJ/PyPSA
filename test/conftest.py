#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 18:29:48 2022.

@author: fabian
"""

import os

import numpy as np
import pandas as pd
import pytest

import pypsa

SUPPORTED_APIS = ["pyomo", "linopy", "native"]
SOLVER_NAME = "glpk"


def optimize(n, api, *args, **kwargs):
    if api == "linopy":
        return n.optimize(solver_name=SOLVER_NAME, *args, **kwargs)
    elif api == "pyomo":
        return n.lopf(pyomo=True, solver_name=SOLVER_NAME, *args, **kwargs)
    elif api == "native":
        return n.lopf(pyomo=False, solver_name=SOLVER_NAME, *args, **kwargs)
    else:
        raise ValueError(f"api must be one of {SUPPORTED_APIS}")


@pytest.fixture(scope="function")
def scipy_network():
    csv_folder = os.path.join(
        os.path.dirname(__file__),
        "..",
        "examples",
        "scigrid-de",
        "scigrid-with-load-gen-trafos",
    )

    return pypsa.Network(csv_folder)


@pytest.fixture(scope="module")
def ac_dc_network():
    csv_folder = os.path.join(
        os.path.dirname(__file__), "..", "examples", "ac-dc-meshed", "ac-dc-data"
    )
    n = pypsa.Network(csv_folder)
    n.links_t.p_set.drop(columns=n.links_t.p_set.columns, inplace=True)
    return n


@pytest.fixture(scope="module")
def ac_dc_network_multiindexed(ac_dc_network):
    n = ac_dc_network
    n.snapshots = pd.MultiIndex.from_product([[2013], n.snapshots])
    gens_i = n.generators.index
    n.generators_t.p[gens_i] = np.random.rand(len(n.snapshots), len(gens_i))
    return n
