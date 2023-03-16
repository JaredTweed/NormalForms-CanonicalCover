from itertools import combinations, permutations

def get_closure(attributes, fds, doPrint=False):
    # Compute the closure of a set of attributes under a set of functional dependencies
    closure = set(attributes)
    changed = True
    while changed:
        changed = False
        for X, Y in fds:
            if set(X).issubset(closure):
                if not set(Y).issubset(closure):
                    closure |= set(Y)
                    changed = True
    
    if(doPrint == True):
        print('['+attributes+']+ = '+''.join(closure))
    
    return closure


def fds_to_items(data):
    letters = set()
    for item in data:
        for letter in item:
            letters.update(set(letter))
    
    return ''.join(sorted(letters))

def isSetClosureEqual(fds1, fds2):
    if(fds_to_items(fds1) != fds_to_items(fds2)): return False
    attributes = fds_to_items(fds1)
    
    
    for length in range(1, len(attributes) + 1):
        for combo in combinations(attributes, length):
            sorted_combo = "".join(sorted(combo))
            
            fds1_closure = get_closure(sorted_combo, fds1)
            fds2_closure = get_closure(sorted_combo, fds2)
            if(fds1_closure != fds2_closure): return False
    # print('closure achieved')
    return True
    

def find_canonical_cover(fds):
    # Find the canonical cover of a set of functional dependencies
    for index, (X, Y) in enumerate(fds):
        # print(X, Y)
        for A in X:
            # Check if A is extraneous
            reduced_X = X.replace(A, '')
            if(reduced_X != ''):
                reduced_fds = fds[:index] + [(reduced_X, Y)] + fds[index+1:]
            else: reduced_fds = fds[:index] + fds[index+1:]
            
            # print(fds, reduced_fds, A)

            if(isSetClosureEqual(fds, reduced_fds) == True):
                fds = reduced_fds
                return False, fds
                
        for A in Y:
            # Check if A is extraneous
            reduced_Y = Y.replace(A, '')
            if(reduced_Y != ''):
                reduced_fds = fds[:index] + [(X, reduced_Y)] + fds[index+1:]
            else: reduced_fds = fds[:index] + fds[index+1:]
            
            # print(fds, reduced_fds, A)

            if(isSetClosureEqual(fds, reduced_fds) == True):
                fds = reduced_fds
                return False, fds
    return True, fds

def call_canonical_cover(fds):
    fds_list = []
    print(fds)
        
    for permutation in permutations(fds):
        perm = list(permutation)
        isFinished = False
        while (isFinished == False):
            isFinished, fds = find_canonical_cover(perm)
        fds.sort()
        # if(fds not in fds_list):
        #     fds_list.append(fds)
    return fds
    

# Example usage:
# fds = [('AB', 'C'), ('C', 'D'), ('BD', 'E'), ('E', 'A'), ('A','C')]
# fds = [('A','BC'), ('B','C'), ('A','B'), ('AB','C')]
# https://www.tutorialspoint.com/find-the-canonical-cover-of-fd-a-bc-b-ac-c-ab-in-dbms
fds = [('A', 'B'), ('A','C'), ('B','A'), ('B','C'), ('C', 'A'), ('C', 'B')]
canonical_cover = call_canonical_cover(fds)
print(canonical_cover)
get_closure('A', fds, doPrint=True)
get_closure('B', fds, doPrint=True)
get_closure('C', fds, doPrint=True)
canonical_cover = call_canonical_cover(canonical_cover)
canonical_cover.sort(key=lambda a: a[1])
print(canonical_cover)

print(canonical_cover)
