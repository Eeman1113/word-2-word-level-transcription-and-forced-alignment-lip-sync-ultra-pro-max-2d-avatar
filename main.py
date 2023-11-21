# %%
import matplotlib.pyplot as plt
from pydub import AudioSegment
import numpy as np
import cv2
from moviepy.editor import VideoFileClip, AudioFileClip
import math
import random

# %%
def calculate_decibel(audio):
    samples = np.array(audio.get_array_of_samples())
    rms = np.sqrt(np.mean(np.square(samples)))

    if rms == 0 or np.isnan(rms) or np.isinf(rms):
        return float('-inf')

    reference = 1.0
    decibel = 20 * np.log10(rms / reference)

    return decibel

# %%
def get_decibel_levels(audio_path):
    audio = AudioSegment.from_file(audio_path)
    decibel_levels = [calculate_decibel(audio[i:i+1]) for i in range(0, len(audio), 1)]
    return decibel_levels



# %%
def process_decibel_levels(decibel_levels):
    for i in range(len(decibel_levels)):
        if math.isinf(decibel_levels[i]):
            decibel_levels[i] = 0
        else:
            decibel_levels[i] = abs(int(decibel_levels[i]))

    avg_decibel = sum(decibel_levels) / len(decibel_levels)
    max_decibel = max(decibel_levels)

    window_size = 40
    decibel_levels = np.convolve(decibel_levels, np.ones(window_size)/window_size, mode='same')

    return avg_decibel, max_decibel, decibel_levels

#%%
def categorize_decibel_levels(decibel_levels, avg_decibel):
    # # calculate the silent and low threshhold by analyzing the decibel levels
    # sorted_levels = np.sort(decibel_levels)
    # silent_threshold_index = int(len(sorted_levels) * 0.1)
    # low_threshold_index = int(len(sorted_levels) * 0.25)
    # silent_threshold = sorted_levels[silent_threshold_index]
    # low_threshold = sorted_levels[low_threshold_index]

    # categorized_levels = []
    # occurences = {"silent": 0, "low": 0, "high": 0}
    # for level in decibel_levels:
    #     if level <= silent_threshold:
    #         categorized_levels.append("silent")
    #         occurences["silent"] += 1
    #     elif level <= low_threshold:
    #         categorized_levels.append("low")
    #         occurences["low"] += 1
    #     else:
    #         categorized_levels.append("high")
    #         occurences["high"] += 1

    categorized_levels = []
    occurences = {"silent": 0, "low": 0, "high": 0}
    for level in decibel_levels:
        if 0 <= level < avg_decibel / 4:
            categorized_levels.append("silent")
            occurences["silent"] += 1
        elif avg_decibel / 4 <= level < avg_decibel / 2:
            categorized_levels.append("low")
            occurences["low"] += 1
        elif avg_decibel / 2 <= level < avg_decibel:
            categorized_levels.append("high")     
            occurences["high"] += 1
        elif level >= avg_decibel * 3 / 4:
            categorized_levels.append("silent")
            occurences["silent"] += 1

    print(occurences)
    return categorized_levels

#%%
def extract_categories_per_fps(categorized_decibels, frame_rate):
    chunk_duration = (1 / frame_rate * 1000)
    total_frames = math.ceil(len(categorized_decibels) / chunk_duration)

    categorized_levels_per_fps = []

    # small little optimization here
    # every frame there is x milliseconds (eg. 24fps = 41.666666666666664ms per frame = 41.66 decibel values per frame)
    # but since we can't index a list with a decimal number, we have to *round it* up to the nearest integer
    # this means that 1) the video will be slightly longer than the audio, and 2) the frames will go out-of-sync with the audio
    # so to minimize this effect, we alternatively switch from rounding up to rounding down every other frame
    # at the end, the extra time will only be the difference of math.ceil(x) and math.floor(x), which will always be <1ms

    round_up = True
    index = 0
    for i in range(total_frames):
        if round_up:
            interval = math.ceil(chunk_duration)
        else:
            interval = math.floor(chunk_duration)
        
        index += interval
        if index <= len(categorized_decibels):
            categorized_levels_per_fps.append(categorized_decibels[index])
        else:
            categorized_levels_per_fps.append(categorized_decibels[-1])

        round_up = not round_up
    
    return categorized_levels_per_fps


#%%
def assign_images(categorized_decibels, frame_rate=12):
    images = []
    
    chunk_duration = (1 / frame_rate * 1000)
    extracted_categories_per_fps = extract_categories_per_fps(categorized_decibels, frame_rate)
    total_frames = len(extracted_categories_per_fps)

    round_up = True
    for i in range(total_frames):
        if round_up:
            chunk_length = math.ceil(chunk_duration)
        else:
            chunk_length = math.floor(chunk_duration)
        round_up = not round_up

        level = extracted_categories_per_fps[i]

        if level == "silent":
            images += ['./gwack/neutral.png']*chunk_length
        elif level == "low":
            visemes = ['open_round', 'lips_pursed', 'tongue', 'teeth_open', 'teeth_close']
            # probabilities = [0.2, 0.3, 0.2, 0.15, 0.15]
            # choice = random.choices(visemes, weights=probabilities)[0]
            choice = random.choices(visemes)[0]
            image_path = './gwack/' + choice + '.png'
            images += [image_path]*chunk_length

        elif level == "high":
            visemes = ['long_open', 'wide_open', 'tongue', 'teeth_open', 'teeth_close']
            # probabilities = [0.125, 0.125, 0.05, 0.2, 0.15, 0.15, 0.15]
            # choice = random.choices(visemes, weights=probabilities)[0]
            choice = random.choices(visemes)[0]
            image_path = './gwack/' + choice + '.png'
            images += [image_path]*chunk_length

    # for level in categorized_decibels:
    #     if level == "silent":
    #         images.append('./gwack/neutral.png')
    #     elif level == "low":
    #         visemes = ['open_round', 'lips_pursed', 'tongue', 'teeth_open', 'teeth_close']
    #         probabilities = [0.2, 0.3, 0.2, 0.15, 0.15]
    #         choice = random.choices(visemes, weights=probabilities)[0]
    #         image_path = './gwack/' + choice + '.png'
    #         images.append(image_path)

    #     elif level == "high":
    #         visemes = ['long_open', 'wide_open', 'open_round', 'lips_pursed', 'tongue', 'teeth_open', 'teeth_close']
    #         probabilities = [0.125, 0.125, 0.05, 0.2, 0.15, 0.15, 0.15]
    #         choice = random.choices(visemes, weights=probabilities)[0]
    #         image_path = './gwack/' + choice + '.png'
    #         images.append(image_path)
    #     else:
    #         images.append('./gwack/neutral.png')

    return images

# %%
def img_array(arr):
    img_array = []

    for i in arr:
        img = cv2.imread(i)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    return img_array

# %%
def stitch_frames_to_video(images, output_path, codec='DIVX', fps=1000):
    animation = img_array(images)
    frame_size = (animation[0].shape[1], animation[0].shape[0])

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*codec), fps, frameSize=frame_size)

    for i in range(len(animation)):
        out.write(animation[i])

    out.release()

# %%
def create_final_video(video_path, audio_path, output_path, title="sample"):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path + ".mp4")


# %%
def main(path):
    audio_path = path
    decibel_levels = get_decibel_levels(audio_path)

    avg_decibel, max_decibel, processed_decibel_levels = process_decibel_levels(decibel_levels)
    categorized_decibels = categorize_decibel_levels(processed_decibel_levels, avg_decibel)

    print("Processed Decibel Levels:", len(processed_decibel_levels))
    print("Average Decibel Level:", avg_decibel)
    print("Max Decibel Level:", max_decibel)

    assigned_images = assign_images(categorized_decibels)
    print("Assigned Images:", len(assigned_images))

    video_output_path_mp4 = 'project.mp4'
    stitch_frames_to_video(assigned_images, video_output_path_mp4, codec='mp4v', fps=1000)
    create_final_video(video_output_path_mp4, audio_path, 'final_output_mp4', title="sample")

    # video_output_path_avi = 'project.avi'
    # stitch_frames_to_video(assigned_images, video_output_path_avi, codec='DIVX', fps=24)
    # create_final_video(video_output_path_avi, audio_path, 'final_output_avi', title="sample")

# %%
if __name__ == "__main__":
    # main("./sound/srishti_dora_sample.m4a")
    main('./sound/repo_description_daniel.mp3')
    print("Finished!")
