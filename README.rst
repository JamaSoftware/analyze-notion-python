Notion API Client
=================

This is the python client for the Notion API.
Use this client to report on ingredients, and create new ingredients.

Install
=======
``pip install notion-python``

Usage
=====
Get your API Token, and ingredient information from here:
https://app.usenotion.com/api_control_panel

.. code:: python

    import notion

    # create a client
    client = notion.NotionClient('YOUR_API_KEY')

    # make a report
    client.report(datetime.now(), 20, ingredient_id='AN_INGREDIENT_KEY')

    # make many reports
    client.batch_report('AN_INGREDIENT_KEY', [
        {'date': datetime.now() - timedelta(days=1), 'value': 2},
        {'date': datetime.now(), 'value': 3},
    ])

    # create a new ingredient
    client.create_ingredient('Ingredient Name', [
        {'date': datetime.now() - timedelta(days=1), 'value': 2},
        {'date': datetime.now(), 'value': 3},
    ])

Error Handling
--------------
All methods will raise a subclass of ``notion.NotionError`` in the event that
the request could not be made, or an error occurred.
