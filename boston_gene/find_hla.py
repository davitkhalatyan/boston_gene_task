import re


def equal_ignore_order(a, b):
    """ Use only when elements are neither hashable nor sortable! """
    unmatched = list(b)
    for element in a:
        try:
            unmatched.remove(element)
        except ValueError:
            return False
    return not unmatched


def find_hla(txt):
    hla_info = {"hla": []}

    pattern = r'(((HLA|Human Leukocyte Antigen)[-)\s]+?)|\s-)' \
              r'(?P<gene>[A-Z]+[14]?)[*]?(?P<allele>0?[1-9]+)?[-.:*]?(?P<protein>0?[0-9]+)?'
    matches = re.finditer(pattern, txt)

    for match in matches:
        for_check = r"\(HLA\)"
        match_start = match.start()

        if txt[match.start():match.end()].startswith(' -'):
            match_start = match.start() + 2

        hla_info["hla"].append({
            "gene": match.group("gene"),
            "allele": match.group("allele"),
            "protein": match.group("protein"),
            "positions": [[match_start, match.end()]]
        })

        if re.search(re.compile(for_check), txt):
            hla_info["hla"][-1]["positions"][0][0] -= 1

        new_pattern = rf'\s{match.group("gene")}[*](?P<allele>0?[1-9]+)[-.:*](?P<protein>0?[0-9]+)'
        new_matches = re.finditer(new_pattern, txt)
        for new_match in new_matches:
            if new_match.start() == 0:
                start = 0
            else:
                start = new_match.start() + 1
            if new_match.end() not in [position[1] for hla in hla_info['hla'] for position in hla['positions']]:
                hla_info["hla"].append({
                    "gene": match.group("gene"),
                    "allele": new_match.group("allele"),
                    "protein": new_match.group("protein"),
                    "positions": [[start, new_match.end()]]
                })

    return hla_info


if __name__ == '__main__':

    import json

    # Open the JSON file for reading
    with open('test_texts.json', 'r') as json_file:

        # Load JSON data from the file
        texts = json.load(json_file)

        for text in texts:
            assert equal_ignore_order(text['hla'], find_hla(text['text'])['hla'])
