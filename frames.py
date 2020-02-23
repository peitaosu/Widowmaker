import os, sys

def create_frames(video_path, percent, output_path):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    out_folder = os.path.join(output_path, video_name)
    if not os.path.isdir(out_folder):
        os.makedirs(out_folder)
    os.system("ffmpeg -i {} -f image2 -vf fps=fps={} {}_%d.jpg".format(video_path, percent, out_folder + "\\" + video_name))

if __name__=="__main__":
    video_path = sys.argv[1]
    output_path = sys.argv[2]
    if not os.path.isdir(video_path):
        print("{} not exists.".format(video_path))
        sys.exit(-1)
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    saved_items = os.listdir(output_path)
    for sub_item in os.listdir(video_path):
        if  os.path.splitext(sub_item)[0] in saved_items:
            print(sub_item + " found, continue...")
            continue
        full_video_path = os.path.join(video_path, sub_item)
        if os.path.isfile(full_video_path):
            create_frames(full_video_path, "1/60", output_path)
            