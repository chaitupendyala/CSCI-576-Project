import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from skimage.feature import graycomatrix, graycoprops


# Explanation

# In this code file overall I have tried to plot three visual feature extractors: Color Histograms, Texture Descriptors
# and Motion Vectors. So we are plotting these visual features and then trying to experiment which of the three or the
# combination of the two or more features will work well for our task of "Scene detection". Further, In the below
# comments, there is an explanation of what individual function does.


# "get_file_size(file_path)": This function takes a file path as input and returns the size of the file in bytes.

# "get_num_frames(file_size, width, height)": This function calculates the number of frames in an RGB video file.
# It takes the file size in bytes, and the width and height of the video frames as input, and returns the total
# number of frames in the video. This is done by dividing the file size by the size of a single frame
# (width * height * 3, since each pixel has 3 bytes for R, G, and B channels).

# "read_video_file(file, width, height, num_frames)": This function reads an RGB video file and returns it as a
# NumPy array with dimensions (num_frames, height, width, 3). It takes the file path, width, height, and the
# number of frames as input. The function first reads the file's binary data, then converts it to a NumPy array
# of unsigned 8-bit integers (uint8). Finally, it reshapes the array to the desired dimensions.

# "update_histogram(frame_index, video, num_bins, ax)": This function updates the histogram plot for a specified frame
# index. It takes the frame index, video array, number of bins, and the Matplotlib axis object as input. It retrieves
# the frame, converts it to BGR format, and plots the color histograms for each channel (blue, green, and red) on the
# provided axis object.

# "on_slider_change(val, video, num_bins, ax)": This function is called when the slider value changes. It takes the new
# slider value, video array, number of bins, and the Matplotlib axis object as input. It converts the slider value to an
# integer frame index and updates the histogram plot using the update_histogram function.

# "on_next_button_click(event, slider)": This function is called when the "Next" button is clicked. It takes the button
# click event and the slider object as input. It updates the slider value to the next frame index, as long as it doesn't
# exceed the maximum frame index.

# "on_previous_button_click(event, slider)": This function is called when the "Prev" button is clicked. It takes the
# button click event and the slider object as input. It updates the slider value to the previous frame index, as long as
# it doesn't fall below the minimum frame index.

# "extract_color_histograms(video, num_bins=64, plot=False)": This is the main function to extract color histograms and
# plot them interactively. It takes the video array, the number of bins for the histogram, and a boolean flag to
# enable/disable plotting. If plot is set to False, the function returns None. If plot is set to True, it creates a
# Matplotlib figure with a slider, "Next" and "Prev" buttons, and an initial color histogram plot for the first frame.
# The slider and buttons are connected to their respective callback functions to update the histogram plot as the user
# interacts with the slider and buttons.

# "update_texture_plot(frame_index, video, ax)": This function updates the texture descriptor plot for a specified frame
# index. It takes the frame index, video array, and the Matplotlib axis object as input. It retrieves the frame,
# converts it to grayscale, calculates the Gray Level Co-occurrence Matrix (GLCM), and computes various texture
# properties (contrast, dissimilarity, homogeneity, energy, correlation, and ASM) from the GLCM. Then, it clears the
# axis and creates a new bar plot with the calculated texture properties on the provided axis object.

# "extract_texture_descriptors(video, plot=False)": This is the main function to extract texture descriptors and plot them
# interactively. It takes the video array and a boolean flag to enable/disable plotting. If plot is set to False, the
# function returns None. If plot is set to True, it creates a Matplotlib figure with a slider, "Next" and "Prev" buttons,
# and an initial texture descriptor plot for the first frame. The slider and buttons are connected to their respective
# callback functions to update the texture descriptor plot as the user interacts with the slider and buttons.

# "update_motion_vectors_plot(frame_index, video, ax)": This function updates the motion vectors plot for a specified
# frame index. It takes the frame index, video array, and the Matplotlib axis object as input. It calculates the optical
# flow between the current frame and the previous frame using the Farneback algorithm and then displays the absolute sum
# of the flow vectors in the plot.

# "extract_motion_vectors(video, plot=False)": This is the main function to extract motion vectors and plot them
# interactively. It takes the video array and a boolean flag to enable/disable plotting. If plot is set to False, the
# function returns None. If plot is set to True, it creates a Matplotlib figure with a slider, "Next" and "Prev"
# buttons, and an initial motion vectors plot for the second frame. The slider and buttons are connected to their
# respective callback functions to update the motion vectors plot as the user interacts with the slider and buttons.

# "compare_histograms(hist1, hist2, method=cv2.HISTCMP_CORREL)": This function computes the similarity between two color
# histograms using the specified comparison method (default is correlation). It takes two histograms as input and
# returns the similarity score.

# "compute_color_histogram_similarity(video, num_bins=64)": This function computes the color histogram similarity between
# consecutive frames in a video. It takes the video array and the number of bins for the histograms as input.
# It calculates the color histograms for each frame and computes the similarity between consecutive frames using the
# compare_histograms function. It returns a list of similarity scores.

# detect_scene_changes_color_histograms(video, threshold=None): This function detects scene changes in a video based on
# color histogram similarity. It takes the video array and an optional threshold value as input. For now I used the
# threshold value of 0.98, it can be changed according to our needs. The function computes the color histogram
# similarities using the compute_color_histogram_similarity function and detects scene changes as the indices where the
# similarity score is below the threshold. It returns a list of scene change indices.






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


def update_motion_vectors_plot(frame_index, video, ax):
    gray = cv2.cvtColor(video[frame_index], cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.cvtColor(video[frame_index - 1], cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    ax.clear()
    ax.imshow(np.abs(flow.sum(axis=-1)), cmap="gray")
    ax.set_title(f"Motion Vectors (Optical Flow) for Frame {frame_index + 1}")


def on_slider_change_motion(val, video, ax):
    frame_index = int(val)
    update_motion_vectors_plot(frame_index, video, ax)


def on_next_button_click_motion(event, slider):
    slider.set_val(min(slider.val + 1, slider.valmax))


def on_prev_button_click_motion(event, slider):
    slider.set_val(max(slider.val - 1, slider.valmin))


def extract_motion_vectors(video, plot=False):
    if not plot:
        return None

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    num_frames = len(video)

    slider_ax = plt.axes([0.15, 0.1, 0.75, 0.03])
    slider = Slider(slider_ax, 'Frame', 1, num_frames - 1, valinit=1, valstep=1)
    slider.on_changed(lambda val: on_slider_change_motion(val, video, ax))

    next_button_ax = plt.axes([0.55, 0.05, 0.05, 0.04])
    next_button = Button(next_button_ax, 'Next')
    next_button.on_clicked(lambda event: on_next_button_click_motion(event, slider))

    previous_button_ax = plt.axes([0.35, 0.05, 0.05, 0.04])
    previous_button = Button(previous_button_ax, 'Prev')
    previous_button.on_clicked(lambda event: on_prev_button_click_motion(event, slider))

    # Display initial frame's motion vectors
    update_motion_vectors_plot(1, video, ax)
    plt.show()


def compare_histograms(hist1, hist2, method=cv2.HISTCMP_CORREL):
    similarity = cv2.compareHist(hist1, hist2, method)
    return similarity


def compute_color_histogram_similarity(video, num_bins=64):
    similarities = []
    for i in range(len(video) - 1):
        frame1 = video[i]
        frame2 = video[i + 1]

        hist1 = cv2.calcHist([frame1], [0, 1, 2], None, [num_bins, num_bins, num_bins], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([frame2], [0, 1, 2], None, [num_bins, num_bins, num_bins], [0, 256, 0, 256, 0, 256])

        similarity = compare_histograms(hist1, hist2)
        similarities.append(similarity)

    return similarities


def detect_scene_changes_color_histograms(video, threshold=None):
    similarities = compute_color_histogram_similarity(video)

    if threshold is None:
        threshold = 0.98

    scene_changes = [i + 1 for i, sim in enumerate(similarities) if sim < threshold]
    return scene_changes


def main():
    file_path = "../Starter Files/Ready_Player_One_rgb/InputVideo.rgb"
    file_size = get_file_size(file_path)
    # print(file_size)

    # The video that was given in the assignment had the below values for the dimensions of the video
    width = 480
    height = 270

    num_frames = get_num_frames(file_size, width, height)
    # print(num_frames)

    video = read_video_file(file_path, width, height, num_frames)

    extract_color_histograms(video, plot=True)
    extract_texture_descriptors(video, plot=True)
    extract_motion_vectors(video, plot=True)

    # Detect scene changes using color histograms
    scene_changes = detect_scene_changes_color_histograms(video)

    print("Scene changes detected at frames:", scene_changes)

    # Plot the detected scene changes
    plt.figure()
    plt.plot(range(1, len(video)), compute_color_histogram_similarity(video))
    plt.axhline(np.mean(compute_color_histogram_similarity(video)), color='r', linestyle='--', label="Threshold")
    plt.xlabel("Frame Index")
    plt.ylabel("Color Histogram Similarity")
    plt.title("Scene Change Detection")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
