#!/bin/bash

#SBATCH -J EndothelialsMasking              # job name
#SBATCH -o error_EndothelialsMasking.o%j          # output and error file name (%j expands to jobID)
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

matlab -nodesktop -nosplash -r "endothelial_whole_brain_segmentation('DAPI_PATH','/project/ece/roysam/lbai/output/reconstruction/registered/R1C1.tif','HISTONE_PATH','/project/ece/roysam/lbai/output/reconstruction/registered/R2C2.tif','GFP_PATH','/project/ece/roysam/lbai/output/reconstruction/registered/R1C4.tif','RECA1_PATH','/project/ece/roysam/lbai/output/reconstruction/registered/R1C6.tif', 'OUTPUT_DIR','/project/ece/roysam/lbai/output/masking/endothelial_OUTPUT','CLASSIFICATION_table_path','/project/ece/roysam/lbai/output/classification/classification_table.csv','SEGMENTATION_MASKS','/project/ece/roysam/lbai/merged_labelmask.txt')"