from mlflow.pyfunc import scoring_server
from mlflow import pyfunc

app = scoring_server.init(pyfunc.load_model("/opt/ml/model/"))
