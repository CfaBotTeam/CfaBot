class CategoryFilterFactory:
    def __init__(self, category):
        self.category_ = category

    def get_filters(self, df):
        return df['category'] == self.category_