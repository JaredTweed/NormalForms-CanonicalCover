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

def candidate_key_list(fds):
    fdsItems = fds_to_items(fds)
    candidateKeyList = []
    for length in range(1, len(fdsItems) + 1):
        for i in combinations(fdsItems, length):
            attributes = "".join(sorted(i))
            
            closure = get_closure(attributes, fds)
            
            # Append list if the attributes are a candidate key
            if(''.join(sorted(closure)) == fdsItems and check_strings(candidateKeyList, attributes) == False):
                candidateKeyList.append(str(attributes))
    return candidateKeyList

def print_closure_list(fds, onlyCandidateKeys=False):
    print('---\nClosure:')
    fdsItems = fds_to_items(fds)
    if(onlyCandidateKeys == False):
        for length in range(1, len(fdsItems) + 1):
            for i in combinations(fdsItems, length):
                attributes = "".join(sorted(i))
                closure = get_closure(attributes, fds)
                
                # Print the closure
                print('['+attributes+']⁺ = '+''.join(sorted(closure)))
    else:
        candidateKeyList = candidate_key_list(fds)
        for attributes in candidateKeyList:
            print('['+attributes+']⁺ = '+fdsItems)

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
            
def subrelation_fds(fds, relation_list):
    if(len(relation_list) == 1): return [fds]
    
    relation_dep_set_list = []
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
        # relation_dep_set may be empty, and that is okay
        relation_dep_set_list.append(relation_dep_set)
    return relation_dep_set_list

def is_dependency_preserved(fds, relation_list, printDiff=False):
    print('---\nDependencies Preservation:')
    if(len(relation_list) == 1): 
        print('All dependencies are preserved because no decomposition occured.')
        return True
    
    # Find the preserved subrelation dependencies
    relation_dep_set_print_list = subrelation_fds(fds, relation_list)
    relation_dep_set_list = []
    for sublist in relation_dep_set_print_list:
        relation_dep_set_list.extend(sublist)
    print(relation_dep_set_list)

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
    return set(R1).issubset(intersection_closure) or set(R2).issubset(intersection_closure)
    
# Check if the given set of relations (notJoinedRelations) can be joined losslessly
# joinedAttributes are the set of joined attributes so far
# joinOrder keeps track of the order in which the relations are joined
def is_lossless(fds, notJoinedRelations, joinedAttributes, joinOrder):
    # If all relations have been joined, return True
    if(len(notJoinedRelations) == 0): return True, joinOrder
    
    # Try joining each relation in notJoinedRelations with joinedAttributes to see if it is a lossless pair
    for R in notJoinedRelations:
        if(is_pair_lossless(fds, joinedAttributes, R)):
            # Iterate over a copy to avoid modification issues
            newNotJoined = notJoinedRelations.copy()
            newNotJoined.remove(R)
            newJoinedAttributes = joinedAttributes | set(R)
            newJoinOrder = joinOrder + [R]

            # recursively check if the remaining relations can be joined losslessly
            output, newJoinOrder = is_lossless(fds, newNotJoined, newJoinedAttributes, newJoinOrder)
            if output: return True, newJoinOrder  # Return immediately if a lossless join is found
    return False, joinOrder

# Check if a given decomposition of relations is lossless
def is_decomposition_lossless(fds, relation_list, printJoinOrder=False):
    print('---\nCheck For Losslessness:')
    
    notJoinedRelations = set(relation_list)
    joinedAttributes = set()
    output, joinOrder = is_lossless(fds, notJoinedRelations, joinedAttributes, [])
        
    # Printing the results
    if output:
        print('The decomposition is lossless.')
        if printJoinOrder:
            print('Relation join order:')
            alreadyJoinedAttrs = set()
            for i in range(len(joinOrder)-1):
                alreadyJoinedAttrs.update(joinOrder[i])  # Update with attributes from the current relation
                intersection = alreadyJoinedAttrs & set(joinOrder[i+1])
                intersection_closure = get_closure("".join(sorted(intersection)), fds)
                # Convert alreadyJoinedAttrs to a sorted list for printing
                alreadyJoinedAttrs_sorted = ''.join(sorted(alreadyJoinedAttrs))
                nextRelation_sorted = ''.join(sorted(joinOrder[i+1]))
                print(f'{alreadyJoinedAttrs_sorted} + {nextRelation_sorted} -> {"".join(sorted(alreadyJoinedAttrs | set(joinOrder[i+1])))}: [{"".join(sorted(intersection))}]⁺ = {"".join(sorted(intersection_closure))}')
                alreadyJoinedAttrs.update(joinOrder[i+1])  # Update with attributes from the next relation
        return True

    print('The decomposition is lossy.')
    return False

def prime_attributes(fds):
    candidateKeys = candidate_key_list(fds)
    
    # create a set to hold the prime_attributes
    prime_attributes = set()
    
    # loop over each string in the list and add its letters to the set
    for keys in candidateKeys:
        for attribute in keys:
            prime_attributes.add(attribute)
    
    # convert the set back to a string, sort it, and return it
    return ''.join(sorted(prime_attributes))
    

def is_decomposition_2NF(fds, decomposition, doPrint=True):
    if(doPrint): print('---\n2NF:')
    non_2NF_relations = []
    decomposition_fds = subrelation_fds(fds, decomposition)
    for i, R_fds in enumerate(decomposition_fds):
        prime_attribute_list = prime_attributes(R_fds)
        is_R_2NF = True
        for X, Y in decomposition_fds[i]:
            # Perform the test if any attribute in Y is non-prime
            nonprimeY = []
            for attribute in Y:
                if (attribute not in prime_attribute_list):
                    nonprimeY.append(attribute)
            if(nonprimeY == []): 
                continue
            
            # Check if the set of attributes in X is a proper subset of any candidate key
            properSubsets = set()
            for key in candidate_key_list(decomposition_fds[i]):
                if set(X).issubset(set(key)) and set(X) != set(key):
                    properSubsets.add(key)
                    is_R_2NF = False
            
            # Print
            if(doPrint and is_R_2NF == False): print(f"{decomposition[i]} is not in 2NF because '{X}' is a proper subset of the candidate keys in '{properSubsets}'.")    
        
        if(not is_R_2NF): non_2NF_relations.append(decomposition[i])
        if(is_R_2NF and doPrint): print(f"{decomposition[i]} is in 2NF.")
    return non_2NF_relations

def is_decomposition_3NF(fds, decomposition, doPrint=True): # new version
    if(doPrint): print('---\n3NF:\nIn 3NF, non-trivial dependencies must either have a superkey on the LHS or only non-prime attributes on the RHS.')
    
    non_3NF_relations = []
    decomposition_fds = subrelation_fds(fds, decomposition)
    for i, R_fds in enumerate(decomposition_fds):
        is_R_3NF = True
        R_fdsItems = fds_to_items(R_fds)
        primes = prime_attributes(R_fds)
        for X, Y in decomposition_fds[i]:
            # functional dependency is 3NF if trivial
            if(set(Y).issubset(X)): continue
            
            # functional dependency is 3NF if X is a superkey
            if(''.join(sorted(get_closure(X, R_fds))) == R_fdsItems): 
                # print(X, Y, ''.join(sorted(get_closure(X, R_fds))))
                continue
            
            # functional dependency is 3NF if Y is prime
            nonprimeY_list = []
            for y in Y:
                if(y not in primes): nonprimeY_list.append(y)
            if(nonprimeY_list == []): continue
        
            is_R_3NF = False
            if(len(nonprimeY_list) > 1): print(R_fdsItems+' is not in 3NF because ['+X+']⁺ = '+''.join(sorted(get_closure(X, R_fds)))+' and '+''.join(sorted(nonprimeY_list))+' are non-prime, and '+f"{X}->{Y} is in "+R_fdsItems+'.')
            else: print(R_fdsItems+' is not in 3NF because ['+X+']⁺ = '+''.join(sorted(get_closure(X, R_fds)))+' and '+''.join(sorted(nonprimeY_list))+' is non-prime, and '+f"{X}->{Y} is in "+R_fdsItems+'.')
            
        if(not is_R_3NF): non_3NF_relations.append(decomposition[i])
        if(is_R_3NF and doPrint): print(f"{decomposition[i]} is in 3NF.")
    return non_3NF_relations
    
def is_decomposition_BCNF(fds, decomposition, doPrint=True):
    if(doPrint): print('---\nBCNF:\nIn BCNF, non-trivial dependencies must have a superkey on the LHS.')
    
    non_BCNF_relations = []
    decomposition_fds = subrelation_fds(fds, decomposition)
    for i, R_fds in enumerate(decomposition_fds):
        is_R_BCNF = True
        R_fdsItems = fds_to_items(R_fds)
        for X, Y in decomposition_fds[i]:
            # functional dependency is BCNF if trivial
            if(set(Y).issubset(X)): continue
        
            # functional dependency is BCNF if X is a superkey
            if(''.join(sorted(get_closure(X, R_fds))) == R_fdsItems): 
                continue
        
            is_R_BCNF = False
            print(R_fdsItems+' is not in BCNF because ['+X+']⁺ = '+''.join(sorted(get_closure(X, R_fds)))+', and '+f"{X}->{Y} is in "+R_fdsItems+'.')
            
        if(not is_R_BCNF): non_BCNF_relations.append(decomposition[i])
        if(is_R_BCNF and doPrint): print(f"{decomposition[i]} is in BCNF.")
    return non_BCNF_relations

# Example usage:
# fds = [('AB', 'C'), ('C', 'D'), ('BD', 'E'), ('E', 'A'), ('A','C')]
# fds = [('A','BC'), ('B','C'), ('A','B'), ('AB','C')]
# fds = [('A', 'B'), ('A','C'), ('B','A'), ('B','C'), ('C', 'A'), ('C', 'B')]
# fds = [('AB', 'C'), ('C', 'E'), ('B','D'), ('E','A')] # ['BCD', 'ACE'] dependency preservation example
# fds = [('AB', 'C'),('C', 'D'),('D', 'EF'),('F', 'A'),('D', 'B')] # ['ABC', 'CDE', 'EF'] is lossy
# fds = [('AB', 'C'),('C', 'D'),('D', 'EF'),('F', 'A'),('D', 'B'),('E', 'F')] # ['ABC', 'CDE', 'EF'] is lossless
# fds = [('A','B'), ('AB', 'CDE')] # [fds_to_items(fds)] should be in 3NF & BCNF
# fds = [('BC','D'), ('AC', 'BE'), ('B', 'E')] # [fds_to_items(fds)] should not be in 3NF nor BCNF
fds = [('AB','C'), ('C', 'B'), ('AB', 'B')] # [fds_to_items(fds)] should be in 3NF but not BCNF
print('Input:')
print(fds)

decomposition = [fds_to_items(fds)]
print(decomposition)

print_closure_list(fds, onlyCandidateKeys=True)
is_dependency_preserved(fds, decomposition, printDiff=True)
is_decomposition_lossless(fds, decomposition, printJoinOrder=True)
is_decomposition_2NF(fds, decomposition)
is_decomposition_3NF(fds, decomposition)
is_decomposition_BCNF(fds, decomposition)
all_canonical_cover(fds)
