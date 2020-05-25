# azure-log-analytics-json-redis
Collecting metrics from redis and sending to Azure Log Analytics thru oms agent fluentd custom JSON data sources

How to send custom metrics from your redis on-prem to Azure Log Analytics.

NOTE: Considering that you already have Azure Log Analytics workspace setup and OMS agent installed and running on your vm.
- Azure Monitor: https://azure.microsoft.com/en-us/services/monitor/
- OMS Agent for Linux: https://github.com/microsoft/OMS-Agent-for-Linux  


I decided to use JSON data as it is already supported by OMS Agent, all you have to do is to configure FluentD plugin as described here:
- Collecting custom JSON data sources with the Log Analytics agent for Linux in Azure Monitor: https://docs.microsoft.com/en-us/azure/azure-monitor/platform/data-sources-json


The only difference is that your command will be:


```
command '/usr/local/bin/redis_info.py'
```

Please refer to redis_info.py file and make sure linux owner and group is set to omsagent:omiusers

Once you have the script setup, run and you will see get something like:

```
{"used_memory": 53858016, "used_memory_rss": 67555328, "keyspace_hits": 3971437, "keyspace_misses": 85502, "expired_keys": 38126, "evicted_keys": 0, "keys": 734}
```

NOTE: remind to check the log file (/var/opt/microsoft/omsagent/WORKSPACE_ID/log/omsagent.log) after restarting the agent. 

Alright, now you should see in Log Analytics Custom Logs a table called redismemory_CL. Here are the queries for basic monitoring.


```
// redis keys
redismemory_CL
| project TimeGenerated, keys_d
| render timechart

// redis used memory
redismemory_CL
| project TimeGenerated, used_memory_d, used_memory_rss_d
| render timechart 

// redis keyspace
redismemory_CL
| project TimeGenerated, keyspace_misses_d, keyspace_hits_d
| render timechart 

// Redis Cache hit Ratio
redismemory_CL
| project TimeGenerated, keyspace_misses_d, keyspace_hits_d
| extend ratio = keyspace_hits_d / (keyspace_hits_d + keyspace_misses_d) * 100
| project TimeGenerated, ratio  | render timechart 
```


Run from bash:
```
# Adding some random keys
for i in $(seq 10000);do  redis-cli -c -h IP -p PORT  -a PWD set mykey1$RANDOM$i 'helloskdjflaskdjflaajsdfjhkasjdfhaksjdhfakjshdfkajhskfdjhaksjdfhaksjdhfkajshdfkjashdkjfhaskjdhfaksjdhf' EX 60;done

# forcing redis to miss 
for i in $(seq 10000);do  redis-cli -c -h IP -p PORT  -a PWD get mykey11111$i;done
```

Result:

