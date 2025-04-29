import pdfplumber
import pandas as pd
import os

class ReadPdf_Table():
    
    def __init__(self, filename, table_column_num = 20):
        self.filename = filename
        self.table_column_num = table_column_num
        self.table_dict = {} 
    
    def loadTable(self):
        """Public method: Extracts and returns PDF tables as DataFrames."""
        self.table_dict = self._pdf_toDict()
        self.dataframes = self._convert_toTable(self.table_dict)
        return self.dataframes
        
        
         
    def _pdf_toDict(self):   
        """Internal method: Extracts tables from PDF into a dictionary."""
        with pdfplumber.open(self.filename) as pdf:
            num_pages = len(pdf.pages)
            for page_num in range(num_pages):
                page = pdf.pages[page_num]
                page_table = page.extract_table()
                for table_column in page_table:
                    for _ in range(self.table_column_num):
                        if len(table_column) == _:
                            table_column_name = f'table_columns_{str(_)}'
                            if table_column_name not in self.table_dict.keys():
                                self.table_dict[table_column_name] = [table_column]
                            else:
                                self.table_dict[table_column_name] += [table_column]
        return self.table_dict
                                
    def _convert_toTable(self, dictionary):
        """Internal method: Converts dictionary to cleaned DataFrames."""
        self.dictionary = dictionary
        self.dataframes = []
        for key, values in self.dictionary.items():
            column_header = values[0]
            content = []
            for value in values[1:]:
                if value == column_header:
                    pass
                else:
                    content.append(value)
            dataframe = pd.DataFrame(content, columns=column_header)
            clean_df = dataframe.dropna(how='all')
            self.dataframes.append(clean_df)
            
        return self.dataframes 
        
