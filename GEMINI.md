# GEMINI.md

## Project Overview

This project is a Python-based automation tool for the game "Fantasy Westward Journey" (梦幻西游). It uses TensorFlow to identify and automatically click on character pop-up windows. The project is designed to run on Windows and utilizes a custom kernel-level driver (`kmclass.sys`) for mouse interactions, which requires enabling test mode and disabling driver signature enforcement in the operating system.

The core functionality is divided into two main parts:
1.  **Auto-Clicking:** This feature continuously takes screenshots of the game window, identifies character pop-up dialogs using a trained TensorFlow model, and then simulates a mouse click on the correct character.
2.  **Model Training:** This feature allows the user to train the TensorFlow model with new images to improve its accuracy.

## Key Technologies

*   **Python 3.7**
*   **TensorFlow 2.1** for the image recognition model.
*   **PyQt5** and **Pillow** for screen capturing and image manipulation.
*   **OpenCV** for image processing and template matching.
*   **pyautogui** for mouse movement automation.
*   **ctypes** to interface with the custom `kmclassdll.dll` for low-level mouse clicks.

## Project Structure

The project is organized into several Python modules:

*   `main.py`: The main entry point of the application. It parses command-line arguments to either run the auto-clicking logic or the model training process.
*   `data_model.py`: Contains all the logic related to the TensorFlow model, including building, training, loading, and predicting.
*   `screen.py`: Handles screen capturing, image processing, template matching to find UI elements, and cropping images for the model.
*   `auto.py`: A wrapper for mouse and keyboard automation, combining `pyautogui` for movement and `keymouse.py` for clicks.
*   `keymouse.py`: Interfaces with the `kmclassdll.dll` to send low-level mouse commands.
*   `constant.py`: Defines all the constants used in the project, such as file paths, image dimensions, and UI element coordinates.
*   `util.py`: Provides utility functions for logging.
*   `driver/`: Contains the custom mouse driver files.
*   `images/`: Stores screenshots, image flags for template matching, and training data.
*   `model/`: Stores the trained TensorFlow model.

## Building and Running

### Prerequisites

1.  **Windows Operating System** with "test mode" enabled and "driver signature enforcement" disabled. This can be done by running the following commands as an administrator and rebooting:
    ```bash
    bcdedit /set nointegritychecks on
    bcdedit /set testsigning on
    shutdown -r -t 0
    ```
2.  **Python 3.7** and the required packages listed in the `README.md` (TensorFlow 2.1, etc.).
3.  The game "Fantasy Westward Journey" running in `800x600` resolution.

### Running the Application

*   **To automatically click pop-ups:**
    ```bash
    python main.py --click 1
    ```

*   **To train the model with new images:**
    ```bash
    python main.py --learn 1
    ```

## Development Conventions

*   The project follows a modular structure, separating concerns into different files.
*   Constants are centralized in `constant.py` for easy configuration.
*   The `README.md` file provides detailed instructions on setting up the environment and running the project.
*   The project uses a combination of `pyautogui` for general mouse movement and a custom driver for more reliable clicks, indicating a need to bypass potential game protections.
*   The model training process is designed to be iterative, allowing users to add new images to the training set and retrain the model.
