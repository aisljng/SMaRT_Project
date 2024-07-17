'''
write program that
1. gets input size by user
2. generates combinations from 17 RE's
3. user inputs the known RE's 
4. the program fills in the remaining size

Js La Sc Y Yb
Sc La Y Nd

'''
import pandas as pd
import itertools

class Generate_RE:

    file = '/Users/aisling/downloads/SMaRT/Ionic_Average_Project.xlsx'
    df1 = pd.read_excel(file, sheet_name='List of Elements', usecols=['Symbol'])

    def __init__(self, size, elements):
        self.size = int(size)
        self.elements = elements.split()

    def validation(self):
        column_values = self.df1['Symbol'].dropna().unique()
        nonexistent = [elem for elem in self.elements if elem not in column_values]

        if nonexistent:
            print(f"One or more of the elements do not exist: {nonexistent}")
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
        print(unique_combinations)
        return unique_combinations

    # def save_to_text_file(self, combinations, output_file):
    #     with open(output_file, 'w') as file:
    #         for comb in combinations:
    #             file.write(', '.join(comb) + '\n')
    #     print(f"Combinations saved to {output_file}")

    def save_to_excel(self, combinations, comb_file):
            df_combinations = pd.DataFrame(combinations)
            df_combinations.to_excel(comb_file, index=False)
            print(f"Combinations saved to {comb_file}")

if __name__ == "__main__":
    size_input = input("Enter the size of elements: ")
    known_re = input("Enter the known RE elements: ")

    generator = Generate_RE(size_input, known_re)
    combos = generator.combinations()

    if combos:
        output_file = '/Users/aisling/downloads/Combinations_Output.xlsx'  # Changed extension to .xlsx
        generator.save_to_excel(combos, output_file)
    else:
        print("No valid combinations could be generated.")


        