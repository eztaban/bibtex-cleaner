import argparse

def get_args():
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="LaTeX Cleaner CLI")
    
    # Add flags
    parser.add_argument(
        "--all_tex",
        action="store_true",
        help="Process all .tex files in the specified location (folder or zip)."
    )
    parser.add_argument(
        "--spec_tex",
        nargs="+",
        type=str,
        help="Process specific .tex files. Provide a space-separated list of filenames."
    )
    parser.add_argument(
        "--bib",
        type=str,
        help="Path to the .bib file to be used with specific .tex files."
    )
    parser.add_argument(
        "--folder",
        type=str,
        metavar="FOLDER",
        help="Path to the folder containing the .tex files (and optional .bib file)."
    )
    parser.add_argument(
        "--zip",
        type=str,
        metavar="ZIP",
        help="Path to the zip file containing the .tex files (and optionally .bib file)."
    )
    
    # Parse arguments
    args = parser.parse_args()

    # Ensure either --folder or --zip is specified
    if not (args.folder or args.zip):
        parser.error("Either --folder or --zip must be specified to locate the input files.")
    
    # If --spec_tex is specified, ensure --bib is also provided
    if args.spec_tex and not args.bib:
        parser.error("The --spec_tex argument requires --bib to be specified.")
    
    return args
