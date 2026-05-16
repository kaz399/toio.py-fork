# -*- coding: utf-8 -*-
import struct
import pytest
from unittest.mock import AsyncMock, MagicMock
from toio.cube.api.configuration import (
    SpeakerMute,
    SetSpeakerMute,
    ResetConfiguration,
    ResponseSpeakerMuteSettings,
    ResponseConfigurationReset,
    Configuration
)
from toio.device_interface import CubeInterface
from toio.toio_uuid import ToioUuid
from toio.cube import ToioCoreCube
from toio.scanner import BLEScanner

# -----------------------------------------------------------------------------
# 1. Unit Tests (Logic Verification)
# -----------------------------------------------------------------------------

def test_set_speaker_mute_bytes():
    # Unmute
    command = SetSpeakerMute(SpeakerMute.Unmute)
    assert bytes(command) == b"\x33\x00\x00"
    
    # MuteAll
    command = SetSpeakerMute(SpeakerMute.MuteAll)
    assert bytes(command) == b"\x33\x00\x01"
    
    # MuteSystemOnly
    command = SetSpeakerMute(SpeakerMute.MuteSystemOnly)
    assert bytes(command) == b"\x33\x00\x02"

def test_reset_configuration_bytes():
    command = ResetConfiguration()
    assert bytes(command) == b"\x0f\x00"

def test_response_speaker_mute_parsing():
    # Success
    payload = b"\xb3\x00\x00"
    response = ResponseSpeakerMuteSettings(payload)
    assert response.result is True
    
    # Failure (e.g., button not pressed)
    payload = b"\xb3\x00\x01"
    response = ResponseSpeakerMuteSettings(payload)
    assert response.result is False

def test_response_configuration_reset_parsing():
    # Success
    payload = b"\x8f\x00\x00"
    response = ResponseConfigurationReset(payload)
    assert response.result is True
    
    # Failure
    payload = b"\x8f\x00\x01"
    response = ResponseConfigurationReset(payload)
    assert response.result is False


# -----------------------------------------------------------------------------
# 2. Semi-normal Integration Tests (Real Device)
# Verification of failure when button is NOT pressed
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_speaker_mute_failure_without_button():
    device_list = await BLEScanner.scan(1)
    assert len(device_list) > 0
    cube = ToioCoreCube(device_list[0].interface)
    await cube.connect()
    
    print("\n** Testing Speaker Mute (Should fail as button is NOT pressed)")
    
    # Track response
    received_response = None
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    async def notification_handler(payload):
        nonlocal received_response
        response = Configuration.is_my_data(payload)
        if isinstance(response, ResponseSpeakerMuteSettings):
            received_response = response
            if not future.done():
                future.set_result(True)

    await cube.api.configuration.register_notification_handler(notification_handler)
    
    # Request mute
    await cube.api.configuration.set_speaker_mute(SpeakerMute.MuteAll)
    
    try:
        # Wait for response with timeout
        await asyncio.wait_for(future, timeout=5.0)
        assert received_response is not None
        print(f"** Result: {received_response.result} (Expected: False)")
        assert received_response.result is False
    except asyncio.TimeoutError:
        pytest.fail("Notification timeout: Cube did not respond to Speaker Mute request")
    finally:
        await cube.disconnect()

@pytest.mark.asyncio
async def test_configuration_reset_failure_without_button():
    device_list = await BLEScanner.scan(1)
    assert len(device_list) > 0
    cube = ToioCoreCube(device_list[0].interface)
    await cube.connect()
    
    print("\n** Testing Config Reset (Should fail as button is NOT pressed)")
    
    received_response = None
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    async def notification_handler(payload):
        nonlocal received_response
        response = Configuration.is_my_data(payload)
        if isinstance(response, ResponseConfigurationReset):
            received_response = response
            if not future.done():
                future.set_result(True)

    await cube.api.configuration.register_notification_handler(notification_handler)
    
    # Request reset
    await cube.api.configuration.reset_configuration()
    
    try:
        await asyncio.wait_for(future, timeout=5.0)
        assert received_response is not None
        print(f"** Result: {received_response.result} (Expected: False)")
        assert received_response.result is False
    except asyncio.TimeoutError:
        pytest.fail("Notification timeout: Cube did not respond to Config Reset request")
    finally:
        await cube.disconnect()

import asyncio
