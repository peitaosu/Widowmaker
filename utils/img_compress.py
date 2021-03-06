import os, sys
from PIL import Image

def image_compress(image_folder, output_folder, quality=80):
    """
    args:
        image_folder(str): relative image folder
        output_folder(str): output folder
        quality(int): jpg quality, default is 80
    """
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)
    for sub_item in os.listdir(image_folder):
        sub_path = os.path.join(image_folder, sub_item)
        if os.path.isdir(sub_path):
            image_compress(sub_path, output_folder, quality)
        else:
            file_name = os.path.basename(sub_path)
            file_dir = os.path.dirname(sub_path)
            file_name_ext = os.path.splitext(file_name)[1]
            file_name_no_ext = os.path.splitext(file_name)[0]
            if file_name_ext.lower() in [".jpg", ".jpeg", ".png", ".bmp"]:
                try:
                    img = Image.open(sub_path)
                    rgb_img = img.convert('RGB')
                except:
                    print("[FAILED] opening {} failed.".format(sub_path))
                    continue
                out_dir = os.path.join(output_folder, file_dir)
                if not os.path.isdir(out_dir):
                    os.makedirs(out_dir)
                rgb_img.save(os.path.join(output_folder, file_dir, file_name_no_ext + ".jpg"), optimize=True, quality=quality)
            else:
                print("[FAILED] {} is not a picture.".format(sub_path))

if __name__=="__main__":
    image_folder = sys.argv[1]
    output_folder = sys.argv[2]
    quality = 80
    if len(sys.argv) > 3:
        quality = int(sys.argv[3])
    if not os.path.isdir(image_folder):
        sys.exit("{} not exists.".format(image_folder))
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)
    image_compress(image_folder, output_folder, quality)
            
