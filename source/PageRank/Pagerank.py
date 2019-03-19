#!/usr/bin/env python
import numpy as np
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

    def rank(self, k, beta):
        page = self.page
        Use_mit = self.matrix.T
        s = Use_mit.shape
        v = page.shape
        for i in range(k):
            #  针对dead ends和spider trap做出调整
            new_page = (Use_mit.dot(page)) * beta + (1 - beta)*np.ones(len(page)) / len(page)
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
    Row, Col = txt.txt_read()   #边从行中节点指向列中节点
    #添加一条边，为了把邻接矩阵调整成方阵，两个节点都没有出现在结果中，应该没影响
    Row.append(8297)
    Col.append(0)
    thepage = Page(Row, Col)
    print(thepage.matrix.shape)      #就得是方阵
    #print(thepage.matrix.toarray())
    thepage.regularize()
    #print(thepage.matrix.toarray())
    Klist = [100]
    betalist =[0.85] #[0.5, 0.6,0.65, 0.7,0.75, 0.8,0.85, 0.9]
    #k = 80
    beta = 0.85
    for k in Klist:

        print("K = "+str(k))
        print("beta= "+str(beta))
        page = thepage.rank(k, beta)
        TopPages = np.argsort(page)[-100:]
        TopPagescores = np.sort(page)[-100:]
        TopPages = TopPages[::-1]
        TopPagescores = TopPagescores[::-1]
        np.save('TopPages, K='+str(k), TopPages)
        np.save('TopPagescores, K='+str(k), TopPagescores)
        print("TopPages")
        print(TopPages)
        print("Scores")
        print(TopPagescores)
        print("------------------------------")
        # with open('TopPage.txt','w') as f:
        #     for i in range(len(TopPages)):
        #         f.write(str(TopPages[i]) + " " + str(TopPagescores[i]) +  '\n')



if __name__ == '__main__':
    main2()