"""Check the real driver against the integration's channel API mappings."""

import inspect

import pytest

from custom_components.smmultiio.data import API, SM_MAP
from SMcommonHA import Card
from SMcommonHA.button import Button
from SMcommonHA.const import COM_NOGET
from SMcommonHA.select import Select


@pytest.mark.parametrize(
    ("platform", "kind", "operation", "method"),
    [
        (platform, kind, operation, method)
        for platform, types in SM_MAP.items()
        for kind, metadata in types.items()
        for operation, method in metadata["com"].items()
        if method != COM_NOGET
    ],
)
def test_driver_method_accepts_expected_arguments(platform, kind, operation, method):
    function = getattr(API, method)
    assert callable(function), f"{platform}.{kind}: {method} is not callable"
    args = [object()]
    if platform == "datetime":
        if operation == "set":
            args.extend([2026, 1, 1, 0, 0, 0])
    elif platform == "button":
        if len(inspect.signature(function).parameters) == 2:
            args.append(1)
    else:
        channel_less = kind in {"motor", "watchdog_period", "watchdog_initial", "watchdog_count"}
        if not channel_less:
            args.append(1)
        if operation == "set":
            args.append(1)
    inspect.signature(function).bind(*args)


@pytest.mark.parametrize(
    ("option", "bits"), [("None", 0), ("Rising", 1), ("Falling", 2), ("Both", 3)]
)
def test_edge_selection_and_counter_reset_use_real_driver(monkeypatch, option, bits):
    import multiio

    registers = {
        multiio.I2C_MEM.OPTO_IT_RISING_ADD: 0,
        multiio.I2C_MEM.OPTO_IT_FALLING_ADD: 0,
    }
    writes = []
    monkeypatch.setattr(API, "__init__", lambda self, stack: None)
    monkeypatch.setattr(API, "_get_byte", lambda self, address: registers[address])

    def write(self, address, value):
        writes.append((address, value))
        registers[address] = value

    monkeypatch.setattr(API, "_set_byte", write)
    monkeypatch.setattr("time.sleep", lambda _: None)
    card = Card("test", "Test", "test", "Test", SM_MAP, API)
    entity = Select("edge", 0, "opto_edge", 2, card)
    entity.select_option(option)
    entity.update()
    assert entity.current_option == option
    assert bool(registers[multiio.I2C_MEM.OPTO_IT_RISING_ADD] & 2) == bool(bits & 1)
    assert bool(registers[multiio.I2C_MEM.OPTO_IT_FALLING_ADD] & 2) == bool(bits & 2)
    Button("reset", 0, "opto_reset", 2, card).press()
    assert writes[-1] == (multiio.I2C_MEM.OPTO_CNT_RST_ADD, 2)
