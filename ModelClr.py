import numpy as np
import cv2 as cv
from datetime import datetime
from pandas_datareader import data
import datetime
import yfinance as yfin
from similarityIndicator import similarityIndicator
import msgpack


class ModelClr:
    def __init__(self, simbol:dict, window_indicator:int, forecast:int):
        self.simbol:dict = simbol
        self.sequences = None
        self.indicator:similarityIndicator = similarityIndicator(window_indicator, forecast)

    def fromArrayToImage(self, df):
        res = len(df['Open'])
        GRID = res-1
        CANDELS = res
        dataY = df['Open']
        blank = np.zeros((res, res, 3))
        points = []
        top = max(dataY[:CANDELS])
        bot = min(dataY[:CANDELS])
        
        def Snap(val, top, bot)->int:
            return (val-bot)//((top-bot)/GRID)
        for candel in range(CANDELS):     
            price = dataY[candel]
            val = int(Snap(price, top, bot))
            points.append((candel, GRID-val))
        for point in points[:len(points)-1]:
            blank = cv.line(blank, point, points[points.index(point)+1], color=(1, 1, 1), thickness=1)
        return blank
    
    def classify_image_cosin(self, candele_df):
        coss:list[float] = []
        with open(f"datas_version.msgpack", "rb") as file:
            sequences = file.read()
        self.sequences = msgpack.unpackb(sequences, raw=False)
        for sequence in list(self.sequences.values()):
            ultime = candele_df.iloc[-len(sequence):]
            norm_B = np.linalg.norm(ultime['Open'])
            dot_product = np.dot(ultime['Open'], sequence)
            norm_A = np.linalg.norm(sequence)
            cosine_sim:float = dot_product / (norm_A * norm_B)
            coss.append(cosine_sim)
        index = np.argmax(coss)
        return list(self.sequences.keys())[index]

    def getData(self, y1, m1, d1, y2, m2, d2, nameClass, index):
        with open(f"datas_version.msgpack", "rb") as file:
            sequences = file.read()
        self.sequences = msgpack.unpackb(sequences, raw=False)
        start = datetime.datetime(y1, m1, d1)
        end = datetime.datetime(y2, m2, d2)
        df = data.get_data_yahoo(self.simbol[index][1], interval='1h', start=start, end=end)
        df = df.reset_index(drop=True)
        df = list(df['Open'][8:len(df['Open'])-8])

        try:
            self.sequences[nameClass] = df
            data = msgpack.packb(self.sequences)
            with open(f'datas_version.msgpack', 'wb') as file:
                file.write(data)
            return "done"
        except Exception as e:
            return str(e)
    
    def download_data(self, index):
        yfin.pdr_override()
        start = datetime.datetime.today().date()-datetime.timedelta(729)
        end = datetime.datetime.today()
        df = data.get_data_yahoo(self.simbol[index][1], interval='1h', start=start, end=end)
        return df

    def returnIndicator(self):
        return self.indicator