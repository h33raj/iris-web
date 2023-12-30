from flask_login import current_user
from sqlalchemy import and_, desc, asc
from sqlalchemy.util import reduce

import app
from app.datamgmt.manage.manage_cases_db import user_list_cases_view
from app.models import CaseAssets, Client, Cases, Tags


def get_filtered_tags(tag_title=None,
                      tag_namespace=None,
                      page=1,
                      per_page=10,
                      sort_by='name',
                      sort_dir='asc'):
    """
    Returns a list of tags, filtered by the given parameters.

    :param tag_title: Tag title
    :param tag_namespace: Tag namespace
    :param page: Page number
    :param per_page: Number of items per page
    :param sort_by: Sort by
    :param sort_dir: Sort direction
    :return: Filtered tags
    """

    conditions = []
    if tag_title:
        conditions.append(CaseAssets.case_id == tag_title)

    if tag_namespace:
        conditions.append(Client.client_id == tag_namespace)

    if len(conditions) > 1:
        conditions = [reduce(and_, conditions)]

    data = Tags.query.filter(*conditions)

    if sort_by is not None:
        order_func = desc if sort_dir == 'desc' else asc

        if sort_by == 'name':
            data = data.order_by(order_func(Tags.tag_title))
        elif sort_by == 'namespace':
            data = data.order_by(order_func(Tags.namespace))
        else:
            data = data.order_by(order_func(Tags.tag_title))

    try:

        filtered_tags = data.paginate(page=page, per_page=per_page)

    except Exception as e:
        app.logger.exception(f"Failed to get filtered tags: {e}")
        raise e

    return filtered_tags
