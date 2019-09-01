from typing import List
import pandas as pd
import math
import operator

class Dinossaur:
    def __init__(self, name: str, leg_length: float, diet: str, stride_length: float, stance: str) -> None:
        """ Dinossaur constructor.

        Args:
            name: The name of the dinossaur
            leg_length: The leg length of the dinossaur 
            diet: The type of diet of the dinossaur
            stride_length: The stride length of the dinossaur 
            stance: The stance of the dinossaur 
            
        """
        self.name = name
        self.leg_length = leg_length
        self.diet = diet
        self.stride_length = stride_length
        self.stance = stance
        self.velocity = self.__get_velocity(self.leg_length, self.stride_length)

    def __get_velocity(self, leg_length: float, stride_length: float) -> float: 
        # Calculates the velocity of the dinossaur

        g = math.pow(9.8, 2)

        if (math.isnan(leg_length) or math.isnan(stride_length)):
            return float('nan')
    
        return round((stride_length / leg_length - 1) * math.sqrt(leg_length * g), 2)

def get_merged_csv_data(file_1: str, file_2: str, on: str, how: str) -> pd.DataFrame:
    """ Read two csv into DataFrames and merge then together

    Args:
        file_1: The first csv path.
        file_1: The second csv path.
        on: Column or index level names to join on
        how: Type of merge to be performed, a database-style join. {‘left’, ‘right’, ‘outer’, ‘inner’}

    Returns:
        A DataFrame of the two merged objects.

    """

    df1 = pd.read_csv(file_1)
    df2 = pd.read_csv(file_2)

    return df1.merge(df2, on=on, how=how)


def create_dinossaurs_objects_from_data_frame(dinos_df: pd.DataFrame) -> List[Dinossaur]:
    """ Create dinossaurs instances from a DataFrame

    Args:
        dinos_df: The dinossaurs DataFrame

    Returns:
        A list of instances of Dinossaur

    """
    dinossaurs = []

    for index, row in dinos_df.iterrows():
        dinossaurs.append(Dinossaur(row['NAME'], row['LEG_LENGTH'], row['DIET'], row['STRIDE_LENGTH'], row['STANCE']))

    return dinossaurs

def get_fastest_dinossaurs_by_stance(dinossaurs: List[Dinossaur], stance: str) -> List[Dinossaur]:
    """ Create a list of dinossaurs by stance and sort by their velocity

    Args:
        dinossaurs: The list of dinossaurs objects
        stance: The stance required of the dinossaurs

    Returns:
        A list of instances of Dinossaur

    """
    dinossaurs_by_stance = []

    for dinossaur in dinossaurs:
        if getattr(dinossaur, 'stance') == stance:
            dinossaurs_by_stance.append(dinossaur)

    return sorted(dinossaurs_by_stance, key= lambda o: float('-inf') if math.isnan(getattr(o, 'velocity')) else getattr(o, 'velocity'), reverse=True)

def save_attribute_into_text(objects: List[object], attribute: str, file: str) -> None:
    """ Save a desired attribute of a list of objects on a .txt file

    Args:
        objects: The list of objects
        attribute: The attribute of the objects
        file: The path on which the attr will be saved

    """
    with open(file, 'w') as f:
        for obj in objects:
            f.write(getattr(obj, attribute) + '\n')

dinos_df = get_merged_csv_data('dataset1.csv', 'dataset2.csv', 'NAME', 'outer')
dinossaurs = create_dinossaurs_objects_from_data_frame(dinos_df)

fastest_bipedals = get_fastest_dinossaurs_by_stance(dinossaurs, 'bipedal')

save_attribute_into_text(fastest_bipedals, 'name', 'output.txt')

# manually deleting variables because the challenge requires all code in the same file
del [dinos_df, dinossaurs, fastest_bipedals]

# ==================================== UNIT TESTING ====================================
import unittest

class TestDinossaur(unittest.TestCase):
    def test_velocity(self):
        d = Dinossaur('Euoplocephalus', 1.6, 'herbivore', 1.87, 'quadrupedal')
        velocity = getattr(d, 'velocity')
        self.assertEqual(2.09, velocity)

    def test_nan_velocity(self):
        d = Dinossaur('Deinonychus', float('nan'), float('nan'), 1.21, 'bipedal')
        velocity = getattr(d, 'velocity')
        self.assertEqual(True, math.isnan(velocity))

class TestMainMethods(unittest.TestCase):
    def test_csv_to_df_merge(self):
        file_1, file_2, on, how = ['dataset1.csv', 'dataset2.csv', 'NAME', 'inner']
        df = get_merged_csv_data(file_1, file_2, on, how)

        self.assertEqual(any(df.NAME == 'Deinonychus'), False)
        self.assertEqual(any(df.NAME == 'Euoplocephalus'), True)

        how = 'outer'
        df = get_merged_csv_data(file_1, file_2, on, how)
        self.assertEqual(any(df.NAME == 'Deinonychus'), True)

    def test_csv_to_df_merge_invalid_attr(self):
        file_1, file_2, on, how = ['dataset1.csv', 'dataset3.csv', 'NAME', 'inner']
        with self.assertRaises(FileNotFoundError):
            get_merged_csv_data(file_1, file_2, on, how)
        
        file_2, on = ['dataset2.csv', 'STANCE']
        with self.assertRaises(KeyError):
            get_merged_csv_data(file_1, file_2, on, how)

        on, how = ['NAME', 'from']
        with self.assertRaises(KeyError):
            get_merged_csv_data(file_1, file_2, on, how)
    
    def test_create_dinos_from_df(self):
        df = pd.DataFrame(columns=['NAME', 'LEG_LENGTH', 'DIET', 'STRIDE_LENGTH', 'STANCE'])
        df.loc[0] = 'Euoplocephalus', 1.6, 'herbivore', 1.87, 'quadrupedal'
        df.loc[1] = 'Deinonychus', float('nan'), float('nan'), 1.21, 'bipedal'

        list_of_dino = create_dinossaurs_objects_from_data_frame(df)
        for dino in list_of_dino:
            self.assertIsInstance(dino, Dinossaur)
    
    def test_create_dinos_from_df_invalid_attr(self):
        df = pd.DataFrame(columns=['NAME', 'LEG_LENGTH', 'DIET', 'STRIDE_LENGTH', 'STANCE'])
        df.loc[0] = 'Euoplocephalus', '1.6', 'herbivore', 1.87, 'quadrupedal'

        with self.assertRaises(TypeError):
            create_dinossaurs_objects_from_data_frame(df)

    def test_get_fastest_dinos_by_stance(self):
        dinossaurs = [Dinossaur('Euoplocephalus', 1.6, 'herbivore', 1.87, 'quadrupedal'), Dinossaur('Deinonychus', float('nan'), float('nan'), 1.21, 'bipedal'), Dinossaur('Hadrosaurus', 1.2, 'herbivore', 1.4, 'bipedal')]        
        fastest_quadrupedals = get_fastest_dinossaurs_by_stance(dinossaurs, 'quadrupedal')

        for quadrupedal in fastest_quadrupedals:
            self.assertEqual(getattr(quadrupedal, 'stance'), 'quadrupedal')

        fastest_bipedals = get_fastest_dinossaurs_by_stance(dinossaurs, 'bipedals')

        for bipedal in fastest_bipedals:
            self.assertEqual(getattr(bipedal, 'stance'), 'bipedal')

        fastest_tetrapods = get_fastest_dinossaurs_by_stance(dinossaurs, 'tetrapods')
        self.assertEqual(fastest_tetrapods, [])

if __name__ == '__main__':
    unittest.main()