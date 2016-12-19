# python 3.5

import copy

# DataSet [P, Q, R, S]
form = [
    [[3],       [1, 3],     [2],        [3]],
    [[2],       [2, 3],     [1, 3],     [1, 3]],
    [[1, 2],    [2],        [3],        [1, 2]],
    [[1],       [3],        [2, 3],     [3]],
    [[3],       [1],        [3],        [1, 2]]
]


class NIS_Apriori:
    def __init__(self, table, support, accurate):
        self.table = table
        self.support = support
        self.accurate = accurate
        self.element_len = len(table)
        self.feature_len = len(table[0]) - 1

        self.sup_list = []
        self.inf_list = []

        self.dict = {0: "P", 1: "Q", 2: "R", 3: "S", -1: "S"}
        self.val_list = [1, 2, 3]
        self.xi_list = [1, 2, 3]

        val_set = set([])
        for s in table:
            for value in s[-1]:
                val_set.add(value)
        self.val_list = list(val_set)
        self.val_list.sort()

        # con = numero of feature, xi = value of feature  //table[i][con] == xi
    def inf(self, condition, xi):
        numero = set([])
        for i in range(self.element_len):
            if len(self.table[i][condition]) == 1:
                if self.table[i][condition][0] == xi:
                    numero.add(i)
        return numero
        # return a set {numero_1, numero_2, ...} of element

    def sup(self, condition, xi):
        numero = set([])
        for i in range(self.element_len):
            if xi in self.table[i][condition]:
                numero.add(i)
        return numero
        # return a set {numero_1, numero_2, ...} of element

    def min_support(self, inf_c, inf_d):
        min_sup_set = inf_c & inf_d
        min_sup = len(min_sup_set)/float(self.element_len)
        return min_sup, min_sup_set

    @staticmethod
    def min_accurate(inf_c, inf_d, sup_c):
        out_acc = sup_c - inf_c - inf_d
        return len(inf_c & inf_d) / float(len(inf_c | out_acc))

    def max_support(self, sup_c, sup_d):
        max_sup_set = sup_c & sup_d
        max_sup = len(max_sup_set)/float(self.element_len)
        return max_sup, max_sup_set

    @staticmethod
    def max_accurate(inf_c, sup_c, sup_d):
        in_acc = (sup_c - inf_c) & sup_d
        return len(sup_c & sup_d) / float(len(inf_c | in_acc))

    def init_inf_sup(self):
        # inf_list[][] = set()
        for i in range(self.feature_len + 1):
            self.inf_list.append([])
            for j in self.xi_list:
                self.inf_list[i].append(self.inf(i, j))
                print("inf[%s, %d] = " % (self.dict[i], j), self.inf(i, j))

        # sup_list[][] = set()
        for i in range(self.feature_len + 1):
            self.sup_list.append([])
            for j in self.xi_list:
                self.sup_list[i].append(self.sup(i, j))
                print("sup[%s, %d] = " % (self.dict[i], j), self.sup(i, j))

    def step1(self):
        min_list_f1 = []
        for i in range(len(self.val_list)):
            min_list_f1.append([])
            for f in range(self.feature_len):
                min_list_f1[i].append([])

        max_list_f1 = copy.deepcopy(min_list_f1)

        print("\n\n\n")
        # min
        for n_i in range(len(self.val_list)):
            v_i = self.val_list[n_i]
            for n_f in range(self.feature_len):
                for n_j in range(len(self.xi_list)):
                    v_j = self.xi_list[n_j]
                    min_sup, min_sup_set = self.min_support(inf_c=self.inf_list[n_f][n_j], inf_d=self.inf_list[-1][n_i])
                    print("[%s=%d] --> [%s=%d], min_support = %f" % (self.dict[n_f], v_j, self.dict[-1], v_i, min_sup))
                    if min_sup >= self.support:
                        min_acc = self.min_accurate(inf_c=self.inf_list[n_f][n_j], inf_d=self.inf_list[-1][n_i], sup_c=self.sup_list[n_f][n_j])
                        if min_acc >= self.accurate:
                            print("!! find min_acc = %f \n" % min_acc)
                        else:
                            min_list_f1[n_i][n_f].append(n_j)
                            print("min_acc = %f \n" % min_acc)

        print("\n\n\n")
        # max
        for n_i in range(len(self.val_list)):
            v_i = self.val_list[n_i]
            for n_f in range(self.feature_len):
                for n_j in range(len(self.xi_list)):
                    v_j = self.xi_list[n_j]
                    max_sup, max_sup_set = self.max_support(sup_c=self.sup_list[n_f][n_j], sup_d=self.sup_list[-1][n_i])
                    print("[%s=%d] --> [%s=%d], max_support = %f" % (self.dict[n_f], v_j, self.dict[-1], v_i, max_sup))
                    if max_sup >= self.support:
                        max_acc = self.max_accurate(inf_c=self.inf_list[n_f][n_j], sup_c=self.sup_list[n_f][n_j], sup_d=self.sup_list[-1][n_i])
                        if max_acc >= self.accurate:
                            print("!! find max_acc = %f \n" % max_acc)
                        else:
                            max_list_f1[n_i][n_f].append(n_j)
                            print("max_acc = %f \n" % max_acc)

        print(min_list_f1)
        print(max_list_f1)

# run
n1 = NIS_Apriori(table=form, support=0.2, accurate=0.8)
n1.init_inf_sup()
n1.step1()