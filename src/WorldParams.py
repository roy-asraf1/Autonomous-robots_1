class WorldParams:
    lidar_limit = 300  # in cm
    lidar_noise = 1  # in cm
    CMPerPixel = 5
    accelerate_per_second = 1.0  # 1 meter per second
    max_speed = 0.5  # meters per second
    rotation_per_second = 60  # degrees per second
    min_motion_accuracy = 0  # minimum motion accuracy
    max_motion_accuracy = 1  # maximum motion accuracy
    min_rotation_accuracy = 0  # minimum rotation accuracy
    max_rotation_accuracy = 1  # maximum rotation accuracy
    SAFE_DISTANCE = 20
