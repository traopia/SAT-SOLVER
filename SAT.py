import random
import time
import copy
import operator
import os
import csv
import itertools

def SAT(file,rules,heuristic):
    def read_dimac(file):
        f = open(file, "r")
        f1 = f.readlines()
        # https://stackoverflow.com/questions/28890268/parse-dimacs-cnf-file-python
        cnf = list()
        cnf.append(list())

        for line in f1:
            tokens = line.split()
            if len(tokens) != 0 and tokens[0] not in ("p", "c"):
                for tok in tokens:
                    lit = int(tok)
                    if lit == 0:
                        cnf.append(list())
                    else:
                        cnf[-1].append(lit)
        assert len(cnf[-1]) == 0
        cnf.pop()
        return cnf

    def remove_given(file, cnf):
        f = read_dimac(file)
        for j in range(len(f)):

            for i in range(len(cnf) - 1, -1, -1):
                if f[j][0] in cnf[i]:
                    del cnf[i]
                else:
                    if -(f[j][0]) in cnf[i]:
                        cnf[i].remove(-(f[j][0]))
        return cnf

    def check_unit_clause(cnf, dict_values):
        for clause in cnf:
            if len(clause) == 1:
                for i in clause:
                    if i not in dict_values:
                        dict_values[i] = 1
                        dict_values[-i] = 0
        return cnf, dict_values

    def remove(cnf, dict_values):
        # cnf2=copy.deepcopy(cnf)
        for clause in cnf:
            rem_clause = False
            for i in clause:
                if i in dict_values and dict_values[i] == 1:
                    rem_clause = True
                    continue
            if rem_clause:
                cnf.remove(clause)
        cnf2 = copy.deepcopy(cnf)
        for clause in cnf2:
            clause_index = cnf.index(clause)
            for i in clause:
                if i in dict_values and dict_values[i] == 0:
                    cnf[clause_index].remove(i)
        return cnf

    def SIMPLIFY(cnf, dict_values):
        count = 0
        previous_count = None
        while count != previous_count:
            previous_count = count
            # cnf = remove_false_elements(cnf, dict_values)
            cnf = remove(cnf, dict_values)
            cnf, dict_values = check_unit_clause(cnf, dict_values)
            count = len(cnf)
        return cnf, dict_values

    # RANDOM
    def random_selection(list_of_lists):
        clause = list_of_lists[random.randint(0, len(list_of_lists) - 1)]
        element = clause[random.randint(0, len(clause) - 1)]
        return element

    def dp_algorithm_ran(list_of_lists, dict_of_answers, counter, switch_counter, up_counter):
        if list_of_lists == []:
            return True, dict_of_answers, counter, switch_counter, up_counter
        elif [] in list_of_lists:
            return False, None, counter, switch_counter, up_counter

        new_element = random_selection(list_of_lists)
        counter += 1
        new_lol = copy.deepcopy(list_of_lists)
        new_doa = copy.deepcopy(dict_of_answers)
        new_doa[new_element] = 1
        new_doa[-new_element] = 0
        new_lol, new_doa = SIMPLIFY(new_lol, new_doa)

        sat, new_dict, counter, switch_counter, up_counter = dp_algorithm_ran(new_lol, new_doa, counter,
                                                                              switch_counter, up_counter)
        if sat:
            return sat, new_dict, counter, switch_counter, up_counter

        new_lol = copy.deepcopy(list_of_lists)
        new_doa = copy.deepcopy(dict_of_answers)
        new_doa[new_element] = 0
        new_doa[-new_element] = 1
        new_lol, new_doa = SIMPLIFY(new_lol, new_doa)
        switch_counter += 1

        sat, new_dict, counter, switch_counter, up_counter = dp_algorithm_ran(new_lol, new_doa, counter,
                                                                              switch_counter, up_counter)
        if sat:
            return sat, new_dict, counter, switch_counter, up_counter
        return False, None, counter, switch_counter, up_counter + 1

    def do_ran(pathname):
        start = time.time()
        up = 0
        new_val_counter = 0
        switch = 0
        answer = []
        dict_values = dict()
        list_random_filled = []
        cnf = read_dimac(rules)
        num_given = remove_given(pathname, cnf)
        base = os.path.basename(pathname)
        puzzle = base.strip('.txt')
        cnf, dict_values = SIMPLIFY(cnf, dict_values)
        if [] in cnf:
            sat = False
        else:
            sat, dict_values, new_val_counter, switch, up = dp_algorithm_ran(cnf, dict_values, new_val_counter,
                                                                             switch, up)
        if sat:
            result = []
            for k, v in dict_values.items():
                if v == 1:
                    result.append(k)
                if v == 0:
                    result.append(-k)

            given = list(itertools.chain(*(read_dimac(pathname))))

            result.extend(given)
            result.sort()
            result = list(set(result))

            res = []
            for i in result:
                res.append([i])

            return res
            # puzzle, num_given, 'SAT', 'Random', new_val_counter, switch, up, time.time() - start
        else:
            return 'UNSAT'
            # puzzle, num_given, 'UNSAT', 'Random', None, None, None, time.time() - start

    # DLCS
    def DLCS(list_of_lists):
        d = {}
        clauses = list_of_lists
        for item in clauses:
            for j in item:
                if j > 0:
                    d[j] = []
        for k in d.keys():
            j_neg = 0
            j_pos = 0
            for c in clauses:
                if k in c:
                    j_pos += 1

                if -k in c:
                    j_neg += 1
            d[k] = [j_pos + j_neg, j_pos, j_neg]
        winner = max(d, key=d.get)
        if d[winner][1] > d[winner][2]:
            p = winner
        else:
            p = -winner
        return p

    def dp_algorithm_dlcs(list_of_lists, dict_of_answers, counter, switch_counter, up_counter):
        if list_of_lists == []:
            return True, dict_of_answers, counter, switch_counter, up_counter
        elif [] in list_of_lists:
            return False, None, counter, switch_counter, up_counter
        new_element = DLCS(list_of_lists)
        counter += 1
        new_lol = copy.deepcopy(list_of_lists)
        new_doa = copy.deepcopy(dict_of_answers)
        new_doa[new_element] = 1
        new_doa[-new_element] = 0
        new_lol, new_doa = SIMPLIFY(new_lol, new_doa)

        sat, new_dict, counter, switch_counter, up_counter = dp_algorithm_dlcs(new_lol, new_doa, counter,
                                                                               switch_counter, up_counter)
        if sat:
            return sat, new_dict, counter, switch_counter, up_counter

        new_lol = copy.deepcopy(list_of_lists)
        new_doa = copy.deepcopy(dict_of_answers)
        new_doa[new_element] = 0
        new_doa[-new_element] = 1
        new_lol, new_doa = SIMPLIFY(new_lol, new_doa)
        switch_counter += 1

        sat, new_dict, counter, switch_counter, up_counter = dp_algorithm_dlcs(new_lol, new_doa, counter,
                                                                               switch_counter, up_counter)
        if sat:
            return sat, new_dict, counter, switch_counter, up_counter
        return False, None, counter, switch_counter, up_counter + 1

    def do_dlcs(pathname):
        start = time.time()
        up = 0
        new_val_counter = 0
        switch = 0
        answer = []
        dict_values = dict()
        list_random_filled = []
        cnf = read_dimac(rules)
        num_given = remove_given(pathname, cnf)
        base = os.path.basename(pathname)
        puzzle = base.strip('.txt')
        cnf, dict_values = SIMPLIFY(cnf, dict_values)
        if [] in cnf:
            sat = False
        else:
            sat, dict_values, new_val_counter, switch, up = dp_algorithm_dlcs(cnf, dict_values, new_val_counter,
                                                                              switch, up)
        if sat:
            result = []
            for k, v in dict_values.items():
                if v == 1:
                    result.append(k)
                if v == 0:
                    result.append(-k)

            given = list(itertools.chain(*(read_dimac(pathname))))

            result.extend(given)
            result.sort()
            result = list(set(result))

            res = []
            for i in result:
                res.append([i])

            return res
            # puzzle, num_given, 'SAT', 'Dynamic largest individual sum', new_val_counter, switch, up, time.time() - start
        else:
            return 'UNSAT'
            # puzzle, num_given, 'UNSAT', 'Dynamic largest individual sum', None, None, None, time.time() - start

    # JW
    def two_sided_jeroslow_wang(list_of_lists):
        d = dict()
        d_polar = dict()
        for clause in list_of_lists:
            for element in clause:
                if element in d:
                    d[abs(element)] += 2 ** -abs(len(clause))
                    d_polar[element] += 2 ** -abs(len(clause))
                else:
                    d[abs(element)] = 2 ** -abs(len(clause))
                    d_polar[element] = 2 ** -abs(len(clause))
        positive = max(d.items(), key=operator.itemgetter(1))[
            0]  # https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
        negative = -positive
        if negative not in d_polar:
            return positive
        elif positive not in d_polar:
            return negative
        elif d_polar[positive] >= d_polar[negative]:
            return positive
        else:
            return negative

    def dp_algorithm_jw(list_of_lists, dict_of_answers, counter, switch_counter, up_counter):
        if list_of_lists == []:
            return True, dict_of_answers, counter, switch_counter, up_counter
        elif [] in list_of_lists:
            return False, None, counter, switch_counter, up_counter

        new_element = two_sided_jeroslow_wang(list_of_lists)
        counter += 1
        new_lol = copy.deepcopy(list_of_lists)
        new_doa = copy.deepcopy(dict_of_answers)
        new_doa[new_element] = 1
        new_doa[-new_element] = 0
        new_lol, new_doa = SIMPLIFY(new_lol, new_doa)

        sat, new_dict, counter, switch_counter, up_counter = dp_algorithm_jw(new_lol, new_doa, counter,
                                                                             switch_counter, up_counter)
        if sat:
            return sat, new_dict, counter, switch_counter, up_counter

        new_lol = copy.deepcopy(list_of_lists)
        new_doa = copy.deepcopy(dict_of_answers)
        new_doa[new_element] = 0
        new_doa[-new_element] = 1
        new_lol, new_doa = SIMPLIFY(new_lol, new_doa)
        switch_counter += 1
        sat, new_dict, counter, switch_counter, up_counter = dp_algorithm_jw(new_lol, new_doa, counter,
                                                                             switch_counter, up_counter)
        if sat:
            return sat, new_dict, counter, switch_counter, up_counter
        return False, None, counter, switch_counter, up_counter + 1

    def do_jw(pathname):
        start = time.time()
        up = 0
        new_val_counter = 0
        switch = 0
        answer = []
        dict_values = dict()
        list_random_filled = []
        cnf = read_dimac(rules)
        num_given = remove_given(pathname, cnf)
        base = os.path.basename(pathname)
        puzzle = base.strip('.txt')
        cnf, dict_values = SIMPLIFY(cnf, dict_values)
        if [] in cnf:
            sat = False
        else:
            sat, dict_values, new_val_counter, switch, up = dp_algorithm_jw(cnf, dict_values, new_val_counter, switch,
                                                                            up)
        if sat:
            result = []
            for k, v in dict_values.items():
                if v == 1:
                    result.append(k)
                if v == 0:
                    result.append(-k)

            # given = chain.from_iterable(read_dimac(pathname))
            given = list(itertools.chain(*(read_dimac(pathname))))

            result.extend(given)
            result.sort()
            result = list(set(result))

            res = []
            for i in result:
                res.append([i])

            return res
            # puzzle, num_given, 'SAT', 'Two-Sided Jeroslow-Wang', new_val_counter, switch, up, time.time() - start
        else:
            return 'UNSAT'
            # puzzle, num_given, 'UNSAT', 'Two-Sided Jeroslow-Wang', None, None, None, time.time() - start


    output= open(file+"out.csv", 'w', newline='')
    if heuristic==1: data = do_ran(file)
    if heuristic==2: data=do_dlcs(file)
    if heuristic == 3: data = do_jw(file)
    with output:
        write = csv.writer(output)
        write.writerows(data)
    output.close()


SAT("escargot.txt","sudoku-rules.txt",1)