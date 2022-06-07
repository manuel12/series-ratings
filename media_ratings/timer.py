import time

class ParserTimer():
    def __init__(self, parser, parser_arg, exec_func=None):
        self.parser_cls = parser
        self.parser_arg = parser_arg
        self.exec_func = exec_func
        self.run_time = 0
        
        
    def run_exec_func(self):
        tic = time.perf_counter()
        parser_instance = self.parser_cls(self.parser_arg)
        if(self.exec_func):
            parser_instance[self.exec_func]()
        
        toc = time.perf_counter()
        self.run_time = toc - tic
        
    def print_run_time(self):
        self.run_exec_func()
        print(self.run_time)
        
    def get_run_time(self):
        self.run_exec_func()
        return self.run_time
