# Autonomous Drone Simulator

This project simulates an autonomous drone navigating a map using LIDAR sensors and AI algorithms. The drone can either explore the map or stay centered on the path using two AI algorithms: the default AI and the center AI.

### Explanation of the project
In this project we convert a java project of Simulation Drone to python.
The project is about a drone that navigates through a map using LIDAR sensors.
The project includes two AI algorithms for drone navigation: Default AI and Center AI.
In the project we have buttons to control the drone, such as start/stop, speed up/slow down, rotate in angles, toggle AI, and toggle AI center.
The return home function is not implemented in the project - only needed in the future expanded project.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [AI Algorithms](#ai-algorithms)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Autonomous Drone Simulator is a Python-based project that models a drone navigating through a map using LIDAR sensors. The project includes two AI algorithms for drone navigation:

- **Default AI**: Allows the drone to explore the map and avoid obstacles.
- **Center AI**: Keeps the drone as centered on the path as possible.

## Features

- **LIDAR Sensors**: The drone is equipped with LIDAR sensors to detect obstacles and navigate the map.
- **AI Algorithms**: Implemented AI algorithms for autonomous navigation.
- **Real-time Simulation**: Real-time visualization of the drone's path and sensor data.
- **Interactive Controls**: Control the simulation using keyboard and mouse inputs.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/autonomous-robots.git
    cd autonomous-robots
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the simulation:**

    ```bash
    python SimulationWindow.py
    ```

## Usage

### Controls

- **Start/Stop**: Toggle the drone's movement.
- **Speed Up/Slow Down**: Adjust the drone's speed.
- **Rotate**: Spin the drone by various angles.
- **Toggle AI**: Switch to use AI algorithm.
- **Toggle AI Center**: Switch to use AI center algorithm.

## AI Algorithms

### Default AI

The default AI enables the drone to explore the map, avoid obstacles, and mark visited areas. The drone uses LIDAR sensors to detect obstacles and navigates based on sensor data.

### Center AI

The center AI algorithm ensures the drone stays as close to the center of the path as possible. The algorithm calculates the center of the path and adjusts the drone's movement to stay centered.

## Project Structure

```plaintext
.
├── src
│   ├── AutoAlgo1.py         # AI algorithms for drone navigation
│   ├── CPU.py               # CPU simulation for handling multiple functions
│   ├── Drone.py             # Drone class and movement logic
│   ├── Lidar.py             # Lidar sensor implementation
│   ├── Map.py               # Map class for loading and displaying the map
│   ├── Point.py             # Point class for coordinates
│   ├── SimulationWindow.py  # Main simulation window and controls
│   ├── Tools.py             # Utility functions
│   ├── WorldParams.py       # Parameters for the world and simulation
├── assets
│   ├── maps                 # Folder containing map images
├── requirements.txt         # List of required packages
├── README.md                # Project README file
└── main.py                  # Main entry point for the simulation
```

## Contributing

Contributions are welcome! If you would like to contribute, please fork the repository and use a feature branch. Pull requests should be made against the `main` branch.

1. **Fork the repository**

2. **Create a feature branch:**

    ```bash
    git checkout -b feature/your-feature-name
    ```

3. **Commit your changes:**

    ```bash
    git commit -m 'Add some feature'
    ```

4. **Push to the branch:**

    ```bash
    git push origin feature/your-feature-name
    ```

5. **Open a pull request**

## Sources
- The project is based on the [Autonomous Drone Simulator](https://github.com/vection/DroneSimulator)
- The task of the project is from the course "Autonomous Robots" [The Task](https://docs.google.com/document/d/1eo34T_M7jfduRZm_oevy94YY2LkGLzRT/edit?usp=sharing&ouid=113711744349547563645&rtpof=true&sd=true)

## Contributors
Elor Israeli, Naor Ladani, Roy Asraf

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
