from app.utils.aggregates import calculate_totals


def register_context_processors(app):
    @app.context_processor
    def inject_totals():
        count, amount = calculate_totals()
        return dict(total_count=count, total_amount=amount)
