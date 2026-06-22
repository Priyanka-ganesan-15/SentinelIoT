DEVICE_PROFILES: dict[str, dict[str, tuple[float, float]]] = {
    "camera": {
        "cpu": (15, 30),
        "memory": (25, 45),
        "battery": (70, 100),
    },
    "sensor": {
        "cpu": (2, 8),
        "memory": (5, 15),
        "battery": (80, 100),
    },
    "thermostat": {
        "cpu": (8, 15),
        "memory": (15, 30),
        "battery": (70, 100),
    },
    "smart_lock": {
        "cpu": (5, 12),
        "memory": (10, 25),
        "battery": (80, 100),
    },
    "gateway": {
        "cpu": (25, 50),
        "memory": (40, 70),
        "battery": (100, 100),
    },
}

DEVICE_WEIGHTS: dict[str, int] = {
    "sensor": 40,
    "camera": 25,
    "thermostat": 15,
    "smart_lock": 10,
    "gateway": 10,
}
