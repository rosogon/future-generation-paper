= SLA+Reputation validation =

== Requirements ==

* SLA, mysql
* KairosDB

== Running ==

1. Run kairosdb and sla-core
2. `./start.sh` -m [min] -M [max] -t [template]

Parameters are passed to server.sh. Run server.sh -h for more help.

`start.sh` does:
1. Restore database
2. `load-samples.sh`
3. `./server.py` "$@"
3. `./client.sh`

Press ctrl-c when finished and then run `./stop.sh` to stop evaluation.
