# Dynamicisland app

## Description

Dynamicisland is a cross-platform application built with Flet, implementing an iOS-style Dynamic Island UI/UX. **Currently, the app only works on Windows.** The app can run as a desktop or web application and can be built for Android, iOS, macOS, Linux, and Windows (Windows support only).

## Features & Functionality

- **Dynamic Island UI**: Animates and displays a floating island element similar to iOS, showing notifications, media controls, and contextual information.
- **Media Integration**: Detects and displays currently playing media, with interactive controls.
- **Custom Animations**: Uses Blender-generated animation data for smooth transitions and effects.
- **Modular Architecture**: Code is organized into layers, functions, and animation managers for easy extension and maintenance.
- **Persistent Storage**: Stores user/session data and temporary files for stateful behavior.
- **Cross-Platform Build**: Easily build and package the app for all major desktop and mobile platforms.

## Project Structure

- `main_curves.py` — main entry point
- `DynamicIsland/` — application source code
  - `src/` — core logic, functions, animations, assets
    - `animation_functions/` — animation management
    - `assets/` — icons, splash screens, animation data
    - `dynamic_island/` — main Dynamic Island class
    - `functions/` — utility and media checker functions
    - `layers/` — UI layers (e.g., music, notifications)
    - `storage/` — persistent and temporary data
  - `config/` — configuration files
- `Blender Files/` — Blender files for animation creation

## How It Works

1. **Startup**: The app initializes the Flet UI and loads configuration and assets.
2. **Dynamic Island Rendering**: The main Dynamic Island component is rendered, listening for system/media events.
3. **Animation**: Animations are triggered based on user actions or system events, using precomputed Blender data.
4. **Media & Notifications**: The app checks for active media sessions and displays relevant controls and notifications in the island.
5. **State Management**: User interactions and app state are stored for a seamless experience across sessions.

## Running the App

### uv

- Desktop:
  ```
  uv run flet run
  ```
- Web:
  ```
  uv run flet run --web
  ```

### Poetry

- Install dependencies:
  ```
  poetry install
  ```
- Desktop:
  ```
  poetry run flet run
  ```
- Web:
  ```
  poetry run flet run --web
  ```

More details: [Getting Started Guide](https://flet.dev/docs/getting-started/)

## Building the App

- Windows: `flet build windows -v`

Build & publish documentation:
- [Windows Packaging Guide](https://flet.dev/docs/publish/windows/)