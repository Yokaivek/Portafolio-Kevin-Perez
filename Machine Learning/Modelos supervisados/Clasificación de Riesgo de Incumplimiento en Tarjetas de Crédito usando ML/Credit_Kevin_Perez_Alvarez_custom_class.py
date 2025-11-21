
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class OutlierClipper(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.numerical_cols = ['LIMIT_BAL','AGE','BILL_AMT1','BILL_AMT2','BILL_AMT3',
                                'BILL_AMT4','BILL_AMT5','BILL_AMT6','PAY_AMT1',
                                'PAY_AMT2','PAY_AMT3','PAY_AMT4','PAY_AMT5','PAY_AMT6']

    def fit(self, X, y=None):
        self.bounds_ = {}
        for col in self.numerical_cols:
            q1 = X[col].quantile(0.25)
            q3 = X[col].quantile(0.75)
            iqr = q3 - q1
            self.bounds_[col] = (q1 - 1.5 * iqr, q3 + 1.5 * iqr)
        return self

    def transform(self, X):
        X_ = X.copy()
        for col in self.numerical_cols:
            low, high = self.bounds_[col]
            X_[col] = X_[col].clip(low, high)
        return X_

# 2. Transformaciones categóricas y features nuevas


class CustomFeatures(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        df.rename(columns={'PAY_0': 'PAY_1'}, inplace=True)
        pay_cols = [f'PAY_{i}' for i in range(1, 7)]
    

        # Limpieza de categóricas
        df['EDUCATION'] = df['EDUCATION'].replace([0, 4, 5, 6], 4)
        df['MARRIAGE'] = df['MARRIAGE'].replace(0, 3)

        # Nuevas features útiles para el modelo
        df['IS_CONSISTENT_PAYER'] = (df[pay_cols] <= 0).all(axis=1).astype(int)
        df['AVG_PAY_DELAY'] = df[pay_cols].mean(axis=1)
        df['MAX_PAY_DELAY'] = df[pay_cols].max(axis=1)
        df['NUM_LATE_PAYMENTS'] = (df[pay_cols] > 0).sum(axis=1)
        df['PAYMENT_TREND'] = df['PAY_AMT1'] - df['PAY_AMT6']

        # Columnas eliminadas para evitar multicolinealidad o ruido
        drop_cols = [
            'ID', 'BILL_AMT2','BILL_AMT3',
            'BILL_AMT4','BILL_AMT5','BILL_AMT6'
        ]
        df.drop(columns=[col for col in drop_cols if col in df.columns], inplace=True)
        return df