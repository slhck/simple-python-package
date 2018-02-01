import os
import sys
import subprocess
from multiprocessing import Pool
from platform import system as _current_os

from ._logger import setup_custom_logger

logger = setup_custom_logger('{{ cookiecutter.app_name }}')

CUR_OS = _current_os()
IS_WIN = CUR_OS in ['Windows', 'cli']
IS_NIX = (not IS_WIN) and any(
    CUR_OS.startswith(i) for i in
    ['CYGWIN', 'MSYS', 'Linux', 'Darwin', 'SunOS', 'FreeBSD', 'NetBSD'])
NUL = 'NUL' if IS_WIN else '/dev/null'

def which(program):
    """
    Find a program in PATH and return path
    From: http://stackoverflow.com/q/377017/
    """
    def is_exe(fpath):
        found = os.path.isfile(fpath) and os.access(fpath, os.X_OK)
        if not found and sys.platform == 'win32':
            fpath = fpath + ".exe"
            found = os.path.isfile(fpath) and os.access(fpath, os.X_OK)
        return found

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            logger.debug("found executable: " + str(program))
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = os.path.expandvars(os.path.expanduser(path)).strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                logger.debug("found executable: " + str(exe_file))
                return exe_file

    return None

def run_command(cmd, dry=False):
    """
    Another generic function to run a command.
    Set dry to just print and don't actually run.

    Returns stdout + stderr.
    """
    logger.debug("Running command: {}".format(cmd))

    if dry:
        logger.debug("Dry mode specified, not actually running command")
        return

    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    stdout, stderr = p.communicate()

    if p.returncode == 0:
        return (stdout + stderr)
    else:
        raise RuntimeError("Error running command {}: {}".format(cmd, str(stderr)))

def shell_call(cmd):
    """
    Run a command and return output of (returncode, stdout, sterr)  as result.

    Arguments:
        - cmd: list of command parts
    """
    try:
        x = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        ret = (x.returncode, str(x.stdout, "utf-8"), str(x.stderr, "utf-8"))
        return ret
    except subprocess.SubprocessError as e:
        logger.error("System error running command: " + str(cmd))
        logger.error(str(e.output))
        raise RuntimeError()

class ParallelRunner():
    """
    Class for running commands in parallel and getting output
    """
    def __init__(self, concurrency=4):
        self.cmds = set()
        self.concurrency = concurrency
        self.outputs = {}

    def log_commands(self):
        for c in self.cmds:
            logger.info(c[0])

    def add_cmd(self, cmd, name=""):
        """
        Add a command to be processed in parallel.
        "name" is an optional short name given to the command which will be printed to output
        """
        if cmd:
            self.cmds.add((cmd, name))

    def _run_single_cmd(self, cmd, name):
        logger.debug("Starting command: {}".format(cmd))
        ret, stdout, stderr = shell_call(cmd)
        if ret != 0:
            logger.error("Error running parallel command: {cmd} \n{stdout}\n{stderr}".format(cmd=cmd, stdout=stdout, stderr=stderr))
        return ret == 0
        self.outputs[cmd] = {
            "stdout": stdout,
            "stderr": stderr
        }

    def run_commands(self):
        logger.debug("starting parallel run of commands")
        pool = Pool(processes=self.concurrency)
        results = pool.starmap(self._run_single_cmd, self.cmds)
        if not all(results):
            logger.error("There were errors in your commands. Please check the output and re-run the processing chain!")
            sys.exit(1)
        logger.debug("all processes completed")
        self.cmds = set()

    def num_commands(self):
        return len(self.cmds)
