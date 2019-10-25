'''
@Author        : fineemb
@Github        : https://github.com/fineemb
@Description   : 
@Date          : 2019-10-25 00:52:13
@LastEditors   : fineemb
@LastEditTime  : 2019-10-26 07:05:32
'''
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.exceptions import (PlatformNotReady)
from homeassistant.components.fan import (SPEED_LOW, SPEED_HIGH,DOMAIN,
                                          FanEntity, SUPPORT_SET_SPEED,
                                          SUPPORT_OSCILLATE, SUPPORT_DIRECTION)
from homeassistant.const import (STATE_UNKNOWN, ATTR_ENTITY_ID, CONF_NAME, CONF_HOST, CONF_TOKEN, )
from datetime import timedelta
from miio import Device, DeviceException

import logging
_LOGGER = logging.getLogger(__name__)

ATTR_ANGLE = 'angle'
ATTR_ANION = 'anion'
ATTR_INIT = 'init'

SERVICE_SET_ANGLE = "yeelink_set_angle"
SERVICE_SET_ANION = "yeelink_set_anion"
SERVICE_SET_INIT = "yeelink_set_init"

SET_SERVICE_SCHEMA = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.entity_id
})


SERVICE_SCHEMA_ANGLE = SET_SERVICE_SCHEMA.extend({
    vol.Required(ATTR_ANGLE):
        vol.All(vol.Coerce(int), vol.Clamp(min=65, max=120))
})

SERVICE_SCHEMA_ANION = SET_SERVICE_SCHEMA.extend({
    vol.Required(ATTR_ANION):
        vol.All(vol.Coerce(str), vol.Clamp('off', 'on'))
})

SERVICE_SCHEMA_INIT = SET_SERVICE_SCHEMA.extend({
    vol.Required(ATTR_INIT):
        vol.All(vol.Coerce(str), vol.Clamp('off', 'on'))
})

YEELINKVEN_FAN_DEVICES = "yeelink.ven_fan.vf1"

def setup_platform(hass, config, add_devices, discovery_info=None):
    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    token = config.get(CONF_TOKEN)

    _LOGGER.info("Initializing Yeelink ven fan with host %s (token %s...)", host, token[:5])

    devices = []
    try:
        device = Device(host, token)
        yeelinkvenfan = YeelinkVenFan(device, name)
        devices.append(yeelinkvenfan)
    except DeviceException:
        _LOGGER.exception('Fail to setup Yeelink ven fan')
        raise PlatformNotReady

    add_devices(devices)
    hass.data[YEELINKVEN_FAN_DEVICES] = devices

    def service_handle(service):
        params = {key: value for key, value in service.data.items()
                  if key != ATTR_ENTITY_ID}
        entity_id = service.data[ATTR_ENTITY_ID]
        device = next((fan for fan in hass.data[YEELINKVEN_FAN_DEVICES] if
                           fan.entity_id == entity_id), None)
        if device is None:
            _LOGGER.warning("Unable to find Yeelink ven fan device %s",
                            str(entity_id))
            return

        if service.service == SERVICE_SET_ANGLE:
            device.set_angle(**params)

        if service.service == SERVICE_SET_ANION:
            device.set_anion(**params)

        if service.service == SERVICE_SET_INIT:
            device.set_init(**params)

    hass.services.register(DOMAIN, SERVICE_SET_ANGLE, service_handle, schema=SERVICE_SCHEMA_ANGLE)
    hass.services.register(DOMAIN, SERVICE_SET_ANION, service_handle, schema=SERVICE_SCHEMA_ANION)
    hass.services.register(DOMAIN, SERVICE_SET_INIT, service_handle, schema=SERVICE_SCHEMA_INIT)

class YeelinkVenFan(FanEntity):

    def __init__(self, device, name) -> None:
        self._device = device
        self._name = name
        self._supported_features = SUPPORT_OSCILLATE | SUPPORT_SET_SPEED
        self._is_on = False
        self._oscillate = False
        self._gears = 0
        self._anion_onoff = 1
        self._init_fan_opt = 0
        self._state_attrs = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def supported_features(self) -> int:
        return self._supported_features

    @property
    def should_poll(self):
        return True

    @property
    def is_on(self):
        return self._is_on

    @property
    def oscillating(self):
        """Return the oscillation state."""
        return self._oscillate 

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        return self._state_attrs

    @property
    def speed_list(self) -> list:
        return [SPEED_LOW,SPEED_HIGH]

    def update(self):
        try:
            bh_mode = self._device.send('get_prop', ["bh_mode"])[0]
            gears = self._device.send('get_prop', ["gears"])[0]
            swing_action = self._device.send('get_prop', ["swing_action"])[0]
            swing_angle = self._device.send('get_prop', ["swing_angle"])[0]
            bh_delayoff = self._device.send('get_prop', ["bh_delayoff"])[0]
            anion_onoff = self._device.send('get_prop', ["anion_onoff"])[0]
            init_fan_opt = self._device.send('get_prop', ["init_fan_opt"])[0]

            _LOGGER.debug('update Yeelink ven fan status: %s %s %s %s %s %s', bh_mode, gears, swing_action, swing_angle, anion_onoff, init_fan_opt)
            
            self._is_on = self.fan_mode(bh_mode) != 0
            self._oscillate = self.swing_on(swing_action) != 0
            self._gears = gears
            self._swing_angle = swing_angle != 0
            self._init_fan_opt = init_fan_opt != 0
            self._anion_onoff  = anion_onoff != 1
            self._state_attrs.update({
                "anion_onoff": anion_onoff,
                "gears": gears,
                "swing_action": swing_action,
                "swing_angle": swing_angle,
                "init_fan_opt": init_fan_opt
            })
            _LOGGER.debug('update Yeelink _is_on: %s', self._is_on)

        except DeviceException:
            _LOGGER.exception('Fail to get_prop from Yeelink ven fan')
            raise PlatformNotReady

    @property
    def speed(self) -> str:           
        if self._gears == 0:
            return SPEED_LOW
        if self._gears == 1:
            return SPEED_HIGH
    def oscillate(self, oscillating: bool) -> None:
        """Oscillate the fan."""
        if oscillating:
            self._device.send('set_swing', ["swing",0])
        else:
            self._device.send('set_swing', ["stop",0])
            
    def angle(self) -> int:           
        return self._swing_angle

    def anion(self) -> bool:           
        return self._anion_onoff

    def init(self) -> bool:           
        return self._init_fan_opt    
            
    def fan_mode(self, bh_mode):
        if bh_mode == "bh_off":
            return False
        if bh_mode == "coolwind":
            return True

    def swing_on(self, swing) -> None:
        if swing == "swing":
            return True
        else:
            return False

    def set_speed(self, speed: str) -> None:
        if speed == SPEED_LOW:
            self._device.send('set_gears_idx', [0])
            self._gears = 0
        elif speed == SPEED_HIGH:
            self._device.send('set_gears_idx', [1])
            self._gears = 1

    def set_angle(self, angle: int) -> None:
        """ 风口角度 """
        self._device.send('set_swing', ["angle",angle])

    def set_anion(self, anion: str) -> None:
        """ 负离子 """
        if anion == 'on':
            self._device.send('set_anion', [1])
        else:
            self._device.send('set_anion', [0])

    def set_init(self, init: str) -> None:
        """ 上电初始化 """
        if init == 'on':
            self._device.send('set_init_fan_opt', [1])
        else:
            self._device.send('set_init_fan_opt', [0])

    def turn_on(self, speed: str = None, **kwargs) -> None:
        if not self._is_on:
            self._device.send('set_bh_mode', ["coolwind"])
            self._is_on = True
        if speed:
            self.set_speed(speed)

    def turn_off(self, **kwargs) -> None:
        if self._is_on:
            self._device.send('set_bh_mode', ["bh_off"])
            self._is_on = False
