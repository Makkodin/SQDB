import re
from .enums import ResourceType
from glob import glob

# Получение субтипа
def get_subtype(ss_path):
    subtype = ss_path.split('/')[-1]
    if 'SampleSheet' not in subtype:
        first_part = re.findall(r'\d{4}_\d{2}_\d{2}_', subtype)[0]
    else: 
        first_part = re.findall(r'SampleSheet_\d{4}_\d{2}_\d{2}_', subtype)[0] 
    
    last_part = re.findall(r'(?i)_pool[a-zA-Z]{,5}\d+.csv', subtype)[0]
    subtype = subtype.replace(first_part, '')
    subtype = subtype.replace(last_part, '')

    return subtype

# Изъятие имени Pool
def get_Pool_num(ss_path): 
    # для 10X_SC_ATAC
    pool = re.findall(r'(?i)pool[a-zA-Z]{,5}\d+', ss_path)[0]
    name = re.findall(r'(?i)pool', pool)[0]
    num = re.findall(r'(?i)\d+', pool)[0]
    new_pool = re.sub(r'(?i)pool', 'run', name) + num
    return new_pool

# Парсим цев для поиска ресурсов
def get_resources_path(resource_type: ResourceType, 
                       flowcell: str,
                       run: str): 

    params = resource_type._get_params()
    if resource_type == ResourceType.TSO500: 
        files = glob(f"{params['ceph_folder']}/*{flowcell}*/*LocalApp*/vcf/Results/*/**{params['postfix']}") +\
                glob(f"{params['ceph_folder']}TSO500/*{flowcell}*/*LocalApp*/vcf/Results/*/**{params['postfix']}") 
              
    elif resource_type == ResourceType.TEN_X_G or \
        resource_type == ResourceType.TEN_X_SC_RNA or \
        resource_type == ResourceType.TEN_X_SC_ATAC:
        files = glob(f"{params['ceph_folder']}/*/*{flowcell}*/*/**{params['postfix']}")

    elif resource_type == ResourceType.RNA_seq or \
        resource_type == ResourceType.FASTQ: 
        files = glob(f"{params['ceph_folder']}/{flowcell}*/**{params['postfix']}") + \
                glob(f"{params['ceph_folder']}/{flowcell}*/*/**{params['postfix']}") + \
                glob(f"{params['ceph_folder']}/{flowcell}*/*/*/**{params['postfix']}") + \
                glob(f"{params['ceph_folder']}/{flowcell}*/*/*/*/**{params['postfix']}")
    else:
        files = None
        print('Unknow type!')
    
    ok_files = []
    for file in files: 
        if '.bak' not in file:
            ok_files.append(file)

    return ok_files


# Смотрим каких биосэмплов нет (не обработаны DRAGEN)
def get_noexit_resources(sample_sheet, fastq_res, metrics_res):

    all_biosamples = []
    for SampleID, SampleName, Project, Pool in sample_sheet.biosamples:
        if SampleName == None: 
            bioS = re.sub(r'_\d{1,2}$', '', SampleID)
        else:
            bioS = re.sub(r'_\d{1,2}$', '', SampleName)
        all_biosamples.append(bioS)
    all_biosamples = set(all_biosamples)

    fastq_biosamples = set(fastq_res.keys())
    metrics_biosamples = set(metrics_res.keys())

    no_fastq = set(list(all_biosamples - fastq_biosamples))
    no_metrics = set(list(all_biosamples - metrics_biosamples))

    return {'No fastqs':list(no_fastq), 
            'No metrics': list(no_metrics),
            'SS biosamples':list(all_biosamples)}

def rename_sNAME_2_sID(sample_name: str, biosamples: str):
    sID = sample_name
    for biosample in biosamples: 
        if sample_name in biosample[0]: 
            if re.search(r'_\d$', biosample[1]) != None: 
                sID = biosample[1].rsplit('_', 1)[0]
            else: 
                sID = biosample[1]
    return sID


def get_replics(biosamples): 

    if biosamples[1] == None:
        biosample = biosamples[0]
    else: 
        biosample = biosamples[1]

    replica = None
    if re.search(r'_\d{1,2}$', biosample) != None:
        biosample_rep = biosample.rsplit("_", maxsplit=1)
    else: 
        biosample_rep = biosample
        
    if len(biosample_rep) == 2:
        biosample_name, replica = biosample_rep
    else:
        biosample_name = biosample
        replica = None
    
    return biosample_name, replica


        #elif 'CombinedVariantOutput.tsv'  in file: 
        #    sample_rep = file.split("/")[-2]
        #    for biosample in biosamples_list: 
        #        bID = biosample[0]
        #        pair_name = biosample[3] 
        #        if sample_rep in pair_name:
        #            if re.search(r'_\d{1,2}$',bID) != None:
        #                bID = bID.rsplit('_',1)[0]
        #                sample_rep = bID
        #            else: 
        #                sample_rep = bID 
        #    if sample_rep not in out:
        #        out[sample_rep] = []  
        #    out[sample_rep].append(file)


#def check_DRAGEN_path(flowcell, resource_type: ResourceType):
#    params = resource_type._get_params()  
#    check_dragen = glob(
#            f"{params['dragen_folder']}/*{flowcell}*") + \
#        glob(
#            f"{params['dragen_folder']}/*/*{flowcell}*")
#    ok_path = []
#    for drag in check_dragen:
#        if '.bak' not in drag:
#            ok_path.append(drag)
#    check_dragen = ok_path
#
#    if len(check_dragen) == 0:
#        check_dragen = False
#    else: 
#        check_dragen = True
#    
#    return check_dragen