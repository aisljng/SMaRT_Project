'''
write program that
1. gets input size by user
2. generates combinations from 17 RE's
3. user inputs the known RE's 
4. the program fills in the remaining size
'''
import pandas as pd
import itertools

class Generate_RE:

    file = '/Users/aisling/downloads/SMaRT/Ionic_Average_Project.xlsx'
    df1 = pd.read_excel(file, sheet_name='List of Elements', usecols=['Symbol', 'Ionic Radius (CN = 8, Å)'])

    def __init__(self, size, elements):
        self.size = int(size)
        self.elements = elements.split()

    def validation(self):
        column_values = self.df1['Symbol'].dropna().unique()
        nonexistent = [elem for elem in self.elements if elem not in column_values]

        if nonexistent:
            print(f"The following elements do not exist: {nonexistent}")
            return False
        else:
            return True

    def combinations(self):
        if not self.validation():
            return []

        df = Generate_RE.df1  
        df = df.iloc[6:23]  # rows 6 to 23
        df.reset_index(drop=True, inplace=True) 
        
        elements = df['Symbol'].values.tolist()

        # print(f"Extracted elements: {elements}")
        # print(f"User provided elements: {self.elements}")

        remaining_elements = [el for el in elements if el not in self.elements] # removes user elements from list

        # print(f"Remaining elements after removing user elements: {remaining_elements}")

        # generates all combos of the remaining elements w  size adjusted from user elements
        comb_size = self.size - len(self.elements)
        if comb_size < 0:
            print("The size of known elements exceeds the desired combination size.")
            return []

        if comb_size == 0:
            final_combinations = [self.elements]
        else:
            all_combinations = list(itertools.combinations(remaining_elements, comb_size))
            # print(f"All combinations of remaining elements: {all_combinations}")

            final_combinations = [self.elements + list(comb) for comb in all_combinations]

        unique_combinations = set(tuple(sorted(comb)) for comb in final_combinations) # avoids dupes

        unique_combinations = [list(comb) for comb in unique_combinations]
        return unique_combinations
    
   
    def average_ionic_radius(self, combinations):
        df = Generate_RE.df1

        data = []
        for comb in combinations:
            row = {}
            total_radius = 0
            valid_elements_count = 0
            for idx, elem in enumerate(comb):
                ionic_radius = df[df['Symbol'] == elem]['Ionic Radius (CN = 8, Å)']
                if not ionic_radius.empty:
                    radius = ionic_radius.values[0]
                    row[f'Element {idx + 1}'] = elem
                    total_radius += radius
                    valid_elements_count += 1
                else:
                    row[f'Element {idx + 1}'] = elem

            row['Combination'] = ', '.join(comb)
            row['Average Ionic Radius'] = total_radius / valid_elements_count if valid_elements_count > 0 else None

            data.append(row)

        df_combinations = pd.DataFrame(data)
        print(df_combinations)
        return df_combinations

    def save_to_excel(self, df_combinations, comb_file):
        if isinstance(df_combinations, pd.DataFrame):
            df_combinations.to_excel(comb_file, index=False)
            print(f"Combinations saved to {comb_file}")
        
if __name__ == "__main__":
    size_input = input("Enter the size of elements: ")
    known_re = input("Enter the known RE elements: ")

    generator = Generate_RE(size_input, known_re)
    combos = generator.combinations()
    ionic_radius_df = generator.average_ionic_radius(combos)

    if combos:
        output_file = '/Users/aisling/downloads/Combinations_Output.xlsx'
        generator.save_to_excel(ionic_radius_df, output_file)
    else:
        print("No valid combinations could be generated.")

 
