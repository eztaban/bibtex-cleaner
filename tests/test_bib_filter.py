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
    filtered_entries = lcc.make_clean_bib()
    
    # this format is the same as...
    known_entries = [
        '@article{smith2023,\n  author    = {John Smith},\n  title     = {A Comprehensive Study of Machine Learning Models},\n  journal   = {Journal of Artificial Intelligence},\n  volume    = {10},\n  number    = {1},\n  pages     = {1--20},\n  year      = {2023},\n  publisher = {Springer},\n}\n\n', '@book{doe2022,\n  author    = {Jane Doe},\n  title     = {Foundations of Data Science},\n  publisher = {Academic Press},\n  year      = {2022},\n  edition   = {2nd},\n  isbn      = {978-1-23456-789-0},\n}\n\n', '@inproceedings{johnson2021,\n  author    = {Robert Johnson},\n  title     = {Advances in Neural Networks for NLP},\n  booktitle = {Proceedings of the 2021 Conference on Computational Linguistics},\n  year      = {2021},\n  pages     = {101--110},\n  organization = {ACL},\n}\n\n', '@article{williams2020,\n  author    = {Emily Williams},\n  title     = {Exploring Reinforcement Learning Techniques},\n  journal   = {AI Research Journal},\n  volume    = {15},\n  number    = {3},\n  pages     = {200--220},\n  year      = {2020},\n  publisher = {Elsevier},\n}\n\n'
                    ]
    
    # this format
    known_entries = [
"""@article{smith2023,
  author    = {John Smith},
  title     = {A Comprehensive Study of Machine Learning Models},
  journal   = {Journal of Artificial Intelligence},
  volume    = {10},
  number    = {1},
  pages     = {1--20},
  year      = {2023},
  publisher = {Springer},
}

""",

"""@book{doe2022,
  author    = {Jane Doe},
  title     = {Foundations of Data Science},
  publisher = {Academic Press},
  year      = {2022},
  edition   = {2nd},
  isbn      = {978-1-23456-789-0},
}

""",

"""@inproceedings{johnson2021,
  author    = {Robert Johnson},
  title     = {Advances in Neural Networks for NLP},
  booktitle = {Proceedings of the 2021 Conference on Computational Linguistics},
  year      = {2021},
  pages     = {101--110},
  organization = {ACL},
}

""",

"""@article{williams2020,
  author    = {Emily Williams},
  title     = {Exploring Reinforcement Learning Techniques},
  journal   = {AI Research Journal},
  volume    = {15},
  number    = {3},
  pages     = {200--220},
  year      = {2020},
  publisher = {Elsevier},
}

""",
                        ]
    
    assert known_entries == filtered_entries
    
