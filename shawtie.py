import cv2
import numpy as np
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip
import math

def calculate_decibel(audio):
    samples = np.array(audio.get_array_of_samples())
    rms = np.sqrt(np.mean(np.square(samples)))

    if rms == 0 or np.isnan(rms) or np.isinf(rms):
        return float('-inf')

    reference = 1.0
    decibel = 20 * np.log10(rms / reference)

    return decibel

def get_decibel_levels(audio_path):
    audio = AudioSegment.from_file(audio_path)
    return [calculate_decibel(audio[i:i+1]) for i in range(0, len(audio), 1)]

def process_decibel_levels(decibel_levels):
    decibel_levels = [0 if math.isinf(d) else int(d) for d in decibel_levels]
    avg_decibel = sum(decibel_levels) / len(decibel_levels)
    max_decibel = max(decibel_levels)
    second_high_decibel = min(decibel_levels, default=0)
    return avg_decibel, max_decibel, second_high_decibel, decibel_levels

def assign_images(decibel_levels, avg_decibel, max_decibel, window_size=40):
    smoothed_levels = np.convolve(decibel_levels, np.ones(window_size)/window_size, mode='same')
    
    images_mapping = {
        (0, avg_decibel / 4): './gwack/line.png',
        (avg_decibel / 4, avg_decibel * 3 / 4): './gwack/Teeth_ee.png',
        (avg_decibel * 3 / 4, max_decibel): './gwack/Teeth.png'
    }

    return [next((image_path for level_range, image_path in images_mapping.items() if level_range[0] <= level < level_range[1]), './gwack/line.png') for level in smoothed_levels]

def img_array(arr):
    return [cv2.imread(i) for i in arr]

def create_video(images, output_path, codec='DIVX', fps=25):
    frame_size = images[0].shape[1], images[0].shape[0]
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*codec), fps, frameSize=frame_size)
    [out.write(image) for image in images]
    out.release()

def create_final_video(video_path, audio_path, output_path, title="sample"):
    video_clip = VideoFileClip(video_path, fps=25)
    audio_clip = AudioFileClip(audio_path)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path + ".mp4", fps=25)

def main(path):
    audio_path = path
    decibel_levels = get_decibel_levels(audio_path)

    avg_decibel, max_decibel, _, processed_decibel_levels = process_decibel_levels(decibel_levels)

    assigned_images = assign_images(processed_decibel_levels, avg_decibel, max_decibel)
    print("Assigned Images:", assigned_images)

    video_output_path_mp4 = 'project.mp4'
    create_video(img_array(assigned_images), video_output_path_mp4, codec='mp4v', fps=25)
    create_final_video(video_output_path_mp4, audio_path, 'final_output_mp4_new', title="sample")

if __name__ == "__main__":
    main("./sound/Ashta 4.m4a")
    print("Finished!")
