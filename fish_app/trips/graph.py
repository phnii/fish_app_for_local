import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker 
import base64
from io import BytesIO
matplotlib.use('AGG')
def output_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img = buffer.getvalue()
    graph = base64.b64encode(img)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def plot_graph(x,y):
  plt.switch_backend("AGG")
  plt.figure(figsize=(10,5))
  gr= plt.bar(x,y)
  def autolabel(gr):
    for rect in gr:
        height = rect.get_height()
        plt.annotate('{}'.format(height),
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha='center', va='bottom')
  autolabel(gr)
  plt.xlabel("month",fontsize=18)
  plt.ylabel("posts",fontsize=18)
  plt.tight_layout()
  plt.xticks(range(1,13),fontsize=18)
  plt.yticks([])
  graph = output_graph()
  return graph