import sys
import logging

log = logging.getLogger(__name__)


def terminal_error(message):
    """
    Called when an error has occurred that prevents fylm_critic from doing anything useful.
    Makes the error message display clearly and terminates the program.

    :param message: a useful explanation as to why the program has to stop
    :type message:  str

    """
    log.error("")
    log.exception("FATAL ERROR! " + message)
    log.error("")
    sys.exit(1)