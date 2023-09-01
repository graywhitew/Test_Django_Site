class CommonMixin:
    title = None
    categories = None

    def get_context_data(self, **kwargs):
        context = super(CommonMixin, self).get_context_data(**kwargs)
        context["title"] = self.title
        context["categories"] = self.categories
        return context
