class generate:

    def __init__(self):
        pass
    def generate_pbs(self,pbs_output,job_name,job_cmd,job_env,job_queue,job_node,job_ppn,job_info_output_path,job_error_output_path,job_walltime='1000:00:00'):

        if job_env == None or job_env == '':
            conda_env = ''
        else:
            conda_env = 'source activate ' + job_env

        context = f'''#!/bin/sh
#PBS -N {job_name}
#PBS -q {job_queue}
#PBS -l nodes={job_node}:ppn={job_ppn}
#PBS -l walltime={job_walltime}
#PBS -o {job_info_output_path}
#PBS -e {job_error_output_path}
#PBS -V
#PBS -S /bin/bash
cat $PBS_NODEFILE > /tmp/nodefile.$$
cd $PBS_O_WORKDIR
echo "------------------------------------------"
echo 'Job identification: ' $PBS_QUEUE - $PBS_JOBID - $PBS_JOBNAME
echo "------------------------------------------"
echo 'Command: {job_cmd}'
echo "------------------------------------------"
echo Start Time: `date`
echo "------------------------------------------"

{conda_env}
{job_cmd}

echo "------------------------------------------"
echo End Time: `date`
echo "------------------------------------------"
rm -rf /tmp/nodefile.$$
rm -rf /tmp/nodes.$$
'''
        with open(pbs_output,'w',encoding='utf8') as f:
            f.write(context)
        return True


    def generate_sample_pbs(self,pbs_output='Sample.pbs'):
        context = '''#!/bin/sh
#PBS -N sample_pbs
#PBS -q cu
#PBS -l nodes=1:ppn=10
#PBS -l walltime=1000:00:00
#PBS -o pbs_info.txt
#PBS -e pbs_error.txt
#PBS -V 
#PBS -S /bin/bash
cat $PBS_NODEFILE > /tmp/nodefile.$$
cd $PBS_O_WORKDIR
echo "------------------------------------------"
echo 'Job identification: ' $PBS_QUEUE - $PBS_JOBID - $PBS_JOBNAME
echo "------------------------------------------"
echo Start Time: `date`
echo "------------------------------------------"

# Input your command...

echo "------------------------------------------"
echo End Time: `date`
echo "------------------------------------------"
rm -rf /tmp/nodefile.$$
rm -rf /tmp/nodes.$$
        '''
        with open(pbs_output,'w',encoding='utf8') as f:
            f.write(context)
        return True

# g = generate()
# g.generate_pbs(
#     pbs_output='test.pbs',
#     job_name='test_job',
#     job_cmd='sleep 10',
#     job_env='aaa',
#     job_queue='cu',
#     job_node=1,
#     job_ppn=1,
#     job_info_output_path='info.txt',
#     job_error_output_path='error.txt'
# )

