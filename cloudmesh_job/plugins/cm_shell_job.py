from __future__ import print_function

# from cloudmesh_job.cm_jobdb import JobDB
from cmd3.console import Console
from cmd3.shell import command
import hostlist
from pprint import pprint
from cloudmesh_base.util import banner
from cloudmesh_job.cm_jobdb import JobDB

class cm_shell_job:
    database = None

    def activate_cm_shell_job(self):
        self.register_command_topic('HPC', 'job')

    @command
    def do_job(self, args, arguments):
        """
        ::

            Usage:
                job server start
                job server stop
                job server clean
                job server kill
                job server deploy
                job server ps
                job stat
                job list
                job add JOBLIST [--host=HOST] [--options=OPTIONS] [--inputs=INPUTS] [--outputs=OUTPUTS]
                job add --file=filename
                job write --file=filename
                job find --name=NAME
                job find --attribute=ATTRIBUTE --value=VALUE
                job delete JOBLIST

            Arguments:

                NAME       the name of the job
                HOST       the host on which the job should run
                OPTIONS    options passed to the command
                INPUTS     input files
                OUTPUTS    output files
                ATTRIBUTE  an attribute
                VALUE      a value
                JOBLIST    the job list

            Description:

                manages a job catalog to submit them to a computation cloud
                or Grid.

                job server start

                    starts the job server

                job server stop

                    stops the job server

                job server clean

                    removes all data in the job server and does a graceful clean, e.g deletes all scheduled jobs

                job server kill

                    kills just the job server, but does not delete the jobs from the schedulers.
                    this command should not be called in normal circumstances.

                job set GROUP

                    sets the default job group

                job add  GROUP TODO

                    adds a job to a group

                job server start

                    starts the server

                job server stop

                    stops the server

                job stat

                    prints a simple statistics of the jobs

                job add NAMES [--host=HOST] [--option=OPTIONS] [--inputs=INPUTS] [--outputs=OUTPUTS]

                    adds a number of jobs

                job add --file=filename

                    adds the job from the file. The postfix of the file deterimnes which
                    format it is. The formats supported are .csv, .yaml, .json

                job write --file=filename

                    writes the jobs to a file. The postfix of the file deterimnes which
                    format it is. The formats supported are .csv, .yaml, .json


                job list [--output=OUTPUT]

                    lists the jobs in the format specified

                job insert NAME [HOST] [OPTIONS] [INPUT_FILES] [OUTPUT_FILES]

                    inserts the job with the name into the job database. Options,
                    input and output files could be specified

                job find --name=NAME

                    find the job with the given name

                job find --attribute=ATTRIBUTE --value=VALUE

                    find jobs that match the given attribute.

                job delete JOBLIST

                    delete the job with the specified names in the joblist.

                THE FOLLOWING IS NOT YET DEFINED OR MAY CHANGE

                job add TODO

                    ... not yet sure what in the rest of the command

                    adds a job to the job server and returns its id

                job last

                    returns the last job added to the server

                job delete ID

                    deletes the job from the job server and cancels it if it is scheduled for execution.

                job info ID

                    give the info of a job

                job submit ID HOST

                    submits the job with the given ID to the host

                job list GROUP

                    lists the jobs in the group

                job status [ID | GROUP]

                    list the status of a single job or the status of all jobs in the group

                job status statistics

                    list the statistics of the jobs in the job server (e.g. for the states)



        """
        # pprint(arguments)

        if arguments.get("server"):

            if arguments["start"]:

                db = JobDB()
                db.start()

                Console.ok("job server start")

            elif arguments["stop"]:

                db = JobDB()
                db.stop()

                Console.ok("job server stop")

            elif arguments["ps"]:

                db = JobDB()
                db.ps()

            elif arguments["clean"]:

                Console.ok("job server clean")

            elif arguments["kill"]:

                Console.ok("job server kill")

            elif arguments["deploy"]:

                Console.ok("job server deploy")

        elif arguments["delete"] and arguments["JOBLIST"]:

            joblist = hostlist.expand_hostlist(arguments["JOBLIST"])

            # debug msg
            print(joblist)

            db = JobDB()
            db.connect()

            for job in joblist:
                # if job exists:
                Console.ok("delete job {:}".format(job))

                db.delete_jobs(attribute="name", value=job)


        elif arguments["add"]:

            joblist = hostlist.expand_hostlist(arguments["JOBLIST"])
            host = arguments["--host"]

            inputs = [None]
            outputs = [None]
            options = [None]

            if arguments["--inputs"]:
                inputs = hostlist.expand_hostlist(arguments["--inputs"])
            if arguments["--outputs"]:
                outputs = hostlist.expand_hostlist(arguments["--outputs"])
            if arguments["--options"]:
                options = hostlist.expand_hostlist(arguments["--options"])
            # check if inputs are either 0, 1 or the length of joblist

            def expand_parameter(parameter, label):
                """

                :param parameter:
                :param label:
                :return: list of strings
                """
                _parameter = parameter
                if len(_parameter) == 1:
                    _parameter = _parameter * len(joblist)
                elif len(_parameter) == len(joblist):
                    pass
                else:
                    Console.error("the number of input files do not match the hostlist")
                    print("joblist count:", len(joblist))
                    print(label, "count: ", len(_parameter))
                return _parameter

            options = expand_parameter(options, "options")
            inputs = expand_parameter(inputs, "inputs")
            outputs = expand_parameter(inputs, "outputs")

            pprint(joblist)
            pprint(inputs)
            pprint(outputs)

            # dependent on if 0, 1, or length of joblist handle that

            # debug msg
            print(joblist)

            for i in range(len(joblist)):
                banner(i)

                Console.ok("add job : {:} ".format(joblist[i]))
                Console.ok("  input : {:} ".format(inputs[i]))
                Console.ok("  output: {:} ".format(outputs[i]))




        elif arguments["stat"]:

            Console.ok("job stat")

        elif arguments["list"]:

            output = arguments["--output"]

            Console.ok("lists the jobs in the format specified")

        elif arguments["insert"]:

            name = arguments["NAME"]
            host = arguments["HOST"]
            options = arguments["OPTIONS"]
            input_files = arguments["INPUT_FILES"]
            output_file = arguments["OUTPUT_FILES"]

            Console.ok("insert")

        elif arguments["find"] and arguments["--name"]:

            name = arguments["NAME"]

            Console.ok("find the job with the given name")

        elif arguments["find"] and arguments["--attribute"] and arguments["--value"]:

            name = arguments["NAME"]
            attribute = arguments["--attribute"]
            value = arguments["--value"]

            Console.ok("job find --attribute=ATTRIBUTE --value=VALUE")



        pass


if __name__ == '__main__':
    command = cm_shell_job()
    command.do_job()