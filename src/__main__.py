import fire
from src.cli import RagCLI


def main():
    cli = RagCLI()


if __name__ == "__main__":
    fire.Fire(RagCLI)
