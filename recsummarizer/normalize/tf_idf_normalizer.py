from .base_normalizer import BaseNormalizer

import numpy as np
import pandas as pd
import math

class TfIdfNormalizer(BaseNormalizer):


    def normalize(self, bow_df):

        tf_idf_df = bow_df.applymap(self.__tf)

        tf_idf_df = self.__idf(tf_idf_df)
    
        return self.__tf_idf(tf_idf_df)

    def __tf(self, cell_value):
        '''
        Function to compute the tf value (term frequency)
        when this function is applied, the dataframe already contains
        the frequency of each word, per cell.
        
        tf = 1 + log2(f_i,j)
        f_i,j = frequency of the term i in document j

        Parameters:
        cell_value (dataframe cell)

        Returns:
            cell_value: the tf value for all the terms

        '''

        if cell_value != 0:
            cell_value = (math.log2(cell_value)) + 1
            return cell_value
        
        return 0

    def __idf(self, dataframe):
        
        '''
        Function to compute the idf value (inverse document frequency)
        idf = log (number of total documents / number of documents having a given term)

        Parameters:
            dataframe

        Returns:
            dataframe with idf values for all the terms

        '''

        total_document_occurences = []

        for row in range(len(dataframe)):

            # rows of the dataframe:
            array_row_values = np.array(dataframe.iloc[row])
            number_document_occurrences = 0
            
            for document_index in array_row_values:
                
                if document_index > 0:
                    number_document_occurrences = number_document_occurrences + 1
            
            total_document_occurences.append(number_document_occurrences)

        number_total_documents = len(dataframe.columns)

        i = 0

        for value in total_document_occurences:
            
            idf_value = number_total_documents/value
            idf_value = math.log2(idf_value)
            total_document_occurences[i] = idf_value
            i = i + 1 
        
        dataframe['idf'] = total_document_occurences 

        return dataframe

    

    def __tf_idf(self,dataframe):
        '''
        Fucntion to calculate the tf-idf value for all the terms
        in the dataframe
        This function only should be applied to the dataframe after 
        the tf and idf function were already applied.

        Parameters:
            dataframe

        Returns:
            dataframe with tf_idf values for all the terms
        '''    

        idf_values = np.array(dataframe['idf'])

        for column_index in range(len(dataframe.columns)-1):
            
            current_column = np.array(dataframe.iloc[:, column_index])
            document_tf_idf_values = np.multiply(current_column, idf_values)

            current_document_norm = np.linalg.norm(document_tf_idf_values, 2) 
            normalized_tf_idf_values = np.divide(document_tf_idf_values, current_document_norm)

            column_name = "tf_idf_document" + str(column_index)
            dataframe[column_name] = normalized_tf_idf_values 
        
        return dataframe