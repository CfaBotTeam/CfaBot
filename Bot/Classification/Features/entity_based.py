from Bot.Features import FeaturesFactory


class EntityFeaturesFactory(FeaturesFactory):
    def __init__(self, glossary):
        self.glossary_ = glossary

    def add_features(self, df):
        #The goal of this method is to extract the subject of a phrase to see whether it matches a technical term
        #'The option adjusted spread (OAS) is best described as the:'
        pass