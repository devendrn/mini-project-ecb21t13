import argparse
from scripts import compress, analysis, pack_score, plot


def compressCmd(args):
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

    compressParser = subparsers.add_parser(
        "compress",
        help="Compression stage"
    )
    compressParser.set_defaults(func=compressCmd)

    analyzeParser = subparsers.add_parser(
        "analyze",
        help="Analysis stage"
    )
    analyzeParser.set_defaults(func=analyzeCmd)

    scoreParser = subparsers.add_parser(
        "score",
        help="Pack score date"
    )
    scoreParser.set_defaults(func=scoreCmd)

    plotParser = subparsers.add_parser(
        "plot",
        help="Create plots from score data"
    )
    plotParser.set_defaults(func=plotCmd)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)


if __name__ == "__main__":
    main()
