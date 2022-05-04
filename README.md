# Proposed Algorithms
The implementation consists of 4 node-allocation algorithms for the SLURM job scheduler. 
* The first three algorithms consider the job's communication behavior based on the communication patterns/underlying algorithms of different MPI collectives.
* The default and greedy algorithms are implemented in the Master branch. 
* The balanced and adaptive algorithms are implemented in the algo2 branch.
* The comm balanced considers the job's actual communication pattern by taking as input a (node x node) communication matrix denoting the total amount of communication between the nodes. It is implemented in the algo3 branch.

## Setup

### Installing and setting up SLURM
We use SLURM version 19.05.0 in our work.
The following steps describe how to setup SLURM and use any of the proposed algorithms:
* Clone the source code present [here](https://github.com/gaganmangat/slurm_changes) in the home directory. To install SLURM and its associated components follow the instructions provided at the [official site](https://slurm.schedmd.com/quickstart_admin.html). Instructions for installing SLURM have also been provided in the [Appendix](#appendix).
* In order to execute the proposed algorithms, we use the environment variable JOBAWARE. **Before running `make` while building SLURM**, add `-DJOBAWARE` to `CFLAGS` in the following Makefiles:
```
/src/plugins/sched/backfill/Makefile
/src/slurmctld/Makefile
/src/plugins/topology/tree/Makefile
```
Add the library `-lm` to `LIBS` in `/src/slurmctld/Makefile`.
* Run `make` and `make install` after making the above changes to the Makefiles.
* Run the script `makefiles.py` outside the SLURM directory (The script assumes that the name of code-repo is slurm_changes and is present in the home directory. Make appropriate changes to the path in the script if needed). This creates a copy of Makefile for each algorithms with appropraite environment varible.
```bash
python3 makefiles.py
```
### Running jobs
After setting up SLURM as described above, we can run the default SLURM algorithm or one of the proposed algorithm (greedy, balanced, adaptive). Run the script `prepare_run.sh` outside SLURM directory (The script assumes that the name of code-repo is slurm_changes and is present in the home directory. Make appropriate changes to the path in the script if needed) with appropriate input as shown to use the different algorithms.
* Default SLURM algorithm
```bash
bash prepare_run.sh default
```
* Greedy algorithm
```bash
bash prepare_run.sh greedy
```
* Balanced algorithm
```bash
bash prepare_run.sh bal
```
* Adaptive algorithm
```bash
bash prepare_run.sh ada
```
* Comm Balanced algorithm
```bash
bash prepare_run.sh combal
```

### Recording the Cost of Communication
The code calculates the cost of communication and writes it to a file. It also records the nodes allocated to a job on different switches. To record the cost of communication and the switch-wise node allocation information of all jobs in a file, the environment variable SLURM_COST_DIR is used. Add the following line with the path of the folder where the files should be saved in the .bashrc file present in your home directory.
```
export SLURM_COST_DIR=/home/gagandeep/slurmcost
```
After adding the line, re-open the terminal to enforce the changes.

### Submitting Jobs
When using the greedy or balanced algorithm, use the comment parameter of `sbatch` command to specify whether a job is communication-intensive or compute-intensive. 
For a communication-intensive job use `--comment=1` and for compute-intensive use `--comment=0`. The sbatch command will be similar to this:
```
sbatch --job-name=test_job --comment=1 --nodes=4 jobfile
```
When submitting jobs using the adaptive algorithm, in addition to specifying if a job is communication-intensive, also provide the commmunication pattern of the job. Currently, the code supports five communication-patterns: RHVD (Recursive-halving vector doubling), RD (Recursive doubling/halving), Binomial, Ring, and a pattern similar to CMC-2D (70% Binomial and 30% RD). The comment parameter for these patterns will be `--comment=1:1` for RHVD, `--comment=1:2` for RD, `--comment=1:3` for Binomial, `--comment=1:4` for Ring, and `--comment=1:5` for CMC-2D.

When using the comm balanced algorithm, the communication matrix path for a job should be given in the comment as `--comment=1:/path/to/comm_matrix/mat.txt` for a communication-intensive job and `--comment=0:/path/to/comm_matrix/mat.txt` for a compute-intensive job. The first character of the comment denotes whether a job is communication-intensive (1) or compute-intensive (0).
 
### Appendix
Follow these steps to install and build SLURM and other required components:
#### Install Pre-requisites
```bash
sudo apt update
sudo apt install -y git gcc make libssl-dev libpam0g-dev libmariadb-client-lgpl-dev libmysqlclient-dev
```
#### Install and enable MUNGE
```bash
sudo apt install -y libmunge-dev libmunge2 munge
sudo systemctl enable munge
sudo systemctl start munge
```
Check that MUNGE has installed correctly
```bash
munge -n | unmunge
```
The output should contain this line:
```
STATUS:     Success(0)
```
#### Install Mariadb and setup the database
```
sudo apt install -y mariadb-server
sudo systemctl enable mysql
sudo systemctl start mysql
```
Setup the database after installing Mariadb. Provide an appropriate username, database name and password in these commands.
```
sudo mysql -u root
create database slurm_acct_db;
create user 'gagandeep'@'localhost';
set password for 'gagandeep'@'localhost' = password('slurmdbpass');
grant usage on *.* to 'gagandeep'@'localhost';
grant all privileges on slurm_acct_db.* to 'gagandeep'@'localhost';
flush privileges;
select user from mysql.user;
```
The ouput from the last line should show the user added to the database.
#### Clone the repository and build SLURM
Clone the repository present [here](https://github.com/gaganmangat/slurm_changes).
Switch to the code-repository (We are assuming it is named slurm_changes) and run configure.
```
cd slurm_changes
./configure --enable-debug --enable-front-end
```
Ensure that configure was successful and there was no error. If the configure failed then it maybe due to some missing pre-requisites. Please resolve those issues before moving ahead. You may refer to the [official site](https://slurm.schedmd.com/quickstart_admin.html) for troubleshooting errors.

**Make changes to the Makefile as [described above](#installing-and-setting-up-slurm).**
Run make and make install
```
make
sudo make install
```
Ensure that the build is successful.

#### Create the required directories
Create the required directories and change the owner to the SLURM user (here gagandeep).
```
sudo mkdir -p /var/spool/slurmctld /var/spool/slurmd /var/log/slurm
sudo chown gagandeep /var/spool/slurmctld /var/spool/slurmd /var/log/slurm
```
#### SLURM configuration files
SLURM requires `slurm.conf` and `topology.conf` files to be present in `/usr/local/etc`. The service files should be present at `/etc/systemd/system`. These files have also been provided in this repository [here](./slurm_config_files). Before, using these files make necessary changes to the node names, node address and other fields as required.
Copy them to the appropriate folders.
```
sudo cp slurm.conf topology.conf slurmdbd.conf /usr/local/etc
sudo cp slurmctld.service slurmdbd.service slurmd.service /etc/systemd/system
```
#### Start the SLURM daemons and check status
```
sudo systemctl enable slurmdbd
sudo systemctl enable slurmctld
sudo systemctl enable slurmd

sudo systemctl start slurmdbd
sudo systemctl status slurmdbd
sudo systemctl start slurmctld
sudo systemctl status slurmctld
sudo systemctl start slurmd
sudo systemctl status slurmd
```
If the build was successful, the status will show the daemons to be active and running.

NOTE: slurmdbd should be be succesfully running before starting slurmctld and slurmd. Therefore, enable and start the daemons in the same order as shown (slurmdbd, followed by slurmctld and then slurmd).

#### Add Cluster
Add a cluster to SLURM (here the name is cluster)
```
sacctmgr add cluster cluster
sacctmgr show cluster
```
The output of the last line should show the cluster added.


