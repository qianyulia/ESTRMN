#Code accompanying the paper "Entropy Similarity-Driven Transformation Reaction Molecular Networking: Revealing Transformation Pathways and Potential Risks of Emerging Contaminants in Wastewater: The Example of Sartans" by Yuli Qian et al.

Files provided:

A.  ESTRMN.py: The main script that performs the analysis of parent and product spectra, calculates entropy similarities, and visualizes the resulting molecular network.

B. parent.xlsx: Example input file containing the parent spectra data. Columns include:
    ID: Unique identifier for each parent spectrum.
    mz: Precursor mass-to-charge ratio (m/z).
    MS2: Fragmented spectrum data, formatted as peak_intensity:mass_ratio.

C. product.xlsx: Example input file containing the product spectra data, formatted the same way as parent.xlsx.

1. Requirements:
   
This program requires the following Python libraries: numpy pandas ms_entropy networkx matplotlib tqdm
You can install them using:
```ruby
pip install numpy pandas ms_entropy networkx matplotlib tqdm
```

2. Running the Script:

To run the program, execute the following command in your terminal:
```ruby
python  ESTRMN.py
```

3. Notes:

Input Data: The script expects parent.xlsx and product.xlsx to be present in the working directory.
Parameters: You can adjust the similarity threshold in the code by changing if similarity > 0.5. The default threshold is set to 0.5 for identifying similar spectra. Adjust the network layout and graph drawing parameters based on your needs.

4. Output:

similarities.csv: This file contains the calculated similarity scores for each pair of parent and product spectra.
network.png: A graph plot visualizing the molecular network based on the calculated similarities.

5. Suggestions:

This is a way to calculate the similarity of the spectra. The known matrix selects the potential transformation product peaks. When identifying a new structure, the new structure can be used to expand the screening range and carry out numerous iterations. It is worth noting that all spectra can also be directly compared in pairs, and then the adjacent nodes can be identified according to the known structure. In addition, the authors of ms_entropy also proposed four search algorithms, which are much faster than the classical entropy similarity algorithm, and can be used to calculate the spectrum of large data sets faster.

Citation: If you use this code, please cite the following paper:
Yuli Qian et al.
"Entropy Similarity-Driven Transformation Reaction Molecular Networking: Revealing Transformation Pathways and Potential Risks of Emerging Contaminants in Wastewater: The Example of Sartans."
