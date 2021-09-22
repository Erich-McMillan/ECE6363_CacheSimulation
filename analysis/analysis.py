import argparse
from pathlib import Path
# import matplotlib
import benchmark

def reformat_cache_info_text(info_text: str) -> str:
   pass

def plot_sim_cycles_vs_cache_size():
   pass

def plot_mem_access_vs_cache_size():
   pass

def plot_miss_rate_vs_cache_size():
   pass

def main():
   parser = argparse.ArgumentParser()

   parser.add_argument('--results-dir', type=Path, help="path to simulator results")
   parser.add_argument('--file-pattern', type=str, help="pattern to find in files and filter by")
   parser.add_argument('--output-dir', type=Path, help="path to output results to")

   args = parser.parse_args()

   benchmarks = benchmark.parse_all_result_files_with_file_pattern(args.results_dir, args.file_pattern)
   print('hello')


if __name__ == "__main__":
   main()
