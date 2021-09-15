#!/bin/bash

#SBATCH -J AstrocyteMasking              # job name
#SBATCH -o error_AstrocyteMasking.o%j          # output and error file name (%j expands to jobID)
#SBATCH -N 2                  # total number of nodes requested
#SBATCH --ntasks-per-node 8   # total number of processors on each node
#SBATCH --mem 360G             # total memory request
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

matlab -nodesktop -nosplash -r "astrocytes_whole_brain_segmentation('DAPI_PATH','/project/ece/roysam/lbai/output/reconstruction/registered/R1C1.tif', 'HISTONE_PATH','/project/ece/roysam/lbai/output/reconstruction/registered/R2C2.tif','S100_PATH','/project/ece/roysam/lbai/output/reconstruction/registered/R3C5.tif','GFAP_PATH', '/project/ece/roysam/lbai/output/reconstruction/registered/R3C3.tif','OUTPUT_DIR','/project/ece/roysam/lbai/output/reconstruction/masking/astrocytes_OUTPUT','CLASSIFICATION_table_path', '/project/ece/roysam/lbai/output/classification/classification_table.csv','SEGMENTATION_MASKS','/project/ece/roysam/lbai/merged_labelmask.txt')"
