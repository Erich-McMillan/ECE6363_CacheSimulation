import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import re
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

def get_DL1_sizes(benchmarks) -> list:
   sizes = []

   for b in benchmarks:
      if b['cache_dl1'] not in sizes:
         sizes.append(b['cache_dl1'])

   return sizes

def get_UL2_sizes(benchmarks) -> list:
   sizes = []

   for b in benchmarks:
      if b['cache_dl2'] not in sizes:
         sizes.append(b['cache_dl2'])

   return sizes

def calc_il1_cache_size(fmtstr: str) -> int:
   matchstr = r":(\d+):(\d+):(\d+):"
   matches = re.findall(matchstr, fmtstr)

   size = 0

   size = int(matches[0][0])
   size = size * int(matches[0][1])
   size = size * int(matches[0][2])

   return size

def calc_dl1_cache_size(fmtstr: str) -> int:
   matchstr = r":(\d+):(\d+):(\d+):"
   matches = re.findall(matchstr, fmtstr)

   size = 0

   size = int(matches[0][0])
   size = size * int(matches[0][1])
   size = size * int(matches[0][2])

   return size

def sort_by_cache_size(dl1fmts: list) -> list:
   sorted = []

   for dl1fmt in dl1fmts:
      idx = 0
      for s in sorted:
         if calc_dl1_cache_size(s) > calc_dl1_cache_size(dl1fmt):
            break
         idx += 1
      sorted.insert(idx, dl1fmt)

   return sorted

def sort_benchmarks_by_il1_cache_size(benchmarks) -> list:
   sorted = []

   for benchmark in benchmarks:
      idx = 0
      for s in sorted:
         if calc_il1_cache_size(s['cache_il1']) > calc_il1_cache_size(benchmark['cache_il1']):
            break
         idx += 1
      sorted.insert(idx, benchmark)

   return sorted

def sort_benchmarks_by_dl1_cache_size(benchmarks) -> list:
   return benchmarks # not yet implemented

def sort_benchmarks_by_ul2_cache_size(benchmarks) -> list:
   return benchmarks # not yet implemented

def get_sim_IPC(benchmarks, programs):
   sim_cycle_results = {}
   sim_cycle_results['il1'] = {}
   sim_cycle_results['dl1'] = {}
   sim_cycle_results['ul2'] = {}

   program_benchmarks = [b for b in benchmarks.values() if b['benchmark_program_name'] == list(benchmarks.values())[0]['benchmark_program_name']]
   IL1_sizes = get_IL1_sizes(program_benchmarks)
   DL1_sizes = get_DL1_sizes(program_benchmarks)
   UL2_sizes = get_UL2_sizes(program_benchmarks)

   for il1 in IL1_sizes:
      sim_cycle_results['il1'][il1] = []

   for dl1 in DL1_sizes:
      sim_cycle_results['dl1'][dl1] = []

   for ul2 in UL2_sizes:
      sim_cycle_results['ul2'][ul2] = []

   for program in programs:
      program_benchmarks = [b for b in benchmarks.values() if b['benchmark_program_name'] == program]
      for benchmark in program_benchmarks:
         sim_cycle_results['il1'][benchmark['cache_il1']].append(benchmark['sim_IPC'])
   
      program_benchmarks = sort_benchmarks_by_dl1_cache_size(program_benchmarks)
      for benchmark in program_benchmarks:
         sim_cycle_results['dl1'][benchmark['cache_dl1']].append(benchmark['sim_IPC'])

      program_benchmarks = sort_benchmarks_by_ul2_cache_size(program_benchmarks)
      for benchmark in program_benchmarks:
         sim_cycle_results['ul2'][benchmark['cache_dl2']].append(benchmark['sim_IPC'])

   return sim_cycle_results

def get_sim_miss_rate(benchmarks, programs, cache_type: str):
   miss_results = {}

   program_benchmarks = [b for b in benchmarks.values() if b['benchmark_program_name'] == list(benchmarks.values())[0]['benchmark_program_name']]
   cache_sizes = []
   search_key = ''
   cache_key = ''

   if cache_type == 'il1':
      cache_sizes = get_IL1_sizes(program_benchmarks)
      search_key = 'il1_miss_rate'
      cache_key = 'cache_il1'
   if cache_type == 'dl1':
      cache_sizes = get_DL1_sizes(program_benchmarks)
      search_key = 'dl1_miss_rate'
      cache_key = 'cache_dl1'
   if cache_type == 'ul2':
      search_key = 'ul2_miss_rate'
      cache_key = 'cache_dl2'
      cache_sizes = get_UL2_sizes(program_benchmarks)

   for size in cache_sizes:
      miss_results[size] = []

   for program in programs:
      program_benchmarks = [b for b in benchmarks.values() if b['benchmark_program_name'] == program]
      for benchmark in program_benchmarks:
         miss_results[benchmark[cache_key]].append(benchmark[search_key])
   
   return miss_results

def get_access_rate(benchmarks, programs, cache_type: str):
   miss_results = {}

   program_benchmarks = [b for b in benchmarks.values() if b['benchmark_program_name'] == list(benchmarks.values())[0]['benchmark_program_name']]
   cache_sizes = []
   search_key = ''
   cache_key = ''

   if cache_type == 'il1':
      cache_sizes = get_IL1_sizes(program_benchmarks)
      search_key = 'il1_accesses'
      cache_key = 'cache_il1'
   if cache_type == 'dl1':
      cache_sizes = get_DL1_sizes(program_benchmarks)
      search_key = 'dl1_accesses'
      cache_key = 'cache_dl1'
   if cache_type == 'ul2':
      search_key = 'ul2_accesses'
      cache_key = 'cache_dl2'
      cache_sizes = get_UL2_sizes(program_benchmarks)

   for size in cache_sizes:
      miss_results[size] = []

   for program in programs:
      program_benchmarks = [b for b in benchmarks.values() if b['benchmark_program_name'] == program]
      for benchmark in program_benchmarks:
         miss_results[benchmark[cache_key]].append(benchmark[search_key])
   
   return miss_results

def plot_sim_IPC_vs_cache_size(benchmarks, file_pattern, output_dir):

   programs = get_distinct_benchmark_programs(benchmarks)

   sim_cycles = get_sim_IPC(benchmarks, programs)

   X_axis = np.arange(len(programs))

   count = 0

   if len(list(sim_cycles['il1'].items())[0][1]) == len(programs):
      count += 1

   if len(list(sim_cycles['dl1'].items())[0][1]) == len(programs):
      count += 1

   if len(list(sim_cycles['ul2'].items())[0][1]) == len(programs):
      count += 1

   fig, axs = plt.subplots(count, 1)

   if not isinstance(axs, np.ndarray):
      axs = [axs]

   axs_num = 0

   if len(list(sim_cycles['il1'].items())[0][1]) == len(programs):
      axs[axs_num].set_title('Cache IL1 Size vs IPC')
      offset = -.2

      keys_sorted = sort_by_cache_size(sim_cycles['il1'].keys())

      for result_key in keys_sorted:
         plt.bar(X_axis - offset, sim_cycles['il1'][result_key], .2, label=result_key)
         offset += .2

      plt.xticks(X_axis, programs)
      plt.legend()
      plt.ylabel("IPC")
      plt.xlabel("Program name")
      axs_num += 1

   if len(list(sim_cycles['dl1'].items())[0][1]) == len(programs):
      axs[axs_num].set_title('Cache DL1 Size vs IPC')
      offset = -.2

      keys_sorted = sort_by_cache_size(sim_cycles['dl1'].keys())

      for result_key in keys_sorted:
         plt.bar(X_axis - offset, sim_cycles['dl1'][result_key], .2, label=result_key)
         offset += .2

      plt.xticks(X_axis, programs)
      plt.legend()
      plt.ylabel("IPC")
      plt.xlabel("Program name")
      axs_num += 1
   
   if len(list(sim_cycles['ul2'].items())[0][1]) == len(programs):
      axs[axs_num].set_title('Cache UL2 Size vs IPC')
      offset = -.2
      for result_key in sim_cycles['ul2'].keys():
         plt.bar(X_axis - offset, sim_cycles['ul2'][result_key], .2, label=result_key)
         offset += .2

      plt.xticks(X_axis, programs)
      plt.legend()
      plt.ylabel("IPC")
      plt.xlabel("Program name")
      axs_num += 1

   # plt.show()

   plt.savefig(Path(output_dir) / Path(f"sim_ipc_{file_pattern}.png"))

def plot_miss_rate_vs_cache_size(benchmarks, file_pattern, output_dir):
   programs = get_distinct_benchmark_programs(benchmarks)

   sim_miss_rate_il1 = get_sim_miss_rate(benchmarks, programs, 'il1')
   sim_miss_rate_dl1 = get_sim_miss_rate(benchmarks, programs, 'dl1')
   sim_miss_rate_ul1 = get_sim_miss_rate(benchmarks, programs, 'ul2')

   X_axis = np.arange(len(programs))

   count = 0

   if len(list(sim_miss_rate_il1.items())[0][1]) == len(programs):
      count += 1

   if len(list(sim_miss_rate_dl1.items())[0][1]) == len(programs):
      count += 1

   if len(list(sim_miss_rate_ul1.items())[0][1]) == len(programs):
      count += 1

   fig, axs = plt.subplots(count, 1)
   if not isinstance(axs, np.ndarray):
      axs = [axs]

   axs_num = 0

   if len(list(sim_miss_rate_il1.items())[0][1]) == len(programs):
      axs[axs_num].set_title('Cache IL1 Size vs IL1 Miss Rate')
      offset = -.2

      keys_sorted = sort_by_cache_size(sim_miss_rate_il1.keys())

      for result_key in keys_sorted:
         plt.bar(X_axis - offset, sim_miss_rate_il1[result_key], .2, label=result_key)
         offset += .2

      plt.xticks(X_axis, programs)
      plt.legend()
      plt.ylabel("IL1 Miss Rate")
      plt.xlabel("Program name")
      axs_num += 1

   if len(list(sim_miss_rate_dl1.items())[0][1]) == len(programs):
      axs[axs_num].set_title('Cache DL1 Size vs DL1 Miss Rate')
      offset = -.2

      keys_sorted = sort_by_cache_size(sim_miss_rate_dl1.keys())

      for result_key in keys_sorted:
         plt.bar(X_axis - offset,sim_miss_rate_dl1[result_key], .2, label=result_key)
         offset += .2

      plt.xticks(X_axis, programs)
      plt.legend()
      plt.ylabel("DL1 Miss Rate")
      plt.xlabel("Program name")
      axs_num += 1
   
   if len(list(sim_miss_rate_ul1.items())[0][1]) == len(programs):
      axs[axs_num].set_title('Cache UL2 Size vs UL2 Miss Rate')
      offset = -.2

      keys_sorted = sort_by_cache_size(sim_miss_rate_ul1.keys())
   
      for result_key in keys_sorted:
         plt.bar(X_axis - offset, sim_miss_rate_ul1[result_key], .2, label=result_key)
         offset += .2

      plt.xticks(X_axis, programs)
      plt.legend()
      plt.ylabel("UL2 Miss Rate")
      plt.xlabel("Program name")
      axs_num += 1

   # plt.show()

   plt.savefig(Path(output_dir) / Path(f"sim_miss_rate_{file_pattern}.png"))

def plot_accesses_vs_cache_size(benchmarks, file_pattern, output_dir):
   programs = get_distinct_benchmark_programs(benchmarks)

   sim_miss_rate_il1 = get_access_rate(benchmarks, programs, 'il1')
   sim_miss_rate_dl1 = get_access_rate(benchmarks, programs, 'dl1')
   sim_miss_rate_ul1 = get_access_rate(benchmarks, programs, 'ul2')

   X_axis = np.arange(len(programs))

   count = 0

   if len(list(sim_miss_rate_il1.items())[0][1]) == len(programs):
      count += 1

   if len(list(sim_miss_rate_dl1.items())[0][1]) == len(programs):
      count += 1

   if len(list(sim_miss_rate_ul1.items())[0][1]) == len(programs):
      count += 1

   fig, axs = plt.subplots(count, 1)
   if not isinstance(axs, np.ndarray):
      axs = [axs]

   axs_num = 0

   if len(list(sim_miss_rate_il1.items())[0][1]) == len(programs):
      axs[axs_num].set_title('Cache IL1 Size vs IL1 Accesses')
      offset = -.2

      keys_sorted = sort_by_cache_size(sim_miss_rate_il1.keys())

      for result_key in keys_sorted:
         plt.bar(X_axis - offset, sim_miss_rate_il1[result_key], .2, label=result_key)
         offset += .2

      plt.xticks(X_axis, programs)
      plt.legend()
      plt.ylabel("IL1 Accesses")
      plt.xlabel("Program name")
      axs_num += 1

   if len(list(sim_miss_rate_dl1.items())[0][1]) == len(programs):
      axs[axs_num].set_title('Cache DL1 Size vs DL1 Accesses')
      offset = -.2

      keys_sorted = sort_by_cache_size(sim_miss_rate_dl1.keys())

      for result_key in keys_sorted:
         plt.bar(X_axis - offset,sim_miss_rate_dl1[result_key], .2, label=result_key)
         offset += .2

      plt.xticks(X_axis, programs)
      plt.legend()
      plt.ylabel("DL1 Accesses")
      plt.xlabel("Program name")
      axs_num += 1
   
   if len(list(sim_miss_rate_ul1.items())[0][1]) == len(programs):
      axs[axs_num].set_title('Cache UL2 Size vs UL2 Accesses')
      offset = -.2

      keys_sorted = sort_by_cache_size(sim_miss_rate_ul1.keys())
   
      for result_key in keys_sorted:
         plt.bar(X_axis - offset, sim_miss_rate_ul1[result_key], .2, label=result_key)
         offset += .2

      plt.xticks(X_axis, programs)
      plt.legend()
      plt.ylabel("UL2 Accesses")
      plt.xlabel("Program name")
      axs_num += 1

   # plt.show()

   plt.savefig(Path(output_dir) / Path(f"sim_mem_accesses_{file_pattern}.png"))

def main():
   parser = argparse.ArgumentParser()

   parser.add_argument('--results-dir', type=Path, help="path to simulator results")
   parser.add_argument('--file-pattern', type=str, help="pattern to find in files and filter by")
   parser.add_argument('--output-dir', type=Path, help="path to output results to")

   args = parser.parse_args()

   benchmarks = benchmark.parse_all_result_files_with_file_pattern(args.results_dir, args.file_pattern)
   
   if (not Path(args.output_dir).exists()):
      Path(args.output_dir).mkdir(parents=True)
   plot_sim_IPC_vs_cache_size(benchmarks,  args.file_pattern, args.output_dir)
   plot_miss_rate_vs_cache_size(benchmarks, args.file_pattern, args.output_dir)
   plot_accesses_vs_cache_size(benchmarks, args.file_pattern, args.output_dir)
   print("hello")

if __name__ == "__main__":
   main()
