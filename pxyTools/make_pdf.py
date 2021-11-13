import img2pdf
import os
import sys
from pathlib import Path
valid_image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".bmp", ".heif", ".heic"]


def make_pdf(in_dir, out_file=None, force_conv=False):
    files = []
    cur_path = Path(in_dir)
    out_name = cur_path.name
    out_file = Path(out_file) if out_file else Path(str(cur_path) + f"/{out_name}.pdf")

    for x in os.listdir(str(cur_path)):
        cur_file = Path(str(cur_path) + "/" + x)
        if cur_file.suffix.lower() in valid_image_extensions:
            files.append(str(cur_file))

    files.sort()
    if force_conv:
        files = convert_images(files)
    try:
        with out_file.open("wb") as f:
            f.write(img2pdf.convert(files))
    except Exception as e:
        print(f"Could not convert to a PDF, attempting to convert images")
        print(f"Error: {e}")
        files = convert_images(files)
        with out_file.open("wb") as f:
            f.write(img2pdf.convert(files))
        [os.remove(y) for y in files if y.endswith("-pdf-conv")]
    return out_file


def convert_images(images):
    from PIL import Image
    n_files = []
    for i in images:
        fg = Image.open(i)
        if fg.mode in ("P", "RGBA", "LA", "PA"):
            fg.load()
            bg = Image.new("RGB", fg.size, (255, 255, 255))
            try:
                bg.paste(fg, mask=fg.split()[3])
            except IndexError:
                bg.paste(fg)
            bg.save(f"{i}-pdf-conv", "JPEG", quality=100)
            n_files.append(f"{i}-pdf-conv")
        else:
            n_files.append(i)
    return n_files


if __name__ == '__main__':
    try:
        gen = make_pdf(sys.argv[1])
        old_path = str(gen)
        new_path = str(Path(str(gen.parents[1]) + "/" + gen.name))
        os.rename(old_path, new_path)
    except IndexError:
        make_pdf(os.getcwd())
