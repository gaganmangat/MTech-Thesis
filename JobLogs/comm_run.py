#!/usr/bin/env python
import numpy as np
import pandas as pd
import os
import sys
import subprocess

logfile = sys.argv[1]
logname = sys.argv[2]
jobfile = sys.argv[3]

## Check if hops and debug files are present
## If present, warn and exit
## Else create files and write the column headers
def create_files():
    """
    if os.path.exists('hops.txt'):
        sys.exit("Hops file exists. Please move content.")
    if os.path.exists('debug.txt'):
        sys.exit("Debug file exists. Please move content.")
    """
    hops = open('/home/gagandeep/slurmcost/hops.txt','w')
    #print(os.environ['SLURM_COST_DIR'] + 'hops.txt')
    #hops = open(os.environ['SLURM_COST_DIR'] + 'hops.txt','w')
    hops.write('Job_name JobID Communication_Pattern Hops\n')
    hops.close()
    
    debug = open('/home/gagandeep/slurmcost/debug.txt','w')
    #debug = open(os.environ['SLURM_COST_DIR'] + 'debug.txt','w')
    debug.write('(row-wise) JobInfo, SwitchIndex, AllocNodes, CommNodes, TotalNodes\n')
    debug.close()
    print("Files created!")

## Scale down time and nodes
def scale(df):
    yes = {'yes','y', 'ye', ''}
    no = {'no','n'}
    sys.stdout.write("Log is %s?"%logname)
    choice = input().lower()
    if choice in yes:
        print("Logname is correct.")
    elif choice in no:
        sys.exit("Logname information was incorrect. Exit!")
    else:
        sys.stdout.write("Please respond with 'yes' or 'no'")
        sys.exit(0)

    #df['Submit'] = df['Submit'] // 10
    #df['Runtime'] = df['Runtime'] // 10
    print("Logs are scaled!")
    return df

def submit_jobs(x,df):

    replace = 'sed -i "s/duration/'+df.loc[x,'Runtime']+'/" '+jobfile
    subprocess.call([replace],shell=True)
    
    cat = 'cat '+jobfile
    subprocess.call([cat],shell=True)
    
    cmd = 'sbatch --job-name='+ df.loc[x,'Job_name'] + ' --comment='+df.loc[x,'Comment']+' --begin=now+'+df.loc[x,'Submit'] + ' --nodes=' + df.loc[x,'Nodes'] + ' '+jobfile
    print(cmd + " duration=" +df.loc[x,'Runtime'])
    subprocess.call([cmd],shell=True)
    #print(cmd)
    replace = 'sed -i "s/'+df.loc[x,'Runtime']+'/duration/" '+jobfile
    subprocess.call([replace],shell=True)
    cat = 'cat '+jobfile
    subprocess.call([cat],shell=True)

def update_comm(df):
    #iterate over all comm patterns
    for i in range(df.shape[0]):
        #read the 2D communication pattern from file
        path_comm = df.iloc[i, 4]
        with open(path_comm[2:]) as textFile:
            data = [row.split() for row in textFile]
        n = int(df.iloc[i, 3]) #number of processes    
        i_list = []
        j_list = []
        val_list = []
        
        for i_ in range(n):
            for j in range(i_+1, n):
                i_list.append(i_)
                j_list.append(j)
                val_list.append(int(data[i_][j]))
        #create dataframe
        top_pairs = pd.DataFrame(zip(i_list, j_list, val_list), columns=["i", "j", "val"])    
        #top_pairs.describe()
        
        #keep rows with values >= mean
        top_pairs = top_pairs[top_pairs["val"] >= top_pairs["val"].mean()]
        newpath = path_comm[:-4] + "_top.txt"
        top_pairs.to_csv(newpath[2:], sep=' ', header=None, index=False)
        #print(df)
        df.iloc[i, 4] = newpath
    return df    

def main():
    
    ## Check if everything is in order
    yes = {'yes','y', 'ye', ''}
    no = {'no','n'}

    subprocess.call(['sinfo'],shell=True)
    subprocess.call(['squeue'],shell=True)
    subprocess.call(['scontrol ping'],shell=True)
    subprocess.call(['scontrol show frontend'],shell=True)
   
    sys.stdout.write("Continue?")
    choice = input().lower()
    if choice in yes:
        print("Next: Read logfiles")
    elif choice in no:
        sys.exit("Exit!")
    else:
        sys.stdout.write("Please respond with 'yes' or 'no'")
        sys.exit(0)

    create_files()
    df = pd.read_csv(logfile, sep=' ')
    #df = pd.read_csv('test4.swf', sep=' ')
    #df = update_comm(df)
    df['Submit'] = df['Submit'] - df.loc[0,'Submit']
    #print(df['Submit'])
    #print(df.loc[0, 'Submit'])
    #print(df['Submit'])
    df = scale(df)
    print("Submitting jobs")
    df.reset_index()['index'].apply(submit_jobs,args=(df.astype('str'),)) 
    #subprocess.call(['sinfo'],shell=True)
    #subprocess.call(['squeue'],shell=True)
    subprocess.call(['scontrol ping'],shell=True)
    subprocess.call(['scontrol show frontend'],shell=True)

if __name__ == '__main__':
    main()

