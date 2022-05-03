The major changes made to the SLURM source code (for all algorithms) are present in the following files:

#### src/common
* node_conf.h - Add the field leaf_switch to struct node_record. This field maintains the leaf switch to which the node is connected.
* slurm_topology.h - Add the following fields to struct switch_record: 
comm_jobs (no of communication-intensive jobs on the switch) and num_nodes (no of direct descendant nodes).

#### src/slurmctld:
* job_scheduler.c - The function _schedule() calls the hop function to record the cost of communication for jobs when they start.
* calc_hops.c - The file contains most of the additional code. 
It includes functions to calculate cost of communication for different patterns and functions to determine node allocation under 
balanced allocation and adaptive allocation.
* read_config.c, node_mgr.c, job_mgr.c - The field comm_jobs for each switch is updated in these files when a job starts or finishes.
The changes can be located using the environment variable JOBAWARE.

#### src/plugins:
* sched/backfill/backfill.c - The function _start_job() calls the hop function to record the cost of communication for backfilled jobs when they start.
* topology/tree/topology_tree.c - Changes are made to the validate_switches() function to initialize the fields 
leaf_switch, comm_jobs and num_nodes added above.
* select/linear/select_linear.c - Changes are made to the _job_test_topo() function to implement the proposed algorithms.

# Greedy Algorithm
* Implemented using the variable JOBAWARE in the _job_test_topo() function inside the select/linear/select_linear.c file.

# Balanced Algorithm
* Implemented using the variable JOBAWARE1 in the _job_test_topo() function inside the select/linear/select_linear.c file, and the balanced_alloc() function inside the src/slurmctld/calc_hops.c file.

# Adaptive Algorithm
* Implemented using the environment variable JOBAWARE2 in the _job_test_topo() function inside the select/linear/select_linear.c file, and the balanced_alloc() function inside the src/slurmctld/calc_hops.c file. It makes use of the variable JOBAWARE to find allocations based on greedy, and the variable JOBAWARE1 to find allocations based on balanced.

# Comm Balanced Algorithm
* Implemented using the environment variable JOBAWARE3 in the _job_test_topo() function inside the select/linear/select_linear.c file, and the combal_alloc() function inside the src/slurmctld/calc_hops.c file. 
* src/slurmctld/step_mgr.c - Changes are made to the build_batch_step() function to change the order of rank to node allocations according to the algorithm.
