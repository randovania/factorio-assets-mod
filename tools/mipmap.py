# /// script
# dependencies = [
#   "pillow",
# ]
# ///

import argparse
from pathlib import Path

from PIL import Image


def create_mipmap(input_path: Path, output_path: Path, *, mimaps: int = 3) -> None:
    img = Image.open(input_path)
    if img.size != (64, 64):
        img = img.resize((64, 64))

    height = img.size[1]
    crop = img.crop((0, 0, height, height))

    result = Image.new(
        "RGBA", (sum(height // (2**mip) for mip in range(mimaps + 1)), height)
    )

    left = 0
    for mipmap in range(mimaps + 1):
        d = 2**mipmap
        smaller = crop.resize((height // d, height // d))

        result.paste(smaller, (left, 0))
        left += smaller.size[0]

    result.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=Path)
    parser.add_argument("output_path", type=Path)
    args = parser.parse_args()

    create_mipmap(args.input_path, args.output_path)


if __name__ == "__main__":
    main()
