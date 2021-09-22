import re
import decimal
from pathlib import Path

m_simulation_parameters_re = r"\n-([\w|:]+)\s+(.+) #"
m_simulation_results_re = r"\n([\w|\.]+)\s+([\w|\.]+) #"

def _match_simulation_parameters(benchmark_str: str) -> list:
   """Returns matches for every enabled simulation parameter
   """
   return re.findall(m_simulation_parameters_re, benchmark_str)

def _match_simulation_results(benchmark_str: str) -> list:
   """Returns matches for every simulation output value
   """
   return re.findall(m_simulation_results_re, benchmark_str)

def parse_benchmark_results(benchmark_str: str) -> dict:
   """ Converts a raw benchmark string produced by simple sim into a data
   object which contains the relevant information
   """
   benchmark_info = {}
   sim_params_raw = _match_simulation_parameters(benchmark_str)
   sim_results_raw = _match_simulation_results(benchmark_str)

   for param in sim_params_raw:
      param_name = param[0].replace(":", "_")
      benchmark_info[param_name] = param[1]

   for result in sim_results_raw:
      result_key = result[0].replace(".", "_")
      try:
         if "0x" in result[1]:
            benchmark_info[result_key] = int(result[1], 16)
         else:
            benchmark_info[result_key] = float(result[1])
      except ValueError as e:
         print(f"Error trying to convert {result_key}:{result[1]}, skipping.")

   return benchmark_info

from os import listdir
from os.path import isfile, join

def parse_all_result_files_with_file_pattern(directory: Path, pattern: str) -> dict:
   filenames = [f for f in listdir(directory) if isfile(join(directory, f)) and pattern in f]

   benchmark_results = {}

   for filename in filenames:
      with open(Path(directory) / Path(filename), "r") as f:
         filecontents = f.read()
         benchmark = parse_benchmark_results(filecontents)
         benchmark_results[filename] = benchmark

   return benchmark_results

# all_results = parse_all_result_files_with_file_pattern("benchmarks/output/spec2000/results/", "QA")
# print('hello')

# with open("benchmarks/output/spec2000/results/bzip2_QA_32K.txt") as f:
#    lines = f.read()
#    parse_benchmark_results(lines)
