import numpy as np

class similarityIndicator:
    
    def __init__(self, window_size, forecast):
        self.window_size = window_size
        self.forecast = forecast
    
    def returnForecast(self):
        return self.forecast
    
    def trova_sequenza_simile(self, candele_df):
        num_candele = len(candele_df)
        sequences = []
        ultime_32 = candele_df.iloc[-self.window_size:]
        norm_B = np.linalg.norm(ultime_32['Open'])
        for i in range(num_candele - ((self.window_size*2)+(self.forecast-self.window_size))):

            subset = candele_df.iloc[i:i+self.window_size]

            dot_product = np.dot(ultime_32['Open'], subset['Open'])
            norm_A = np.linalg.norm(subset['Open'])
            cosine_sim = dot_product / (norm_A * norm_B)

            sequences.append(cosine_sim)

        indice_simile = np.argmax(sequences)
        print(indice_simile)
        return candele_df.iloc[indice_simile:indice_simile+self.window_size], candele_df.iloc[indice_simile+self.window_size:indice_simile+self.window_size+self.forecast]