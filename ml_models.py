import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import pickle


def create_conf_bias_predict_files():
    # cols_to_use= ["date", "greenbox", "opening_level", "closing_level", "dr_upday"]
    x_vars = ["greenbox", "opening_level", "closing_level"]
    y_var = ["dr_upday"]

    for file in os.scandir(".\dr_data"):
        df = pd.read_csv(file.path, sep=";")
        file_identifier = file.name.replace(".csv", "")

        X = df[x_vars]
        y = df[y_var]

        imputer = SimpleImputer(strategy="median")
        imputer.fit(X)
        X = imputer.transform(X)

        # Feature-Scaling
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        model = RandomForestClassifier(bootstrap=True, criterion="entropy", max_features=0.15000000000000002,
                                       min_samples_leaf=19, min_samples_split=19, n_estimators=100)

        model.fit(X, y)

        filename_model = f".\ml_models\{file_identifier}_simple_confirmation_bias_model.pickle"
        filename_scaler = f".\ml_models\{file_identifier}_simple_confirmation_bias_scaler.pickle"

        pickle.dump(model, open(filename_model, "wb"))
        pickle.dump(scaler, open(filename_scaler, "wb"))


def create_all_model_tables(symbol="all"):

    symbol_list = ["nq", "es", "ym", "cl", "gc", "eurusd", "gbpusd", "fdax", "audjpy"]

    if symbol == "all":
        for i in symbol_list:
            create_model_table(i)
    else:
        create_model_table(symbol)


def create_model_table(symbol):

    def define_model(row, current_session, prev_session):

        if current_session == "asia":
            prev_session = "ny_preday"

        if row[f'dr_low_{prev_session}'] <= row[f'dr_low_{current_session}'] <= row[f'midline_{prev_session}'] and row[
            f'dr_high_{current_session}'] >= row[f'dr_high_{prev_session}']:
            return "Weak Uptrend"

        elif row[f'midline_{prev_session}'] <= row[f'dr_low_{current_session}'] <= row[f'dr_high_{prev_session}'] <= \
                row[f'dr_high_{current_session}']:
            return "Medium Uptrend"

        elif row[f'dr_low_{current_session}'] >= row[f'dr_high_{prev_session}']:
            return "Strong Uptrend"

        elif row[f'dr_high_{prev_session}'] >= row[f'dr_high_{current_session}'] >= row[f'midline_{prev_session}'] and \
                row[f'dr_low_{current_session}'] <= row[f'dr_low_{prev_session}']:
            return "Weak Downtrend"

        elif row[f'dr_high_{prev_session}'] >= row[f'midline_{prev_session}'] >= row[f'dr_high_{current_session}'] >= \
                row[f'dr_low_{prev_session}'] >= row[f'dr_low_{current_session}']:
            return "Medium Downtrend"

        elif row[f'dr_low_{prev_session}'] >= row[f'dr_high_{current_session}']:
            return "Strong Downtrend"

        elif row[f'dr_high_{current_session}'] <= row[f'dr_high_{prev_session}'] and row[f'dr_low_{current_session}'] >= \
                row[f'dr_low_{prev_session}']:
            return "Contraction"

        elif row[f'dr_high_{current_session}'] >= row[f'dr_high_{prev_session}'] and row[f'dr_low_{current_session}'] <= \
                row[f'dr_low_{prev_session}']:
            return "Expansion"
        else:
            return "Not defined"

    def is_previous_day(row):
        index = row.name

        if index > model_df.index[0]:  # Überprüfen, ob der Index-Wert nicht der erste ist
            previous_date = model_df.index[model_df.index.get_loc(index) - 1]
            previous_day = previous_date.day_name()
            current_day = index.day_name()
            if current_day == "Monday" and previous_day == "Friday":
                return True
            elif (index - previous_date).days == 1:
                return True
        return False

    dr_df = pd.read_csv(os.path.join("dr_data", f"{symbol.lower()}_dr.csv"), sep=";",
                        usecols=["date", "dr_high", "dr_low", "dr_upday", "dr_true", "greenbox"],
                        index_col=0)
    odr_df = pd.read_csv(os.path.join("dr_data", f"{symbol.lower()}_odr.csv"), sep=";",
                         usecols=["date", "dr_high", "dr_low", "dr_upday", "dr_true", "greenbox"],
                         index_col=0)
    adr_df = pd.read_csv(os.path.join("dr_data", f"{symbol.lower()}_adr.csv"), sep=";",
                         usecols=["date", "dr_high", "dr_low", "dr_upday", "dr_true", "greenbox"],
                         index_col=0)

    dr_df["midline"] = dr_df.dr_low + (dr_df.dr_high - dr_df.dr_low) / 2
    odr_df["midline"] = odr_df.dr_low + (odr_df.dr_high - odr_df.dr_low) / 2
    adr_df["midline"] = adr_df.dr_low + (adr_df.dr_high - adr_df.dr_low) / 2

    model_df = dr_df.join(odr_df, rsuffix="_ldn")
    model_df = model_df.join(adr_df, lsuffix="_ny", rsuffix="_asia")
    model_df = model_df.dropna()

    #Shifting new york session for asia model calculation
    model_df["dr_high_ny_preday"] = model_df["dr_high_ny"].shift(1)
    model_df["dr_low_ny_preday"] = model_df["dr_low_ny"].shift(1)
    model_df["midline_ny_preday"] = model_df["midline_ny"].shift(1)
    model_df["greenbox_ny_preday"] = model_df["greenbox_ny"].shift(1)
    model_df["dr_upday_ny_preday"] = model_df["dr_upday_ny"].shift(1)
    model_df["dr_true_ny_preday"] = model_df["dr_true_ny"].shift(1)

    model_df["ny_model"] = model_df.apply(define_model, current_session="ny", prev_session="ldn", axis=1)
    model_df["ldn_model"] = model_df.apply(define_model, current_session="ldn", prev_session="asia", axis=1)
    model_df["asia_model"] = model_df.apply(define_model, current_session="asia", prev_session="ny", axis=1)

    # Filter out days where preday is not previous day
    model_df.index = pd.to_datetime(model_df.index)
    model_df['is_previous_day'] = model_df.apply(is_previous_day, axis=1)
    model_df = model_df[model_df.is_previous_day]



    model_df["asia_outcome"] = model_df.apply(
        lambda row: "Broken" if not row["dr_true_asia"]
                                or ("Uptrend" in row["asia_model"] and not row["dr_upday_asia"])
                                or ("Downtrend" in row["asia_model"] and row["dr_upday_asia"])
        else "Complete",
        axis=1
    )

    model_df["ldn_outcome"] = model_df.apply(
        lambda row: "Broken" if not row["dr_true_ldn"]
                                or ("Uptrend" in row["ldn_model"] and not row["dr_upday_ldn"])
                                or ("Downtrend" in row["ldn_model"] and row["dr_upday_ldn"])
        else "Complete",
        axis=1
    )

    model_df["ny_outcome"] = model_df.apply(
        lambda row: "Broken" if not row["dr_true_asia"]
                                or ("Uptrend" in row["ny_model"] and not row["dr_upday_ny"])
                                or ("Downtrend" in row["ny_model"] and row["dr_upday_ny"])
        else "Complete",
        axis=1
    )

    model_df.to_csv(f"session_models/{symbol}_model_table.csv", sep=";")
        # dr_table.apply(
        #     lambda row: False if (pd.isna(row['up_confirmation']) and pd.isna(row['down_confirmation']))
        #     else (True if pd.to_datetime(row['up_confirmation']) < pd.to_datetime(row['down_confirmation'])
        #           else (True if pd.notna(row['up_confirmation']) and pd.isna(row['down_confirmation']) else False)),
        #     axis=1)


# df = pd.read_csv("test.csv", sep=";")

# create_all_model_tables("all")

class MlModelling:
    def __init__(self, X, y):
        self.accuracy = None
        self.y_pred = None
        self.symbol_list = ["nq", "es", "ym", "cl", "gc", "eurusd", "gbpusd", "fdax", "audjpy"]
        self.sessions = ["ny", "ldn", "asia"]

        self.X = X
        self.y = y
        self.data = self.read_file()
        self.rf = RandomForestClassifier()
        self.fit_the_model()
        
    def read_file(self):
        df = pd.read_csv(r"C:\Users\timon\PycharmProjects\dr_dashboard\data\es_ny_60.csv", sep=";")

        self.X = np.array(df[self.X]).reshape(-1, 1)
        self.y = np.array(df[self.y]).reshape(-1, 1)
        print(self.X)
        print(len(self.X))
        print(self.y)

    def fit_the_model(self):
        # Train Test Split


        imputer = SimpleImputer(strategy="median")
        imputer.fit(self.X)
        X = imputer.transform(self.X)

        # Feature-Scaling
        scaler = StandardScaler()
        self.X = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2)

        # Fitting the Model 
        self.rf.fit(X_train, y_train)
        self.y_pred = self.rf.predict(X_test)
        self.accuracy = accuracy_score(y_test, self.y_pred)

    def get_accuracy(self):
        print("Accuracy:", self.accuracy)
        return self.accuracy


model = MlModelling(
    X="upday",
    y=["upday_prev", ]
)

model.get_accuracy()