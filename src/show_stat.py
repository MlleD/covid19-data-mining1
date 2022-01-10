import regex as re
import cst
import matplotlib.pyplot as plt
import cleaning_text as text

#count occurences of words in column list and put the result in dict
def count_occurences(lsCol):
    count = {}
    for s in range(len(lsCol)):
      count[lsCol[s]] = lsCol.count(lsCol[s])
    return count

#show feeling statistics  
def feeling_stat(dictOcc):
    x = list(dictOcc.keys())
    y = list(dictOcc.values())
    plt.bar(range(len(dictOcc)),sorted(y),tick_label=x)
    plt.savefig('feelingStat.png')
    plt.show()

#show date statistics  
def date_stat(dictOcc):
    x = list(dictOcc.keys())
    y = list(dictOcc.values())
    y_pos = range(len(x))
    plt.bar(range(len(dictOcc)),y,tick_label=sorted(x))
    plt.xticks(y_pos, x, rotation=90)
    plt.savefig('dateStat.png')
    plt.show()

if __name__ == "__main__": 
    print(feeling_stat(count_occurences(text.read_column(cst.TRAIN, 5))))
    print(feeling_stat(count_occurences(text.read_column(cst.TEST, 5))))
    print(date_stat(count_occurences(text.read_column(cst.TRAIN, 3))))
