## Running Job Logs
The job logs from Intrepid, Mira, and Theta supercomputers are anl.swf, theta.swf, and mira.swf.
The script continuous_run.py can be used to run the given job logs. It also performs the relevant scaling of the number of nodes and the job runtime according to the input logs.
Usage:
```
python3 continuous_run.py logfile logname pattern jobfile
```
where:
* logfile: Job Log file (For e.g., anl.swf, mira.swf, theta.swf)
* logname: Name of Job Log (anl/theta/mira)
* pattern: Pattern is specified as None for default, greedy, balanced, and comm-balanced algorithm. For adaptive algorithm, pattern should specify the communication pattern (rhvd/rd/bin/cmc/ring).
* jobfile: Name of job script (jobfile.sh)
