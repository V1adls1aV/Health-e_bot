from matplotlib import pyplot as plt
from PIL.Image import open as open_image
from datetime import datetime
from io import BytesIO


class Graph:
    def __init__(self, dates) -> None:
        self.x = dates
        self.res = len(dates)
        self.y = list(range(1, self.res + 1))
    
    def get_image(self) -> None:
        print(f'{datetime.now()} --- Getting image from graph')
        stream = BytesIO()
        
        plt.title('Количество пользователей')
        plt.xticks(rotation=20)
        plt.plot_date(self.x, self.y, ls='-', fmt='.', color='green')
        
        plt.savefig(stream, format='png')
        plt.clf()
        return open_image(stream)
