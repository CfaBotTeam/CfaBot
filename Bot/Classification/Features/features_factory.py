

class FeaturesFactory:
    def calc_features(self):
        raise NotImplementedError('base class. need to subclass method')

    def add_features(self, df):
        feature_serie = df.apply(self.calc_features, axis=1)
        for i, feature in enumerate(self.features_):
            df[feature] = feature_serie.apply(lambda serie: serie[i])
