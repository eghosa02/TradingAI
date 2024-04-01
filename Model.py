from ModelClr import ModelClr
from ModelScr import ModelScr

class Model:
    def __init__(self, Cluster:ModelClr, Scraping:ModelScr):
        self.Cluster:ModelClr = Cluster
        self.Scraping:ModelScr = Scraping
        self.simbol = None
        self.dataset = None
    
    def predictCluster(self):
        cluster = self.Cluster.classify_image_cosin(self.dataset)
        return cluster
    
    def predictImage(self):
        indicator = self.Cluster.returnIndicator()
        df = self.dataset.tail(5000).reset_index(drop=True)
        sequenza_simile1, sequenza_simile2 = indicator.findSequences(df)
        sequenza_simile2 = sequenza_simile2.reset_index(drop=True)
        sequenza_simile1 = sequenza_simile1.reset_index(drop=True)
        return sequenza_simile2['Open'][len(sequenza_simile2['Open'])-1], min(sequenza_simile2['Open']), max(sequenza_simile2['Open'])

    def predictScraping(self, simbol:int):
        return self.Scraping.scrape(simbol)

    def predict(self, simbol:int):
        self.simbol = simbol
        self.dataset = self.Cluster.download_data(self.simbol)
        cluster = self.predictCluster()
        goTo, minim, maximum = self.predictImage()
        decision, infos, datas = self.predictScraping(simbol)
        return cluster, goTo, f"{decision}\n{infos}", datas, "", minim, maximum