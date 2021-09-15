import os
import sys
import time
import argparse
import subprocess

###################################################################
# NAMING PROTOCOL: RxCy (x = round number | y = channel number)
###################################################################


parser = argparse.ArgumentParser()
parser.add_argument('--INPUT_DIR', type=str, default='/project/ece/roysam/lbai/S1/original', help='/path/to/input/dir')
parser.add_argument('--OUTPUT_DIR', type=str, default='/project/ece/roysam/lbai/output/reconstruction', help='/path/to/output/dir')
parser.add_argument('--MODE', type=str, default=r'unsupervised', help='supervised | unsupervised')
args, _ = parser.parse_known_args()

# for supervised
if args.MODE == 'supervised':
    parser.add_argument('--SCRIPT', type=str, default=r'scripts/20_plex.csv', help='/path/to/script.csv')

# for unsupervised
if args.MODE == 'unsupervised':
    parser.add_argument('--DEFAULT_BOX', type=int, nargs='+', default=[34000, 8000, 44000, 15000], help='xmin ymin xmax ymax')
    parser.add_argument('--BRIGHTFIELD', type=int, default=11, help='int | None')
    args, _ = parser.parse_known_args()
    # create script if not specified
    from RECONSTRUCTION.prepare_script import create_script
    create_script(os.path.join(args.OUTPUT_DIR, 'script.csv'), args.INPUT_DIR, args.DEFAULT_BOX, brightfield=args.BRIGHTFIELD)
    parser.add_argument('--SCRIPT', type=str, default=os.path.join(args.OUTPUT_DIR, 'script.csv'), help='/path/to/script.csv')

args = parser.parse_args()


# REGISTRATION
RECONSTRUCTION_DIR = os.path.join(os.getcwd(),"RECONSTRUCTION")
sys.path.append(RECONSTRUCTION_DIR)  # To find local version of the library


from RECONSTRUCTION.registration import registration
start = time.time()
input_dir = args.INPUT_DIR
output_dir = os.path.join(args.OUTPUT_DIR, 'registered')
registration(input_dir,output_dir)
# p = subprocess.call(command, shell=True)
duration = time.time() - start
m, s = divmod(int(duration), 60)
h, m = divmod(m, 60)
print('Registration pipeline finished successfully in {:d} hours, {:d} minutes and {:d} seconds.'.format(h, m, s))
# INTRA CHANNEL CORRECTION
from RECONSTRUCTION.intra_channel_correction import intra_channel_correct
ipnut_dir = os.path.join(args.OUTPUT_DIR, 'registered')
output_dir = os.path.join(args.OUTPUT_DIR, 'intra_corrected')
disk_size = [40, 80]
start = time.time()
intra_channel_correct(ipnut_dir, output_dir, disk_size, args.SCRIPT)
duration = time.time() - start
m, s = divmod(int(duration), 60)
h, m = divmod(m, 60)
print('Intra channel correction finished successfully in {:d} hours, {:d} minutes and {:d} seconds.'.format(h, m, s))


# INTER CHANNEL CORRECTION
input_dir = os.path.join(args.OUTPUT_DIR, 'intra_corrected')
output_dir = os.path.join(args.OUTPUT_DIR, 'inter_corrected')
start = time.time()
if args.MODE == 'unsupervised':
    from RECONSTRUCTION.inter_channel_correction import inter_channel_correct_unsupervised
    inter_channel_correct_unsupervised(input_dir, output_dir, args.SCRIPT)
elif args.MODE == 'supervised':
    from RECONSTRUCTION.inter_channel_correction import inter_channel_correct_supervised
    inter_channel_correct_supervised(input_dir, output_dir, args.SCRIPT)
duration = time.time() - start
m, s = divmod(int(duration), 60)
h, m = divmod(m, 60)
print('Inter channel correction finished successfully in {:d} hours, {:d} minutes and {:d} seconds.'.format(h, m, s))
