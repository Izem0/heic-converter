from functools import partial
from multiprocessing import Pool
from pathlib import Path

from wand.image import Image

from utils import setup_logger, timer


BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR / "heic_images/"
SOURCE_DIR.mkdir(exist_ok=True)
TARGET_DIR = BASE_DIR / "converted_images/"
TARGET_DIR.mkdir(exist_ok=True)
LOGS_DIR = BASE_DIR / "logs/"
LOGS_DIR.mkdir(exist_ok=True)
LOGGER = setup_logger(
    "converter",
    log_config_file=BASE_DIR / "logging.yaml",
    log_file=LOGS_DIR / "converter.log",
)
FORMAT = "jpg"


def convert_image(sourcefile: str, targetdir: str, format: str = "jpg") -> str:
    sourcefile = Path(sourcefile)
    with Image(filename=sourcefile) as original:
        with original.convert(format) as converted:
            targetdir = Path(targetdir)
            converted_filename = targetdir / f"{sourcefile.stem}.{format}"
            converted.save(filename=converted_filename)
            return sourcefile, converted_filename


@timer(LOGGER)
def main():
    # check presence of .heic images in source dir
    to_convert_images = list(SOURCE_DIR.glob("*.heic"))
    if not to_convert_images:
        raise FileNotFoundError(
            f"No files to convert found in directory '{SOURCE_DIR}'."
        )

    # use multiprocessing to process all images
    partial_func = partial(convert_image, targetdir=TARGET_DIR, format=FORMAT)
    with Pool() as pool:
        rslt = pool.imap_unordered(partial_func, iterable=to_convert_images)
        for source, target in rslt:
            LOGGER.info(f"{source.name} successfully converted to {target.name}.")

    # ending message
    LOGGER.info(
        f"All {len(to_convert_images)} images were converted to jpg and saved to '{TARGET_DIR.as_posix()}'."
    )


if __name__ == "__main__":
    main()
