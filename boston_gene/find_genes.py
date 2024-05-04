import re


def find_genes(txt):

    txt = txt.lower()

    import yaml

    gene_info = {"genes": []}

    with open('genes.yaml', 'r') as genes_file:
        genes = yaml.safe_load(genes_file)
        gene_synonyms = dict()

        for gene in genes:
            gene_synonyms[gene['name']] = gene['synonyms']

    matches = []
    for gene_name, synonyms in gene_synonyms.items():
        to_find = synonyms + [gene_name.lower()]

        for name in to_find:
            name_regex = name.lower().replace(' ', '.').replace('-', '.').replace('(', r'\(').replace(')', r'\)')
            pattern = re.compile(rf"(^|[^a-z]){name_regex}([^a-z]|$)")
            for match in pattern.finditer(txt):
                if re.match(re.compile(rf"^{name_regex}[^a-z]"), txt) and match.start() == 0:
                    is_beginning = True
                else:
                    is_beginning = False
                if re.match(re.compile(rf"{name_regex}([^a-z]|$)$"), txt) and match.end() == len(txt) - 1:
                    is_end = True
                else:
                    is_end = False
                matches += [(gene_name, match, is_beginning, is_end)]
    if matches:
        gene_in_text = min(matches, key=lambda x: x[1].start())[0]
        positions = []
        for match in matches:
            if match[0] == gene_in_text and [match[1].start() + 1, match[1].end() - 1] not in positions and \
                    match[2] is False and match[3] is False:
                positions.append([match[1].start() + 1, match[1].end() - 1])
            elif match[0] == gene_in_text and [match[1].start(), match[1].end() - 1] not in positions and \
                    match[2] is True:
                positions.append([match[1].start(), match[1].end() - 1])
            elif match[0] == gene_in_text and [match[1].start() + 1, match[1].end()] not in positions and \
                    match[3] is True:
                positions.append([match[1].start() + 1, match[1].end()])
        positions.sort(key=lambda x: x[0])
        starts = [p[0] for p in positions]
        for position in positions:
            if starts.count(position[0]) > 1:
                positions.remove([position[0], position[1]])
        gene_info["genes"].append({"name": gene_in_text, "positions": positions})

    return gene_info


if __name__ == '__main__':

    import json

    # Open the JSON file for reading
    with open('test_texts.json', 'r') as json_file:

        # Load JSON data from the file
        texts = json.load(json_file)

        for text in texts:
            assert text['genes'] == find_genes(text['text'])['genes']

