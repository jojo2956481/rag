import fire
from src.cli import RagCLI


def main():
    cli = RagCLI()
    fire.Fire(cli)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)


