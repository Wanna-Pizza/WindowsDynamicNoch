# Dynamicisland app


![image](https://github.com/user-attachments/assets/370921ef-f3d2-4703-bfa7-1e1c88cd0227)


## Description

## CURRENTLY NOT POSSIBLE TO BUILD DUE COMPLAINS FLET ON PYWIN32

Dynamicisland is a cross-platform application built with Flet, implementing an iOS-style Dynamic Island UI/UX. **Currently, the app only works on Windows.** The app can run as a desktop or web application and can be built for Android, iOS, macOS, Linux, and Windows (Windows support only).


https://github.com/user-attachments/assets/045d5094-4772-465e-82ca-d879ad286d93



## Features & Functionality

- **Dynamic Island UI**: Animates and displays a floating island element similar to iOS, showing notifications, media controls, and contextual information.
- **Media Integration**: Detects and displays currently playing media, with interactive controls.
- **Custom Animations**: Uses Blender-generated animation data for smooth transitions and effects.
- **Modular Architecture**: Code is organized into layers, functions, and animation managers for easy extension and maintenance.
- **Persistent Storage**: Stores user/session data and temporary files for stateful behavior.
- **Cross-Platform Build**: Easily build and package the app for all major desktop and mobile platforms.

## Project Structure

- `DynamicIsland/` — application source code
  - `src/` — core logic, functions, animations, assets
    - `animation_functions/` — animation management
    - `assets/` — icons, splash screens, animation data
    - `dynamic_island/` — main Dynamic Island class
    - `functions/` — utility and media checker functions
    - `layers/` — UI layers (e.g., music, notifications)
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

### Poetry

- Install dependencies:
  ```
  poetry install
  ```
- Desktop:
  ```
  poetry run flet run
  ```

More details: [Getting Started Guide](https://flet.dev/docs/getting-started/)

## Building the App

- Windows: `flet build windows -v`

Build & publish documentation:
- [Windows Packaging Guide](https://flet.dev/docs/publish/windows/)

## Future Plans

- [x] **Cover Background**: Add a primary color thumbnail to replace the plain black background.
- [ ] **Shared Clipboard**: Implement a shared clipboard feature to allow files from different folders to be added to the island and then dragged to a single location.
- [ ] **Notifications**: Explore the possibility of integrating system notifications into the Dynamic Island.
- [ ] **Screenshot Detection**: Enable detection of screenshots for easy drag-and-drop functionality using the mouse.
