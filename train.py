import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--data_path", help="relative path to the csv file for which the transition probabilities are to be calculated", default="data/germany.csv")
parser.add_argument("-m", "--model_path", help="relative path to the csv file to which the transition probabilities should be saved", default="models/german_model.csv")

args = parser.parse_args()

# load dataset
df = pd.read_csv(args.data_path)

infected = df["infected"].to_numpy()
recovered = df["recovered"].to_numpy()
healthy = df["healthy"].to_numpy()
deceased = df["deceased"].to_numpy()

# get average transition probabilities
probabilities = {
    "healthy_to_recovered": 0,
    "healthy_to_deceased": 0,
    "infected_to_healthy": 0,
    "recovered_to_healthy": 1,
    "recovered_to_infected": 0,
    "recovered_to_recovered": 0,
    "recovered_to_deceased": 0,
    "deceased_to_healthy": 0,
    "deceased_to_infected": 0,
    "deceased_to_recovered": 0,
    "deceased_to_deceased": 1,
}

# we need to shift the arrays by one such that we match the entries with the entries for the next day
healthy_tomorrow = healthy[1:]
healthy = healthy[:-1]
infected_tomorrow = infected[1:]
infected = infected[:-1]
deceased_tomorrow = deceased[1:]
deceased = deceased[:-1]
recovered_tomorrow = recovered[1:]
recovered = recovered[:-1]

# for each pair of days compute the ratio of transiting people for each transition
healthy_that_stay_healthy = healthy_tomorrow-recovered
ratios_healthy_to_healthy = np.divide(healthy_that_stay_healthy, healthy, where=healthy!=0, out=np.zeros_like(healthy, dtype='float64'))
healthy_that_become_infected = healthy - healthy_that_stay_healthy
# ratios_healthy_to_infected = np.divide(healthy_that_become_infected, healthy, where=healthy!=0, out=np.zeros_like(healthy, dtype='float64'))
infected_that_stay_infected = infected_tomorrow-healthy_that_become_infected
ratios_infected_to_infected = np.divide(infected_that_stay_infected, infected, where=infected!=0, out=np.zeros_like(infected, dtype='float64'))
infected_that_recover = recovered_tomorrow
ratios_infected_to_recovered = np.divide(infected_that_recover, infected, where=infected!=0, out=np.zeros_like(infected, dtype='float64'))
# infected_that_die = infected-(infected_that_stay_infected+infected_that_recover)
# ratios_infected_to_deceased = np.divide(infected_that_die, infected, where=infected!=0, out=np.zeros_like(infected, dtype='float64'))

# compute the mean of the ratios
probabilities["healthy_to_healthy"] = np.mean(ratios_healthy_to_healthy)
probabilities["healthy_to_infected"] = 1 - probabilities["healthy_to_healthy"]
probabilities["infected_to_infected"] = np.mean(ratios_infected_to_infected)
probabilities["infected_to_recovered"] = np.mean(ratios_infected_to_recovered)
probabilities["infected_to_deceased"] = 1 - (probabilities["infected_to_recovered"]+probabilities["infected_to_infected"])

print(probabilities["healthy_to_healthy"]+probabilities["healthy_to_infected"])
print(probabilities["infected_to_infected"]+probabilities["infected_to_deceased"]+probabilities["infected_to_recovered"])
print(probabilities)

# save transition probabilities to csv
pd.DataFrame(probabilities, index=[0]).to_csv(args.model_path)