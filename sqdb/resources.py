# %%
from glob import glob
import os
import re 
from .dbapi import BioSample, Resource
from .enums import ResourceType, SeqType
from .annotation import GENCODE, GENCODE_MUS
from .added_params import get_subtype,\
                        get_Pool_num, \
                        get_resources_path, \
                        rename_sNAME_2_sID


import json
from random import paretovariate
import pandas as pd
import csv
from io import StringIO

#---------------------------------------------------------------------------------
def get_samplesheet_info(pattern):
    found_path = sorted(glob(f"/mnt/ngs_stats/*/*{pattern}*.csv")) +\
                    sorted(glob(f"/mnt/ngs_stats_nextseq/*/*{pattern}*.csv"))
    # Ищем SampleSheet 
    ok_paths = []                                           

    if '10X' not in pattern:                                                    
        type_seq = pattern                                                 
    else:
        type_seq = pattern.split('_')[0]


    for path in found_path:
        path_dict = {}
        if 'bak' not in path and os.access(path, os.R_OK) is True:                          # Фильтр от .bak
            if 'convert' not in path:                                                       # Фильтр от convert
                path_dict['SampleSheet'] = path                                             # Путь SampleSheet
                path_dict['Flowcell'] = path.split('/')[-2]                                 # Имя Flowcell
                path_dict['SampleSheet_name'] = path.split('/')[-1].split('.csv')[0]        # Имя SampleSHeet
                path_dict['Pool'] = get_Pool_num(path)                                      # Номер Pool
                path_dict['Type'] = type_seq                                                # Общий тип
                path_dict['Subtype'] = get_subtype(path)                                    # Подтип    

                # Проверяем норм ли имя ячейки (чтобы избежать _tmp_10X )
                if re.search(r'^\d{6}_.*_.*', path.split('/')[-2]) != None:  
                    ok_paths.append(path_dict)

    return ok_paths

def get_flowcell_resources(resource_type: ResourceType, 
                           flowcell: str, 
                           samplesheet_content=None, 
                           run=None):
    
    files = get_resources_path(resource_type, flowcell, run)                            # Парсинг по цефу для поиска файлов-ресурсов
    
    out = {}
    if files != None:
        for file in files: 
            if '.bam' in file or '.fastq.gz' in file:                                       # Словарь для RNASeq.bam и FASTQ
                sample_rep = file.split("/")[-1].split("_S")[0]
                sample_rep = re.sub(r'_\d{1,2}$', '', sample_rep)

            elif 'summary.csv' in file:                                                     # Словарь для 10X
                sample_rep = file.split('/')[-3]
                sample_rep = rename_sNAME_2_sID(sample_rep, 
                                                samplesheet_content.biosamples)             # Переименование SampleID (если 2 колонки)

            if sample_rep not in out:                                                         
                out[sample_rep] = []
            out[sample_rep].append(file)

    return out

def get_pattern_resources(sample_sheet: str, 
                          flowcell: str, 
                          samplesheet_content=None, 
                          run=None):
    
    metrics = None
    fastqs = None
    
    if 'RNASeq' in sample_sheet:                                                        # Собираем метрики для RNASeq
        metrics = get_flowcell_resources(ResourceType.RNA_seq, 
                                    flowcell,
                                    samplesheet_content,
                                    run)
    elif '10X_G' in sample_sheet:                                                       # Собираем метрики для 10X_G
        metrics = get_flowcell_resources(ResourceType.TEN_X_G, 
                                    flowcell,
                                    samplesheet_content,
                                    run)
    elif '10X_SC_RNA' in sample_sheet:                                                  # Собираем метрики для 10X_SC_RNA
        metrics = get_flowcell_resources(ResourceType.TEN_X_SC_RNA, 
                                    flowcell,
                                    samplesheet_content,
                                    run)
    elif '10X_SC_ATAC' in sample_sheet:                                                 # Собираем метрики для 10X_SC_ATAC
        metrics = get_flowcell_resources(ResourceType.TEN_X_SC_ATAC, 
                                    flowcell,
                                    samplesheet_content,
                                    run)

    fastqs = get_flowcell_resources(ResourceType.FASTQ,                                 # Собираем фалйы для FASTQ
                                    flowcell,
                                    samplesheet_content,
                                    run)
    
    return {'metrics':metrics, 
            'fastqs':fastqs}
#--------------------------------------------------------------------------------

class FastqResource(Resource):

    def get_metrics(self):
        self.metrics = None

class TenXResource(Resource): 
     
    def get_metrics(self): 
        
        csv_path = self.path
        convert_json = pd.read_csv(csv_path).fillna(0).to_dict(orient='records')[0]

        self.metrics = convert_json

class TSO500Resource(Resource): 
    
    def get_metrics(self): 
        
        tsv_path = self.path
        
        pair = tsv_path.split('/')[-2]
        metrics_path = tsv_path.rsplit('/', 2)[0]
        metrics_path = f'{metrics_path}/MetricsOutput.tsv'
   
        with open(metrics_path) as file:
            ss = {}
            raw_text = file.read().replace('\t',',')
            parts = re.finditer(r"\[.*\],*\n", raw_text)

            last_ch = None

            for part in parts:
                chapter, bounds = part.group().replace('\n', '').replace(',',''), part.span()
                ss[chapter] = [bounds[1]]
                if last_ch is not None:
                    ss[last_ch].append(bounds[0])
                last_ch = chapter

            for ch, bounds in ss.items():
                if len(bounds) < 2:
                    ss[ch] = raw_text[bounds[0]:]
                    continue
                ss[ch] = raw_text[bounds[0]:bounds[1] - 1]

        dict_metrics = {}
        
        for metrica_tsv_name in ['DNA Library QC Metrics', 
                                 'DNA Library QC Metrics for Small Variant Calling and TMB',
                                 'DNA Library QC Metrics for MSI', 
                                 'DNA Library QC Metrics for CNV', 
                                 'DNA Expanded Metrics', 
                                 'RNA Library QC Metrics', 
                                 'RNA Expanded Metrics']:
        
            take_part_Data = ss[f'[{metrica_tsv_name}]']
            take_part_Data = re.sub(r',{2}', '', take_part_Data)

            reader_Data = csv.DictReader(StringIO(take_part_Data))
            metrica_tsv_name = metrica_tsv_name.replace(' ','_').lower()

            dict_metrics[metrica_tsv_name] = {}   

            for line in reader_Data:

                name_metrica = list(line.keys())[0]

                if pair in line: 

                    metrica = line[name_metrica]
                    value = line[pair]

                    if value == None:
                        value = 0

                    if value != 'NA': 
                        value = float(value)
                    else: 
                        value = 0
                else: 
                    metrica = line[name_metrica]
                    value = 0

                metrica = metrica.replace(' ', '_').lower().replace("_(%)", '').replace('(', '').replace(')','').replace('.','')
                dict_metrics[metrica_tsv_name][metrica] = value

        
        self.metrics = dict_metrics
  
class RnaBamResource(Resource):

    def _get_quant_metrics(self, quant_genes_file, gencode_hum, gencode_mus):

        if 'rna_mus' in quant_genes_file: 
            gencode = gencode_mus
        else: 
            gencode = gencode_hum

        df = pd.read_csv(quant_genes_file, sep='\t')
        df = pd.merge(df, gencode[['gene_id', 'gene_name', 'gene_type']], how='left', left_on='Name', right_on='gene_id')

        gene_types = set(gencode['gene_type'])

        quant_metrics = {}
        df['reads_proportion'] = df['NumReads'] / df['NumReads'].sum()

        for gt in gene_types:
            if gt not in set(df['gene_type']):
                quant_metrics[gt] = 0.0
                continue

            quant_metrics[gt] = df.loc[df['gene_type'] == gt, 'reads_proportion'].sum()

        quant_metrics['globins'] = df.loc[df['gene_name'].isin(
            ['CYGB', 'HBA1', 'HBA2', 'HBB', 'HBD', 'HBE1', 'HBG1', 'HBG2', 'HBM', 'HBQ1', 'HBZ', 'MB']), 'reads_proportion'].sum()
        quant_metrics['protein_coding'] -= quant_metrics['globins']

        return quant_metrics

    def _get_mapping_metrics(self, mapping_metrics_file):
        # print(mapping_metrics_file)
        with open(mapping_metrics_file) as file:
            return json.load(file)['Attributes']['illumina_dragen_complete_v0_1']

    def get_metrics(self):
        sample_prefix = self.path.replace(".bam", "")
        quant_metrics = self._get_quant_metrics(f"{sample_prefix}.quant.genes.sf", GENCODE, GENCODE_MUS)
        mapping_metrics = self._get_mapping_metrics(f"{sample_prefix}.metrics.json")

        self.metrics = {"quant_metrics": quant_metrics, "mapping_metrics": mapping_metrics}

# %%
