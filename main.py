if __name__ == '__main__':
    import sys
    from app.route_builder import RouteBuilder
    from app.exceptions import PlotDescriptionParsingError, UnprocessablePlotError

    route_builder = RouteBuilder(
        plot_description=sys.argv[1],
        starting_point=(0, 0),
        filter_duplicated_points=False
    )

    try:
        route = route_builder.build_route()
        print(route)
    except (PlotDescriptionParsingError, UnprocessablePlotError) as e:
        print(e)
