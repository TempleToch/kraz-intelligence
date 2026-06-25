from extractor import run_extract
from enrich import run_enrich
from scoring import run_score

def main():
    run_extract()
    run_enrich()
    run_score()

if __name__ == "__main__":
    main()