import os,sys,getopt,subprocess
from tqdm import tqdm
from .generate import generate

def help_command():
    msg = f'''Program:  pbstool
A simple-to-use program for quickly batch creating job tasks based on the PBS job 
scheduling system (including OpenPBS, PBS Pro, and TORQUE) based on a command list.

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
    '''
    print(msg)

def version_command():
    msg = '''
    ____  __        ______            __
   / __ \/ /_  ____/_  __/___  ____  / / 
  / /_/ / __ \/ ___// / / __ \/ __ \/ /     
 / ____/ /_/ (__  )/ / / /_/ / /_/ / /  
/_/   /_.___/____//_/  \____/\____/_/   

Version:2.2

Author: Wangzt (interestingcn01@gmail.com)
Bioinformatics Laboratory of South China Agricultural University
    '''
    print(msg)


def error(msg,stop=True):
    print('[ERROR] - ' + str(msg))
    if stop:
        exit(1)

def info(msg):
    print('[INFO] - ' + str(msg))


def fastpbs():
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   'hvVsc:n:e:q:o:',
                                   ['help', 'version', 'sample','cmd=', 'name=', 'env=', 'queue=','node=', 'ppn=','walltime=','output=','log_info_output=','log_error_output=',
                                    'output='])
    except getopt.GetoptError as e:
        error(e)

    # init
    cmd_file_path = ''
    job_name = 'Job'
    job_env = None
    job_queue = None
    job_node = '1'
    job_ppn = '1'
    job_walltime = '1000:00:00'
    PROJECT_PATH = os.getcwd()


    log_info_output_path = PROJECT_PATH
    log_error_output_path = PROJECT_PATH
    job_output_path = PROJECT_PATH

    if opts == []:
        help_command()
        exit()


    for opt_name,opt_value in opts:
        if opt_name in ('-h', '--help'):
            help_command()
            exit()
        if opt_name in ('-v','-V', '--version'):
            version_command()
            exit()
        if opt_name in ('-s', '--sample'):
            g = generate()
            g.generate_sample_pbs('sample.pbs')
            info('Create sample pbs successfully')
            exit()

        if opt_name in ('-c', '--cmd'):
            cmd_file_path = opt_value
        if opt_name in ('-n','--name'):
            job_name = opt_value
        if opt_name in ('-e','--env'):
            job_env = opt_value
        if opt_name in ('-q','--queue'):
            job_queue = opt_value

        if opt_name == '--node':
            job_node = opt_value
        if opt_name == '--ppn':
            job_ppn = opt_value
        if opt_name == '--log_info_output':
            log_info_output_path = opt_value
        if opt_name == '--log_error_output':
            log_error_output_path = opt_value
        if opt_name == '--walltime':
            job_walltime = opt_value

        if opt_name in ('-o', '--output'):
            job_output_path = opt_value
            if not os.path.isdir(job_output_path):
                try:
                    os.makedirs(job_output_path)
                except Exception as e:
                    error('Failed to create job output path:',stop=False)
                    error(e)


    if cmd_file_path == '' or not os.path.exists(cmd_file_path):
        error('The job command file does not exist!')

    if not os.path.exists(log_info_output_path):
        try:
            os.makedirs(log_info_output_path)
        except Exception as e:
            error('Failed to create standard log output path',stop=False)
            error(e)

    if not os.path.exists(log_error_output_path):
        try:
            os.makedirs(log_error_output_path)
        except Exception as e:
            error('Failed to create error log output path',stop=False)
            error(e)

    if job_queue == '' or job_queue == None:
        print(job_queue)
        error('Calculation queue not set!')

    g = generate()

    with open(cmd_file_path,'r',encoding='utf8') as cmd_file:
        cmd_file = cmd_file.read().splitlines()

        job_num = 1

        for cmd in tqdm(cmd_file,desc='Processing: ',leave=False):
            if cmd.startswith('#') or cmd.startswith(';'):continue
            this_job_name = f'{job_name}_{job_num}'
            this_job_filename = this_job_name+'.pbs'
            this_job_log_info = os.path.join(log_info_output_path,this_job_name+'_info.log')
            this_job_log_error = os.path.join(log_error_output_path, this_job_name + '_error.log')

            job_num += 1

            g.generate_pbs(
                pbs_output=os.path.join(job_output_path,this_job_filename),
                job_name=this_job_name,
                job_cmd=cmd,
                job_env=job_env,
                job_queue=job_queue,
                job_node=job_node,
                job_ppn=job_ppn,
                job_info_output_path=this_job_log_info,
                job_error_output_path=this_job_log_error,
                job_walltime=job_walltime
            )

def qsubs():
    filelist = [i for i in os.listdir(os.getcwd()) if i.endswith('.pbs')]
    if filelist == []:
        msg = ''' 
MM'"""""`MMM                   dP                
M  .mmm,  MM                   88                
M  MMMMM  MM .d8888b. dP    dP 88d888b. .d8888b. 
M  MM  M  MM Y8ooooo. 88    88 88'  `88 Y8ooooo. 
M  `MM    MM       88 88.  .88 88.  .88       88 
MM.    .. `M `88888P' `88888P' 88Y8888' `88888P' 
MMMMMMMMMM Qsubs is released as part of [pbstool]'''
        print(msg)
        exit()
        
    for filename in tqdm(filelist,desc='Submitting: ',leave=False):
        res = subprocess.run(f'qsub {filename}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
        if res.returncode != 0:
            tqdm.write(f'[!] Failed: {res.stdout}')
            exit()
        # tqdm.write(f'Job ID: {res.stdout}')

# if __name__ == '__main__':
#     fastpbs()