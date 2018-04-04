

class FeaturesFactory:
    def calc_features(self):
        raise NotImplementedError('base class. need to subclass method')

    def add_features(self, df):
        feature_serie = df.apply(self.calc_features, axis=1)
        if len(self.features_) == 1:
            df[self.features_[0]] = feature_serie
        else:
            for i, feature in enumerate(self.features_):
                df[feature] = feature_serie.apply(lambda serie: serie[i])
