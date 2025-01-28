import sys
import os

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    

import os
from src.latex_citation_tool import LatexCitationCleaner

def test_unique_cites():
    lcc = LatexCitationCleaner()
    bib = os.path.join("tests", "test_material", "biblio.bib")
    tex = os.path.join("tests", "test_material", "citations.tex")
    
    lcc.specific_files(dot_bib_location=bib, dot_tex_location=tex)
    lcc.load()
    lcc.analyze()
    
    found_citations = lcc.cites
    
    unique_cites = ["doe2022", "johnson2021", "smith2023", "williams2020"]
    
    assert unique_cites == found_citations
    
