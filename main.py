from src import get_args
from src import CLILatexCitationCleaner as LatexCitationCleaner  # Adjust this import based on your project structure

def main():
    lcc = LatexCitationCleaner()
    # Parse command-line arguments
    args = get_args()
    
    # Default to --all_tex if only --folder or --zip is specified
    if (args.folder or args.zip) and not (args.all_tex or args.spec_tex):
        args.all_tex = True

    # Check if --all_tex is specified
    if args.all_tex:
        if args.folder:
            print(f"Processing all .tex files in folder: {args.folder}")
            lcc.process_all_tex_in_folder(args.folder)
        elif args.zip:
            print(f"Processing all .tex files from zip file: {args.zip}")
            lcc.process_all_tex_in_zip(args.zip)
    
    # Check if --spec_tex and --bib are specified
    if args.spec_tex and args.bib:
        if args.folder:
            print(f"Processing specific .tex files: {args.spec_tex}")
            print(f"Using .bib file: {args.bib}")
            print(f"From folder: {args.folder}")
            tex_files = [tf for tf in args.spec_tex]
            lcc.process_specific_tex_in_folder(tex_files, args.bib, args.folder)
        elif args.zip:
            print(f"Processing specific .tex files: {args.spec_tex}")
            print(f"Using .bib file: {args.bib}")
            print(f"From zip file: {args.zip}")
            tex_files = [tf for tf in args.spec_tex]
            lcc.process_specific_tex_in_zip(tex_files, args.bib, args.zip)

if __name__ == "__main__":
    main()
