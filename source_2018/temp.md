
```{code-cell}
### BEGIN SOLUTION
for season in ['spring','fall']: 
    print(f'\nseason: {season}')
    red=file_dict[season]['reflect']['red']
    nearir=file_dict[season]['reflect']['nearir']
    ndvi = (nearir - red)/(nearir + red)
    file_dict[season]['ndvi']=ndvi
### END SOLUTION
```
