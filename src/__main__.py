import fire
from src.cli import RagCLI
import traceback

def main():
    cli = RagCLI()
    fire.Fire(cli)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        print(e, )


