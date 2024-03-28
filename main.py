import argparse
import config
from scripts import compress


def main():
    parser = argparse.ArgumentParser(description="Compression analysis")
    parser.add_argument(
        "--compress",
        action="store_true",
        help="Compression stage"
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analysis stage"
    )
    args = parser.parse_args()

    if args.compress:
        compress.run(config.FORMATS, config.REF_DIR, config.OUT_DIR)
    elif args.analyze:
        print("Analyze stage not implemented yet")
    else:
        print("No option specified. Use --help or -h to see usage.")


if __name__ == "__main__":
    main()
