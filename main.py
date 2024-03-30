import argparse
from scripts import compress, analysis, evaluate


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
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Evaluation stage"
    )
    args = parser.parse_args()

    if args.compress:
        compress.run()
    elif args.analyze:
        analysis.run()
    elif args.evaluate:
        evaluate.run()
    else:
        print("No option specified. Use --help or -h to see usage.")


if __name__ == "__main__":
    main()
