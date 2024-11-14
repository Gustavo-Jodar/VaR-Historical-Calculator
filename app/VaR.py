import numpy as np
import pandas as pd

'''
Class that implements VaR calculation:
 - Sorts the pnl_vector and produces VaR = (1 - confidence_level) percentile of sorted pnl_vector
 - Contructor:
    - api = flask_restx Api Object
    - file_path = csv portifolio/trade file location
'''
class VaR:
    def __init__(self, api, file_path: str) -> None:
        # Setting API for error handling 
        self.api = api
        # Load the CSV file and parse it into structured data
        self.data = self.read_csv(file_path)

    # Converts csv file to data and sorted pnl_vector
    def read_csv(self, file_path: str) -> dict:
        try:
            # Read the CSV file
            df = pd.read_csv(file_path, header=0, names=["trade_id", "pnl_vector", "vector_size", "pnl"])
            
            # Converts pnl_vector to np.array
            df['pnl_vector'] = df['pnl_vector'].apply(lambda x: np.array([float(i) for i in x.split(';')]))
            
            return df

        # Corrupted file
        except:
             self.api.abort(400, "Input file not accepted, please review the accepted format.")

    # Calculates
    def get_var(self, confidence_level):
        try:
            pnl_vectors = np.array(self.data['pnl_vector'].tolist())

            var_sum = np.sum(pnl_vectors, axis=0)
            var_sum.sort()
            
            # Calculates VaR using np.percentile
            var_np = np.percentile(np.array(var_sum), 100 * (1 - confidence_level), method='lower')

            return var_np
        except:
             self.api.abort(400, "VaR calculation failed.")

    def get_sorted_scenarios_sum(self):
        try:
            pnl_vectors = np.array(self.data['pnl_vector'].tolist())

            var_sum = np.sum(pnl_vectors, axis=0)
            var_sum.sort()
            
            return var_sum.tolist()
        except:
             self.api.abort(400, "VaR calculation failed.")

    def get_trades_var(self, confidence_level):
        try:

            # Organizes data in dict    
            
            trades_data = []
            for i, row in self.data.iterrows():
                    self.data["pnl_vector"][i].sort()
                    trades_data.append({
                        'trade_id': row['trade_id'],
                        "pnl_vector": self.data["pnl_vector"][i],
                        "vector_size": row['vector_size'],
                        "pnl": row['pnl']
                    })
            
            
            # Calculates VaR using np.percentile for every trade in a portifolio
            response = []
            for trade in trades_data:
                response.append(
                    {
                        "trade_id": trade['trade_id'],
                        "trade VaR": np.percentile(trade['pnl_vector'], 100 * (1 - confidence_level), method='lower')
                    }
                )
            
            return response
        except:
             self.api.abort(400, "VaR calculation failed.")
