A simple python script for generating crossword.

Here's the process:

1. Create a grid of whatever size and a list of words.

2. Shuffle the word list, and then sort the words by longest to shortest.

3. Place the first and longest word at the upper left most position, 1,1 (vertical or horizontal).

4. Move onto next word, loop over each letter in the word and each cell in the grid looking for letter to letter matches.

5. When a match is found, simply add that position to a suggested coordinate list for that word.

6. Loop over the suggested coordinate list and "score" the word placement based on how many other words it crosses. Scores of 0 indicate either bad placement (adjacent to existing words) or that there were no word crosses.

7. Back to step #4 until word list is exhausted. Optional second pass.

8. We should now have a crossword, but the quality can be hit or miss due to some of the random placements. So, we buffer this crossword and go back to step #2. If the next crossword has more words placed on the board, it replaces the crossword in the buffer. This is time limited (find the best crossword in x seconds).

By the end, you have a decent crossword puzzle or word search puzzle, since they are about the same. It tends to run rather well, but let me know if you have any suggestions on improvement. Bigger grids run exponentially slower; bigger word lists linearly. Bigger word lists also have a much higher chance at better word placement numbers.

Reference: Byran's answer on https://stackoverflow.com/questions/943113/algorithm-to-generate-a-crossword
