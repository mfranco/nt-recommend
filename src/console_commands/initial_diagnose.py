from app.analytics import initial_analysis
import argparse


def run(**kwargs):
    """
    Basic analisys for the movilens dataset
    """
    parser = argparse.ArgumentParser()
    args, extra_params = parser.parse_known_args()

    initial_analysis.compute()
