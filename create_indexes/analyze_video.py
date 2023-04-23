import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from skimage.feature import graycomatrix, graycoprops


def get_file_size(file_path):
    return os.path.getsize(file_path)


def get_num_frames(file_size, width, height):
    frame_size = width * height * 3
    return file_size // frame_size


def read_video_file(file, width, height, num_frames):
    with open(file, "rb") as f:
        data = f.read()

    video = np.frombuffer(data, dtype=np.uint8)
    video = video.reshape((num_frames, height, width, 3))
    return video


# Function to update color histogram plot for a given frame index
def update_histogram(frame_index, video, num_bins, ax):
    # Get the specified frame and convert it to BGR format
    frame = video[frame_index]
    bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    colors = ('b', 'g', 'r')

    # Clear the plot and create a new histogram plot for the current frame
    ax.clear()
    for channel, color in enumerate(colors):
        hist_channel = cv2.calcHist([bgr_frame], [channel], None, [num_bins], [0, 256])
        ax.plot(hist_channel, color=color)

    # Set the axis labels and title for the plot
    ax.set_title(f"Color Histogram for Frame {frame_index + 1}")
    ax.set_xlabel("Bins")
    ax.set_ylabel("Frequency")
    plt.draw()


# Function to update the histogram plot when the slider value changes
def on_slider_change(val, video, num_bins, ax):
    frame_index = int(val)
    update_histogram(frame_index, video, num_bins, ax)


# Function to update the slider value to the next frame
def on_next_button_click(event, slider):
    slider.set_val(min(slider.val + 1, slider.valmax))


# Function to update the slider value to the previous frame
def on_previous_button_click(event, slider):
    slider.set_val(max(slider.val - 1, slider.valmin))


# Main function to extract color histograms and plot them interactively
def extract_color_histograms(video, num_bins=64, plot=False):
    if not plot:
        return None

    # Create the main plot and slider
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    num_frames = len(video)

    slider_ax = plt.axes([0.15, 0.1, 0.75, 0.03])
    slider = Slider(slider_ax, 'Frame', 0, num_frames - 1, valinit=0, valstep=1)
    slider.on_changed(lambda val: update_histogram(val, video, num_bins, ax))

    # Create the next and previous buttons
    next_button_ax = plt.axes([0.55, 0.05, 0.05, 0.04])
    next_button = Button(next_button_ax, 'Next')
    next_button.on_clicked(lambda event: on_next_button_click(event, slider))

    previous_button_ax = plt.axes([0.35, 0.05, 0.05, 0.04])
    previous_button = Button(previous_button_ax, 'Prev')
    previous_button.on_clicked(lambda event: on_previous_button_click(event, slider))

    # Display initial frame's histogram
    update_histogram(0, video, num_bins, ax)
    plt.show()


# Function to update texture descriptor plot for a given frame index
def update_texture_plot(frame_index, video, ax):
    # Get the specified frame and convert it to grayscale
    frame = video[frame_index]
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Calculate the GLCM (Gray Level Co-occurrence Matrix)
    glcm = graycomatrix(gray_frame, [1], [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4], symmetric=True, normed=True)

    # Calculate texture properties from the GLCM
    contrast = graycoprops(glcm, 'contrast')
    dissimilarity = graycoprops(glcm, 'dissimilarity')
    homogeneity = graycoprops(glcm, 'homogeneity')
    energy = graycoprops(glcm, 'energy')
    correlation = graycoprops(glcm, 'correlation')
    asm = graycoprops(glcm, 'ASM')

    # Prepare the data and labels for the bar plot
    properties = [contrast, dissimilarity, homogeneity, energy, correlation, asm]
    property_names = ['Contrast', 'Dissimilarity', 'Homogeneity', 'Energy', 'Correlation', 'ASM']

    # Clear the plot and create a new bar plot with the calculated texture properties
    ax.clear()
    for i, prop in enumerate(properties):
        ax.bar(i, np.mean(prop), label=property_names[i])

    # Set the axis labels, title, and legend for the plot
    ax.set_xticks(range(len(properties)))
    ax.set_xticklabels(property_names)
    ax.set_ylabel("Value")
    ax.set_title(f"Texture Descriptors")
    ax.legend()
    plt.draw()


# Function to update the texture plot when the slider value changes
def on_slider_change_texture(val, video, ax):
    frame_index = int(val)
    update_texture_plot(frame_index, video, ax)


# Function to update the slider value to the previous frame
def on_next_button_click_texture(event, slider):
    slider.set_val(min(slider.val + 1, slider.valmax))


# Function to update the slider value to the previous frame
def on_previous_button_click_texture(event, slider):
    slider.set_val(max(slider.val - 1, slider.valmin))


# Main function to extract texture descriptors and plot them interactively
def extract_texture_descriptors(video, plot=False):
    if not plot:
        return None

    # Create the main plot and slider
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    num_frames = len(video)

    slider_ax = plt.axes([0.25, 0.1, 0.50, 0.03])
    slider = Slider(slider_ax, 'Frame', 0, num_frames - 1, valinit=0, valstep=1)
    slider.on_changed(lambda val: on_slider_change_texture(val, video, ax))

    # Create the next and previous buttons
    next_button_ax = plt.axes([0.55, 0.05, 0.05, 0.04])
    next_button = Button(next_button_ax, 'Next')
    next_button.on_clicked(lambda event: on_next_button_click_texture(event, slider))

    previous_button_ax = plt.axes([0.35, 0.05, 0.05, 0.04])
    previous_button = Button(previous_button_ax, 'Prev')
    previous_button.on_clicked(lambda event: on_previous_button_click_texture(event, slider))

    # Display initial frame's texture descriptors
    update_texture_plot(0, video, ax)
    plt.show()


def main():
    file_path = "../Starter Files/Ready_Player_One_rgb/InputVideo.rgb"
    file_size = get_file_size(file_path)

    width = 480
    height = 270

    num_frames = get_num_frames(file_size, width, height)
    print(num_frames)

    video = read_video_file(file_path, width, height, num_frames)

    extract_color_histograms(video, plot=True)
    extract_texture_descriptors(video, plot=True)


if __name__ == "__main__":
    main()
