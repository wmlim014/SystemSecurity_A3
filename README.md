# SystemSecurity_A3 Compile in Window
```
python main.py
```

>[!NOTE]
>1. Please open file in sub_program to modified the program for testing
>2. Please declare a function for each functionality, this is easy to include the new code to the `main.py`
>3. Before merging the program into `main.py` and push to origin, please inform team.

# Understand the file in `sub_program` with the following sequence
1. `read_files.py`: Prompt user to key in the file name and load through the data in file
    > Step 1 and 2

2. `check_file_data.py`: Check the consistencies and alert value...
    > Step 3

3. `generate_logs.py`: Generate the events for days base on mean, standard deviation with min <= x => max
    > Step 4