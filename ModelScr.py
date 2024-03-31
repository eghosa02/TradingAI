from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from IPython.display import HTML

class ModelScr:
    def __init__(self, Simbol):
        self.Simbol = Simbol
        self.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }

    def scrape(self, simbol:int):
        self.links = [
            f"https://www.investing.com/currencies/{self.Simbol[simbol][0]}",
            f"https://www.investing.com/currencies/{self.Simbol[simbol][0]}-news",
            f"https://www.investing.com/currencies/{self.Simbol[simbol][0]}-opinion",
            f"https://www.investing.com/currencies/{self.Simbol[simbol][0]}-technical",
            f"https://www.myfxbook.com/community/outlook/{self.Simbol[simbol][2]}",
            f"https://www.investing.com/currencies/{self.Simbol[simbol][0]}-candlestick",
            f"https://www.investing.com/currencies/{self.Simbol[simbol][0]}-commentary",
            f"https://www.investing.com/currencies/{self.Simbol[simbol][0]}-scoreboard",
            f"https://www.investing.com/currencies/{self.Simbol[simbol][0]}-rankings"
        ]
        r = Request(url=self.links[3], headers=self.headers)
        response = urlopen(r)
        soup = BeautifulSoup(response.read(), "html.parser")
        try:
            decision = soup.find("div", {"class":"mb-6 mt-1 rounded-full px-4 py-1.5 text-center -mt-2.5 font-semibold leading-5 text-white bg-positive-main"})
            
            if not decision:
                decision = soup.find("div", {"class":"mb-6 mt-1 rounded-full px-4 py-1.5 text-center -mt-2.5 font-semibold leading-5 text-white bg-negative-main"})
            else:
                decision = decision.get_text()

            if not decision:
                decision = soup.find("div", {"class":"mb-6 mt-1 rounded-full px-4 py-1.5 text-center -mt-2.5 font-semibold leading-5 text-white bg-primary-main"})
            else:
                decision = decision.get_text()
            if not decision:
                decision = ""
        except:
            decision = ""

        try:
            infos = soup.find("div", {"class":"flex items-center gap-x-4 text-xs md2:gap-x-3.5 lg:gap-x-4"})
            if not infos:
                infos = ""
            else:
                infos = infos.get_text()
        except:
            infos = ""
        
        try:
            r = Request(url=self.links[4], headers=self.headers)
            response = urlopen(r)
            soup = BeautifulSoup(response, "html.parser")
            datas = soup.find("table", {"id":"currentMetricsTable"})
        except:
            datas = "<p></p>"
        return decision, infos, str(datas)