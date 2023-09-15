# %%
import pandas as pd


def split_annotation(ann_str):
    res = {}
    for param in ann_str.split(";")[:-1]:
        key, val = param.strip().split(" ")
        res[key] = val.replace("\"", "")
    return res


def get_gencode_annotation(path):
    gen = pd.read_csv(path, sep='\t',comment='#', header=None)
    gen = gen.loc[gen[2] == 'gene']
    gencode = gen[8].apply(split_annotation).apply(pd.Series)
    gen = gen.drop(columns = [8, 1]).join(gencode)
    return gen


print("Loading annotation file...")
GENCODE = get_gencode_annotation("/srv/nvme/011_RNAseq_QC/gencode.v36.annotation.gtf")
GENCODE_MUS = get_gencode_annotation("/srv/data/mouses_new_gencode/gencode.vM10.primary_assembly.annotation.gtf")
print("Annotation file loaded")

# %%

genc = GENCODE
genc[genc['gene_name'].isin(
    ['CYGB', 'HBA1', 'HBA2', 'HBB', 'HBD', 'HBE1', 'HBG1', 'HBG2', 'HBM', 'HBQ1', 'HBZ', 'MB'])]

genc[genc['gene_name'].isin(['FP671120.6', 'FP236383.4', 'FP236383.5'])]
# len(set(genc['gene_type']))
