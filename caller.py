from subprocess import call
import subprocess
from AI import main


def open_py_file(link, questions, choices, answers):
    main(link, questions, choices, answers)
    
# open_py_file()