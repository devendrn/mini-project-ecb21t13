import argparse
from scripts import compress, analysis, pack_score, plot


def compress_cmd(args):
    compress.run()


def analyzeCmd(args):
    analysis.run()


def scoreCmd(args):
    pack_score.run()


def plotCmd(args):
    plot.run()


def main():
    parser = argparse.ArgumentParser(description="Compression analysis")
    subparsers = parser.add_subparsers(title="Commands", required=True)

    compress_parser = subparsers.add_parser(
        "compress",
        help="Compresion stage"
    )
    compress_parser.set_defaults(func=compress_cmd)

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analysis stage"
    )
    analyze_parser.set_defaults(func=analyzeCmd)

    score_parser = subparsers.add_parser(
        "score",
        help="Pack score date"
    )
    score_parser.set_defaults(func=scoreCmd)

    plot_parser = subparsers.add_parser(
        "plot",
        help="Create plots from score data"
    )
    plot_parser.set_defaults(func=plotCmd)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)


if __name__ == "__main__":
    main()
