# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 16:21:23 2018

@author: hasee
"""

#!/usr/bin/env python
import numpy as np
import time
from scipy.sparse import csc_matrix,csr_matrix,coo_matrix,save_npz,load_npz
import txt

class Page(object):
    def __init__(self, Row, Col):
        data = np.ones(len(Col))
        self.matrix = csr_matrix((data, (Row, Col)))  #这个实际上转置完才是书里可以拿来乘的矩阵，见rank函数
        self.page = np.ones(self.matrix.shape[0])
        self.page = self.page/len(self.page)

    def regularize(self):
        # max = np.max(self.matrix.shape)
        # self.matrix.reshape((max, max))
        s = self.matrix.nonzero()
        Row = s[0]
        Row = set(Row)
        for i in Row:
            row = self.matrix.getrow(i)
            col = row.nonzero()[1]
            mean = row.getnnz()
            for j in col:
                self.matrix[i, j] = 1 / mean
        #save_npz('Inimit', self.matrix)

    def issame(self, page, newpage):
        d = self.differ(page, newpage)
        if d < 1E-12:
            print("convergence at "+str(d))
            return True
        return False

    def differ(self, oldrank, newrank):  #这个检测标准我自己瞎选的，没在书里找到相关的
        dif = oldrank - newrank
        dif = dif/oldrank
        dif = dif**2
        return np.mean(dif)
    
    def save(self):
        page = self.page
        l=len(page)
        #将矩阵分为10部分存储，每次读取、运算一块
        partlen=int(l/parts)
        Use_mit = self.matrix.T
        
        for i in range(parts-1):
            begin=i*partlen
            end=begin+partlen
            save_npz('Use_mit'+str(i), Use_mit[begin:end])
        begin=(parts-1)*partlen
        end=l;
        save_npz('Use_mit'+str(parts-1), Use_mit[begin:end])

    def rank(self, k, beta):
        page = self.page
        l=len(page)
        #将矩阵分为10部分存储，每次读取、运算一块
        partlen=int(l/parts)
        for i in range(k):
            #  针对dead ends和spider trap做出调整
            
            #print(str(i)+'/'+str(k))
            new_page = np.ones(l)
            for j in range(parts-1):
                begin=j*partlen
                end=begin+partlen
                part=load_npz('Use_mit'+str(j)+'.npz')
                temp=part.dot(page)
                new_page[begin:end] = temp * beta + (1 - beta)*np.ones(partlen) / l
                
            begin=(parts-1)*partlen
            end=l
            part=load_npz('Use_mit'+str(parts-1)+'.npz')
            temp=part.dot(page)
            #print(temp)
            new_page[begin:end] = temp * beta + (1 - beta)*np.ones(end-begin) / l
            #new_page = (Use_mit.dot(page)) * beta + (1 - beta)*np.ones(len(page)) / len(page)
            # if i > 10:  #检测是否收敛，其实很多时候10转以上就收敛了
            #             #但是TopPage还在有微小的变化，我最后选的是80转
            #     if self.issame(page, new_page):  #检测是否收敛
            #         print("convergence when K = "+str(i))
            #         break
                    #pass
            if i == k - 1:
                d = self.differ(page, new_page)
                print("deffer = "+str(d))
            page = new_page
        return page


def main():
    Row, Col = txt.txt_read()
    Col = np.array(Col)
    Row = np.array(Row)
    data = np.ones(len(Col))
    sparse_matrix = csc_matrix((data, (Row, Col)))
    #每列和为一
    for i in sparse_matrix.indices:
        row = sparse_matrix.getrow(i)
        col = row.nonzero()[1]
        mean = row.getnnz()
        for j in col:
            sparse_matrix[i,j] = 1/mean
    save_npz('Inimit',sparse_matrix.T)

    Use_mit = sparse_matrix.T
    r = Use_mit.shape[0]
    c = Use_mit.shape[1]
    print("R = "+str(r)+" C =" + str(c))
    Page = np.ones(r)
    Page = Page/len(Page)

    for i in range(20):
        Page = Use_mit.dot(Page)
    print(Page)

def main2():
    print("Start")
    
    time_start=time.time() 
    global parts
    parts=10
    Row, Col = txt.txt_read()   #边从行中节点指向列中节点
    #添加一条边，为了把邻接矩阵调整成方阵，两个节点都没有出现在结果中，应该没影响
    Row.append(8297)
    Col.append(0)
    thepage = Page(Row, Col)
    print(thepage.matrix.shape)      #就得是方阵
    #print(thepage.matrix.toarray())
    thepage.regularize()
    #print(thepage.matrix.toarray())
    #Klist = [1,3,6,10,20, 25, 30, 40, 50, 60, 70, 80]
    betalist =[0.85] #[0.5, 0.6,0.65, 0.7,0.75, 0.8,0.85, 0.9]
    k = 100
    for beta in betalist:

        print("K = "+str(k))
        print("beta= "+str(beta))
        thepage.save()
        page = thepage.rank(k, beta)
        TopPages = np.argsort(page)#[-100:]
        TopPagescores = np.sort(page)#[-100:]
        TopPages = TopPages[::-1]
        TopPagescores = TopPagescores[::-1]
        np.save('TopPages, K='+str(k), TopPages)
        np.save('TopPagescores, K='+str(k), TopPagescores)
        time_end=time.time()

        print('totally cost',time_end-time_start)
        print("TopPages")
        print(TopPages)
        print("Scores")
        print(TopPagescores)
        print("------------------------------")
        with open('TopPage.txt','w') as f:
            for i in range(len(TopPages)):
                f.write(str(TopPages[i]) + " " + str(TopPagescores[i]) +  '\n')
        
        



if __name__ == '__main__':
    main2()

