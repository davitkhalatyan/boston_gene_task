from find_hla import find_hla, equal_ignore_order
from find_genes import find_genes
import json

"""
Negatives: There is no gene/hla.
Positives: There is gene/hla.
True Positives: Correctly identifies existing gene/hla.
True Negative: Finds no gene/hla.
False Positive: Cannot find gene/hla although it is in the text or it finds wrong gene/hla.
False Negative: Finds gene/hla although there is none.
"""

tp_gene = 0
fp_gene = 0
tn_gene = 0
fn_gene = 0

tp_hla = 0
fp_hla = 0
tn_hla = 0
fn_hla = 0

with open('test_texts.json', 'r') as json_file:
    items = json.load(json_file)

    for item in items:

        genes = find_genes(item['text'])['genes']
        hla = find_hla(item['text'])['hla']

        if equal_ignore_order(item['genes'], genes):
            if item['genes']:
                tp_gene += 1
            else:
                tn_gene += 1
        else:
            if item['genes']:
                fp_gene += 1
            else:
                fn_gene += 1

        if equal_ignore_order(item['hla'], hla):
            if item['hla']:
                tp_hla += 1
            else:
                tn_hla += 1
        else:
            if item['hla']:
                fp_hla += 1
            else:
                fn_hla += 1

    print("find_genes TP: ", tp_gene)
    print("find_genes FP: ", fp_gene)
    print("find_genes TN: ", tp_gene)
    print("find_genes FN: ", fn_gene)
    print("find_hla TP: ", tp_hla)
    print("find_hla FP: ", fp_hla)
    print("find_hla TN: ", tn_hla)
    print("find_hla FN: ", fn_hla)

    precision_gene = tp_gene/(tp_gene + fp_gene)
    print("find_gene Precision: ", precision_gene)
    precision_hla = tp_hla/(tp_hla + fp_hla)
    print("find_hla Precision: ", precision_hla)

    recall_gene = tp_gene/(tp_gene + fn_gene)
    print("find_gene Recall: ", recall_gene)
    recall_hla = tp_hla/(tp_hla + fn_gene)
    print("find_hla Recall: ", recall_hla)

    f1_gene = 2 * precision_gene * recall_gene/(precision_gene + recall_gene)
    print("find_gene F1: ", f1_gene)
    f1_hla = 2 * precision_hla * recall_hla/(precision_hla + recall_hla)
    print("find_hla F1: ", f1_hla)
