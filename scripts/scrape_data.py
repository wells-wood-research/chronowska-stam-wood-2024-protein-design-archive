import argparse
import os
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import re
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')

import gc
import logging
import numpy as np

log_path = "scraping_log.txt"
os.remove(log_path)
logging.basicConfig(filename=log_path, level=logging.INFO)

# "Get" functions - data scraping
def get_picture_path(pdb):
    picture_path = "https://cdn.rcsb.org/images/structures/" + pdb + "_assembly-1.jpeg"
    return picture_path

def get_authors(pdb, cif_dict):
    try:
        auth = []
        authors = []
        i = 0
        while i < 100000:
            try:
                if cif_dict["_citation_author.citation_id"][i] == 'primary':
                    auth.append(cif_dict["_citation_author.name"][i].strip())
                    i += 1
                else:
                    break
            except IndexError:
                break
        for author in auth:
            forename = author.split(",")[1].strip()
            surname = author.split(",")[0].strip()
            authors.append({"forename":forename, "surname": surname})
    except:
        authors = []

    if not authors:
        summary[pdb].append("Missing authors.")
        
    return authors

def get_classification(pdb, authors, class_dict):
    classification = "unknown"
    classification_suggested = []
    classification_suggested_reason = []
    
    dek_pdb = dek_data[dek_data["pdb"] == pdb]
    if len(dek_pdb) != 0:
        dek_class = dek_pdb["classification"].values[0]
        try:
            classification_suggested = class_dict[dek_class]
        except:
            classification_suggested = []
        classification_suggested_reason = ["Dek's classification: " + dek_class]

    for author in authors:
        key = author["forename"] + " " + author["surname"]
        try:
            classification_suggested += class_dict[key]
            classification_suggested_reason += ["Author is: " + key]
        except:
            pass

    if not classification_suggested:
        summary[pdb].append("No suggestion for classification.")
        
    return classification, classification_suggested, classification_suggested_reason

def get_release_date(pdb, cif_dict):
    try:
        release_date = cif_dict["_pdbx_audit_revision_history.revision_date"][0].strip()
    except:
        release_date = '1900-01-01'

    if (not release_date) or (release_date == ""):
        summary[pdb].append("No release date.")
        
    return release_date

def get_publication(pdb, cif_dict):
    publication = ""
    publication_country = ""
    publication_fields = []
    publication_ref = {"DOI":"", "PubMed":"", "CSD":"", "ISSN":"", "ASTM":""}
    
    try:
        publication_title = "\"" + cif_dict["_citation.title"][0].strip().rstrip('.') + "\""
    except:
        publication_title = ""
    try:
        publication_journal_abbrev = cif_dict["_citation.journal_abbrev"][0]
    except:
        publication_journal_abbrev = ""
        
    if ("to be published" in publication_journal_abbrev.lower()) or (publication_journal_abbrev == "") or (not publication_journal_abbrev) or ("tba" in publication_title.lower()):
        summary[pdb].append("Publication \"to be published\" ")
        publication = "To be published"
    
    else:
        try:
            publication_journal_volume = cif_dict["_citation.journal_volume"][0].strip().rstrip('.')
        except:
            publication_journal_volume = ""
        try:
            publication_page_first = cif_dict["_citation.page_first"][0].strip().rstrip('.')
        except:
            publication_page_first = ""
        try:
            publication_page_last = cif_dict["_citation.page_last"][0].strip().rstrip('.')
        except:
            publication_page_last = ""
        try:
            publication_id_astm = cif_dict["_citation.journal_id_ASTM"][0].strip().rstrip('.')
        except:
            publication_id_astm = ""
        try:
            publication_country = cif_dict["_citation.country"][0].strip()
        except:
            publication_country = ""
        try:
            publication_id_issn = cif_dict["_citation.journal_id_ISSN"][0].strip().rstrip('.')
        except:
            publication_id_issn = ""
        try:
            publication_id_csd = cif_dict["_citation.journal_id_CSD"][0].strip().rstrip('.')
        except:
            publication_id_csd = ""
        try:
            publication_id_pubmed = cif_dict["_citation.pdbx_database_id_PubMed"][0].strip().rstrip('.')
        except:
            publication_id_pubmed = ""
        try:
            publication_id_doi = cif_dict["_citation.pdbx_database_id_DOI"][0].strip().rstrip('.')
        except:
            publication_id_doi = ""

        if (not publication_page_last or publication_page_last == "" or publication_page_last == "?"):
            if (not publication_page_first or publication_page_first == "" or publication_page_first == "?"):
                publication_page_range = ""
            else:
                publication_page_range = publication_page_first
        else:
            if (not publication_page_first or publication_page_first == "" or publication_page_first == "?"):
                publication_page_range = publication_page_last
            else:
                publication_page_range = publication_page_first + "-" + publication_page_last
                
        publication_fields = [publication_title, publication_journal_abbrev, publication_journal_volume, publication_page_range]
        for i in publication_fields:
            if (not i) or (i == "") or (i == "?"):
                pass
            else:
                if not publication or publication == "":
                    publication = i
                else:
                    publication = publication + ", " + i
        
        publication_ref["DOI"] = (publication_id_doi if publication_id_doi != "?" else "")
        publication_ref["PubMed"] = (publication_id_pubmed if publication_id_pubmed != "?" else "")
        publication_ref["CSD"] = (publication_id_csd if publication_id_csd != "?" else "")
        publication_ref["ISSN"] = (publication_id_issn if publication_id_issn != "?" else "")
        publication_ref["ASTM"] = (publication_id_astm if publication_id_astm != "?" else "")

    if (publication == "") or (not publication) or (publication == "To be published"):
        summary[pdb].append("No publication citation info.")

    try:
        if (publication_ref["DOI"] == "") or (not publication_ref["DOI"]):
            summary[pdb].append("Missing DOI")
    except:
        pass

    return publication, publication_ref, publication_country

def get_chains(pdb, cif_dict):
    try:
        chains = []
        elements = cif_dict["_entity_poly.entity_id"]
        seq_unnat = cif_dict["_entity_poly.pdbx_seq_one_letter_code"]
        seq_nat = cif_dict["_entity_poly.pdbx_seq_one_letter_code_can"]
        seq_id = cif_dict["_entity_poly.pdbx_strand_id"]
        
        for i in range(len(elements)):
            element = elements[i]
            try:
                chain_seq_unnat = seq_unnat[i].strip().replace("\n", "")
                chain_seq_nat = seq_nat[i].strip().replace("\n", "")
                chain_id = seq_id[i].strip()
            
                seq_source = ""
                try:
                    for x in range(len(elements)):
                        if cif_dict["_entity_src_gen.entity_id"][x] == element:
                            seq_source = cif_dict["_entity_src_gen.pdbx_gene_src_scientific_name"][x]
                            break
                        elif cif_dict["_pdbx_entity_src_syn.entity_id"][x] == element:
                            seq_source = cif_dict["_pdbx_entity_src_syn.organism_scientific"][x]
                            break
                except:
                    seq_source = "unknown"
                
                if ("unknown" in seq_source) or ("unidentified" in seq_source):
                    chain_source = "unknown"
                    chain_type = "U"
                    
                else:
                    chain_source = seq_source.strip()
                    if "?" in chain_source.lower():
                        chain_source = "unknown"
                        chain_type = "U"
                    elif "synthetic" in chain_source.lower() or "artificial" in chain_source.lower():
                        chain_type = "D"
                    else:
                        chain_type = "N"
                        
                chain_length = len(seq_nat[i])
                chains.append({"chain_id": chain_id, "chain_source": chain_source, "chain_type": chain_type, "chain_seq_unnat": chain_seq_unnat, "chain_seq_nat": chain_seq_nat, "chain_length": chain_length})
            except IndexError:
                continue
    except:
        print("Error in getting chain information for", pdb)
        chains = []

    if not chains:
        summary[pdb].append("Missing sequence information.")
    
    return chains

def get_tags(pdb, cif_dict):
    tags = []
    try:
        subtitle = [title.capitalize().strip().rstrip('.') for title in cif_dict["_struct.title"]][0]
    except:
        summary[pdb].append("No keyword.")
        subtitle = ""
    try:
        keyword_struct_pdbx_descriptor = [keyword.lower().strip().rstrip('.') for keyword in cif_dict["_struct_keywords.pdbx_keywords"]]
    except:
        keyword_struct_pdbx_descriptor = []
    try:
        keyword_text = [keyword.lower().strip().rstrip('.') for keyword in cif_dict["_struct_keywords.text"][0].split(",")]
    except:
        keyword_text = []
    try:
        for tag in (keyword_struct_pdbx_descriptor+keyword_text):
            if tag not in tags:
                tags.append(tag.strip())
    except:
        tags = []

    if (not subtitle) or (subtitle == ""):
        summary[pdb].append("No subtitle.")
    
    if not tags:
        summary[pdb].append("No tags.")

    tags = list(set(tags))
    
    return subtitle, tags

def get_xray(pdb, cif_dict):
    try:
        xray_cell_length_a = cif_dict["_cell.length_a"][0].strip()
        xray_cell_length_b = cif_dict["_cell.length_b"][0].strip()
        xray_cell_length_c = cif_dict["_cell.length_c"][0].strip()
    except:
        xray_cell_length_a = ""
        xray_cell_length_b = ""
        xray_cell_length_c = ""
    try:
        xray_cell_angle_alpha = cif_dict["_cell.angle_alpha"][0].strip()
        xray_cell_angle_beta = cif_dict["_cell.angle_beta"][0].strip()
        xray_cell_angle_gamma = cif_dict["_cell.angle_gamma"][0].strip()
    except:
        xray_cell_angle_alpha = ""
        xray_cell_angle_beta = ""
        xray_cell_angle_gamma = ""
        
    crystal_structure = {"length_a":xray_cell_length_a, "length_b":xray_cell_length_b, "length_c":xray_cell_length_c, "angle_a":xray_cell_angle_alpha, "angle_b":xray_cell_angle_beta, "angle_g":xray_cell_angle_gamma}

    for key, value in crystal_structure.items():
        if (not value) or (value == "") or (value == "?"):
            crystal_structure[key] = ""
    
    for key, value in crystal_structure.items():
        if (not value) or (value == ""):
            summary[pdb].append("Missing crystal structure information.")
            break
    
    return crystal_structure

def get_exptl(pdb, cif_dict):
    try:
        exptl_method = [exptl.upper().strip().rstrip('.') for exptl in cif_dict["_exptl.method"]]
    except:
        exptl_method = ""
    try:
        formula_weight = cif_dict["_entity.formula_weight"][0].strip()
    except:
        formula_weight = ""
    try:
        synthesis_comment = cif_dict["_pdbx_entity_src_syn.details"][0].capitalize().strip().rstrip('.')
    except:
        synthesis_comment =  ""

    if (not exptl_method) or (exptl_method == ""):
        summary[pdb].append("Missing exptl_method information.")
    if (not formula_weight) or (formula_weight == ""):
        summary[pdb].append("Missing formula_weight information.")
    if (not synthesis_comment) or (synthesis_comment == ""):
        summary[pdb].append("Missing synthesis_comment information.")
    
    return exptl_method, formula_weight, synthesis_comment

def get_abstract(pdb):
    try:
        url = "https://www.rcsb.org/structure/"+pdb
        with urllib.request.urlopen(url) as response:
            xml_content = response.read()
        soup = BeautifulSoup(xml_content, "html.parser")
        text = soup.text
        # Extract abstract
        abstract_match = re.search(r"PubMed Abstract:\xa0([^&]+)", text)
        if abstract_match:
            abstract = abstract_match.group(1)
        else:
            abstract = "No description found."
    except:
        abstract = "No description found."

    if (not abstract) or (abstract == "") or ("abctract" == "No description found."):
        summary[pdb].append("No abstract description found.")
    
    return abstract

def extract_keywords_nltk(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_words = [word.lower() for word in word_tokens if word.lower() not in stop_words and word.isalnum()]
    return list(set(filtered_words))

def get_symmetry(pdb, cif_dict):
    try:
        symmetry = cif_dict["_symmetry.space_group_name_H-M"][0]
    except:
        symmetry = ""
    
    if (not symmetry) or (symmetry == ""):
        summary[pdb].append("Missing symmetry information.")
    
    return symmetry

def add_sequence_length(df):
    for i, row in df.iterrows():
        chain_list = row["chains"]
        for chain in chain_list:
            chain["chain_length"] = len(chain["chain_seq_nat"])
    return df

def fix_single_unknown_chains(df):
    for i, row in df.iterrows():
        chain_list = row["chains"]
        if all(element.get("chain_type") == "N" for element in chain_list):
            for chain in chain_list:
                chain["chain_type"] = "M"
    return df

# Fill new dataframe
def fill_data(data, pdb, cif_dir_path):
    summary[pdb] = []
    
    try:
        cif_dict = MMCIF2Dict(cif_dir_path+pdb.upper()+".cif")
    except:
        try:
            cif_dict = MMCIF2Dict(cif_dir_path+pdb.lower()+".cif")
        except:
            logging.warning(f"{pdb} file not found.")
            
            index = len(data.index)
            pdb_data = {"pdb":None, "picture_path":None, "chains":None, "authors":None, 
                "classification":None, "classification_suggested":None, "classification_suggested_reason":None, 
                "subtitle":None, "tags":None, "keywords":None, "release_date":None, 
                "publication":None, "publication_ref":None, "publication_country":None,
                "abstract":None, "crystal_structure":None, "symmetry":None,
                "exptl_method":None, "formula_weight":None, "synthesis_comment":None, 
                "review":None}
            for key, value in pdb_data.items():
                data.at[index, key] = value
            return data

    picture_path = get_picture_path(pdb)
    authors = get_authors(pdb, cif_dict)
    classification, classification_suggested, classification_suggested_reason = get_classification(pdb, authors, class_dict)
    release_date = get_release_date(pdb, cif_dict)
    publication, publication_ref, publication_country = get_publication(pdb, cif_dict)
    chains = get_chains(pdb, cif_dict)
    subtitle, tags = get_tags(pdb, cif_dict)
    crystal_structure = get_xray(pdb, cif_dict)
    symmetry = get_symmetry(pdb, cif_dict)
    exptl_method, formula_weight, synthesis_comment = get_exptl(pdb, cif_dict)
    review = True
    abstract = get_abstract(pdb)
    keywords = extract_keywords_nltk(abstract)
    
    pdb_data = {"pdb":pdb, "picture_path":picture_path, "chains":chains, "authors":authors, 
                "classification":classification, "classification_suggested":classification_suggested, "classification_suggested_reason":classification_suggested_reason, 
                "subtitle":subtitle, "tags":tags, "keywords":keywords, "release_date":release_date, 
                "publication":publication, "publication_ref":publication_ref, "publication_country":publication_country,
                "abstract":abstract, "crystal_structure":crystal_structure, "symmetry":symmetry,
                "exptl_method":exptl_method, "formula_weight":formula_weight, "synthesis_comment":synthesis_comment, 
                "review":review}
    
    for key in pdb_data:
        if pdb_data[key] == "?":
            pdb_data[key] = ""
        try:
            pdb_data[key] = pdb_data[key].replace("\n", " ")
        except:
            continue

    index = len(data.index)
    for key, value in pdb_data.items():
        data.at[index, key] = value
    
    # Clean up variables
    del cif_dict, pdb, picture_path, chains, authors, classification, classification_suggested, classification_suggested_reason
    del subtitle, tags, keywords, release_date, publication, publication_ref, publication_country, abstract
    del crystal_structure, symmetry, exptl_method, formula_weight, synthesis_comment, review
    gc.collect()

    return data

def get_prev_and_next_design(df):
    df = df.sort_values("pdb").reset_index(drop=True)
    for i in range(len(df)):
        previous_index = i - 1 if i > 0 else (len(df) - 1)
        next_index = i + 1 if i < (len(df) - 1) else 0
        
        df.at[i, "previous_design"] = df.at[previous_index, "pdb"]
        df.at[i, "next_design"] = df.at[next_index, "pdb"]
    return df

def main(next_date, prev_date, all_option):
    global summary, cif_dir_path, dek_data, class_dict

    # Define paths
    base_dir_data = "/home/mchrnwsk/pda-destress-analysis/data"
    base_dir_git = "/home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive"
    cif_dir_path = f"{base_dir_data}/cif_files/"

    # Filenames:
    filename_old_pdb_codes = f"{base_dir_git}/data/{prev_date}_data_curated.json"
    filename_new_pdb_codes = f"{base_dir_git}/data/{next_date}_pdb_codes.csv"
    filename_pdb_codes_to_manually_add = f"{base_dir_git}/entries_to_manually_include.csv"
    filename_pdb_codes_to_manually_remove = f"{base_dir_git}/entries_to_manually_exclude.csv"
    filename_output = f"{base_dir_data}/{next_date}_data"

    new_data_column_names = ["pdb","picture_path", "chains", "authors", "classification", "classification_suggested", "classification_suggested_reason", "subtitle", "tags", "keywords", "release_date", "publication", "publication_ref",  "publication_country", "abstract", "crystal_structure", "symmetry", "exptl_method", "formula_weight", "synthesis_comment", "review", "previous_design", "next_design"]

    # Read in pdb codes to scrape information for
    old_pdb = pd.read_json(filename_old_pdb_codes)["pdb"].reset_index(drop=True)
    new_pdb_codes = pd.read_csv(filename_new_pdb_codes, sep=",", header=None)[0].reset_index(drop=True)
    pdb_codes_to_manually_add = pd.read_csv(filename_pdb_codes_to_manually_add, sep=",", header=None)[0].reset_index(drop=True)
    pdb_codes_to_manually_remove = pd.read_csv(filename_pdb_codes_to_manually_remove, sep=",", header=None)[0].reset_index(drop=True)

    if not all_option:
        pdb_codes = pd.concat([new_pdb_codes, pdb_codes_to_manually_add])
        pdb_codes.drop_duplicates(inplace=True)
        pdb_codes = pdb_codes[~pdb_codes.isin(old_pdb)]
        pdb_codes = pdb_codes[~pdb_codes.isin(pdb_codes_to_manually_remove)]
        pdb_codes.sort_values(inplace=True)
        pdb_codes.reset_index(drop=True, inplace=True)
    else:
        pdb_codes = pd.concat([old_pdb, new_pdb_codes, pdb_codes_to_manually_add])
        pdb_codes.drop_duplicates(inplace=True)
        pdb_codes = pdb_codes[~pdb_codes.isin(pdb_codes_to_manually_remove)]
        pdb_codes.sort_values(inplace=True)
        pdb_codes.reset_index(drop=True, inplace=True)

    print("PDB codes to add initiated:\n", pdb_codes)

    summary = {}

    dek_data = pd.read_csv(f"{base_dir_data}/dek_classification.csv", sep=",", index_col=0) 
    class_dict = {
        "small, non-systematic, and other":["minimal"],
        "engineered":["engineered"],
        "D.N. Woolfson":["rational"],
        "C.W. Wood":["computational"],
        "D. Baker":["computational", "deep-learning based"],
        "W.F. DeGrado":["computational", "consensus"], #"minimal", "rational", "physics-based"
        "M.H. Hecht":["minimal"],
        "J.S. Richardson":["minimal"],
        "D.C. Richardson":["minimal"],
        "P.L. Dutton":["minimal"],
        "R.S. Hodges":["minimal"],
        "L. Regan":["rational", "consensus"],
        "T. Alber":["rational", "computational", "physics-based"],
        "V.P. Conticello":["rational"],
        "P.S. Kim":["rational", "computational", "physics-based"],
        "V.L. Pecoraro":["rational"],
        "T. Kortemme":["rational"],
        "L. Serrano":["rational"],
        "J.M. Berg":["consensus"],
        "B. Imperiali":["consensus"],
        "Z.-Y. Peng":["consensus"],
        "A. Pluckthun":["consensus"],
        "A.M. Buckle":["consensus"],
        "M. Lehmann":["consensus"],
        "P. Minard":["consensus"],
        "O. Rackham":["consensus"],
        "P.B. Harbury":["computational", "physics-based"],
        "B.R. Donald":["computational"],
        "A.R. Thomson":["computational"],
        "S.L. Mayo":["computational"]
        }

    # Define chunk size for next_dateing
    chunk_size = 100
    num_chunks = len(pdb_codes) // chunk_size + 1

    for i, chunk in enumerate(np.array_split(pdb_codes, num_chunks)):
        print(f"Processing chunk {i} of {num_chunks}.")
        new_data = pd.DataFrame(columns=new_data_column_names)
        for pdb in chunk:
            logging.info(f"updating chunk: {i}, entry: {pdb}")
            try:
                new_data = fill_data(new_data, pdb, cif_dir_path)
            except Exception as e:
                logging.error(f"Error updating {pdb}: {str(e)}")
        new_data["formula_weight"] = new_data["formula_weight"].astype(float)
        new_data.to_json(f"{filename_output}_{i}", orient="records", indent=4)
        del new_data
        gc.collect()

    print("Concatenating chunks into one dataframe.")    
   # Concatenating chunks into one dataframe
    all_chunked_data = pd.DataFrame(columns=new_data_column_names)
    for i in range(num_chunks):
        path = f"{filename_output}_{i}"
        df = pd.read_json(path)
        all_chunked_data = pd.concat([all_chunked_data, df], ignore_index=True)
        try:
            os.remove(path)
        except OSError as e:
            logging.error(f"Error deleting file {path}: {str(e)}")

    # Ensure '0' column is removed if it appears
    all_chunked_data = all_chunked_data.loc[:, new_data_column_names]
    old_pdb = pd.read_json(filename_old_pdb_codes).reset_index(drop=True)

    # Concatenate old and new data
    if not all_option:
        new_data = pd.concat([old_pdb, all_chunked_data], ignore_index=True)
    else:
        new_data = all_chunked_data

    new_data_curated = new_data[~new_data["pdb"].isin(pdb_codes_to_manually_remove)]
    # Tidy up
    print("Tidy up: remove duplicates.")
    tidy_data = new_data_curated.drop_duplicates(subset="pdb")
    print("Tidy up: sort values.")
    tidy_data.sort_values(by="pdb", inplace=True)
    print("Tidy up: reset index.")
    tidy_data.reset_index(drop=True)
    tidy_data["formula_weight"] = tidy_data["formula_weight"].astype(float)
    print("Tidy up: encode previous and next designs.")
    reordered_data = get_prev_and_next_design(tidy_data)

    data_result = reordered_data.to_json(f"{base_dir_data}/{next_date}_data_reordered.json", orient="records", indent=4)
    print(f"Data saved to {base_dir_data}/{next_date}_data.json")

if __name__ == "__main__":
   # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Scrape PDB data')
    parser.add_argument('--next', required=True, help='Next date (e.g., 20240930)')
    parser.add_argument('--prev', required=True, help='Prev date (e.g., 20240827)')
    parser.add_argument('--all', action='store_true', help='Scrape for the whole dataset, not just new codes.')
    args = parser.parse_args()
    
    next_date = args.next
    prev_date = args.prev
    all_option = args.all

    print("Logging in /home/mchrnwsk/pda-destress-analysis/scraping_log.txt")
    main(next_date, prev_date, all_option)