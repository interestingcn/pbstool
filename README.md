Pbstool
====
# Introduction
A simple-to-use program for quickly batch creating job tasks based on the PBS job scheduling system (including OpenPBS, PBS Pro, and TORQUE) based on a command list.

This application consists of two parts, pbstool is used to quickly create pbs job scripts, and qsubs is used to submit job scripts in batches.

# Install
----
From source code
```bash
git clone https://github.com/interestingcn/pbstool.git
cd pbstool
pip install .
```
From Pypi
```bash
pip install pbstool
```

# Usages
----
## Quick start
```shell
# Create job script
pbstool -c cmd.txt -n job_name -q cu 
# Submit them all!
qsubs
```
## pbstool: help information
```shell
Useage: pbstool  <command> [options]
Commands:
    -c / --cmd          Set job command list path.
    -n / --name         Job name prefix.
    -e / --env          If the software you are using is in a conda environment,
                        define the conda environment name here.
    -q / --queue        Target queue name.
    -- / --node         Set the number of nodes required for the job.Default 1.
    -- / --ppn          Set the number of CPU cores that can be used by each node.Default 1.
    -o / --output       Output path to generate job script.Default current path
    --walltime          Set the maximum wallclock time required for the job.Default 1000hours.
    --log_info_output   Job standard log output path.Default current path.
    --log_error_output  Job error log output path.Default current path.
    
    -s / --sample       Create a sample pbs script.
    -h / --help         Display this help message.
    -v / --version      Detailed version information.
```

## qsubs 
qsubs has no parameters. It will submit all pbs job scripts in the current path by default. You only need to execute `qsubs` under the path to be submitted.
```shell
qsubs
```

# License
----
Copyright [2023] [wangzt]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

# About
----
Author: Wangzt (interestingcn01@gmail.com)

Bioinformatics Laboratory of South China Agricultural University

