#!/usr/bin/env python
import copy
class Matrix(object):
    def __init__(self, element_list):
        self.m = len(element_list)      #stroka,   row, i, m
        self.n = len(element_list[0])   #stolbets, col, j, n
        self.element_list = copy.deepcopy(element_list)

    def __add__(self, other):
        if self.colCount() == other.colCount() and self.rowCount() == other.rowCount():
            m = E(min(self.rowCount(),self.colCount()))
            for i in range(self.colCount()):
                for j in range(self.rowCount()):
                    m.getElements()[i][j] = self.getElement(i,j) + other.getElement(i,j)
        else:
            print("Can not add matrices. Their dimensions do not match")
            return None
        return m

    def __sub__(self, other):
        if self.colCount() == other.colCount() and self.rowCount() == other.rowCount():
            m = Matrix([[0 for i in range(self.colCount())] for j in range(self.rowCount())])
            for i in range(self.rowCount()):
                for j in range(self.colCount()):
                    m.getElements()[i][j] = self.getElement(i,j) - other.getElement(i,j)
        else:
            print("Can not subtract matrices. Their dimensions do not match")
            return None
        return m

    def __neg__(self):
        m = Matrix([[-self.getElement(i,j) for j in range(self.colCount())] for i in range(self.rowCount())])
        return m

    def __mul__(self, other):
        if self.colCount() == other.rowCount() and self.rowCount() == other.colCount():
            m = E(self.rowCount())
            for i in range(self.rowCount()):
                for j in range(other.colCount()):
                    summa = 0
                    for k in range(other.rowCount()):
                        summa += self.getElement(i,k)*other.getElement(k,j)
                        m.getElements()[i][j] = summa
        else:
            print("Can not multiply the matrices. Their dimensions do not match")
            return None
        return m

    def __rmul__(self, a):
        m = Matrix([[0 for i in range(self.colCount())] for j in range(self.rowCount())])
        for i in range(self.rowCount()):
            for j in range(self.colCount()):
                m.getElements()[i][j] = self.getElement(i,j) * a
        return m
    
    def __div__(self, other):
        m = self*other.inverse()
        return m

    def __str__(self):
        s = ""
        for i in range(self.rowCount()):
            for j in range(self.colCount()):
                s += str(self.element_list[i][j]) + " "
            s += "\n"
        return s

    def __eq__(self, other):
        eq = True
        if self.colCount() == other.colCount() and self.rowCount() == other.rowCount():
            for row in [[self.getElement(i,j) == other.getElement(i,j) for j in range(self.colCount())] for i in range(self.rowCount())]:
                for el in row:
                    eq &= el
        else:
            return False
        return eq

    def __pow__(self, exp):
        exp = int(exp)
        m = self.copy()
        for i in range(exp-1):
            m *= self
        return m

    def getElements(self):
        return self.element_list

    def getElement(self, i, j):
        return self.element_list[i][j]

    def rowCount(self):
        return self.m

    def colCount(self):
        return self.n

    def setElement(self, i, j, value):
        self.element_list[i][j] = value

    def slice(self,el_coord_list):
        """slicing"""
        if type([]) is not type(el_coord_list):
            print("Invalid enry data. Use list (e.g. [1,0])")
            return None
        if len(el_coord_list) < 2:
            print("list is too short. At least two integers required (e.g. [1,0])")
            return None
        
        #TODO sdelat preobrazovanie v int pervih dvuh elementov ili proverku intov v spiske

        if el_coord_list[0] > self.rowCount() or el_coord_list[1] > self.colCount():
            print("Slicing was not successfull. Element coordinates (%d,%d) are out of the matrix [%d,%d] index range [0..%d,0..%d]"%(el_coord_list[0],el_coord_list[1],self.rowCount(),self.colCount(),self.rowCount()-1,self.colCount()-1))
            return None

        new_row_count = self.rowCount()-1
        new_col_count = self.colCount()-1
        l = []
        ll = [[0 for i in range(new_col_count)]for j in range(new_row_count)]
        for i in range(self.rowCount()):
            if i == el_coord_list[0]:
                pass
            else:
                for j in range(self.colCount()):
                    if j == el_coord_list[1]:
                        pass
                    else:
                        l.append(self.getElement(i, j))

        for i in range(new_row_count):
            for j in range(new_col_count):
                ll[i][j] = l[j+new_row_count*i]
        return Matrix(ll)

    @property
    def is_square(self):
        return self.m == self.n

    def det(self):
        det = 0
        if self.colCount() == self.rowCount() == 2:
            return self.getElement(0,0)*self.getElement(1,1) - self.getElement(0,1)*self.getElement(1,0)
        
        elif self.colCount() == self.rowCount() == 3:
            return self.getElement(0,0)*(self.getElement(1,1)*self.getElement(2,2) - self.getElement(1,2)*self.getElement(2,1)) - self.getElement(0,1)*(self.getElement(1,0)*self.getElement(2,2) - self.getElement(2,0)*self.getElement(1,2)) + self.getElement(0,2)*(self.getElement(1,0)*self.getElement(2,1) - self.getElement(2,0)*self.getElement(1,1))

        elif (self.colCount() == self.rowCount()) and (self.colCount != 3):
            for i in range(self.rowCount()):
                minor = (-1)**i*self.getElement(0,i)*self.slice([0,i]).det()
                det += minor
        else:
            print("Can not find determinant. The matrix is not square.")
            return None
        return det

    def det_(self):
        det = 0
        if self.is_square:
            for i in range(self.rowCount()):
                minor = (-1)**i*self.getElement(0,i)*self.slice([0,i]).det_()
                det += minor
        else:
            print("Can not find determinant. The matrix is not square.")
            return None
        return det

    def inverse(self):
        d = self.det()
        if d:
            m = Matrix([[0 for i in range(self.colCount())] for j in range(self.rowCount())])
            for i in range(self.rowCount()):
                for j in range(self.colCount()):
                    m.getElements()[j][i] = float(((-1)**(i+j))*self.slice([i,j]).det())/d
                    # m.setElement(j, i, float(((-1)**(i+j))*self.slice([i,j]).det())/d)
        else:
            print("det is %s"%d)
            return None
        return m

    def reverse(self):
        self.inverse()

    def transpose(self):
        if self.is_square():
            for i in range(self.rowCount()):
                for j in range(self.colCount()-i):
                    self.element_list[i][j+i], self.element_list[j+i][i] = self.element_list[j+i][i], self.element_list[i][j+i]
            return self
        else:
            element_list = [[self.element_list[i][j] for i in range(self.rowCount())] for j in range(self.colCount())]
            self.m = len(element_list)
            self.n = len(element_list[0])
            self.element_list = element_list
        return self

    def transposed(self):
        return Matrix(self.element_list).transpose()
        
    def copy(self):
        return Matrix(self.element_list)

    def trace(self):
        trace = 0
        for k in range(min(self.colCount(), self.rowCount())):
            trace += self.getElement(k,k)
        return trace


class E(Matrix):
    """ Edinichnaya
    """
    def __init__(self, n):
        self.n = n
        self.m = n
        self.element_list = [[(1 if i==j else 0) for i in range(self.colCount())] for j in range(self.rowCount())]





######################################################################################################################################################################

if __name__ == "__main__":

    m  = Matrix([[1,2,3],[4,5,6]])
    mv = Matrix([[1,2,3],[4,5,6]])
    mb = Matrix([[1,2,3],[4,5,76]])

    l = Matrix([[1,2,3],[4,5,7]])
    k = Matrix([[1,2],[4,5],[111,8]])

    M = Matrix([[1,2,3],[4,5,6],[10,21,-1]])
    # print(M.det())
    print(M*M*M*M*M*M)
    print(M**2.5)
    # print M += M
    print M.is_square
