import numpy as np
import glob
from PIL import Image
import imageio


def trim_image(path="screenshots/0.png", out="screenshots/0_trim.png"):
    image = Image.open(path)
    image.load()

    image_data = np.asarray(image)
    image_data_bw = image_data.max(axis=2)
    non_empty_columns = np.where(image_data_bw.max(axis=0) > 0)[0]
    non_empty_rows = np.where(image_data_bw.max(axis=1) > 0)[0]
    c = (min(non_empty_rows), max(non_empty_rows), min(
        non_empty_columns), max(non_empty_columns))

    image_data_new = image_data[c[0]:c[1]+1, c[2]:c[3]+1, :]

    new_image = Image.fromarray(image_data_new)
    new_image.save(out)


def make_gif(frame_folder="screenshots_trimmed"):
    frames = [Image.open(image)
              for image in glob.glob(f'{frame_folder}/*.png')]
    frame_one = frames[0]
    frame_one.save('fetch.gif', format="GIF", append_images=frames,
                   save_all=True, duration=100, loop=0, optimize=False)


def make_gif_new(frame_folder="screenshots_trimmed"):
    images = []
    for image in glob.glob(f'{frame_folder}/*.png'):
        images.append(imageio.imread(image))

    imageio.mimsave('fetch_new.gif', images)


def make_gif_new_new(frame_folder="screenshots_trimmed"):
    frames = []

    for image in glob.glob(f'{frame_folder}/*.png'):
        frames.append(gen_frame(image))

    frame_one = frames[0]
    frame_one.save('fetch_new_new.gif', append_images=frames,
                   save_all=True, duration=100, loop=0, optimize=False)


def gen_frame(path):
    im = Image.open(path)
    alpha = im.getchannel('A')

    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)

    # Set all pixel values below 128 to 255 , and the rest to 0
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)

    # Paste the color of index 255 and use alpha as a mask
    im.paste(255, mask)

    # The transparency index is 255
    im.info['transparency'] = 255

    return im
