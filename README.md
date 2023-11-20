# Word-2-Word Level Transcription and Forced Alignment Lip Sync Ultra Pro Max 2D Avatar

Welcome to the repository for the "Word-2-Word Level Transcription and Forced Alignment Lip Sync Ultra Pro Max 2D Avatar" project! This project involves analyzing audio files, calculating decibel levels, and generating a synchronized video with dynamic images based on the audio characteristics.

## Overview

This Python script utilizes various libraries such as `matplotlib`, `pydub`, `numpy`, `cv2`, `glob`, `os`, `moviepy`, and `pathlib` to perform the following tasks:

1. **Decibel Calculation**: The script calculates decibel levels from an input audio file using the root mean square (RMS) method.

2. **Processing Decibel Levels**: After obtaining decibel levels, the script processes them, replacing any infinite or NaN values and providing average and maximum decibel levels.

3. **Image Assignment**: Based on the processed decibel levels, the script assigns different images to different ranges of decibel values. This can be customized to create a visually dynamic representation of the audio.

4. **Video Creation**: The assigned images are then used to create a video file in both AVI and MP4 formats. The resulting videos visually represent the audio characteristics over time.

5. **Final Video**: The script combines the generated video with the original audio to produce a final synchronized video.

## How to Use

1. Clone the repository:

    ```bash
    git clone https://github.com/Eeman1113/word-2-word-level-transcription-and-forced-alignment-lip-sync-ultra-pro-max-2d-avatar.git
    ```

2. Install the required libraries:

    ```bash
    pip install matplotlib pydub numpy opencv-python moviepy
    ```

3. Run the script:

    ```bash
    python Some_Diffrent_Shit.py
    ```

    Make sure to replace `script_name.py` with the actual name of your Python script.

4. Customize the input audio file path:

    Modify the `main` function to point to your desired audio file:

    ```python
    if __name__ == "__main__":
        main("/path/to/your/audio/file.m4a")
        print("Finished!")
    ```

## Results

The script generates both AVI and MP4 video files along with a final synchronized video. The processed decibel levels and assigned images are printed for analysis.

Feel free to experiment with different audio files and customize the image assignment logic for your creative needs.

Enjoy exploring the world of audio visualization with the "Word-2-Word Level Transcription and Forced Alignment Lip Sync Ultra Pro Max 2D Avatar" project!
