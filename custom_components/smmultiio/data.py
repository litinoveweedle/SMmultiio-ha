FULL_NAME = "Multi-IO"
LINK = "https://sequentmicrosystems.com/products/multi-io-8-layer-stackable-hat-for-raspberry-pi"


import multiio

API = multiio.SMmultiio
DOMAIN = "smmultiio"
NAME_PREFIX = "mio"

SM_MAP = {
    "select": {
        "opto_edge": {
            "chan_no": 4,
            "optional": True,
            "com": {"get": "get_opto_edge", "set": "set_opto_edge"},
            "option_map": {"None": 0, "Rising": 1, "Falling": 2, "Both": 3},
        },
    },
    "button": {
        "opto_reset": {
            "chan_no": 4,
            "optional": True,
            "com": {"set": "reset_opto_counter"},
        },
        "encoder_reset": {
            "chan_no": 2,
            "optional": True,
            "com": {"set": "reset_opto_encoder_counter"},
        },
        "watchdog_reload": {
            "chan_no": 1,
            "optional": True,
            "com": {"set": "wdt_reload"},
        },
    },
    "datetime": {
        "rtc": {
            "chan_no": 1,
            "com": {
                "get": "get_rtc",
                "set": "set_rtc",
            },
            "icon": {
                "on": "mdi:calendar",
            },
        },
    },
    "binary_sensor": {
        "opto_in": {
            "chan_no": 4,
            "uom": "",
            "com": {
                "get": "get_opto",
            },
            "icon": {
                "on": "mdi:numeric-1",
            },
        },
    },
    "sensor":  {
        "opto_count": {
            "chan_no": 4,
            "optional": True,
            "com": {"get": "get_opto_counter"},
        },
        "encoder_count": {
            "chan_no": 2,
            "optional": True,
            "com": {"get": "get_opto_encoder_counter"},
        },
        "opto_frequency": {
            "chan_no": 4,
            "optional": True,
            "uom": "Hz",
            "com": {"get": "get_opto_frequency"},
        },
        "opto_pwm": {
            "chan_no": 4,
            "optional": True,
            "uom": "%",
            "com": {"get": "get_opto_pwm_fill"},
        },
        "watchdog_count": {
            "chan_no": 1,
            "optional": True,
            "com": {"get": "wdt_get_reset_count"},
        },
        "rtd_res": {
            "chan_no": 2,
            "uom": "Ohm",
            "com": {
                "get": "get_rtd_res",
            },
            "icon": {
                "on": "mdi:omega",
                "off": "mdi:omega"
            },
            "optional": True,
        },
        "rtd_temp": {
            "chan_no": 2,
            "uom": "°C",
            "com": {
                "get": "get_rtd_temp",
            },
            "icon": {
                "on": "mdi:thermometer",
                "off": "mdi:thermometer"
            },
        },
        "iin": {
            "chan_no": 2,
            "uom": "mA",
            "com": {
                "get": "get_i_in",
            },
            "icon": {
                "on": "mdi:current-dc",
                "off": "mdi:current-dc"
            },
        },
        "uin": {
            "chan_no": 2,
            "uom": "V",
            "com": {
                "get": "get_u_in",
            },
            "icon": {
                "on": "mdi:flash",
                "off": "mdi:flash"
            },
        },
    },
    "switch": {
        "encoder_enable": {
            "chan_no": 2,
            "optional": True,
            "com": {"get": "get_opto_encoder_state", "set": "set_opto_encoder_state"},
        },
        "led": {
            "chan_no": 6,
            "com": {
                "get": "get_led",
                "set": "set_led"
            },
            "icon": {
                "on": "mdi:led-on",
                "off": "mdi:led-off"
            },
        },
        "relay": {
            "chan_no": 2,
            "com": {
                "get": "get_relay",
                "set": "set_relay"
            },
            "icon": {
                "on": "mdi:toggle-switch-variant",
                "off": "mdi:toggle-switch-variant-off",
            },
        },
    },
    "number": {
        "watchdog_period": {
            "chan_no": 1,
            "optional": True,
            "uom": "s",
            "min_value": 1,
            "max_value": 65535,
            "step": 1,
            "com": {"get": "wdt_get_period", "set": "wdt_set_period"},
        },
        "watchdog_initial": {
            "chan_no": 1,
            "optional": True,
            "uom": "s",
            "min_value": 1,
            "max_value": 65535,
            "step": 1,
            "com": {"get": "wdt_get_init_period", "set": "wdt_set_init_period"},
        },
        "uout": {
            "chan_no": 2,
            "uom": "V",
            "min_value": 0.0,
            "max_value": 10.0,
            "step": 0.01,
            "com": {
                "get": "get_u_out",
                "set": "set_u_out"
            },
            "icon": {
                "on": "mdi:flash",
                "off": "mdi:flash"
            },
        },
        "iout": {
            "chan_no": 2,
            "uom": "mA",
            "min_value": 4.0,
            "max_value": 20.0,
            "step": 0.01,
            "com": {
                "get": "get_i_out",
                "set": "set_i_out"
            },
            "icon": {
                "on": "mdi:current-dc",
                "off": "mdi:current-dc"
            },
        },
        "servo": {
            "chan_no": 2,
            "uom": "%",
            "min_value": -140.0,
            "max_value": +140.0,
            "step": 0.1,
            "com": {
                "get": "get_servo",
                "set": "set_servo"
            },
            "icon": {
                "on": "mdi:rotate-3d-variant",
                "off": "mdi:rotate-3d-variant"
            },
        },
        "motor": {
            "chan_no": 1,
            "uom": "%",
            "min_value": -100.0,
            "max_value": +100.0,
            "step": 0.1,
            "com": {
                "get": "get_motor",
                "set": "set_motor"
            },
            "icon": {
                "on": "mdi:engine",
                "off": "mdi:engine"
            },
        },
    },
}
