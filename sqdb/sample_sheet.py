# %%
import re
import csv


from io import StringIO


class SampleSheet():

    def __init__(self, path=None) -> None:
        super().__init__()
        self.path = path
        self.name = path.split('/')[-1]
        self.raw_text = ""
        self.ss_dict = None
        self.biosamples = None
        #self.seq_type = seq_type

        if self.path is not None:
            self.ss_dict = self._read_sample_sheet()
            self.biosamples = self._get_biosamples()


    def _read_sample_sheet(self):
        '''
        reads SampleSheet file\n
        mutates raw_text and ss_dict fields
        '''
        with open(self.path) as file:
            ss = {}
            self.raw_text = file.read().replace(';','')
            parts = re.finditer(r"\[.*\],*\n", self.raw_text)

            last_ch = None
            
            # разделение по главам 
            for part in parts:
                chapter, bounds = part.group().replace('\n', '').replace(',', ''), part.span()
                ss[chapter] = [bounds[1]]
                if last_ch is not None:
                    ss[last_ch].append(bounds[0])

                last_ch = chapter

            # заполнение глав содержимым из csv 
            for ch, bounds in ss.items():
                if len(bounds) < 2:
                    ss[ch] = self.raw_text[bounds[0]:]
                    continue
                ss[ch] = self.raw_text[bounds[0]:bounds[1] - 1]

        return ss

    def _get_biosamples(self):

        if "[Cloud_Data]" in self.ss_dict:
            data_chapter, project_columns = "[Cloud_Data]", ("ProjectName",)
        elif "[Data]" in self.ss_dict:
            data_chapter = "[Data]"
            project_columns = ("Sample_Project", "Sample_Plate")
        elif "[BCLConvert_Data]" in self.ss_dict:
            data_chapter, project_columns = "[BCLConvert_Data]", None
        else:
            print("Unknown SampleSheet format")
            raise Exception("Unknown SampleSheet format")

        take_part_Data = self.ss_dict[data_chapter]
        test = take_part_Data
        
        take_part_Data = re.sub(r'(?i)sample_id', "Sample_ID", take_part_Data)
        take_part_Data = re.sub(r'(?i)sample_project', "Sample_Project", take_part_Data)
        take_part_Data = re.sub(r'(?i)sample_plate', "Sample_Plate", take_part_Data)
        take_part_Data = re.sub(r'(?i)projectname', "ProjectName", take_part_Data)
        take_part_Data = re.sub(r'(?i)sample_name', "Sample_Name", take_part_Data)
        take_part_Data = re.sub(r'(?i)pair_id', "Pair_ID", take_part_Data)
        
        if take_part_Data != test:
            print('-------------')
            print(f'Error column name in SampleSheet:\n     {self.path}')
            print('-------------')
        
        reader_Data = csv.DictReader(StringIO(take_part_Data))
        biosamples = []

        for line in reader_Data:
            
            if 'Sample_Name' in line:
                sample_name = line['Sample_Name']
            else: 
                sample_name = None

            if 'Pair_ID' in line: 
                pair_id = line['Pair_ID']
            else: 
                pair_id = None    

            sample_id = line["Sample_ID"]
            
            project = None
            if project_columns is not None:
                for project_column in project_columns:
                    if project_column not in line:
                        continue
                    project = line[project_column]
                    if project != None and project != '':
                        break
            project = None if project == '' else project    

            if sample_name == '':
                sample_name = None

            biosamples.append((sample_id,sample_name, project, pair_id)) 

            
        return biosamples

# %%
