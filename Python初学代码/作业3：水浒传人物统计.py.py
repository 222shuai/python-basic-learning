import jieba

str="一两个只看见如何这那里哥说道军马头领人出来听此时你我他不兄弟梁山好汉便是甚么今日先锋"
txt=open("E:\python学习文件\水浒传.txt", "r",  encoding="utf-8").read()
for ch in str:
        txt = txt.replace(ch, " ")
words  = jieba.lcut(txt)
counts = {}
for word in words:
        if len(word)<2:
                continue
        else:
                counts[word] = counts.get(word,0) + 1
a = list(counts.items())
a.sort(key=lambda x:x[1], reverse=True) 
for i in range(10):
    word, count = a[i]
    print ("{0:<10}{1:>5}".format(word, count))
        
