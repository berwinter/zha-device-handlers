"""Device handler for Bosch RBSH-RTH0-ZB-EU thermostat."""

from zigpy.profiles import zha
import zigpy.types as t
from zigpy.quirks import CustomDevice
from zigpy.zcl.clusters.homeautomation import Diagnostic
from zigpy.zcl.clusters.general import Basic, Identify, Ota, Time, ZCLAttributeDef
from zigpy.zcl.clusters.measurement import RelativeHumidity
from zigpy.zcl.clusters.hvac import Thermostat, UserInterface
from zigpy.zcl.clusters.homeautomation import Diagnostic

from zhaquirks.bosch import BOSCH
from zhaquirks import CustomCluster
from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)

class BoschOperatingMode(t.enum8):
    Schedule = 0x00
    Manual = 0x01
    Pause = 0x05


class State(t.enum8):
    Off = 0x00
    On = 0x01


class BoschDisplayOrientation(t.enum8):
    Normal = 0x00
    Flipped = 0x01


class BoschDisplayedTemperature(t.enum8):
    Target = 0x00
    Measured = 0x01


class BoschThermostatCluster(CustomCluster, Thermostat):
    """Bosch thermostat cluster."""

    class AttributeDefs(Thermostat.AttributeDefs):
        operating_mode = ZCLAttributeDef(
            id=t.uint16_t(0x4007),
            type=BoschOperatingMode,
            is_manufacturer_specific=True,
        )

        pi_heating_demand = ZCLAttributeDef(
            id=t.uint16_t(0x4020),
            # Values range from 0-100
            type=t.uint8_t,
            is_manufacturer_specific=True,
        )

        attr_0x4022 = ZCLAttributeDef(
            id=t.uint16_t(0x4022),
            type=t.enum8,
            is_manufacturer_specific=True,
        )

        attr_0x4023 = ZCLAttributeDef(
            id=t.uint16_t(0x4023),
            type=t.enum8,
            is_manufacturer_specific=True,
        )

        attr_0x4024 = ZCLAttributeDef(
            id=t.uint16_t(0x4024),
            type=t.enum8,
            is_manufacturer_specific=True,
        )

        attr_0x4025 = ZCLAttributeDef(
            id=t.uint16_t(0x4025),
            type=t.enum8,
            is_manufacturer_specific=True,
        )

        window_open = ZCLAttributeDef(
            id=t.uint16_t(0x4042),
            type=State,
            is_manufacturer_specific=True,
        )

        boost = ZCLAttributeDef(
            id=t.uint16_t(0x4043),
            type=State,
            is_manufacturer_specific=True,
        )

        attr_0x4050 = ZCLAttributeDef(
            id=t.uint16_t(0x4050),
            type=t.enum8,
            is_manufacturer_specific=True,
        )

        attr_0x4051 = ZCLAttributeDef(
            id=t.uint16_t(0x4051),
            type=t.int16s,
            is_manufacturer_specific=True,
        )

        attr_0x4052 = ZCLAttributeDef(
            id=t.uint16_t(0x4052),
            type=t.int16s,
            is_manufacturer_specific=True,
        )

        attr_0x405b = ZCLAttributeDef(
            id=t.uint16_t(0x405b),
            type=t.enum8,
            is_manufacturer_specific=True,
        )

        attr_0x4060 = ZCLAttributeDef(
            id=t.uint16_t(0x4060),
            type=t.enum8,
            is_manufacturer_specific=True,
        )

        attr_0x4061 = ZCLAttributeDef(
            id=t.uint16_t(0x4061),
            type=t.enum8,
            is_manufacturer_specific=True,
        )

        attr_0x4062 = ZCLAttributeDef(
            id=t.uint16_t(0x4062),
            type=t.enum8,
            is_manufacturer_specific=True,
        )

        attr_0x4063 = ZCLAttributeDef(
            id=t.uint16_t(0x4063),
            type=t.enum8,
            is_manufacturer_specific=True,
        )

        attr_0x5000 = ZCLAttributeDef(
            id=t.uint16_t(0x5000),
            type=t.bitmap8,
            is_manufacturer_specific=True,
        )

        attr_0x501f = ZCLAttributeDef(
            id=t.uint16_t(0x501f),
            type=t.enum8,
            is_manufacturer_specific=True,
        )

class BoschUserInterfaceCluster(CustomCluster, UserInterface):
    """Bosch UserInterface cluster."""

    class AttributeDefs(UserInterface.AttributeDefs):
        attr_0x4032 = ZCLAttributeDef(
            id=t.uint16_t(0x4032),
            type=t.enum8,
            is_manufacturer_specific=True,
        )

        attr_0x4033 = ZCLAttributeDef(
            id=t.uint16_t(0x4033),
            type=t.enum8,
            is_manufacturer_specific=True,
        )

        display_ontime = ZCLAttributeDef(
            id=t.uint16_t(0x403a),
            # Usable values range from 2-30
            type=t.uint8_t,
            is_manufacturer_specific=True,
        )

        display_brightness = ZCLAttributeDef(
            id=t.uint16_t(0x403b),
            # Values range from 0-10
            type=t.uint8_t,
            is_manufacturer_specific=True,
        )

        attr_0x406a = ZCLAttributeDef(
            id=t.uint16_t(0x406a),
            type=t.enum8,
            is_manufacturer_specific=True,
        )

        attr_0x406b = ZCLAttributeDef(
            id=t.uint16_t(0x406b),
            type=t.enum8,
            is_manufacturer_specific=True,
        )

class BoschThermostat(CustomDevice):
    """Bosch thermostat custom device."""

    signature = {
        MODELS_INFO: [(BOSCH, "RBSH-RTH0-ZB-EU")],
        ENDPOINTS: {
            # <SimpleDescriptor endpoint=1 profile=260 device_type=769
            # device_version=1
            # input_clusters=[0, 3, 513, 516, 1029, 2821]
            # output_clusters=[10, 25]>
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.THERMOSTAT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Thermostat.cluster_id,
                    UserInterface.cluster_id,
                    RelativeHumidity.cluster_id,
                    Diagnostic.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    BoschThermostatCluster,
                    BoschUserInterfaceCluster,
                    RelativeHumidity.cluster_id,
                    Diagnostic.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            },
        },
    }

