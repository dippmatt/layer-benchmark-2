from typing import Dict, List
from shared_scripts.step import Step

class Pipeline:
    def __init__(self, args, validate_args: callable):
        """
        Args:
            args (_type_): Expects argumets from argparse module.
                Arguments passed to main()
            steps (list): list of Step objects to run one after another
        """
        # parsed arguments from argparse
        self.args = args
        validate_args(self.args)
        # ordered list of steps to run
        self.steps = []

    def add_step(self, method: callable, requirements: List[Dict]):
        """Adds a step to the pipeline.

        Args:
            method (callable): function to run
            requirements (List[Dict]): list of requirements for the step
                requirements can be from the output of previous steps,
                or as a argparse argument from self.args
        """
        self.steps.append(Step(method.__name__, method, requirements))

    def get_step_args(self, requirements: List[Dict]):
        """Collects arguments for a step.
        
        Arguments can be from the output of previous steps,
        or as a argparse argument from self.args

        Args:
            requirements (List[Dict]): _description_

        Returns:
            _type_: _description_
        """        
        args = []
        for requirement in requirements:
            # in case we require a argparse argument from main
            if 'main_arg' in requirement:
                arg_name = requirement['main_arg']
                args.append(getattr(self.args, arg_name))
            # in case we require the output of a previous step
            else:
                req_index = requirement['step']
                req_name = requirement['name']
                args.append(self.steps[req_index].output[req_name])
        return tuple(args)

    def run(self):
        for step in self.steps:
            print(f"NOW RUNNING STEP: {step.name}")
            step.set_args(self.get_step_args(step.requirements))
            step.run()
            print(f"STEP {step.name} FINISHED\n")

