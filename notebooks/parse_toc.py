import yaml
from pathlib import Path

def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in dict_generator(value, pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in dict_generator(v, pre + [key]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]



print(str(Path()))
with open('_toc.yml','r') as infile:
  the_toc = yaml.load(infile, Loader=yaml.CLoader) 

for item in the_toc:
    the_list = list(dict_generator(item))
    for member in the_list:
        print(member[-1])
        
          
    
    
