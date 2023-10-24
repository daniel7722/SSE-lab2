#include <iostream>
#include <fstream>
#include <cstdlib>

using namespace std;

void load_board(const char* filename, char board[9][9]) {

  ifstream in(filename);
  if (!in) {
    exit(1);
  }

  char buffer[512];
  int row = 0;
  in.getline(buffer, 512);
  while (in && row < 9) {
    for (int n=0; n<9; n++) {
      board[row][n] = buffer[n];
    }
    row++;
    in.getline(buffer,512);
  }
}

bool make_move (int row, int col, char digit, char board[9][9]) {
  // check if the position is out of range
  if ((row > 8) || (row < 0) || (col > 8) || (col < 0))
    return false;

  // check if the position is empty
  if (board[row][col] != '.')
    return false;

  // check if there's identical number in the same row or the same column;
  for (int count = 0; count < 9; count++) {
    
    if (board[count][col] == digit || board[row][count] == digit) 
      return false;
    
  }

  // check if there's identical number in the box
  int row_box = row - row % 3;
  int col_box = col - col % 3;
 
  for (int r = 0; r < 3; row_box++, r++) {
    
    for (int c = 0; c < 3; col_box++, c++) {
      
      if (board[row_box][col_box] == digit)
	return false;
      
    }

    // restore column number to the original one for the next row
    col_box -= 3;
  }

  // It is a valid move, so update the board and return true
  board[row][col] = digit;
  return true;
}

bool save_board (const char* filename, char board[9][9]) {
   
  ofstream out;
  out.open(filename);

  if (out.fail()) {
    
    return false;
    
  }

  // loop over the whole board to output characters
  for (int row = 0; row < 9; row++) {
    
    for (int col = 0; col < 9; col++) {
      
      out.put(board[row][col]);
      
    }

    // end of row character is added once we reach the end of row
    out.put('\n');
    
  }
  
  out.close();
  return true;
}

bool solve_board(char board[9][9], int row, int col){
  // Base case: when all rows have been solved
  if (row == 9) {
    
    return true;
    
  }

  // Special case: when reaches the end of row, update row and col number
  if (col == 9) {
    
    return solve_board(board, row + 1, 0);

  }

  // only enter loop of making moves if the square we look at is empty 
  if (board[row][col] == '.') {

    // try to put every possible number in that square
    for (char num = '1'; num <= '9'; num++) {
      
      // check if it is a valid move
      if (make_move(row, col, num, board)) {

	// if it is a valid move, call solve_board again to the next square and check if the board is solved
	if (solve_board(board, row, col + 1))
	  return true;

	// if not solved back track the square to empty so the next number can be tested
	board[row][col] = '.';
	
      }
      
    }
    
  } else { // if the square is not empty, go to the next square
    
    return solve_board(board, row, col + 1);
    
  }

  // if we try every combination to go forward and it doesn't work, the board has no solution
  return false;
}


int main (int argc, char* argv[]) {
  if (argc != 3) {
    cerr << "usage: " << argv[0] << "input.dat output.dat" << endl;
    return 1;
  }
  
  const char* inputFilename = argv[1];
  const char* outputFilename = argv[2];
  char board[9][9];

  load_board(inputFilename, board);

  if (solve_board(board, 0, 0)) {
    cout << "Sudoku solved successfully. " << endl;
  } else {
    cout << "Sudoku has no solution. " << endl;
  }

  if (!save_board(outputFilename, board)) {
    cerr << "Failed to save the solution to " << outputFilename << endl;
    return 1;
  }

  return 0;

}

  
