import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import operator

# Reading data
df = pd.read_csv('fruit_database.csv')

# insert dataframe, which index, name of fruit
# example: df=df, index='fruit', fruit='banana'


def fruit_mask(df, index, fruit):
    return df[index] == fruit


def graph_each_fruit_with_certainty_percent(df, label):
    plt.figure()
    count = 1
    fruit_graph = {}
    # Iter over banana dataset and create dict with bananas aplt.show()nd % guessed
    for i, row in df.iterrows():
        fruit_graph[count] = row['certainty_level %']
        count += 1
    # Display graph
    plt.title(f'{label} and their certainity %')
    plt.plot(fruit_graph.keys(), fruit_graph.values())
    plt.yticks(np.arange(0, 101, 10))

#Making it into a module :)
def graph_file():
#1) Graph that shows how many banana, orange, apples have been chosen, x=fruit, y=amount
# Autistic solution, wouldt recommend as u will choke in exam if ur asked to explain
# fruit_dir = {fruit_dir.setdefault(row['fruit'], len(df[fruit_mask(df, 'fruit', row['fruit'])])) for i,row in df.iterrows()}
# simpler solution, we should use this
    fruit_dir = {}
    for i, row in df.iterrows():
        fruit_dir.setdefault(row['fruit'], len(
            df[fruit_mask(df, 'fruit', row['fruit'])]))

    # the x locations for the groups
    plt.figure()
    ind = list(range(0, len(fruit_dir.items())))
    width = 0.35       # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, fruit_dir.values(), width)
    plt.ylabel('Found amount of times')
    plt.title('See how many times each fruit has been scanned')
    plt.xticks(ind, fruit_dir.keys())
    max_value_from_dir = fruit_dir[max(
        fruit_dir.items(), key=operator.itemgetter(1))[0]]
    plt.yticks(np.arange(0, max_value_from_dir, 5))

    #2) Graph that shows average % certainty when each fruit is chosen, fx banana: 57%, apple 42%, orange 44%, x=fruit, y = %
    data = df[['fruit', 'certainty_level %']]
    certainty_dir = {}
    for i, row in data.iterrows():
            # set default values
            certainty_dir.setdefault(row['fruit'], 0)
            certainty_dir.setdefault(row['fruit']+'amount', 0)
            # add to values
            certainty_dir[row['fruit']] += row['certainty_level %']
            certainty_dir[row['fruit']+'amount'] += 1

    # divide each fruit sum % with amount of fruits, to get the average % of certainty
    del_list = []
    # Dividing the values by their total amounts
    for key, value in certainty_dir.items():
        if("amount" not in key):
            certainty_dir[key] = certainty_dir[key] / certainty_dir[key+'amount']
        else:
            # add to delete list, you cant delete keys while iterating dict, so have to do it afterwards
            del_list.append(key)
    # clean up the dict from useless values, for the graphs sake
    for i in del_list:
        del certainty_dir[i]


    plt.figure()
    ind = list(range(0, len(certainty_dir.items())))
    width = 0.35       # the width of the bars: can also be len(x) sequence

    p2 = plt.bar(ind, certainty_dir.values(), width)

    plt.ylabel("perfect certainty each guess")
    plt.title('Percent certainty for each guessed fruit')
    plt.xticks(ind, certainty_dir.keys())
    plt.yticks(np.arange(0, 101, 10))

    #3) Takes a set of df[fruit] to find all fruit names, used to create a dynamic solution that
    # shows fruits and their certainty for each recognition theyve had in the network
    #  all fruits are in this case shown together
    #dynamic solution, looks at allf ruits and plots afterwards
    data = set(df['fruit'])
    plt.figure()
    for x in data:
        element = df[fruit_mask(df, 'fruit', x)]
        count = 1
        fruit_graph = {}
        # Iter over banana dataset and create dict with bananas and % guessed
        for i, row in element.iterrows():
            fruit_graph[count] = row['certainty_level %']
            count += 1
        # Display graph
        plt.plot(fruit_graph.keys(), fruit_graph.values(), label=x)

    plt.legend()
    plt.title(f'Fruits and their certainity %')
    plt.yticks(np.arange(0, 101, 10))

    #4) calls function on each fruit name and displays it as a graph
    #dynamic solution for each fruit in the dataset
    for i in data:
        graph_each_fruit_with_certainty_percent(df[fruit_mask(df, 'fruit', i)], i.capitalize()+'s')

    plt.show()


if __name__ == "__main__":
    graph_file()