# 1

## Formulation
The game “Find words”. One should find words which are present on the game field of symbols.

## Essence
Game "Find words": the application shows matrix of letters to user, user predict a word, application checks the word presence in the matrix.

## Ideas
1. Receive some list of words, generate `random` matrix, when user will have typed a word check the word first with all words, then find it in the matrix;
2. Receive list of words, generate matrix of 100% words of English, fill gaps between them.

## Input
File with language words.

## Output
Matrix with hidden words for find word game. Words can be from left to right, from right to left, top bottom, bottom top, diagonally with any angle.