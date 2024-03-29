import argparse
from scripts import compress, analysis


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
        compress.run()
    elif args.analyze:
        analysis.run()
    else:
        print("No option specified. Use --help or -h to see usage.")


if __name__ == "__main__":
    main()
