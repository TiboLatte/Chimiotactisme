class Genome:
    '''
    Genome class for each cell cell, it will be contained in a file and will be readen as follow:
        - Each gene will start with the same sequence and end with the same sequence
        - A gene will be referenced as it's index in the file
        - A gene can be mutated in each cell
        - The gene will be caracterized on the cell as it's color and more informations when the cell is selected
        
    '''
    def __init__(self, cell):
        