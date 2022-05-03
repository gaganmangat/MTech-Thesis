sudo systemctl reset-failed
sudo systemctl stop slurmctld
sudo systemctl stop slurmd
sudo systemctl start slurmctld
scancel -u gagandeep
sudo systemctl start slurmd
