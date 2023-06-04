class Genome:
    '''
    Genome class for each cell cell, it will be contained in a file and will be readen as follow:
        - Each gene will start with the same sequence and end with the same sequence
        - A gene will be referenced as it's index in the file
        - A gene can be mutated in each cell
        - The gene will be caracterized on the cell as it's color and more informations when the cell is selected
        - The first gene that will be listed is the one that regulate the intensity of the pheromone
        - The second gene that will be listed is the one that will specify the pheromone
    '''

    def __init__(self, cell):
        self.cell = cell
        cellName = cell.name.replace(" ", "")
        self.genesList = []
        file1_path = "basic_" + cell.type + "_" + "genome.txt"  # Replace with the actual path to file1
        output_file_path = "genomes/" + cellName + "_" + cell.type + "_genome.txt"
        
        with open(file1_path, 'r') as file1:
            file1_content = file1.read()
        
        with open(output_file_path, 'w+') as genome_file:
            existing_content = genome_file.read()
            genome_file.seek(0)  # Move the file pointer to the start of the file
            genome_file.write(file1_content + existing_content)


    def linkGenome(self):
        filepath = "genomes/" + self.cell.name.replace(" ", "") + "_" + self.cell.type + "_genome.txt"
        with open(filepath, "r") as f:
            genome = f.readlines()
            for gene in genome:
                if not gene.startswith("#"):
                    try:
                        self.genesList.append(int(gene))
                    except ValueError as e:
                        self.genesList.append(gene[:len(gene)-2])
                else:
                    print("Linking gene : " + gene[1:])

    