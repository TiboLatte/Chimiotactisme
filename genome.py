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


    def linkBasicGenome(self):
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

    def updateGene(self, geneIndex, value):
        filepath = "genomes/" + self.cell.name.replace(" ", "") + "_" + self.cell.type + "_genome.txt"

        # Read the contents of the genome file and store them in a list
        with open(filepath, "r") as f:
            genome = f.readlines()

        # Modify the desired gene value
        currentGeneIndex = -1
        for i, line in enumerate(genome):
            if not line.startswith("#"):
                currentGeneIndex += 1
                if currentGeneIndex == geneIndex:
                    genome[i] = str(value) + "\n"

        # Write the modified data back to the genome file, excluding the lines starting with "#"
        with open(filepath, "w") as f:
            f.writelines(genome)

    def reloadGenome(self):
        self.genesList = []
        self.linkBasicGenome()
    def initialize(self):
        self.linkBasicGenome() #should be called if i want it to be initialized automatically.

        color = "" + str(self.cell.color[0]) + str(self.cell.color[1]) + str(self.cell.color[2])

        self.updateGene(0, color) #SET COLOR
        self.updateGene(1, self.cell.radius) #SET RADIUS
        self.updateGene(2, self.cell.agac) #SET AG OR AC
