#!/bin/bash

#SBATCH -J NUCLEAR_SEG              # job name
#SBATCH -e NUCLEAR_SEG/error_output/error_NUCLEAR_SEG.o%j          # error file name (%j expands to jobID)
#SBATCH -o NUCLEAR_SEG/error_output/output_NUCLEAR_SEG.o%j          # output file name (%j expands to jobID)
#SBATCH --gres=gpu:1
#SBATCH -N 1                 # total number of nodes requested
#SBATCH --ntasks-per-node 4   # total number of processors on each node
#SBATCH --mem 200G             # total memory request
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

python main_nucleiSeg.py train \
 --dataset=NUCLEAR_SEG/data/multiplex.tif \
 --label=NUCLEAR_SEG/label/labels.npy \
 --logs=NUCLEAR_SEG/logs



#python main_nucleiSeg.py detect \
# --dataset=NUCLEAR_SEG/data/multiplex.tif \
# --weights=NUCLEAR_SEG/"pretrained_weights.h5" \
# --results=NUCLEAR_SEG/results


#python main_nucleiSeg.py detect \
# --dataset=NUCLEAR_SEG/demo/demo_input.jpeg \
# --weights=NUCLEAR_SEG/"pretrained_weights.h5" \
# --toRGBOpt=1 \
# --results=NUCLEAR_SEG/demo/demo_out