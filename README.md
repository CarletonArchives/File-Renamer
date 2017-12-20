# File-Renamer
Bulk renames files.
The program is split into two parts:
NameReformatter.py creates a "map" file ("map.csv"), containing a list of all filenames in the selected directory,
and the filename to change each of them into.
Copier.py takes in an existing map, and actually copies the original files to the selected folder under the new filenames.

Formats:
* Name Reformatter requires an input and an output format. Anything inside []s is treated as a variable (e.g. [Year]\_[Month]\_[Day].jpg) will match the files you'd expect. Anything outside brackets must be matched exactly (e.g. 2017\_[Month]\_[Day].[extension])
* Variables will match as few characters as possible, but at least one. They will match until the end of the filename, so [filename] will get anything, but [character][filename] will give [character] the first character, and [filename] the rest.
* Variables do not match over / characters. Inputs should be sanitized to remove them first. This is to allow moving items in/out of folders. (e.g. folder1/[filename] -> folder2/[filename])
* Outputs can use any variables in the input. Also, they can pad a variable with leading zeroes to force it to be the useful length(e.g. [Y]\_[M]\_[D].[extension] -> [YYYY]\_[MM]\_[DD].[extension])

Maps:
* Name Reformatter does not overwrite maps. It will instead add on to the current map. If you want to start over, delete the map.
* Files that didn't match any input pattern and files that would be renamed to the same thing will be sorted to the top of the map, and given a "Value" of -1.
* Files that have a valid output filename will be given a "Value" of 0. The Name Reformatter will not try to give them a different output.
* The map is just a csv file. Feel free to make changes to it by hand.

Copier:
* The copier copies all files in the map with a "Value" of 1 to {selected\_folder}/{output\_filename\_in\_map}. It will delete the map after it is finished.
