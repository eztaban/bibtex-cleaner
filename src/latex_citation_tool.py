import os
import re
import shutil
import zipfile
import pandas as pd
from typing import List, Union

class LatexCitationCleaner:
    
    def __init__(self):
        self.tex_locations = list()
        self.bib_locations = None
        
        self.tex_content: List[str] = list()
        self.bib_content: str = None
        
        self.cites: List[str] = list()
        self.cite_keys: List[str] = list()
        
        self.folder = None
        # read bib content
        # for each entry in tex, read tex content
        
        # find matches for bib, do the same for all tex files
        # then ensure that all relevant information is made available in a nice format
        # make sure it can be exported to excel or similar
        # make sure new .bib file contains references from all .tex files
    
    def specific_files(self, dot_bib_location:str, dot_tex_location: Union[List[str], str]) -> None:
        """This method will load locations of specific .bib and .tex files to be analyzed

        Args:
            dot_bib_location (str): The .bib file to clean
            dot_tex_location (Union[List[str], str]): The .tex files with citations.
        """
        if isinstance(dot_tex_location, str):
            dot_tex_location = [dot_tex_location]
        self.tex_locations = dot_tex_location
        self.bib_locations = dot_bib_location
        
    def specific_fiels_in_zip(self, zip:str, dot_bib_location:str, dot_tex_location: Union[List[str], str]) -> None:
        """This method will unpack a specified zip file and load locations of specific .bib and .tex files to be analyzed

        Args:
            zip (str): zip file containing latex project
            dot_bib_location (str): The .bib file to clean
            dot_tex_location (Union[List[str], str]): The .tex files with citations.
        """
        folder = self.unpack_zip(zip_file=zip)
        self.specific_files(dot_bib_location=dot_bib_location, dot_tex_location=dot_tex_location)
    
    def all_tex_in_folder(self, folder:str, bib_file:str=None):
        """This method will assume all .tex files in the specified folder should be used to clean the .bib file.
        If no .bib file is specified, the program will automatically find the .bib file.

        Args:
            folder (str): Folder containing latex project.
            bib_file (str, optional): The .bib file to clean. Defaults to automatically searching for the .bib file.
        """
        self.folder = folder
        if bib_file is None:
            self.bib_locations = self.get_biblio_in_folder()
        else:
            self.bib_locations = os.path.join(folder, bib_file)
        self.tex_locations = self.get_tex_files_in_folder()
    
    def all_tex_in_zip(self, zip:str, bib_file:str = None):
        """_summary_

        Args:
            zip (str): Zip file containing latex project
            bib_file (str, optional): The .bib file to clean. Defaults to automatically searching for the .bib file.
        """
        folder = self.unpack_zip(zip_file=zip)
        self.all_tex_in_folder(folder=folder, bib_file=bib_file)
        
    def load(self):
        """This method will load content off all .tex-files and the .bib-file specified upon instantiation
        """
        for tex_file in self.tex_locations:
            self.tex_content.append(self.read_tex_file(tex_file))
        self.bib_content = self.read_bib_file(self.bib_locations)
        
    def analyze(self):
        """This method will identify unique cites in the specified .tex files as well as unique citation IDs in the .bib file.
        """
        for tf in self.tex_content:
            self.cites.append(self.find_unique_cites(tf))
        self.cites = list(set(*self.cites))
        self.cite_keys = self.find_unique_citation_keys(self.bib_content)
    
    def to_excel(self, filename:str=None) -> pd.DataFrame:
        """This method will create an overview of unused and used citations, export it to excel and return the same overview as a pandas dataframe.

        Args:
            filename (str, optional): Filename for exported overview. Defaults to None.

        Returns:
            pd.DataFrame: Overview of unused citations in the .bib file as well as used citations in the .tex files
        """
        if filename is None:
            overview = self.export_citations_to_excel(self.cite_keys, self.cites)
        else:
            # todo: check filename ends with xlsx
            overview = self.export_citations_to_excel(self.cite_keys, self.cites, filename=filename)
        return overview
    
    def make_clean_bib(self, bib_name: str=None) -> None:
        """Creates a new .bib file with only used citations as used in the .tex files.

        Args:
            bib_name (str, optional): Name of exported .bib-file. Defaults to filtered_biblio.bib.
        """
        if bib_name is None:
            self.filter_bib_entries(self.bib_content, self.cites)   
        else:
            # todo: check filename ends with bib
            self.filter_bib_entries(self.bib_content, self.cites)   
        
    def read_tex_file(self, filepath: str) -> str:
        """Reads the entire content of a .tex file."""
        with open(filepath, 'r', encoding='utf-8') as file:
            tex_content = file.read()
        return tex_content

    def read_bib_file(self, filepath: str) -> str:
        """Reads the entire content of a .bib file."""
        with open(filepath, 'r', encoding='utf-8') as file:
            bib_content = file.read()
        return bib_content
    
    def find_unique_citation_keys(self, stringline: str) -> List[str]:
        """Will read content of .bib file.
        Find all citation IDs, meaning @type{ID,}
        It will return a list of unique IDs

        Args:
            stringline (str): Content of .bib file

        Returns:
            List[str]: All citation keys in a list
        """
        # Regex pattern to match @type{key,
        pattern = r"@(\w+)\{([^,]+),"
        # Find all matches of @type{key,
        matches = re.findall(pattern, stringline)
        # Extract only the keys (second part of each tuple), then remove duplicates
        unique_keys = list(set(match[1] for match in matches))
        return unique_keys
    
    def find_unique_cites(self, stringline: str) -> List[str]:
        """Will read the content of a .tex file.
        Find all citation IDs used in the .tex file, meaning \cite{ID}.
        It will return a list of unique used citations.

        Args:
            stringline (str): Content of .tex file

        Returns:
            List[str]: All citations used in a .tex file
        """
        # Regex pattern to match \cite{...} and capture the content inside the braces
        pattern = r"\\cite\{([^}]+)\}"
        # Find all matches of \cite{...}
        matches = re.findall(pattern, stringline)
        # Split any comma-separated IDs and flatten the list
        flattened_matches = [item.strip() for match in matches for item in match.split(',')]
        # Convert matches to a set to get unique values, then back to a list
        unique_matches = list(set(flattened_matches))
        # Sort the list for consistent output
        unique_matches.sort()
        return unique_matches

    def export_citations_to_excel(self, all_references:List[str], used_citations:List[str], filename:str="citations_report.xlsx") -> pd.DataFrame:
        """Will consider the list of all references in the .bib file and the used citations in the .tex file and export them in an excel file, separated into two columns.
        It will also return the same data as a pandas dataframe

        Args:
            all_references (List[str]): All references in .bib file
            used_citations (List[str]): All used citations in .tex file
            filename (str, optional): The desired filename for the analysed references when saved to excel. Defaults to "citations_report.xlsx".

        Returns:
            pd.DataFrame: _description_
        """
        # Ensure uniqueness by converting to sets
        all_references_set = set(all_references)
        used_citations_set = set(used_citations)
        
        # Calculate unused references
        unused_references = list(all_references_set - used_citations_set)
        used_citations = list(used_citations_set)  # Unique citations
        
        # Create a dictionary for DataFrame
        data = {
            'Unused References': unused_references + [None] * (max(len(unused_references), len(used_citations)) - len(unused_references)),
            'Used Citations': used_citations + [None] * (max(len(unused_references), len(used_citations)) - len(used_citations))
        }
        
        # Create the DataFrame
        df = pd.DataFrame(data)
        
        output_location = os.path.join("output", filename)
        # Export to Excel
        df.to_excel(output_location, index=False)
        print(f"Data exported to {output_location}") 
        return df


    def filter_bib_entries(self, bib_content: str, used_citations: list, output_filename: str = "filtered_biblio.bib"):
        """Will compare the raw content of .bib and a list of used citations from the .tex files extracted with find_unique_cites().
        It will then remove any unused citation from the content of the .bib file and export it to a new .bib file

        Args:
            bib_content (str): The raw content of a .bib file.
            used_citations (list): Used citation IDs from .tex files.
            output_filename (str, optional): The name of the new .bib file to be exported. Defaults to "filtered_biblio.bib".
        """
        # Create a set of used citation keys for faster lookup
        used_citations_set = set(used_citations)
        
        # Pattern to match the start of each BibTeX entry with the citation key
        entry_pattern = r'@(\w+)\{([^,]+),'
        entries = re.split(r'(?=@\w+\{)', bib_content)  # Split at each entry start

        filtered_entries = []

        for entry in entries:
            # Find the citation key in the current entry
            match = re.match(entry_pattern, entry)
            if match:
                citation_key = match.group(2)  # Extract citation key
                
                # Check if the citation key is in the used list
                if citation_key in used_citations_set:
                    filtered_entries.append(entry)
        
        output_location = os.path.join("output", output_filename)
        # Write the filtered entries to a new .bib file
        with open(output_location, 'w') as f:
            for entry in filtered_entries:
                f.write(entry.strip() + "\n\n")  # Add extra line breaks between entries
        
        print(f"Filtered .bib file saved as '{output_location}'")
    
    
    def get_tex_files_in_folder(self) -> List[str]:
        """
        Returns a list of full file paths for all files in a specified folder that end with .tex.

        Args:
            folder (str): Path to the folder to search.

        Returns:
            List[str]: A list of file paths for all .tex files in the folder.
        """
        if not os.path.isdir(self.folder):
            raise ValueError(f"The specified path '{self.folder}' is not a valid directory.")

        tex_files = [
            os.path.join(self.folder, file) 
            for file in os.listdir(self.folder) 
            if file.endswith(".tex")
        ]
        return tex_files

    def get_biblio_in_folder(self) -> str:
        """
        Finds the single .bib file in the specified folder.

        Args:
            folder (str): Path to the folder to search.

        Returns:
            str: Full path to the .bib file.

        Raises:
            ValueError: If there is no .bib file or more than one .bib file in the folder.
        """
        if not os.path.isdir(self.folder):
            raise ValueError(f"The specified path '{self.folder}' is not a valid directory.")

        # List all files ending with .bib
        bib_files = [
            os.path.join(self.folder, file) 
            for file in os.listdir(self.folder) 
            if file.endswith(".bib")
        ]

        # Check for the number of .bib files found
        if len(bib_files) == 0:
            raise ValueError(f"No .bib file found in the folder: {self.folder}")
        elif len(bib_files) > 1:
            raise ValueError(f"Multiple .bib files found in the folder: {self.folder}: {bib_files}")

        return bib_files[0]
        
    @staticmethod
    def unpack_zip(zip_file: str, target_folder: str = "tmp"):
        """
        Unpacks a zip file into a specified folder.

        Args:
            zip_file (str): Path to the zip file.
            target_folder (str): Path to the folder where files will be unpacked.

        Returns:
            str: Path to the folder where the files were unpacked.

        Raises:
            ValueError: If the file is not a valid zip file.
        """
        # Validate the zip file
        if not zipfile.is_zipfile(zip_file):
            raise ValueError(f"The file '{zip_file}' is not a valid zip file.")

        # Ensure the target folder exists
        os.makedirs(target_folder, exist_ok=True)

        # Unpack the zip file
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            print(f"Unpacking files from '{zip_file}' to '{target_folder}'...")
            zip_ref.extractall(target_folder)

        print(f"Files successfully unpacked to: {target_folder}")
        return target_folder
        
    @staticmethod
    def clear_folder(folder: str):
        """
        Deletes the content of a folder without removing the folder itself.

        Args:
            folder (str): Path to the folder whose content needs to be deleted.

        Raises:
            ValueError: If the specified path is not a valid directory.
        """
        if not os.path.isdir(folder):
            raise ValueError(f"The specified path '{folder}' is not a valid directory.")

        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)  # Remove the file or symbolic link
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Remove the directory and its contents
            except Exception as e:
                print(f"Failed to delete '{item_path}'. Reason: {e}")


class CLILatexCitationCleaner(LatexCitationCleaner):
    def __init__(self):
        self.folder: str = None
        self.zip: str = None
        self.tex_locations = None
        self.bib_locations = None
        
        self.tex_content: List[str] = list()
        self.bib_content: str = None
        
        self.cites: List[str] = list()
        self.cite_keys: List[str] = list()
        
    def autorun(self):
        self.load()
        self.analyze()
        self.to_excel()
        self.make_clean_bib()
        
    def process_all_tex_in_folder(self, folder:str):
        self.folder = folder
        self.tex_locations = self.get_tex_files_in_folder()
        self.bib_locations = self.get_biblio_in_folder()
        self.autorun()
        
    def process_all_tex_in_zip(self, zip_file:str):
        folder = self.unpack_zip(zip_file=zip_file)
        self.process_all_tex_in_folder(folder=folder)
        self.clear_folder(folder)
    
    def process_specific_tex_in_folder(self, tex_files: List[str], bib_file:str, folder:str):
        self.folder = folder
        self.tex_locations = [os.path.join(folder, tf) for tf in tex_files]
        self.bib_locations = os.path.join(folder, bib_file)
        self.autorun()
    
    def process_specific_tex_in_zip(self, tex_files: List[str], bib_file:str, zip_file:str):
        folder = self.unpack_zip(zip_file=zip_file)
        self.process_specific_tex_in_folder(tex_files=tex_files, bib_file=bib_file, folder=folder)
        self.clear_folder(folder)
    

    
