 # Variables that tells if you *can* keep moving in a given direction, if false it means you found an obstacle
        up, down, right, left = (True, True, True, True)
        
        # WIP, MAYBE SHOULD IMPLEMENT IT to ease the process of checking up true, down true, left true, right true
        #keepGoing = True

        for i in range(0,9):
            for j in range (0,9):
                # If [i,j] is an empty cell, just do nothing
                if state[i,j] != Pawn.EMPTY.value:

                    # The selected cell has a White pawn in it
                    if state[i,j] == Pawn.WHITE.value:

                        # K variable moves the pawn in the matrix
                        k = 1
                        while k < 8 and (up == True or down == True or right == True or left == True):
                            
                            # Check if you can keep moving up
                            if up == True:
                                newRow = i-k
                                
                                # Check if index is out of bounds
                                if newRow == 0: up = False
                                
                                if up:
                                    # Check if the destination cell is a Camp
                                    for cell in self.camps:
                                        if cell[0] == newRow and cell[1] == j:
                                            up = False
                                            break
                                    # Check if the destination cell is the Castle
                                    if newRow == 4 and j == 4:
                                        up = False

                                    # Check if you found another Pawn/King
                                    if up and state[newRow,j] != Pawn.EMPTY.value: up = False
                                    # If this is a proper move, add it to the result in a tuple: (from, to)
                                    else: result.append(([i,j],[newRow,j]))

                            # Check if you can keep moving down
                            if down == True:
                                newRow = i+k
                                if newRow == 8: down = False
                                
                                if down:
                                    for cell in self.camps:
                                        if cell[0] == newRow and cell[1] == j:
                                            down = False
                                            break
                                    if newRow == 4 and j == 4:
                                        up = False
                                    
                                    if down and state[newRow,j] != Pawn.EMPTY.value: down = False
                                    else: result.append(([i,j],[newRow,j]))

                            # Check if you can keep moving left
                            if left == True:
                                newCol = j-k
                                if newCol == 0: left = False
                                
                                if left:
                                    for cell in self.camps:
                                        if cell[0] == i and cell[1] == newCol:
                                            left = False
                                            break
                                    if i == 4 and newCol == 4:
                                        up = False
                                    
                                    if left and state[i,newCol] != Pawn.EMPTY.value: left = False
                                    else: result.append(([i,j],[i,newCol]))

                            # Check if you can keep moving right
                            if right == True:
                                newCol = j+k
                                if newCol == 8: right = False
                                
                                if right:
                                    for cell in self.camps:
                                        if cell[0] == i and cell[1] == newCol:
                                            right = False
                                            break
                                    if i == 4 and newCol == 4:
                                        up = False
                                    
                                    if right and state[i,newCol] != Pawn.EMPTY.value: right = False
                                    else: result.append(([i,j],[i,newCol]))

                            # Checked all four direction, so we extend the "radius" (k) and iterate
                            k = k + 1

                    up, down, right, left = (True, True, True, True)

                    # The selected cell has a Black pawn in it
                    if state[i,j] == Pawn.BLACK.value:

                        # K variable moves the pawn in the matrix
                        k = 1
                        while k < 8 and (up == True or down == True or right == True or left == True):
                            
                            # Check if you can keep moving up
                            if up == True:
                                newRow = i-k
                                
                                # Check if index is out of bounds
                                if newRow == 0: up = False
                                
                                if up:
                                    # Check if the destination cell is a Camp
                                    for cell in self.camps:
                                        if self.isSameCamp((newRow, j), cell) == False and cell[0] == newRow and cell[1] == j:
                                            up = False
                                            break
                                    # Check if the destination cell is the Castle
                                    if newRow == 4 and j == 4:
                                        up = False

                                    # Check if you found another Pawn/King
                                    if up and state[newRow,j] != Pawn.EMPTY.value: up = False
                                    # If this is a proper move, add it to the result in a tuple: (from, to)
                                    else: result.append(([i,j],[newRow,j]))

                            # Check if you can keep moving down
                            if down == True:
                                newRow = i+k
                                if newRow == 8: down = False
                                
                                if down:
                                    for cell in self.camps:
                                        if self.isSameCamp((newRow, j), cell) == False and cell[0] == newRow and cell[1] == j:
                                            down = False
                                            break
                                    if newRow == 4 and j == 4:
                                        up = False
                                    
                                    if down and state[newRow,j] != Pawn.EMPTY.value: down = False
                                    else: result.append(([i,j],[newRow,j]))

                            # Check if you can keep moving left
                            if left == True:
                                newCol = j-k
                                if newCol == 0: left = False
                                
                                if left:
                                    for cell in self.camps:
                                        if self.isSameCamp(cell, (i, newCol)) == False and cell[0] == i and cell[1] == newCol:
                                            left = False
                                            break
                                    if i == 4 and newCol == 4:
                                        up = False
                                    
                                    if left and state[i,newCol] != Pawn.EMPTY.value: left = False
                                    else: result.append(([i,j],[i,newCol]))

                            # Check if you can keep moving right
                            if right == True:
                                newCol = j+k
                                if newCol == 9: right = False
                                
                                if right:
                                    for cell in self.camps:
                                        if self.isSameCamp(cell, (i, newCol)) == False and cell[0] == i and cell[1] == newCol:
                                            right = False
                                            break
                                    if i == 4 and newCol == 4:
                                        up = False
                                    
                                    if right and state[i,newCol] != Pawn.EMPTY.value: right = False
                                    else: result.append(([i,j],[i,newCol]))

                            # Checked all four direction, so we extend the "radius" (k) and iterate
                            k = k + 1
                          
                    up, down, right, left = (True, True, True, True)
                    
                    # The selected cell has a KiNG in it  
                    if state[i,j] == Pawn.KING.value:

                        # K variable moves the pawn in the matrix
                        k = 1
                        while k < 8 and (up == True or down == True or right == True or left == True):
                            
                            # Check if you can keep moving up
                            if up == True:
                                newRow = i-k
                                
                                # Check if index is out of bounds
                                if newRow == 0: up = False
                                
                                if up:
                                    # Check if the destination cell is a Camp
                                    for cell in self.camps:
                                        if cell[0] == newRow and cell[1] == j:
                                            up = False
                                            break
                                    # Check if the destination cell is the Castle
                                    if newRow == 4 and j == 4:
                                        up = False

                                    # Check if you found another Pawn/King
                                    if up and state[newRow,j] != Pawn.EMPTY.value: up = False
                                    # If this is a proper move, add it to the result in a tuple: (from, to)
                                    else: result.append(([i,j],[newRow,j]))

                            # Check if you can keep moving down
                            if down == True:
                                newRow = i+k
                                if newRow == 8: down = False
                                
                                if down:
                                    for cell in self.camps:
                                        if cell[0] == newRow and cell[1] == j:
                                            down = False
                                            break
                                    if newRow == 4 and j == 4:
                                        up = False
                                    
                                    if down and state[newRow,j] != Pawn.EMPTY.value: down = False
                                    else: result.append(([i,j],[newRow,j]))

                            # Check if you can keep moving left
                            if left == True:
                                newCol = j-k
                                if newCol == 0: left = False
                                
                                if left:
                                    for cell in self.camps:
                                        if cell[0] == i and cell[1] == newCol:
                                            left = False
                                            break
                                    if i == 4 and newCol == 4:
                                        up = False
                                    
                                    if left and state[i,newCol] != Pawn.EMPTY.value: left = False
                                    else: result.append(([i,j],[i,newCol]))

                            # Check if you can keep moving right
                            if right == True:
                                newCol = j+k
                                if newCol == 8: right = False
                                
                                if right:
                                    for cell in self.camps:
                                        if cell[0] == i and cell[1] == newCol:
                                            right = False
                                            break
                                    if i == 4 and newCol == 4:
                                        up = False
                                    
                                    if right and state[i,newCol] != Pawn.EMPTY.value: right = False
                                    else: result.append(([i,j],[i,newCol]))

                            # Checked all four direction, so we extend the "radius" (k) and iterate
                            k = k + 1

                    up, down, right, left = (True, True, True, True)