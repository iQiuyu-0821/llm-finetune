import requests
import json
import argparse

def runModel(serverAddr, entryPoint):
    res = requests.post(
        serverAddr + "/api/jobs/",
        json={ "entrypoint": entryPoint }
    )
    rst = json.loads(res.text)
    job_id = rst["job_id"]
    print('submit.submission_id:', job_id)

def deleteJob(serverAddr, subID):
    res = requests.delete(serverAddr + "/api/jobs/" + subID)
    print('delete.res', res)

def stopJob(serverAddr, subID):
    res = requests.post(serverAddr + "/api/jobs/" + subID + "/stop")
    print('stop.res', res)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", default="xxxxxx", help="submit or delete or stop")
    parser.add_argument("--address", default="http://127.0.0.1:8265", help="server address http://127.0.0.1:8265")
    parser.add_argument("--cmdpath", default="/data/miniconda3_envs/ray/bin", help="python command path")
    parser.add_argument("--runpath", default="/data/hub/llm-inference", help="run command path")
    parser.add_argument("--modelfile", default="test.yaml", help="model yaml file")
    parser.add_argument("--subid", default="xxxxxx", help="submission id of job")
    args = parser.parse_args()
    
    # apiUrl = "http://127.0.0.1:8265"
    #cmdpath = "/Users/hub/anaconda3/envs/ray/bin"
    
    action = args.action
    apiUrl = args.address
    cmdpath = args.cmdpath
    runpath = args.runpath
    modelfile = args.modelfile
    submissionID = args.subid
    print('Input:', action, apiUrl, cmdpath, runpath, modelfile)
    
    # cmdline = f"{cmdpath}/python {cmdpath}/llm-executor run-experimental --model models/text-generation--gpt2.yaml"
    # cmdline = f"{cmdpath}/python {cmdpath}/llm-executor start-apiserver"
    if action == 'submit':
        cmdline = f"{cmdpath}/python {runpath}/test_local_cmd.py run-experimental --model={runpath}/models/{modelfile}"
        runModel(apiUrl,cmdline)
    
    if action == 'delete':
        deleteJob(apiUrl, submissionID)
        
    if action == 'stop':
        stopJob(apiUrl, submissionID)
        
    if action == 'delserv':
        cmdline = f"{cmdpath}/python {runpath}/test_local_cmd.py del-serve --appname {submissionID}"
        runModel(apiUrl,cmdline)
        
