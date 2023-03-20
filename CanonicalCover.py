from itertools import combinations, permutations
from collections import defaultdict

def check_strings(list_of_strings, given_string):
    for string in list_of_strings:
        if set(string).issubset(set(given_string)):
            # All characters in at least one string exist in the given string.
            return True
    return False

def fds_to_items(data):
    # Convert a set of functional dependencies to a string of all the attributes in the dependencies
    letters = set()
    for item in data:
        for letter in item:
            letters.update(set(letter))
    
    # Return the sorted string of attributes
    return ''.join(sorted(letters))

def get_closure(attributes, fds):
    # Compute the closure of a set of attributes under a set of functional dependencies
    
    # Set the closure to the original set of sorted attributes
    attributes = ''.join(sorted(attributes))
    closure = set(attributes)
    changed = True
    
    # Repeat until the closure no longer changes
    while changed:
        changed = False
        # For each functional dependency in the set
        for X, Y in fds:
            # If the left-hand side of the dependency is a subset of the current closure
            if set(X).issubset(closure):
                # If the right-hand side is not already in the closure
                if not set(Y).issubset(closure):
                    # Add the right-hand side to the closure and mark that the closure has changed
                    closure |= set(Y)
                    changed = True
    
    # Return the final closure
    return closure
    
def print_closure_list(fds, onlyCandidateKeys=False):
    print('---\nClosure:')
    candidateKeyList = []
    for length in range(1, len(fds_to_items(fds)) + 1):
        for i in combinations(fds_to_items(fds), length):
            attributes = "".join(sorted(i))
            
            closure = get_closure(attributes, fds)
            
            # Print the closure
            if(onlyCandidateKeys == False):
                print('['+attributes+']⁺ = '+''.join(sorted(closure)))
            elif(''.join(sorted(closure)) == fds_to_items(fds) and check_strings(candidateKeyList, attributes) == False):
                print('['+attributes+']⁺ = '+''.join(sorted(closure)))
                candidateKeyList.append(str(attributes))

def isSetClosureEqual(fds1, fds2):
    # Check if the closures of two sets of functional dependencies are equal
    if(fds_to_items(fds1) != fds_to_items(fds2)): return False
    attributes = fds_to_items(fds1)
    
    # For each subset of attributes, compute the closure using both sets of dependencies
    for length in range(1, len(attributes) + 1):
        for combo in combinations(attributes, length):
            sorted_combo = "".join(sorted(combo))
            
            fds1_closure = get_closure(sorted_combo, fds1)
            fds2_closure = get_closure(sorted_combo, fds2)
            
            # If the closures are not equal, return False
            if(fds1_closure != fds2_closure): return False
    
    # Otherwise, return True
    return True
    

def find_canonical_cover(fds):
    # Loop through each functional dependency in fds and check if the left-hand side (LHS) or right-hand side (RHS) has an extraneous attribute.
    for index, (X, Y) in enumerate(fds):
        for A in X:
            # Check if attribute A in the LHS of the FD is extraneous
            reduced_X = X.replace(A, '') # remove attribute A from the LHS
            if reduced_X != '':
                reduced_fds = fds[:index] + [(reduced_X, Y)] + fds[index+1:] # create a new set of FDs without the FD (X -> Y) and add the reduced FD (reduced_X -> Y)
            else:
                reduced_fds = fds[:index] + fds[index+1:] # create a new set of FDs without the FD (X -> Y)
            
            # Check if the closure of the new set of FDs is the same as that of the original set of FDs
            if isSetClosureEqual(fds, reduced_fds) == True:
                fds = reduced_fds
                return False, fds # if the closure is the same, the FD (X -> Y) is redundant and can be removed from the set of FDs
        
        for A in Y:
            # Check if attribute A in the RHS of the FD is extraneous
            reduced_Y = Y.replace(A, '') # remove attribute A from the RHS
            if reduced_Y != '':
                reduced_fds = fds[:index] + [(X, reduced_Y)] + fds[index+1:] # create a new set of FDs without the FD (X -> Y) and add the reduced FD (X -> reduced_Y)
            else:
                reduced_fds = fds[:index] + fds[index+1:] # create a new set of FDs without the FD (X -> Y)
            
            # Check if the closure of the new set of FDs is the same as that of the original set of FDs
            if isSetClosureEqual(fds, reduced_fds) == True:
                fds = reduced_fds
                return False, fds # if the closure is the same, the FD (X -> Y) is redundant and can be removed from the set of FDs
    
    return True, fds # if no extraneous attribute was found in any of the FDs, the set of FDs is the canonical cover

def clean_fds(data):
    d = defaultdict(list)

    # Group the data based on the first element of each tuple
    for key, value in data:
        key = ''.join(sorted(key))
        value = ''.join(sorted(value))
        d[key].append(value)

    # Merge the values of each group into a single string
    result = [(key, ''.join(sorted(set(values)))) for key, values in d.items()]

    # Sort the result based on the first element of each tuple
    result = sorted(result, key=lambda x: x[0])

    return result

def call_canonical_cover(fds):
    # Call the find_canonical_cover function until no further changes are made
    isFinished = False
    while (isFinished == False):
        isFinished, fds = find_canonical_cover(fds)
    fds = clean_fds(fds)
    fds.sort()
    return fds
    
def all_canonical_cover(fds):
    print('---\nAll Canonical Covers:')
    # Find all possible canonical covers for a set of functional dependencies
    fds_list = []
    for permutation in permutations(fds):
        perm = list(permutation)
        cover = call_canonical_cover(perm)
        if(cover not in fds_list):
            print(cover)
            fds_list.append(cover)
            
def is_dependency_preserved(fds, relation_list, printDiff=False):
    print('---\nDependencies Preservation:')
    relation_dep_set_list = []
    relation_dep_set_print_list = []
    for R in relation_list:
        relation_dep_set = []
        # Find the closure for each combination of elements in the sub-relation
        for length in range(1, len(R) + 1):
            for i in combinations(R, length):
                attributes = "".join(sorted(i))

                # Create the subrelation functional dependency set
                rhs = ''.join(sorted((get_closure(attributes, fds) & set(R)) - set(attributes)))
                if(rhs != ''): relation_dep_set.append((attributes, rhs))
        relation_dep_set = call_canonical_cover(relation_dep_set)
        relation_dep_set_list = relation_dep_set_list + relation_dep_set
        relation_dep_set_print_list.append(relation_dep_set)

    # Check whether closure of fds == relation_dep_set_list
    isPreserved = True
    relation_unequal_closure_list = []
    for X, Y in fds:
        # we only need to check the closure of the original determinant attributes
        attributes = "".join(sorted(set(X)))
    
        fds_closure = get_closure(attributes, fds)
        relation_closure = get_closure(attributes, relation_dep_set_list)
        if(fds_closure != relation_closure):
            if(isPreserved == True): 
                print('The sub-relations do not preserve all the dependencies.')
                print(relation_dep_set_print_list)
                if(printDiff == True): print('The unequal closures are shown below.\nOriginal Closure:')
                isPreserved = False
            if(printDiff == True): 
                print('['+attributes+']⁺ = '+''.join(sorted(fds_closure)))
                relation_unequal_closure_list.append('['+attributes+']⁺ = '+''.join(sorted(relation_closure)))
                
    if(isPreserved == True): print('The sub-relations preserved all the dependencies.')
    elif(printDiff == True): 
        print('Relation Closure:')
        for c in relation_unequal_closure_list:
            print(c)
    return isPreserved
        

# Example usage:
# fds = [('AB', 'C'), ('C', 'D'), ('BD', 'E'), ('E', 'A'), ('A','C')]
# fds = [('A','BC'), ('B','C'), ('A','B'), ('AB','C')]
# fds = [('A', 'B'), ('A','C'), ('B','A'), ('B','C'), ('C', 'A'), ('C', 'B')]
fds = [('AB', 'C'), ('C', 'E'), ('B','D'), ('E','A')]
print('Input:')
print(fds)

print_closure_list(fds, onlyCandidateKeys=True)
is_dependency_preserved(fds, ['BCD', 'ACE'], printDiff=True)
all_canonical_cover(fds)
