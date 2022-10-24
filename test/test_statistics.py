# -*- coding: utf-8 -*-
import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import pypsa
from pypsa.statistics import get_bus_and_carrier


@pytest.fixture
def ac_dc_network_r():
    csv_folder = os.path.join(
        os.path.dirname(__file__),
        "..",
        "examples",
        "ac-dc-meshed",
        "ac-dc-data",
        "results-lopf",
    )
    return pypsa.Network(csv_folder)


def test_default_unsolved(ac_dc_network):
    df = ac_dc_network.statistics()
    assert not df.empty


def test_default_solved(ac_dc_network_r):
    df = ac_dc_network_r.statistics()
    assert not df.empty


def test_per_bus_carrier_unsolved(ac_dc_network):
    df = ac_dc_network.statistics(groups=get_bus_and_carrier)
    assert not df.empty


def test_per_bus_carrier_solved(ac_dc_network_r):
    df = ac_dc_network_r.statistics(groups=get_bus_and_carrier)
    assert not df.empty


def test_column_grouping_unsolved(ac_dc_network):
    df = ac_dc_network.statistics(groups=["bus0", "carrier"], comps={"Link"})
    assert not df.empty


def test_column_grouping_solved(ac_dc_network_r):
    df = ac_dc_network_r.statistics(groups=["bus0", "carrier"], comps={"Link"})
    assert not df.empty


def test_zero_profit_rule_branches(ac_dc_network_r):
    df = ac_dc_network_r.statistics(aggregate_time="sum")
    df = df.loc[["Line", "Link"]]
    assert np.allclose(df["Revenue"], df["Capital Expenditure"])
