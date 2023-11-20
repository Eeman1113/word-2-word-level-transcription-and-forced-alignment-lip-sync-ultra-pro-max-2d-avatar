import matplotlib.pyplot as plt
from pydub import AudioSegment
import numpy as np
import cv2
import glob
import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from pathlib import Path
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
    decibel_levels = [calculate_decibel(audio[i:i+1]) for i in range(0, len(audio), 1)]
    return decibel_levels


def process_decibel_levels(decibel_levels):
    for i in range(len(decibel_levels)):
        if math.isinf(decibel_levels[i]):
            decibel_levels[i] = 0
        else:
            decibel_levels[i] = int(decibel_levels[i])

    avg_decibel = sum(decibel_levels) / len(decibel_levels)
    max_decibel = max(decibel_levels)
    # second_high_decibel = decibel_levels.sort()[-2]

    return avg_decibel, max_decibel, decibel_levels


def assign_images(decibel_levels, avg_decibel, max_decibel):
    images = []
    for i in range(len(decibel_levels)):
        if decibel_levels[i] == 0:
            images.append('./gwack/Line.png')
        elif 0 <= decibel_levels[i] < avg_decibel / 2:
            images.append('./gwack/Teeth.png')
        elif avg_decibel / 2 <= decibel_levels[i] < avg_decibel:
            images.append("./gwack/big.png")
        elif decibel_levels[i] == avg_decibel:
            images.append('./gwack/circle.png')
        elif avg_decibel < decibel_levels[i] <= max_decibel:
            images.append('./gwack/Biggest.png')

    return images

def img_array(arr):
    img_array = []
    for i in arr:
        img = cv2.imread(i)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    return img_array

def create_video(images, output_path, codec='DIVX', fps=1000):
    animation = img_array(images)
    frame_size = (animation[0].shape[1], animation[0].shape[0])

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*codec), fps, frameSize=frame_size)

    for i in range(len(animation)):
        out.write(animation[i])

    out.release()


def create_final_video(video_path, audio_path, output_path, title="sample"):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path + ".mp4")


def main(path):
    audio_path = path
    decibel_levels = get_decibel_levels(audio_path)

    avg_decibel, max_decibel, processed_decibel_levels = process_decibel_levels(decibel_levels)

    print("Processed Decibel Levels:", processed_decibel_levels)
    print("Average Decibel Level:", avg_decibel)
    print("Max Decibel Level:", max_decibel)

    assigned_images = assign_images(processed_decibel_levels, avg_decibel, max_decibel)
    print("Assigned Images:", assigned_images)

    video_output_path_avi = 'project.avi'
    video_output_path_mp4 = 'project.mp4'

    create_video(assigned_images, video_output_path_avi, codec='DIVX', fps=1000)
    create_video(assigned_images, video_output_path_mp4, codec='mp4v', fps=1000)

    create_final_video(video_output_path_avi, audio_path, 'final_output_avi', title="sample")
    create_final_video(video_output_path_mp4, audio_path, 'final_output_mp4', title="sample")


if __name__ == "__main__":
    main("./sound/Ashta 4.m4a")
    print("Finished!")
