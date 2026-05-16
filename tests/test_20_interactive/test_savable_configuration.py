# -*- coding: utf-8 -*-
# ************************************************************
#
#     test_savable_configuration.py
#
#     Copyright 2026 Yabe Kazuhiro
#
# ************************************************************

import asyncio
from logging import getLogger

import pytest

from toio.cube import ToioCoreCube
from toio.cube.api.configuration import (
    Configuration,
    SpeakerMute,
    ResponseSpeakerMuteSettings,
    ResponseConfigurationReset
)
from toio.cube.api.sound import Note, MidiNote
from toio.scanner import BLEScanner

logger = getLogger(__name__)


@pytest.mark.asyncio
async def test_speaker_mute(interactive, confirm, get_result):
    device_list = await BLEScanner.scan(1)
    assert len(device_list)
    cube = ToioCoreCube(device_list[0].interface)
    logger.info("** CONNECTING...")
    await cube.connect()
    logger.info("** CONNECTED")

    from toio.cube.api.button import Button, ButtonInformation, ButtonState
    
    received_response = None
    async def notification_handler(payload):
        nonlocal received_response
        response = Configuration.is_my_data(payload)
        if isinstance(response, ResponseSpeakerMuteSettings):
            received_response = response
            logger.info("** RECEIVED RESPONSE: %s", "SUCCESS" if response.result else "FAILED")

    await cube.api.configuration.register_notification_handler(notification_handler)

    # 1. Mute All
    logger.info("===== MUTE ALL TEST =====")
    logger.info(">> PLEASE HOLD THE CUBE BUTTON")
    
    button_event = asyncio.Event()
    def button_handler(payload):
        button_info = Button.is_my_data(payload)
        if isinstance(button_info, ButtonInformation):
            if button_info.state == ButtonState.PRESSED:
                button_event.set()
            else:
                button_event.clear()

    await cube.api.button.register_notification_handler(button_handler)
    await button_event.wait()
    
    logger.info(">> BUTTON DETECTED. SENDING MUTE COMMAND...")
    received_response = None
    await cube.api.configuration.set_speaker_mute(SpeakerMute.MuteAll)
    
    # Wait for response or timeout
    for _ in range(20):
        if received_response is not None:
            break
        await asyncio.sleep(0.1)
    
    if received_response and received_response.result:
        logger.info("** MUTE ALL SUCCESS")
    else:
        logger.info("** MUTE ALL FAILED")
    
    logger.info(">> PLAYING SOUND (Should be SILENT)")
    await cube.api.sound.play_midi(repeat=1, midi_notes=[MidiNote(duration_ms=1000, note=Note.C4, volume=255)])
    await asyncio.sleep(2)

    # 2. Unmute
    logger.info("===== UNMUTE TEST =====")
    logger.info(">> PLEASE HOLD THE CUBE BUTTON AGAIN")
    button_event.clear()
    await button_event.wait()
    
    logger.info(">> BUTTON DETECTED. SENDING UNMUTE COMMAND...")
    received_response = None
    await cube.api.configuration.set_speaker_mute(SpeakerMute.Unmute)
    
    for _ in range(20):
        if received_response is not None:
            break
        await asyncio.sleep(0.1)
        
    if received_response and received_response.result:
        logger.info("** UNMUTE SUCCESS")
    else:
        logger.info("** UNMUTE FAILED")
    
    logger.info(">> PLAYING SOUND (Should be AUDIBLE)")
    await cube.api.sound.play_midi(repeat=1, midi_notes=[MidiNote(duration_ms=1000, note=Note.C4, volume=255)])
    await asyncio.sleep(2)

    await cube.api.button.unregister_notification_handler(button_handler)
    await cube.api.configuration.unregister_notification_handler(notification_handler)
    logger.info("** DISCONNECTING")
    await cube.disconnect()
    logger.info("** DISCONNECTED")


@pytest.mark.asyncio
async def test_configuration_reset(interactive, confirm, get_result):
    device_list = await BLEScanner.scan(1)
    assert len(device_list)
    cube = ToioCoreCube(device_list[0].interface)
    logger.info("** CONNECTING...")
    await cube.connect()
    logger.info("** CONNECTED")

    logger.info("===== CONFIGURATION RESET TEST =====")
    
    from toio.cube.api.button import Button, ButtonInformation, ButtonState
    
    received_response = None
    async def notification_handler(payload):
        nonlocal received_response
        response = Configuration.is_my_data(payload)
        if isinstance(response, ResponseConfigurationReset):
            received_response = response
            logger.info("** RECEIVED RESPONSE: %s", "SUCCESS" if response.result else "FAILED")

    await cube.api.configuration.register_notification_handler(notification_handler)

    logger.info(">> PLEASE HOLD THE CUBE BUTTON")
    button_event = asyncio.Event()
    def button_handler(payload):
        button_info = Button.is_my_data(payload)
        if isinstance(button_info, ButtonInformation):
            if button_info.state == ButtonState.PRESSED:
                button_event.set()
            else:
                button_event.clear()

    await cube.api.button.register_notification_handler(button_handler)
    await button_event.wait()
    
    logger.info(">> BUTTON DETECTED. SENDING RESET COMMAND...")
    received_response = None
    await cube.api.configuration.reset_configuration()
    
    for _ in range(20):
        if received_response is not None:
            break
        await asyncio.sleep(0.1)
        
    if received_response and received_response.result:
        logger.info("** RESET SUCCESS")
    else:
        logger.info("** RESET FAILED")
    
    await cube.api.button.unregister_notification_handler(button_handler)
    await cube.api.configuration.unregister_notification_handler(notification_handler)

    logger.info("** DISCONNECTING")
    await cube.disconnect()
    logger.info("** DISCONNECTED")
