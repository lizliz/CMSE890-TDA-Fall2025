#----------------------
# Smith normal form code
# Warning: This assumes Z_2 coefficients!
#
# Author - Liz Munch <muncheli@egr.msu.edu>
#------------------------


import numpy as np 
import matplotlib.pyplot as plt
import PIL
import urllib





def moveOneToPivot(N,U,V,s):
	# Find first location in matrix
	# N[s:,s:] (the bottom right chunk)
	# which has a non-zero entry.

	locOfOnes = np.where(N[s:,s:] == 1)
	i = locOfOnes[0][0]
	j = locOfOnes[1][0]

	# Swap row i+s with row s
	N[s,:], N[i+s,:] = N[i+s,:].copy(), N[s,:].copy()
	U[s,:], U[i+s,:] = U[i+s,:].copy(), U[s,:].copy()

	# Swap col j+s with col s
	N[:,s], N[:,j+s] = N[:,j+s].copy(), N[:,s].copy()
	V[:,s], V[:,j+s] = V[:,j+s].copy(), V[:,s].copy()


	return N,U,V



def clearCol(N,U,V,s):
	locsOfOnes = np.where(N[s+1:,s] == 1)[0]
	for i in locsOfOnes:
		# Add row s to row s+1+i
		N[s + 1 + i,:] += N[s,:]
		U[s + 1 + i,:] += U[s,:]

		# Clear out mod 2
		N[s + 1 + i,:]  = np.mod(N[s + 1 + i,:] ,2)
		U[s + 1 + i,:]  = np.mod(U[s + 1 + i,:] ,2)

	return N,U,V

def clearRow(N,U,V,s):
	locsOfOnes = np.where(N[s,s+1:] == 1)[0]
	for j in locsOfOnes:
		# Add col s to col s+1+j
		N[:,s+1+j] += N[:,s]
		V[:,s+1+j] += V[:,s]

		# Clear out mod 2
		N[:,s+1+j] = np.mod(N[:,s+1+j],2)
		V[:,s+1+j] = np.mod(V[:,s+1+j],2)

	return N,U,V

def check(N,U,V,A):
	diff = N - U.dot(A.dot(V))
	diff = np.mod(diff,2)

	if set(np.unique(diff)) == {0}:
		return True
	else:
		# This means that we don't have
		# N = U*A*V
		print('Another buuuuuuuuug!')
		return False

def smith_form(A, returnRank = False):
	numRows, numCols = np.shape(A)
	N = A.copy()
	U = np.eye(numRows)
	V = np.eye(numCols)

	rank = 0

	# Check that we have a 0,1 matrix since we are assuming Z_2 coefficients	
	entries = set(np.unique(A))
	if entries == {0}:
		return N,U,V,rank
	elif entries != {0,1}:
		print('WARNING: This code only works with 0,1 matrices.')
		print('Exiting...')
		return

	for s in range(min(numRows,numCols)):

		if N[s:,s:].any():
			N,U,V = moveOneToPivot(N,U,V,s)
			check(N,U,V,A)

			N,U,V = clearCol(N,U,V,s)
			check(N,U,V,A)

			clearRow(N,U,V,s)
			check(N,U,V,A)
		else:
			# This means that we're all done
			break

	N = N.astype(int)
	U = U.astype(int)
	V = V.astype(int)

	if returnRank:
		return N,U,V,s
	else:
		return N,U,V


# Plotting scripts
def plotFirstSetOfMatrices(N1,U0,B1,V1,edge_list,vertex_list,figure_file = 'SimplexExamples_1.png'):

    fig, ax = plt.subplots(nrows=1, ncols=5, figsize = (20,10))

    ax[0].spy(N1)
    ax[0].set_title("$N_1$")
    ax[0].set_xticks(list(range(len(edge_list))))
    ax[0].set_xticklabels(edge_list)
    ax[0].set_yticks(list(range(len(vertex_list))))
    ax[0].set_yticklabels(vertex_list)

    ax[1].spy(U0)
    ax[1].set_title("$U_0$")
    ax[1].set_xticks(list(range(len(vertex_list))))
    ax[1].set_xticklabels(vertex_list)
    ax[1].set_yticks(list(range(len(vertex_list))))
    ax[1].set_yticklabels(vertex_list)

    ax[2].spy(B1)
    ax[2].set_title("$B_1$")
    ax[2].set_xticks(list(range(len(edge_list))))
    ax[2].set_xticklabels(edge_list)
    ax[2].set_yticks(list(range(len(vertex_list))))
    ax[2].set_yticklabels(vertex_list)

    ax[3].spy(V1)
    ax[3].set_title("$V_1$")
    ax[3].set_xticks(list(range(len(edge_list))))
    ax[3].set_xticklabels(edge_list)
    ax[3].set_yticks(list(range(len(edge_list))))
    ax[3].set_yticklabels(edge_list)

    img = np.array(PIL.Image.open(urllib.request.urlopen('https://raw.githubusercontent.com/lizliz/CMSE890-TDA-Fall2025/main/JupyterFigures/' + figure_file)))
    ax[4].imshow(img)
    ax[4].axis('off')

def plotSecondSetOfMatrices(N2,U1,B2, V2,edge_list,triangle_list,figure_file = 'SimplexExamples_1.png'):
    fig, ax = plt.subplots(nrows=1, ncols=5, figsize = (20,10))

    ax[0].spy(N2)
    ax[0].set_title("$N_2$")
    ax[0].set_xticks(list(range(len(triangle_list))))
    ax[0].set_xticklabels(triangle_list)
    ax[0].set_yticks(list(range(len(edge_list))))
    ax[0].set_yticklabels(edge_list)

    ax[1].spy(U1)
    ax[1].set_title("$U_1$")
    ax[1].set_xticks(list(range(len(edge_list))))
    ax[1].set_xticklabels(edge_list)
    ax[1].set_yticks(list(range(len(edge_list))))
    ax[1].set_yticklabels(edge_list)


    ax[2].spy(B2)
    ax[2].set_title("$B_2$")
    ax[2].set_xticks(list(range(len(triangle_list))))
    ax[2].set_xticklabels(triangle_list)
    ax[2].set_yticks(list(range(len(edge_list))))
    ax[2].set_yticklabels(edge_list)

    ax[3].spy(V2)
    ax[3].set_title("$V_2$")
    ax[3].set_xticks(list(range(len(triangle_list))))
    ax[3].set_xticklabels(triangle_list)
    ax[3].set_yticks(list(range(len(triangle_list))))
    ax[3].set_yticklabels(triangle_list)

    img = np.array(PIL.Image.open(urllib.request.urlopen('https://raw.githubusercontent.com/lizliz/CMSE890-TDA-Fall2025/main/JupyterFigures/'+figure_file)))
    ax[4].imshow(img)
    ax[4].axis('off')
