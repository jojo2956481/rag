import fire
from src.cli import RagCLI
from src.indexing import Indexing



def main():
    cli = RagCLI()
    


if __name__ == "__main__":
    fire.Fire(RagCLI)
