def sample_to_file(sample, f = 'sample.txt'):
    with open(f, 'w') as workfile:
        for l in sample:
        workfile.write('{}\n'.format(l))

def sample_from_file(f = 'sample.txt'):
    with open(f) as workfile:
        sample = workfile.readlines()
        return sample
    
"""def find_object(line):
    from spacy.en import English
    nlp = English()
    doc = nlp(line)

    sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]

    return sub_toks or list(doc.noun_chunks)[0]"""
