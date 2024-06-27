import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--model_path", help="relative path to the csv file with the transition probabilities", default="models/german_model.csv")
parser.add_argument("-d", "--data_path", help="relative path to the csv file containing the data that is used to make predictions", default="data/germany.csv")
parser.add_argument("-p", "--prediction_path", help="relative path to where the predictions should be saved", default="predictions/germany_germany.csv")
parser.add_argument("-s", "--start_day", help="day at which the model should start predicting", default=260)
parser.add_argument("-e", "--end_day", help="day at which the model should stop predicting", default=560)

args = parser.parse_args()

prob_df = pd.read_csv(args.model_path)
data_df = pd.read_csv(args.data_path)

assert args.start_day < args.end_day
assert args.start_day < len(data_df) - 1
assert len(data_df) >= args.end_day

data_df = data_df.iloc[args.start_day:args.end_day].reset_index(drop=True)

# make transition matrix
trans_prob = np.array([
    [prob_df["healthy_to_healthy"].iloc[0], prob_df["infected_to_healthy"].iloc[0], prob_df["deceased_to_healthy"].iloc[0], prob_df["recovered_to_healthy"].iloc[0]],
    [prob_df["healthy_to_infected"].iloc[0], prob_df["infected_to_infected"].iloc[0], prob_df["deceased_to_infected"].iloc[0], prob_df["recovered_to_infected"].iloc[0]],
    [prob_df["healthy_to_deceased"].iloc[0], prob_df["infected_to_deceased"].iloc[0], prob_df["deceased_to_deceased"].iloc[0], prob_df["recovered_to_deceased"].iloc[0]],
    [prob_df["healthy_to_recovered"].iloc[0], prob_df["infected_to_recovered"].iloc[0], prob_df["deceased_to_recovered"].iloc[0], prob_df["recovered_to_recovered"].iloc[0]]
])

# predict
all_predictions = []
current_day = np.array([data_df["healthy"].iloc[0], data_df["infected"].iloc[0], data_df["deceased"].iloc[0], data_df["recovered"].iloc[0]])
all_predictions.append(current_day)
print(all_predictions)

for i in range(1, len(data_df)):
    next_day = np.matmul(
        trans_prob,
        current_day,
    )
    # print(current_day)
    # print(next_day)
    all_predictions.append(next_day)
    # current_day = np.array([data_df["healthy"].iloc[i], data_df["infected"].iloc[i], data_df["deceased"].iloc[i], data_df["recovered"].iloc[i]])
    current_day = next_day

all_predictions = np.array(all_predictions)

# print(len(all_predictions))
# print(all_predictions)

data_df["predicted_healthy"] = pd.Series(all_predictions[:, 0])
data_df["predicted_healthy_error"] = pd.Series(np.abs(all_predictions[:, 0] - data_df["healthy"].to_numpy()))
data_df["predicted_infected"] = pd.Series(all_predictions[:, 1])
data_df["predicted_infected_error"] = pd.Series(np.abs(all_predictions[:, 1] - data_df["infected"].to_numpy()))
data_df["predicted_deceased"] = pd.Series(all_predictions[:, 2])
data_df["predicted_deceased_error"] = pd.Series(np.abs(all_predictions[:, 2] - data_df["deceased"].to_numpy()))
data_df["predicted_recovered"] = pd.Series(all_predictions[:, 3])
data_df["predicted_recovered_error"] = pd.Series(np.abs(all_predictions[:, 3] - data_df["recovered"].to_numpy()))

# print(pd.Series(np.abs(all_predictions[:, 1] - data_df["infected"].to_numpy())))
print(data_df["predicted_infected"])
print(all_predictions)

# print(data_df["predicted_healthy_error"].to_numpy().mean()/data_df["healthy"].to_numpy().mean())
# print(data_df["predicted_infected_error"].to_numpy().mean()/data_df["infected"].to_numpy().mean())
# print(data_df["predicted_deceased_error"].to_numpy().mean()/data_df["deceased"].to_numpy().mean())
# print(data_df["predicted_recovered_error"].to_numpy().mean()/data_df["recovered"].to_numpy().mean())

data_df.to_csv(args.prediction_path)

infected_df = data_df.drop(["healthy", "deceased", "recovered", "predicted_healthy", "predicted_healthy_error", "predicted_deceased", "predicted_deceased_error", "predicted_recovered", "predicted_recovered_error"], axis=1)

figure = infected_df.plot().get_figure()
figure.savefig("plots/fig1.png")