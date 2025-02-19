from math import ceil

def paginate_query(query, page, limit):
    """
    Paginate SQLAlchemy queries.

    :param query: SQLAlchemy query object to paginate
    :param request: Flask request object to get query parameters (page, limit)
    :param default_limit: Default number of records per page if limit is not provided
    :return: Dictionary with paginated data and meta information
    """

    # Calculate total number of records
    total_items = query.count()

    # Calculate offset and apply limit and offset to the query
    offset = (page - 1) * limit
    paginated_query = query.limit(limit).offset(offset)

    # Get the paginated results
    items = paginated_query.all()

    # Calculate total pages
    total_pages = ceil(total_items / limit)

    # Return the paginated data and meta information
    return {
        "items": items,
        "meta": {
            "total_items": total_items,
            "current_page": page,
            "limit": limit,
            "total_pages": total_pages,
        }
    }
