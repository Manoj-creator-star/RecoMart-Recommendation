import joblib

model = joblib.load("models/saved_models/svd_model.pkl")

print(model)
print(type(model))