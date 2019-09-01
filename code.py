from typing import List
import pandas as pd
import math
import operator

class Dinossaur:
    def __init__(self, name: str, leg_length: float, diet: str, stride_length: float, stance: str) -> None:
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
    # read csv into DataFrame

    df1 = pd.read_csv(file_1)
    df2 = pd.read_csv(file_2)

    return df1.merge(df2, on=on, how=how)


def create_dinossaurs_objects_from_data_frame(dinos_df: pd.DataFrame) -> List[Dinossaur]:
    dinossaurs = []

    for index, row in dinos_df.iterrows():
        dinossaurs.append(Dinossaur(row['NAME'], row['LEG_LENGTH'], row['DIET'], row['STRIDE_LENGTH'], row['STANCE']))

    return dinossaurs

def get_fastest_dinossaurs_by_stance(dinossaurs: List[Dinossaur], stance: str) -> List[Dinossaur]:
    bipedals = []

    for dinossaur in dinossaurs:
        if getattr(dinossaur, 'stance') == stance:
            bipedals.append(dinossaur)

    return sorted(bipedals, key= lambda o: float('-inf') if math.isnan(getattr(o, 'velocity')) else getattr(o, 'velocity'), reverse=True)

def save_attribute_into_text(objects: List[object], attribute: str, file: str) -> None:

    with open(file, 'w') as f:
        for obj in objects:
            f.write(getattr(obj, attribute) + '\n')

dinos_df = get_merged_csv_data('dataset1.csv', 'dataset2.csv', 'NAME', 'outer')
dinossaurs = create_dinossaurs_objects_from_data_frame(dinos_df)

fastest_bipedals = get_fastest_dinossaurs_by_stance(dinossaurs, 'bipedal')

save_attribute_into_text(fastest_bipedals, 'name', 'output.txt')