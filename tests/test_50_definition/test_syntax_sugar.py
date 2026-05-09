#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ************************************************************
#
#     test_syntax_sugar.py
#
#     Copyright 2026 Yabe Kazuhiro
#
# ************************************************************

import pytest
from toio.cube import ToioCoreCube, MultipleToioCoreCubes
from toio.scanner.ble import UniversalBleScanner

@pytest.mark.asyncio
async def test_toio_core_cube_syntax_sugar(mocker):
    # Mock UniversalBleScanner.scan
    scan_mock = mocker.patch.object(UniversalBleScanner, 'scan', return_value=[])
    
    # Initialize with keyword arguments
    cube = ToioCoreCube(strategy="quick", timeout=1.23, sort="local_name")
    
    # Trigger scan
    await cube.scan()
    
    # Check if scan was called with correct keyword arguments
    # Note: ToioCoreCube.scan calls scanner().scan(1, *args, **kwargs)
    scan_mock.assert_called_once_with(1, strategy="quick", timeout=1.23, sort="local_name")

@pytest.mark.asyncio
async def test_multiple_toio_core_cubes_syntax_sugar(mocker):
    # Mock UniversalBleScanner.scan
    scan_mock = mocker.patch.object(UniversalBleScanner, 'scan', return_value=[])
    
    # Initialize with keyword arguments
    cubes = MultipleToioCoreCubes(2, strategy="best", timeout=5.0)
    
    # Trigger scan
    await cubes.scan()
    
    # Check if scan was called with correct keyword arguments
    # Note: MultipleToioCoreCubes.scan calls scanner().scan(num, *args, **kwargs)
    scan_mock.assert_called_once_with(2, strategy="best", timeout=5.0)

@pytest.mark.asyncio
async def test_syntax_sugar_with_positional_args(mocker):
    scan_mock = mocker.patch.object(UniversalBleScanner, 'scan', return_value=[])
    
    # Mixed positional and keyword arguments
    # scanner_args = (sort, timeout)
    cube = ToioCoreCube(scanner_args=("rssi", 10.0), strategy="quick")
    
    await cube.scan()
    
    # Should combine both
    scan_mock.assert_called_once_with(1, "rssi", 10.0, strategy="quick")
