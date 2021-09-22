import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import benchmark

def get_distinct_benchmark_programs(benchmarks) -> list:
   program_list = []
   for benchmark in benchmarks.values():
      program_name = benchmark['benchmark_program_name']
      if program_name not in program_list:
         program_list.append(program_name)

   return program_list

def get_IL1_sizes(benchmarks) -> list:
   sizes = []

   for b in benchmarks:
      if b['cache_il1'] not in sizes:
         sizes.append(b['cache_il1'])

   return sizes

def sort_benchmarks_by_il1_cache_size(benchmarks) -> list:
   return benchmarks # not yet implemented

def get_sim_cycles(benchmarks, programs):
   sim_cycle_results = {}
   sim_cycle_results['il1'] = {}
   sim_cycle_results['dl1'] = {}
   sim_cycle_results['ul1'] = {}

   program_benchmarks = [b for b in benchmarks.values() if b['benchmark_program_name'] == list(benchmarks.values())[0]['benchmark_program_name']]
   IL1_sizes = get_IL1_sizes(program_benchmarks)
   # DL1_sizes = get_DL1_sizes(benchmarks, programs[0])
   # UL2_sizes = get_UL2_sizes(benchmarks, programs[0])

   for il1 in IL1_sizes:
      sim_cycle_results['il1'][il1] = []

   # for dl1 in DL1_sizes:
   #    sim_cycle_results['dl1'][dl1] = []

   # for ul2 in UL2_sizes:
   #    sim_cycle_results['ul1'][ul2] = []

   for program in programs:
      program_benchmarks = [b for b in benchmarks.values() if b['benchmark_program_name'] == program]
      program_benchmarks = sort_benchmarks_by_il1_cache_size(program_benchmarks)
      for benchmark in program_benchmarks:
         sim_cycle_results['il1'][benchmark['cache_il1']].append(benchmark['sim_IPC'])
   
      # program_benchmarks = sort_benchmarks_by_dl1_cache_size(program_benchmarks)
      # for benchmark in program_benchmarks:
      #    sim_cycle_results['dl1'][benchmark['cache_dl1']].append(benchmark['sim_IPC'])

      # program_benchmarks = sort_benchmarks_by_ul1_cache_size(program_benchmarks)
      # for benchmark in program_benchmarks:
      #    sim_cycle_results['ul1'][benchmark['cache_ul2']].append(benchmark['sim_IPC'])

   return sim_cycle_results

def plot_sim_cycles_vs_cache_size(benchmarks, output_dir):
   fig, axs = plt.subplots(3,1)

   programs = get_distinct_benchmark_programs(benchmarks)

   sim_cycles = get_sim_cycles(benchmarks, programs)

   X_axis = np.arange(len(programs))

   axs[0].set_title('Cache IL1 Size vs SimCycles')
   # cnt = len(sim_cycles['il1'].keys())
   # width = 2/cnt
   offset = -.2
   for result_key in sim_cycles['il1'].keys():
      plt.bar(X_axis - offset, sim_cycles['il1'][result_key], .2, label=result_key)
      offset += .2

   plt.xticks(X_axis, programs)
   plt.legend()

   axs[1].set_title('Cache DL1 Size vs SimCycles')
   axs[2].set_title('Cache UL2 Size vs SimCycles')

   plt.show()

   # plt.savefig(Path(output_dir) / Path("Simcycles.img"))

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
   
   plot_sim_cycles_vs_cache_size(benchmarks, args.output_dir)
   print("hello")

if __name__ == "__main__":
   main()
