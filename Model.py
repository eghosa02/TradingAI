from ModelClr import ModelClr
from ModelScr import ModelScr
import matplotlib.pyplot as plt

class Model:
    def __init__(self, Cluster:ModelClr, Scraping:ModelScr):
        self.Cluster = Cluster
        self.Scraping = Scraping
        self.simbol = None
        self.dataset = None#391
    
    def predictCluster(self):
        cluster = self.Cluster.classify_image_cosin(self.dataset)
        return cluster
    
    def predictImage(self):
        indicator = self.Cluster.returnIndicator()
        df = self.dataset.tail(5000).reset_index(drop=True)#df = self.dataset.reset_index(drop=True)
        sequenza_simile1, sequenza_simile2 = indicator.trova_sequenza_simile(df)
        sequenza_simile2 = sequenza_simile2.reset_index(drop=True)
        sequenza_simile1 = sequenza_simile1.reset_index(drop=True)
        diff = sequenza_simile2['Open'][0]-sequenza_simile2['Open'][len(sequenza_simile2['Open'])-1]
        img = self.Cluster.fromArrayToImage(sequenza_simile2)
        plt_format = ({"cross": "X", "line": "-", "circle": "o--"})['circle']
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([i for i in range(len(sequenza_simile2['Open']))], sequenza_simile2['Open'], plt_format)
        return fig, diff, min(sequenza_simile2['Open']), max(sequenza_simile2['Open'])

    def predictScraping(self, simbol:int):
        return self.Scraping.scrape(simbol)

    def predict(self, simbol:int, start, end, nameClass):#vero un bel pò, claro che si, ti mostro il molo o ti mollo il mostro, te capissi sempre cassi per catenassi, se non è zuppa le pan bagnato
        try:
            y1, m1, d1 = start.split("-")
            y2, m2, d2 = end.split("-")
            self.get_cluster_model().getData(y1, m1, d1, y2, m2, d2, nameClass, simbol)
            return "", 0, 0, "", "<p></p>", "done"
        except:   
            self.simbol = simbol
            self.dataset = self.Cluster.download_data(self.simbol)
            cluster = self.predictCluster()
            img, diff, minim, maximum = self.predictImage()
            decision, infos, datas = self.predictScraping(simbol)
            goTo = self.dataset['Open'][len(self.dataset['Open'])-1] - diff
            return cluster, goTo, img, f"{decision}\n{infos}", datas, "", minim, maximum
