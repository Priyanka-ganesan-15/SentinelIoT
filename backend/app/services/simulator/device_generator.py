from __future__ import annotations

import random
import uuid
from datetime import datetime, timezone

from app.models.device import Device
from app.services.simulator.device_profiles import DEVICE_PROFILES, DEVICE_WEIGHTS


class DeviceGenerator:
    def __init__(self) -> None:
        self._type_counter: dict[str, int] = {key: 0 for key in DEVICE_PROFILES}

    def generate_devices(self, device_count: int) -> list[Device]:
        devices: list[Device] = []
        for _ in range(device_count):
            device_type = self._pick_weighted_type()
            profile = DEVICE_PROFILES[device_type]
            self._type_counter[device_type] += 1

            cpu = self._sample_range(profile["cpu"])
            memory = self._sample_range(profile["memory"])
            battery = self._sample_range(profile["battery"])

            devices.append(
                Device(
                    id=str(uuid.uuid4()),
                    name=f"{device_type.replace('_', ' ').title().replace(' ', '')}-{self._type_counter[device_type]}",
                    device_type=device_type,
                    state="healthy",
                    cpu=cpu,
                    memory=memory,
                    battery=battery,
                    trust_score=100.0,
                    created_at=datetime.now(timezone.utc),
                )
            )

        return devices

    def _pick_weighted_type(self) -> str:
        types = list(DEVICE_WEIGHTS.keys())
        weights = list(DEVICE_WEIGHTS.values())
        return random.choices(types, weights=weights, k=1)[0]

    @staticmethod
    def _sample_range(bounds: tuple[float, float]) -> float:
        low, high = bounds
        return round(random.uniform(low, high), 2)
