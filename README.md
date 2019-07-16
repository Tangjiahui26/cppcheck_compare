# cppcheck_compare

## cppcheck
 - A static analysis tool for C/C++ code
 - To detect bugs, undefined behaviors and dangerous coding constructs

```
[cppcheck/bad_example/array_index_out_of_bounds.cpp:6]: (error) Array 'a[2]' accessed at index 2, which is out of bounds.
[cppcheck/bad_example/assignment_address_to_integer.cpp:3]: (portability) Assigning a pointer to an integer is not portable.
[cppcheck/bad_example/auto_variables.cpp:4]: (error) Address of local auto-variable assigned to a function parameter.
[cppcheck/bad_example/buffer_access_out_of_bounds.cpp:6]: (error) Array 'a[2]' accessed at index 2, which is out of bounds.
```

## diff
- Linux command line tool to find differences between files

## problem
- Line numbers will be changed after modifying the codes, so diff does not work so well.

![](https://github.com/Tangjiahui26/cppcheck_compare/blob/master/fig/problem.png)

## solution
- Write a Python script to solve the problem of line number changes. The workflow is as follows:
    1. Checkout all the files in branch1 and branch2 to a temporary location
    2. Execute cppcheck on both checked out branches and save the results
    3. Parse data from the cppcheck output, then re-write it to new files without line numbers using Regex
    4. Execute diff on the new output files and save the diff result
    5. Re-write the diff result with the original line numbers
    6. Save the output to a local file 
    7. Delete all temporary files created
    
## Usage

```
Python cppcheck_compare.py <branch1> <branch2> <save path>
```
    
## Result

![](https://github.com/Tangjiahui26/cppcheck_compare/blob/master/fig/result.png)

