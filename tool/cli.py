import argparse
import stages.compress as compress_stage
import stages.analyze as analysis_stage
import stages.pack_score as score_stage


def compress(args):
    compress_stage.run()


def analyze(args):
    analysis_stage.run()


def score(args):
    score_stage.run()


def start():
    parser = argparse.ArgumentParser(description="Compression analysis")
    subparsers = parser.add_subparsers(title="Commands", required=True)

    compress_parser = subparsers.add_parser(
        "compress",
        help="Compresion stage"
    )
    compress_parser.set_defaults(func=compress)

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analysis stage"
    )
    analyze_parser.set_defaults(func=analyze)

    score_parser = subparsers.add_parser(
        "score",
        help="Pack score date"
    )
    score_parser.set_defaults(func=score)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
