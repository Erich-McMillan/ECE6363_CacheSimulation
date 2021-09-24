#!/bin/bash
# This script runs sim-outorder for some set of benchmarks for the Alpha architecture,
# running each with some set of arguments. This script assumes it is run from the base
# directory of simple-scalar, and that the benchmark files live in a sub-directory
# named 'benchmarks'. The benchmarks are invoked with the following syntax:
#  - anagram    : sim-outorder ${arguments} anagram.alpha words < anagram.in
#  - compress95 : sim-outorder ${arguments} compress95.alpha < compress95.in
#  - gcc        : sim-outorder ${arguments} cc1.alpha -O 1stmt.i
#  - go         : sim-outorder ${arguments} go.alpha 50 9 2stone9.in
# If the SPEC2000 flag is set, the script will run all of the SPEC benchmarks with an
# initial window of 20M ignored instructions and a benchmark window of 50M instructions.

suite_name=results

pushd benchmarks > /dev/null

output_dir="output/spec2000/${suite_name}"
mkdir -p "${output_dir}"
rm -rf "${output_dir}/*"

benchmarks=( $(ls -d SPEC2000/spec2000args/* | grep -Po "(?<=spec2000args/).*") )
echo $benchmarks
for benchmark in "${benchmarks[@]}"; do
  pushd SPEC2000/spec2000args/${benchmark} > /dev/null
  binary="./../../spec2000binaries/${benchmark}00.peak.ev6"
  run="./RUN${benchmark}"

  echo "Running QA"
  echo "Running ${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 > ./../../../${output_dir}/${benchmark}.txt 2>&1"
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:il1 il1:256:32:1:l" > ./../../../${output_dir}/${benchmark}_QA_8K.txt 2>&1
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:il1 il1:1024:32:1:l" > ./../../../${output_dir}/${benchmark}_QA_32K.txt 2>&1
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:il1 il1:2048:32:1:l" > ./../../../${output_dir}/${benchmark}_QA_64K.txt 2>&1

  echo "Running QB"
  echo "Running ${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 > ./../../../${output_dir}/${benchmark}.txt 2>&1"
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:dl1 dl1:16:32:4:l" > ./../../../${output_dir}/${benchmark}_QB_2K.txt 2>&1
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:dl1 dl1:256:32:4:l" > ./../../../${output_dir}/${benchmark}_QB_32K.txt 2>&1
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:dl1 dl1:1024:32:4:l" > ./../../../${output_dir}/${benchmark}_QB_128K.txt 2>&1

  echo "Running QC"
  echo "Running ${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 > ./../../../${output_dir}/${benchmark}.txt 2>&1"
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:dl1 dl1:1024:32:1:l" > ./../../../${output_dir}/${benchmark}_QC_1way.txt 2>&1
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:dl1 dl1:512:32:2:l" > ./../../../${output_dir}/${benchmark}_QC_2way.txt 2>&1
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:dl1 dl1:128:32:8:l" > ./../../../${output_dir}/${benchmark}_QC_8way.txt 2>&1

  echo "Running QD"
  echo "Running ${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 > ./../../../${output_dir}/${benchmark}.txt 2>&1"
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:dl2 ul2:512:64:4:l" > ./../../../${output_dir}/${benchmark}_QD_128K.txt 2>&1
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:dl2 ul2:2048:64:4:l" > ./../../../${output_dir}/${benchmark}_QD_512K.txt 2>&1
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:dl2 ul2:4096:64:4:l" > ./../../../${output_dir}/${benchmark}_QD_1M.txt 2>&1

  echo "Running QE"
  echo "Running ${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 > ./../../../${output_dir}/${benchmark}.txt 2>&1"
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:dl1 dl1:256:32:1:l -cache:dl2 ul2:2048:32:4:l" > ./../../../${output_dir}/${benchmark}_QE_32B_Block.txt 2>&1
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:dl1 dl1:128:64:1:l -cache:dl2 ul2:1024:64:4:l" > ./../../../${output_dir}/${benchmark}_QE_64B_Block.txt 2>&1
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:dl1 dl1:64:128:1:l -cache:dl2 ul2:512:128:4:l" > ./../../../${output_dir}/${benchmark}_QE_128B_Block.txt 2>&1
  eval time "${run} './../../../../sim-outorder' ${binary} -fastfwd 20000000 -max:inst 200000000 -cache:dl1 dl1:32:256:1:l -cache:dl2 ul2:256:256:4:l" > ./../../../${output_dir}/${benchmark}_QE_256B_Block.txt 2>&1

  popd > /dev/null
done

popd > /dev/null

