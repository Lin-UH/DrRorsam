#!/bin/bash

#SBATCH -J main_prepare_images              # job name
#SBATCH -o error_main_prepare_images.o%j          # output and error file name (%j expands to jobID)
#SBATCH -N 1                  # total number of nodes requested
#SBATCH --ntasks-per-node 4   # total number of processors on each node
#SBATCH --mem 90G             # total memory request
#SBATCH -p batch              # queue (partition)
#SBATCH -t 14-00:00:00        # run time (days-hh:mm:ss)
#SBATCH --mail-user=lbai@uh.edu
#SBATCH --mail-type=begin     # email me when the job starts
#SBATCH --mail-type=end       # email me when the job finishes


module load anaconda3
source activate
source deactivate
conda activate /project/ece/roysam/lbai/DrRorsam/program/NUCLEAR_SEG/envs
module load cudatoolkit/10.1


python main_prepare_images.py \
--INPUT_DIR=/project/ece/roysam/lbai/output/reconstruction/registered \
--OUTPUT_DIR=/project/ece/roysam/lbai/DrRorsam/program/NUCLEAR_SEG/data/8channels \
--DAPI R2C1.tif \
--HISTONES R2C2.tif \
--NEUN R2C4.tif \
--S100 R3C5.tif \
--OLIG2 R1C9.tif \
--IBA1 R1C5.tif \
--RECA1 R1C6.tif
#python main_prepare_images.py \
# --INPUT_DIR=/project/ece/roysam/lbai/output/reconstruction/registered \
# --OUTPUT_DIR=data \
# --DAPI R2C1.tif \
# --HISTONES R2C2.tif
