import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import functools


def colex_compare(a, b, f = lambda x: x):
    """
    Colexicographic comparison based on function f.
    Returns -1 if a < b, 0 if a == b, 1 if a > b.
    """
    la, lb = len(a), len(b)
    for i in range(1, min(la, lb)+1):
        va, vb = f[a[-i]], f[b[-i]]
        if va < vb:
            return -1
        elif va > vb:
            return 1
    # If all compared are equal, shorter comes first
    if la < lb:
        return -1
    elif la > lb:
        return 1
    else:
        return 0
    
def colex_order(S, f):
    """
    Sorts the simplices in S using the colex_compare function.
    :param S: List of simplices
    :param f: Function to compute the value of a simplex
    :return: Sorted list of simplices
    """
    # First, sort each simplex in S so that the order of elements is the same as the order in f. 
    S = [sorted(s, key=lambda x: f[x]) for s in S]
    # Then sort the simplices using the colex_compare function
    
    return sorted(S, key=functools.cmp_to_key(lambda a, b: colex_compare(a, b, f)))


def boundary(simplices):
    """Create the boundary matrix B from the list of simplices S.

    Args:
        simplices (list): List of simplices, where each simplex is represented as a list of vertices.
        For example, [[0, 1], [1, 2], [0, 2]] represents a triangle with vertices 0, 1, and 2.
        
    Returns:    
        np.ndarray: Boundary matrix B, where B[i][j] = 1 if simplex i is a boundary of simplex j, 0 otherwise.
    """
    S = simplices
    B = np.zeros((len(S), len(S)), dtype=int)
    for i, s in enumerate(S):
        for j, t in enumerate(S):
            if i != j and set(s).issubset(set(t)) and len(s) + 1 == len(t):
                B[i][j] = 1
    return B



# Implement the standard persistence reduction algorithm on B
def standard_persistence_reduction(B, exhaustive = False, return_type = 'U', verbose = False):
    """
    Perform standard persistence reduction on the boundary matrix B. 
    If exhaustive is True, it will perform exhaustive reduction on R, which clears out the entries in each column that are the lowest 1 for a previous column. 
    
    :param B: Boundary matrix
    :param exhaustive: If True, perform exhaustive reduction
    :param return_type: If 'U', return R,U,Low where RU = B. If 'V', return the R, V, Low where R = BV. 
    :return: Triple: (R, U or V, Low) where R is the reduced boundary matrix, U or V is the transformation matrix, and Low is the list of lowest 1s in each column with a -1 if there is no lowest 1.
    """
    
    assert return_type in ['U', 'V'], "return_type must be either 'U' or 'V'."
    
    # Get the number of rows and columns in B
    n, m = B.shape

    # Initialize the reduced boundary matrix
    R = np.copy(B)
    
    if return_type == 'V':
        # Initialize the V matrix, which will be R = BV decomposition. 
        
        V = np.eye(n, dtype=int)
    else:
        # This will result in an RU = B decomposition 
        U = np.eye(n, dtype=int)
    
    
    # Track the lowest 1 in each column. 
    # If there is none, represent it with -1
    low = np.zeros(m, dtype=int)-1 

    # Iterate over each column
    for j in range(m):
        done = False
        
        while not done:
            # Find the lowest 1 in the column
            try:
                low[j] = np.where(R[:, j] == 1)[0][-1]
            except:
                low[j] = -1
                done = True
                
            # If a previous entry shares this lowest 1, add that column to this one mod 2
            if low[j] != -1:
                # Find the entry in low that has the same lowest 1
                col = np.where(low == low[j])[0][0]
                # If the column is the same, break
                if col >= j:
                    done = True
                    break
                else:
                    # print(f"Adding column {col} to column {j}")
                    # Add the column to this one mod 2 in R
                    R[:, j] = (R[:, j] + R[:, col]) % 2
                    if return_type == 'V':
                        # Do the same in V, but with cols
                        V[:, j] = (V[:, j] + V[:, col]) % 2
                    else:
                        # Now with U, but adding column col to column j turns into adding row j to row col
                        U[col,:] = (U[col, :] + U[j, :]) % 2
            
        # If exhaustive is True, we work up the entries in teh column and add the column that shares the lowest one there if it exists 
        if exhaustive and low[j] != -1: 
            if verbose:
                print(f"\n---\nProcessing column {j} with low(j) = {low[j]}\n---\n")
                print(R[:low[j]+1, j])
            for k in range(low[j]-1,-1, -1):
                # print(f"Checking ({k}, {j}) in R, which is {R[k, j]}")
                if R[k, j] == 1:
                    # print(f"Checking for column with lowest 1 at {k}")
                    try:
                        col = np.where(low[:j] == k)[0][0]
                        R[:, j] = (R[:, j] + R[:, col]) % 2
                        if return_type == 'V':
                            V[:, j] = (V[:, j] + V[:, col]) % 2
                        else:
                            U[col,:] = (U[col, :] + U[j, :]) % 2
                        
                        if verbose:
                            print(f"Found column {col} with lowest 1 at {k} before column {j} and added to {j}")
                    
                    except:
                        if verbose:
                            print(f"No column found with lowest 1 at {k}")
    if return_type == 'U':
        # RU = B
        return R, U, low
    else:
        # R = BV
        return R, V,low



def drawMat(R, S, ax = None):
    """
    Draw the matrix R with simplices S.
    :param R: Boundary matrix (possibly reduced)
    :param S: List of simplices
    """
    
    if ax is None:
        plt.figure(figsize=(5,4))
        ax = plt.gca()
    
    
    sns.heatmap(R, annot=True,  cmap='Blues', xticklabels=S, yticklabels=S, ax = ax, cbar = False)
    ax.set_title('Reduced Boundary Matrix')
    ax.set_xlabel('Simplices')
    ax.set_ylabel('Simplices')
    
    
    single_vertex_indices = [i for i, s in enumerate(S) if len(s) == 1][1:]
    
    for i in single_vertex_indices:
        # Vertical lines between columns 
        ax.axvline(x=i, color='black', linestyle='-')
        # Horizontal lines between rows
        ax.axhline(y=i, color='black', linestyle='-')
        
    
    fig, ax = plt.gcf(), plt.gca()
    return fig, ax



    
def find_lowest_ones(R, S):
    """
    This function will produce a list of birth-death pairs in the **reduced** boundary matrix.
    For each non-zero column in the binary matrix, find the (row_header, column_header)
    of the lowest occurrence of the value 1.

    Parameters:
    R: Boundary matrix
    S: List of simplices.
    
    Returns:
    List of (birth_simplex, death_simplex) pairs from the reduced boundary matrix
    """
    if not isinstance(R, np.ndarray):
        raise TypeError("Input must be a NumPy array.")
    if R.ndim != 2:
        raise ValueError("Input must be a 2D array.")
    if R.shape[0] != R.shape[1]:
        raise ValueError("Input must be a square matrix (n x n).")

    n = R.shape[0]

    # Set default headers if none provided
    if S is None:
        row_headers = [f"Row{i}" for i in range(n)]
        col_headers = [f"Col{j}" for j in range(n)]

    if len(S) != n:
        raise ValueError("Length of simplex list must match matrix dimensions.")

    result = []

    for col in range(n):
        column_data = R[:, col]
        if np.any(column_data):  # Check if the column has any 1s
            row_indices = np.where(column_data == 1)[0]
            if row_indices.size > 0:
                last_row = row_indices[-1]
                result.append((S[last_row], S[col]))

    return result

#============================
if __name__ == "__main__":
    # Example simplices
    print("First Example:")
    S = [[0], [1], [2], [3], [0, 1], [1, 2], [0, 2], [1,3], [2,3], [0, 1, 2]]
    # Example function f
    f = {0:0, 1:13, 2:8, 3:27}
    
    # Sort simplices using colex_order
    S = colex_order(S, f)
    print("Sorted simplices:", S)
    # Create the boundary matrix
    B = boundary(S)

    drawMat(B, S)
    plt.show()
    
    # Perform standard persistence reduction
    R = standard_persistence_reduction(B)
    print("Reduced boundary matrix:\n", R)
    
    positions = find_lowest_ones(R, S)
    print("Positions of lowest 1s:")
    for birth, death in positions:
        print(f"Birth simplex: {birth}, Death simplex: {death}")
    
    # Draw the reduced boundary matrix
    drawMat(R, S)
    plt.show()


    # # Second example 
    # print("\nSecond Example:")
    # R = np.array([
    #     [0, 0, 0, 0],
    #     [1, 0, 1, 0],
    #     [0, 1, 0, 0],
    #     [0, 0, 1, 0]
    # ])
    # S = ['A', 'B', 'C', 'D']
    # positions = find_lowest_ones(R, S)
    # print("Positions of lowest 1s in each non-zero column:", positions)

