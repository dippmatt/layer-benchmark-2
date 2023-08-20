from typing import Dict, List, Tuple

class Step:
    def __init__(self, name, step_method: callable, requirements: List[Dict]):
        """A single step in the benchmark pipeline 

        Args:
            step_method (callable): Callable method, executes the step
            requirements (List[Dict]): List of requirements.
                Each element of list is a dict with keys:
                    - 'main_arg' argparse argument name
                    if 'main_arg' is not set as key we set 2 other keys
                    - 'step' previous step that produced the data for the requirement
                    - 'name' name of the requirement to find it in output data of prevous step.
        """
        self.name = name
        self._callable = step_method
        self.requirements = requirements
        self.args = None
        # output will be set after self.run() was successful
        self.output = None

    def set_args(self, args: Tuple):
        """Sets arguments required before running self.run()

        Args:
            args (Tuple): Tuple of arguments to pass to self._callable
        """
        self.args = args
        
    def run(self):
        """Executes the step's callable method
        """        
        assert self.args is not None, f"Arguments for {self._callable} have not been set yet!"
        self.output = self._callable(* self.args)
        assert self.output is not None, f"Step {self.name} did not run successfully!"
        return
        