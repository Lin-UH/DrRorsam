#!/bin/bash

#SBATCH -J OligodendrocyteMasking              # job name
#SBATCH -o error_OligodendrocyteMasking.o%j          # output and error file name (%j expands to jobID)
#SBATCH -N 1                  # total number of nodes requested
#SBATCH --ntasks-per-node 4   # total number of processors on each node
#SBATCH --mem 90G             # total memory request
#SBATCH -p batch              # queue (partition)
#SBATCH -t 14-00:00:00        # run time (days-hh:mm:ss)
#SBATCH --mail-user=lbai@uh.edu
#SBATCH --mail-type=begin     # email me when the job starts
#SBATCH --mail-type=end       # email me when the job finishes


module load anaconda3
module load matlab
source activate
source deactivate
conda activate /project/ece/roysam/lbai/DrRorsam/serverenvs

matlab -nodesktop -nosplash -r "oligodendrocytes_whole_brain_segmentation('DAPI_PATH','/project/ece/roysam/lbai/output/reconstruction/registered/R1C1.tif','HISTONE_PATH','/project/ece/roysam/lbai/output/reconstruction/registered/R2C2.tif','OLIG2_PATH','/project/ece/roysam/lbai/output/reconstruction/registered/R1C5.tif','CNPASE_PATH','/project/ece/roysam/lbai/output/reconstruction/registered/R5C4.tif','OUTPUT_DIR','/project/ece/roysam/lbai/output/reconstruction/masking/oligodendrocytes_OUTPUT','CLASSIFICATION_table_path','/project/ece/roysam/lbai/output/classification/classification_table.csv','SEGMENTATION_MASKS','/project/ece/roysam/lbai/merged_labelmask.txt')"