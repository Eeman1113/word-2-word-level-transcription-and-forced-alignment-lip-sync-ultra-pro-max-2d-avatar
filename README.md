# Word-2-Word Level Transcription and Forced Alignment Lip Sync Ultra Pro Max 2D Avatar

Let the code introduce itself...

https://github.com/Eeman1113/word-2-word-level-transcription-and-forced-alignment-lip-sync-ultra-pro-max-2d-avatar/assets/54275491/306a1bb5-2ee8-48ad-8794-be89f9052ba8



Welcome to the repository for the "Word-2-Word Level Transcription and Forced Alignment Lip Sync Ultra Pro Max 2D Avatar" project! This unique Python script takes audio processing to the next level, creating a mesmerizing 2D avatar that syncs with spoken words.

## Overview

This script, powered by libraries such as `matplotlib`, `pydub`, `numpy`, `cv2`, `glob`, `os`, `moviepy`, and `pathlib`, performs a variety of tasks:

1. **Decibel Calculation**: The script calculates decibel levels using the root mean square (RMS) method from an input audio file.

2. **Processing Decibel Levels**: After obtaining decibel levels, the script processes them, addressing infinite or NaN values, and provides average and maximum decibel levels.

3. **Image Assignment**: Based on processed decibel levels, the script assigns dynamic images to different decibel value ranges, creating an engaging visual representation of the audio.

4. **Video Creation**: Using the assigned images, the script generates both AVI and MP4 video files, capturing the audio characteristics visually.

5. **Final Video**: The script combines the generated video with the original audio, producing a final synchronized masterpiece.

## How to Use

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Eeman1113/word-2-word-level-transcription-and-forced-alignment-lip-sync-ultra-pro-max-2d-avatar.git
    ```

2. **Install the Required Libraries:**

    ```bash
    pip install matplotlib pydub numpy opencv-python moviepy
    ```

3. **Run the Script:**

    ```bash
    python main.py
    ```

    Replace `main.py` with the actual name of your Python script.

4. **Customize the Input Audio File Path:**

    Modify the `main` function to point to your desired audio file:

    ```python
    if __name__ == "__main__":
        main("/path/to/your/audio/file.m4a")
        print("Finished!")
    ```

## Results

The script generates both AVI and MP4 video files, along with a final synchronized video. Processed decibel levels and assigned images are printed for analysis.

Feel free to experiment with different audio files and customize the image assignment logic to suit your creative needs.

Embark on a journey into the realm of audio visualization with the "Word-2-Word Level Transcription and Forced Alignment Lip Sync Ultra Pro Max 2D Avatar" project!
