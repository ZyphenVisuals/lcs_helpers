from pathlib import Path

if __name__ == "__main__":
    # create/clear files for parser.py
    f = Path("logs/")
    f.mkdir(exist_ok=True)
    f = open("logs/parser.log", "w", encoding="utf-8")
    f.close()
    f = Path("data/")
    f.mkdir(exist_ok=True)
    f = open("data/parser.dat", "w")
    f.close()