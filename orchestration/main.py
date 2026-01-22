# ------------------
# IMPORTS
# ------------------
import argparse
import sys

from utils import fresh_setup as fs
from utils import zip_setup as zs
from api import api_call as ap
from utils import setup_update as stp
from utils import supplementary as sp

# ------------------
# PARSING
# ------------------
def build_parser():
    p = argparse.ArgumentParser(
        prog="Setting-up Directories for different Hackathon based projects.",
        description="Provides functionality for the user to set-up directories and subsequent steps needed"
                    "for completion of a hackathon based ML project"
    )

    subparsers = p.add_subparsers(
        dest="command",
        required=True
    )

    # Setting Up Directories for First Time Users (No Positionals)
    file_parser = subparsers.add_parser(
        "new_user", help="Creates directories for the FIRST TIME USER, Moves files for script execution."
    )
    file_parser.add_argument("--dirs", action="store_true")

    # Normal Operation (Positionals + Optionals)
    ops_parser = subparsers.add_parser(
        "norm_ops", help="Returning User for Normal Operations"
    )
    ops_parser.add_argument("site_abv", type=str,
                            help="Abbreviated Site Name for the Project")

    ops_parser.add_argument('proj_type', type=int,
                            help="Mentions the type of project being done. 0: Regression, 1: Tabular Classification")

    ops_parser.add_argument("--api", action="store_true")

    return p


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "new_user":
        try:
            if args.dirs:
                def_inst_paths = int(input("Do you want default installation paths? 1/0: "))
                fs.NewUser(def_path=def_inst_paths).run()

        except ModuleNotFoundError:
            print("Error in Importing the Module")

        else:
            print("Setup Directories have been set-up")

    if args.command == "norm_ops":
        if args.api:
            stp.ReturnUser(site_abv=args.site_abv)
            ap.register_api(site_abv=args.site_abv)
            sp.unzip_and_extract()
            sp.copy_template(args.proj_type)

        else:
            zs.DataFoldDeal(site_abv=args.site_abv)
            sp.copy_template(args.proj_type)


# ------------------
# INITIALIZATION
# ------------------
if __name__ == "__main__":
    main()