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
                
    if(isPreserved == True): 
        print('The sub-relations preserved all the dependencies.\nSub-relation functional dependencies below:')
        print(relation_dep_set_print_list)
    elif(printDiff == True): 
        print('Relation Closure:')
        for c in relation_unequal_closure_list:
            print(c)
    return isPreserved
        
# Check if R1 and R2 are pair lossless with respect to fds
def is_pair_lossless(fds, R1, R2):
    intersection = set(R1) & set(R2)
    intersection_closure = get_closure("".join(sorted(intersection)), fds)
    # If either R1 or R2 is a subset of the intersection closure, then the pair is lossless
    if(set(R1).issubset(intersection_closure) or set(R2).issubset(intersection_closure)):
        return True
    else: return False
    
# Check if the given set of relations (notJoinedRelations) can be joined losslessly
# joinedAttributes are the set of joined attributes so far
# joinOrder keeps track of the order in which the relations are joined
def is_lossless(fds, notJoinedRelations, joinedAttributes, joinOrder):
    output = False
    # If all relations have been joined, return True
    if(len(notJoinedRelations) == 0): return True
    # Try joining each relation in notJoinedRelations with joinedAttributes to see if it is a lossless pair
    for R in notJoinedRelations:
        if(is_pair_lossless(fds, joinedAttributes, R)):
            notJoinedRelations.remove(R)
            joinedAttributes = joinedAttributes | set(R)
            # recursively check if the remaining relations can be joined losslessly
            output = is_lossless(fds, notJoinedRelations, joinedAttributes, joinOrder)
            if(output == True): joinOrder.insert(0, R)
            return output, joinOrder
    return output, joinOrder

# Check if a given decomposition of relations is lossless
def is_decomposition_lossless(fds, relation_list, printJoinOrder=False):
    print('---\nCheck For Losslessness:')
    isLossless = False
    joinOrder = []
    
    # Try joining each pair of relations to see if the decomposition is lossless
    for R_pair in combinations(relation_list, 2):
        notJoinedRelations = set(relation_list)
        R_pair_l = list(R_pair)
        # If the pair is pair lossless, join them and then recursively check if the remaining relations can be joined losslessly
        if(is_pair_lossless(fds, R_pair_l[0], R_pair_l[1])):
            notJoinedRelations.remove(R_pair_l[0])
            notJoinedRelations.remove(R_pair_l[1])
            joinedAttributes = set(R_pair_l[0]) | set(R_pair_l[1])
            if(len(notJoinedRelations) != 0):
                output, joinOrder = is_lossless(fds, notJoinedRelations, joinedAttributes, joinOrder)
                if(output == True):
                    # If the decomposition is lossless, update joinOrder and set isLossless to True
                    joinOrder.insert(0, R_pair_l[1])
                    joinOrder.insert(0, R_pair_l[0])
                    isLossless = True
                    break
            else: 
                # If all relations have been joined and the decomposition is lossless, update joinOrder and set isLossless to True
                joinOrder.insert(0, R_pair_l[1])
                joinOrder.insert(0, R_pair_l[0])
                isLossless = True
                break
    if(isLossless == False): print('The decomposition is lossy.')
    elif(printJoinOrder):
        print('The decomposition is lossless.')
        print('Relation join order:')
        for i,R in enumerate(joinOrder):
            print(str(i+1)+'. '+R)
                
    

# Example usage:
# fds = [('AB', 'C'), ('C', 'D'), ('BD', 'E'), ('E', 'A'), ('A','C')]
# fds = [('A','BC'), ('B','C'), ('A','B'), ('AB','C')]
# fds = [('A', 'B'), ('A','C'), ('B','A'), ('B','C'), ('C', 'A'), ('C', 'B')]
# fds = [('AB', 'C'), ('C', 'E'), ('B','D'), ('E','A')] # ['BCD', 'ACE'] dependency preservation example
# fds = [('AB', 'C'),('C', 'D'),('D', 'EF'),('F', 'A'),('D', 'B')] # ['ABC', 'CDE', 'EF'] is lossy
fds = [('AB', 'C'),('C', 'D'),('D', 'EF'),('F', 'A'),('D', 'B'),('E', 'F')] # ['ABC', 'CDE', 'EF'] is lossless
print('Input:')
print(fds)

print_closure_list(fds, onlyCandidateKeys=True)
is_dependency_preserved(fds, ['ABC', 'CDE', 'EF'], printDiff=True)
is_decomposition_lossless(fds, ['ABC', 'CDE', 'EF'], printJoinOrder=True)
all_canonical_cover(fds)
