# Functional Dependency Analysis Tool

This Python script is a tool for analyzing functional dependencies in a relational database. It provides various functions to check for properties like closure, candidate keys, canonical covers, and normalization levels (2NF, 3NF, BCNF). Additionally, it can determine if a given decomposition of relations is lossless and dependency-preserving.

## How to Use

1. Ensure you have Python installed on your system.

2. Copy and paste the provided code into a Python (.py) file.

3. Import the required modules and use the provided functions as needed in your Python script.

### Example Usage

```python
# Example usage:
fds = [('AB','C'), ('C', 'B'), ('AB', 'B')]  # Replace with your functional dependencies
decomposition = [fds_to_items(fds)]  # Initial decomposition
print('Input:')
print(fds)

print_closure_list(fds, onlyCandidateKeys=True)
is_dependency_preserved(fds, decomposition, printDiff=True)
is_decomposition_lossless(fds, decomposition, printJoinOrder=True)
is_decomposition_2NF(fds, decomposition)
is_decomposition_3NF(fds, decomposition)
is_decomposition_BCNF(fds, decomposition)
all_canonical_cover(fds)
```

## Functions

Here is a brief description of the functions provided in the script:

1. `check_strings(list_of_strings, given_string)`: Checks if all characters in at least one string exist in the given string.

2. `fds_to_items(data)`: Converts a set of functional dependencies to a string of all the attributes in the dependencies.

3. `get_closure(attributes, fds)`: Computes the closure of a set of attributes under a set of functional dependencies.

4. `candidate_key_list(fds)`: Finds all candidate keys in a set of functional dependencies.

5. `print_closure_list(fds, onlyCandidateKeys=False)`: Prints the closure of attributes based on the given functional dependencies.

6. `isSetClosureEqual(fds1, fds2)`: Checks if the closures of two sets of functional dependencies are equal.

7. `find_canonical_cover(fds)`: Finds the canonical cover of a set of functional dependencies.

8. `clean_fds(data)`: Cleans up a set of functional dependencies by removing redundant dependencies.

9. `call_canonical_cover(fds)`: Calls `find_canonical_cover` until no further changes are made to obtain the canonical cover.

10. `all_canonical_cover(fds)`: Finds all possible canonical covers for a set of functional dependencies.

11. `subrelation_fds(fds, relation_list)`: Decomposes a set of functional dependencies based on a list of relations.

12. `is_dependency_preserved(fds, relation_list, printDiff=False)`: Checks if a given decomposition of relations preserves all functional dependencies.

13. `is_pair_lossless(fds, R1, R2)`: Checks if two relations can be joined losslessly.

14. `is_lossless(fds, notJoinedRelations, joinedAttributes, joinOrder)`: Checks if a set of relations can be joined losslessly.

15. `is_decomposition_lossless(fds, relation_list, printJoinOrder=False)`: Checks if a given decomposition of relations is lossless.

16. `prime_attributes(fds)`: Finds all prime attributes in a set of functional dependencies.

17. `is_decomposition_2NF(fds, decomposition, doPrint=True)`: Checks if a given decomposition is in 2NF.

18. `is_decomposition_3NF(fds, decomposition, doPrint=True)`: Checks if a given decomposition is in 3NF.

19. `is_decomposition_BCNF(fds, decomposition, doPrint=True)`: Checks if a given decomposition is in BCNF.

## Disclaimer

This script is a tool for educational and analytical purposes. It may not cover all edge cases, and you should thoroughly test it with your own datasets before relying on it for critical tasks.
