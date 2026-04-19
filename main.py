from datetime import date
import json
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session

from lib.api import Ebaki
from lib.model import Base, Ledger

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--sqlite", default=":memory:", help="Path to sqlite file")
parser.add_argument(
    "--year-start",
    required=True,
    help="Initial scrape point",
    type=int,
)
parser.add_argument(
    "--year-end",
    required=False,
    help="Last scrape point",
    type=int,
)
parser.add_argument(
    "--credentials",
    required=True,
    help="JSON credential file for logon. Keys required: username, password",
)


def init_table(url: str):
    engine = create_engine(url, echo=True)
    Base.metadata.create_all(engine)
    return engine


def main():
    args = parser.parse_args()
    with open(args.credentials, "r") as f:
        creds = json.load(f)
        api = Ebaki(username=creds["username"], password=creds["password"])
    api.login()
    engine = init_table(f"sqlite:///{args.sqlite}")
    with Session(engine) as session:
        session.execute(delete(Ledger))

        curr_year = date.today().year
        year_end = args.year_end or (curr_year + 1)
        if year_end < args.year_start:
            raise RuntimeError("Start year is after the end year")

        for year in range(args.year_start, year_end):
            if year == curr_year:
                data = [Ledger(**d) for d in reversed(api.current_year_ledger())]
            else:
                data = [Ledger(**d) for d in reversed(api.past_year_ledger(str(year)))]
            session.bulk_save_objects(data)
        session.commit()


if __name__ == "__main__":
    main()
