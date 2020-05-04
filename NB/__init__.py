import pandas as pd
import numpy as np
import pyodbc
import json
import azure.functions as func
import os

from sklearn.model_selection import train_test_split
#IMPORTAR LIBRERIAS DEL ALGORITMO
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB

 
def main(req: func.HttpRequest) -> func.HttpResponse:
    driverAzure = os.environ["DriverAzure"]
    serverAzure = os.environ["ServerBdAzure"]
    databaseAzure = os.environ["DataBaseAzure"]
    usernameAzure = os.environ["UserNameBdAzure"]
    passwordAzure = os.environ["PassWordBdAzure"]
    SQL_datos = os.environ["SQL_datos"]
    conStringAzure = "DRIVER={{{}}};SERVER={};DATABASE={};UID={};PWD={}".format(driverAzure,serverAzure,databaseAzure,usernameAzure,passwordAzure) #INGRESA LOS DATOS EN ORDEN
    cnxn = pyodbc.connect(conStringAzure)
    req_body = req.get_json()
    variable1 = req_body.get('variable1')
    cursor = cnxn.cursor()
    Yquery = "SELECT [Y] FROM logsY;"
    YSQL = pd.read_sql(Yquery, cnxn)
    Xquery = "SELECT [X1],[X2],[X3],[X4],[X5],[X6],[X7],[X8],[X9],[X10],[X11],[X12] FROM logsX;"
    XSQL = pd.read_sql(Xquery, cnxn)
    Y=YSQL.values
    X=XSQL.values
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.3,random_state=42)
    #sc = StandardScaler()
    #X_train = sc.fit_transform(X_train)
    #X_test = sc.transform(X_test)
    classifier = GaussianNB()
    classifier.fit(X_train, Y_train)
    Y_pred = classifier.predict(X_test)
    json_response = json.dumps(classification_report(Y_test, Y_pred),indent=2)
    json_response = classification_report(Y_test, Y_pred,labels=[-1,0,1])
    if variable1 < 10:
        return func.HttpResponse(json_response)
    else:
        return func.HttpResponse("NUBE Puede que se ingresara un valor mal en el postman pero la funcion se ejecuto bien",status_code=200)