import argparse
import stages.compress as compress_stage
import stages.analyze as analysis_stage
import stages.pack_score as score_stage
import server as visualize_server


def compress(args):
    compress_stage.run()


def analyze(args):
    analysis_stage.run()


def score(args):
    score_stage.run()


def visualize(args):
    visualize_server.start_server()


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

    visualize_parser = subparsers.add_parser(
        "visualize",
        help="Start a local server to visualize data"
    )
    visualize_parser.set_defaults(func=visualize)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
