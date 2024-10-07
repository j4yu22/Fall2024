
"""

"""
def stateOfCells(cells, days):

	for _ in range(days):
		new_cells = [0] * len(cells)

		for i in range(1,  len(cells) - 1):
			left = cells[i - 1]
			right = cells[i + 1]

			if left == right:
				new_cells[i] = 0

			else:
				new_cells[i] = 1

			cells = new_cells

	return cells

def main():
	#input for cell
	cells = []
	cell_size  = int(8)
	cells = list(map(int(0 1 0 0 0 1 0 1).split()))
	
	#input for days
	days = int(1)
	
	
	result = stateOfCells(cells, days)
	print(" ".join([str(res) for res in result]))	

if __name__ == "__main__":
	main()