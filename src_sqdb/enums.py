from enum import unique, Enum


@unique
class ResourceType(Enum):

    FASTQ = 'fastq'
    BAM = 'bam'
    CSV = 'csv'
    TSV = 'tsv'

    RNA_seq = 'RNAseq'
    TEN_X_G = '10X_G'
    TEN_X_SC_RNA = 'SC_RNA'
    TEN_X_SC_ATAC = 'SC_ATAC'
    TSO500 = 'TSO500'

    def _get_params(self):
        path_to_params = {
            "fastq": {
                "ceph_folder": "/mnt/cephfs5_ro/FASTQS/*",
                "postfix": ".fastq.gz"
            },
            "RNAseq": {
                "ceph_folder": "/mnt/cephfs4_ro/DRAGEN_RES/*",
                "postfix": "/*.bam"
            }, 
            '10X_G': {
                "ceph_folder": "/mnt/cephfs3_rw/10X_RES/wgs",
                "postfix": "/*summary.csv"
            }, 
            'SC_ATAC': {
                "ceph_folder": "/mnt/cephfs3_rw/10X_RES/scATAC",
                "postfix": "/*summary.csv"
            }, 
            'SC_RNA': {
                "ceph_folder": "/mnt/cephfs3_rw/10X_RES/scRNA",
                "postfix": "/*summary.csv"
            }, 
            'TSO500': {
                "ceph_folder": "/srv/data/TSO500",
                "postfix": "*CombinedVariantOutput.tsv"
            }

        }
        return path_to_params[self.value]


@unique
class SeqType(Enum):
    seq_10X = '10X'
    seq_RNASeq = 'RNASeq'
    seq_TSO500 = 'TSO500'


@unique
class SequencerOutFormat(Enum):
    BCL = 'BCL',
    FAST5 = 'fast5'
